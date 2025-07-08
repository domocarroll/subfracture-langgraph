"""
SUBFRACTURE Error Handling & Recovery System

Comprehensive error handling, recovery mechanisms, and resilience features
for production SUBFRACTURE LangGraph workflows.

Features:
- Graceful degradation for agent failures
- Automatic retry with exponential backoff
- State recovery and checkpoint restoration
- Circuit breaker patterns for external APIs
- Comprehensive error classification and reporting
- Fallback strategies for critical workflow components
"""

import asyncio
import time
import traceback
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass
import structlog
from functools import wraps

from langsmith import traceable

logger = structlog.get_logger()


class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"              # Non-critical, workflow can continue
    MEDIUM = "medium"        # Important but recoverable
    HIGH = "high"           # Critical but may have fallbacks
    CRITICAL = "critical"    # System-breaking, requires immediate attention


class ErrorCategory(Enum):
    """Error categories for classification"""
    API_TIMEOUT = "api_timeout"
    API_RATE_LIMIT = "api_rate_limit" 
    MODEL_ERROR = "model_error"
    VALIDATION_FAILURE = "validation_failure"
    DATA_CORRUPTION = "data_corruption"
    MEMORY_ERROR = "memory_error"
    NETWORK_ERROR = "network_error"
    CONFIGURATION_ERROR = "configuration_error"
    BUSINESS_LOGIC_ERROR = "business_logic_error"
    EXTERNAL_SERVICE_ERROR = "external_service_error"


class RecoveryStrategy(Enum):
    """Recovery strategy types"""
    RETRY = "retry"                    # Simple retry
    RETRY_WITH_BACKOFF = "retry_with_backoff"  # Exponential backoff retry
    FALLBACK = "fallback"              # Use fallback method
    GRACEFUL_DEGRADATION = "graceful_degradation"  # Continue with reduced functionality
    CIRCUIT_BREAKER = "circuit_breaker"  # Temporary disable and retry later
    MANUAL_INTERVENTION = "manual_intervention"  # Requires human intervention


@dataclass
class SubfractureError:
    """Structured error information"""
    error_id: str
    timestamp: datetime
    severity: ErrorSeverity
    category: ErrorCategory
    component: str
    operation: str
    error_message: str
    stack_trace: Optional[str]
    context: Dict[str, Any]
    recovery_strategy: RecoveryStrategy
    retry_count: int = 0
    resolved: bool = False
    resolution_timestamp: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "error_id": self.error_id,
            "timestamp": self.timestamp.isoformat(),
            "severity": self.severity.value,
            "category": self.category.value,
            "component": self.component,
            "operation": self.operation,
            "error_message": self.error_message,
            "stack_trace": self.stack_trace,
            "context": self.context,
            "recovery_strategy": self.recovery_strategy.value,
            "retry_count": self.retry_count,
            "resolved": self.resolved,
            "resolution_timestamp": self.resolution_timestamp.isoformat() if self.resolution_timestamp else None
        }


class CircuitBreaker:
    """Circuit breaker for external service calls"""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half_open
        
    def can_execute(self) -> bool:
        """Check if execution is allowed"""
        if self.state == "closed":
            return True
        elif self.state == "open":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "half_open"
                return True
            return False
        else:  # half_open
            return True
    
    def record_success(self):
        """Record successful execution"""
        self.failure_count = 0
        self.state = "closed"
    
    def record_failure(self):
        """Record failed execution"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "open"


class SubfractureErrorHandler:
    """
    Comprehensive error handling system for SUBFRACTURE workflows
    """
    
    def __init__(self):
        self.logger = logger.bind(component="error_handler")
        self.error_history: List[SubfractureError] = []
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.fallback_strategies: Dict[str, Callable] = {}
        self.retry_configs: Dict[str, Dict[str, Any]] = self._initialize_retry_configs()
        
    def _initialize_retry_configs(self) -> Dict[str, Dict[str, Any]]:
        """Initialize retry configurations for different operations"""
        return {
            "api_call": {
                "max_retries": 3,
                "base_delay": 1.0,
                "max_delay": 30.0,
                "exponential_base": 2
            },
            "model_inference": {
                "max_retries": 2,
                "base_delay": 2.0,
                "max_delay": 60.0,
                "exponential_base": 2
            },
            "validation": {
                "max_retries": 1,
                "base_delay": 0.5,
                "max_delay": 5.0,
                "exponential_base": 2
            },
            "data_processing": {
                "max_retries": 2,
                "base_delay": 1.0,
                "max_delay": 15.0,
                "exponential_base": 1.5
            }
        }
    
    @traceable(name="handle_error")
    async def handle_error(
        self,
        error: Exception,
        component: str,
        operation: str,
        context: Dict[str, Any] = None,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM
    ) -> SubfractureError:
        """Handle and classify errors with appropriate recovery strategy"""
        
        error_id = f"subfracture_error_{int(time.time())}_{len(self.error_history)}"
        context = context or {}
        
        # Classify error
        category = self._classify_error(error)
        recovery_strategy = self._determine_recovery_strategy(category, severity)
        
        # Create error record
        subfracture_error = SubfractureError(
            error_id=error_id,
            timestamp=datetime.now(),
            severity=severity,
            category=category,
            component=component,
            operation=operation,
            error_message=str(error),
            stack_trace=traceback.format_exc(),
            context=context,
            recovery_strategy=recovery_strategy
        )
        
        # Store error
        self.error_history.append(subfracture_error)
        
        # Log error
        self.logger.error("SUBFRACTURE error occurred",
                         error_id=error_id,
                         severity=severity.value,
                         category=category.value,
                         component=component,
                         operation=operation,
                         error_message=str(error),
                         recovery_strategy=recovery_strategy.value)
        
        return subfracture_error
    
    def _classify_error(self, error: Exception) -> ErrorCategory:
        """Classify error into appropriate category"""
        
        error_str = str(error).lower()
        error_type = type(error).__name__.lower()
        
        # API-related errors
        if "timeout" in error_str or "timeouterror" in error_type:
            return ErrorCategory.API_TIMEOUT
        elif "rate limit" in error_str or "429" in error_str:
            return ErrorCategory.API_RATE_LIMIT
        elif "api" in error_str or "http" in error_str:
            return ErrorCategory.EXTERNAL_SERVICE_ERROR
        
        # Model/LLM errors
        elif "model" in error_str or "anthropic" in error_str or "openai" in error_str:
            return ErrorCategory.MODEL_ERROR
        
        # Validation errors
        elif "validation" in error_str or "pydantic" in error_type:
            return ErrorCategory.VALIDATION_FAILURE
        
        # Memory errors
        elif "memory" in error_str or "memoryerror" in error_type:
            return ErrorCategory.MEMORY_ERROR
        
        # Network errors
        elif "network" in error_str or "connection" in error_str:
            return ErrorCategory.NETWORK_ERROR
        
        # Configuration errors
        elif "config" in error_str or "environment" in error_str:
            return ErrorCategory.CONFIGURATION_ERROR
        
        # Data corruption
        elif "corrupt" in error_str or "invalid" in error_str:
            return ErrorCategory.DATA_CORRUPTION
        
        # Default to business logic error
        else:
            return ErrorCategory.BUSINESS_LOGIC_ERROR
    
    def _determine_recovery_strategy(self, category: ErrorCategory, severity: ErrorSeverity) -> RecoveryStrategy:
        """Determine appropriate recovery strategy"""
        
        # Critical errors require manual intervention
        if severity == ErrorSeverity.CRITICAL:
            return RecoveryStrategy.MANUAL_INTERVENTION
        
        # Strategy by category
        strategy_map = {
            ErrorCategory.API_TIMEOUT: RecoveryStrategy.RETRY_WITH_BACKOFF,
            ErrorCategory.API_RATE_LIMIT: RecoveryStrategy.CIRCUIT_BREAKER,
            ErrorCategory.MODEL_ERROR: RecoveryStrategy.RETRY_WITH_BACKOFF,
            ErrorCategory.VALIDATION_FAILURE: RecoveryStrategy.FALLBACK,
            ErrorCategory.DATA_CORRUPTION: RecoveryStrategy.GRACEFUL_DEGRADATION,
            ErrorCategory.MEMORY_ERROR: RecoveryStrategy.GRACEFUL_DEGRADATION,
            ErrorCategory.NETWORK_ERROR: RecoveryStrategy.RETRY_WITH_BACKOFF,
            ErrorCategory.CONFIGURATION_ERROR: RecoveryStrategy.MANUAL_INTERVENTION,
            ErrorCategory.BUSINESS_LOGIC_ERROR: RecoveryStrategy.FALLBACK,
            ErrorCategory.EXTERNAL_SERVICE_ERROR: RecoveryStrategy.CIRCUIT_BREAKER
        }
        
        return strategy_map.get(category, RecoveryStrategy.RETRY)
    
    async def execute_with_recovery(
        self,
        operation: Callable,
        component: str,
        operation_name: str,
        context: Dict[str, Any] = None,
        retry_config_key: str = "api_call"
    ) -> Any:
        """Execute operation with automatic error handling and recovery"""
        
        context = context or {}
        retry_config = self.retry_configs.get(retry_config_key, self.retry_configs["api_call"])
        
        # Check circuit breaker if applicable
        circuit_breaker_key = f"{component}_{operation_name}"
        if circuit_breaker_key not in self.circuit_breakers:
            self.circuit_breakers[circuit_breaker_key] = CircuitBreaker()
        
        circuit_breaker = self.circuit_breakers[circuit_breaker_key]
        
        if not circuit_breaker.can_execute():
            raise Exception(f"Circuit breaker open for {component}.{operation_name}")
        
        last_error = None
        retry_count = 0
        
        while retry_count <= retry_config["max_retries"]:
            try:
                # Execute operation
                if asyncio.iscoroutinefunction(operation):
                    result = await operation()
                else:
                    result = operation()
                
                # Record success
                circuit_breaker.record_success()
                
                # Log successful recovery if this was a retry
                if retry_count > 0:
                    self.logger.info("Operation recovered after retries",
                                   component=component,
                                   operation=operation_name,
                                   retry_count=retry_count)
                
                return result
                
            except Exception as error:
                last_error = error
                retry_count += 1
                
                # Handle error
                subfracture_error = await self.handle_error(
                    error=error,
                    component=component,
                    operation=operation_name,
                    context={**context, "retry_count": retry_count}
                )
                
                # Record failure for circuit breaker
                circuit_breaker.record_failure()
                
                # Check if we should retry
                if retry_count <= retry_config["max_retries"]:
                    # Calculate delay with exponential backoff
                    delay = min(
                        retry_config["base_delay"] * (retry_config["exponential_base"] ** (retry_count - 1)),
                        retry_config["max_delay"]
                    )
                    
                    self.logger.info("Retrying operation with backoff",
                                   component=component,
                                   operation=operation_name,
                                   retry_count=retry_count,
                                   delay=delay)
                    
                    await asyncio.sleep(delay)
                else:
                    # Max retries exceeded
                    self.logger.error("Max retries exceeded",
                                    component=component,
                                    operation=operation_name,
                                    max_retries=retry_config["max_retries"])
                    break
        
        # If we get here, all retries failed
        raise last_error
    
    def register_fallback(self, component: str, operation: str, fallback_func: Callable):
        """Register fallback function for specific component/operation"""
        key = f"{component}.{operation}"
        self.fallback_strategies[key] = fallback_func
        self.logger.info("Fallback strategy registered", component=component, operation=operation)
    
    async def execute_with_fallback(
        self,
        primary_operation: Callable,
        component: str,
        operation: str,
        context: Dict[str, Any] = None
    ) -> Any:
        """Execute operation with fallback if available"""
        
        try:
            return await self.execute_with_recovery(primary_operation, component, operation, context)
        except Exception as error:
            # Try fallback
            fallback_key = f"{component}.{operation}"
            if fallback_key in self.fallback_strategies:
                self.logger.info("Executing fallback strategy",
                               component=component,
                               operation=operation)
                
                fallback_func = self.fallback_strategies[fallback_key]
                try:
                    if asyncio.iscoroutinefunction(fallback_func):
                        return await fallback_func(context or {})
                    else:
                        return fallback_func(context or {})
                except Exception as fallback_error:
                    self.logger.error("Fallback strategy also failed",
                                    component=component,
                                    operation=operation,
                                    fallback_error=str(fallback_error))
                    raise error  # Raise original error
            else:
                # No fallback available
                raise error
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of error history and system health"""
        
        if not self.error_history:
            return {
                "total_errors": 0,
                "system_health": "excellent",
                "error_categories": {},
                "recovery_success_rate": 1.0
            }
        
        # Calculate metrics
        total_errors = len(self.error_history)
        resolved_errors = sum(1 for e in self.error_history if e.resolved)
        recovery_success_rate = resolved_errors / total_errors if total_errors > 0 else 1.0
        
        # Count by category
        category_counts = {}
        for error in self.error_history:
            category = error.category.value
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # Count by severity
        severity_counts = {}
        for error in self.error_history:
            severity = error.severity.value
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        # Determine system health
        critical_errors = severity_counts.get("critical", 0)
        high_errors = severity_counts.get("high", 0)
        
        if critical_errors > 0:
            system_health = "critical"
        elif high_errors > 3:
            system_health = "degraded"
        elif recovery_success_rate < 0.8:
            system_health = "poor"
        elif recovery_success_rate < 0.95:
            system_health = "good"
        else:
            system_health = "excellent"
        
        return {
            "total_errors": total_errors,
            "resolved_errors": resolved_errors,
            "recovery_success_rate": recovery_success_rate,
            "system_health": system_health,
            "error_categories": category_counts,
            "error_severities": severity_counts,
            "recent_errors": [e.to_dict() for e in self.error_history[-5:]],  # Last 5 errors
            "circuit_breaker_status": {
                name: {"state": cb.state, "failure_count": cb.failure_count}
                for name, cb in self.circuit_breakers.items()
            }
        }


# Global error handler instance
error_handler = SubfractureErrorHandler()


def with_error_handling(
    component: str,
    operation: str = None,
    retry_config: str = "api_call",
    severity: ErrorSeverity = ErrorSeverity.MEDIUM
):
    """Decorator for automatic error handling"""
    
    def decorator(func: Callable) -> Callable:
        operation_name = operation or func.__name__
        
        @wraps(func)
        @traceable(name=f"error_handled_{func.__name__}")
        async def wrapper(*args, **kwargs):
            async def execute_func():
                return await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
            
            return await error_handler.execute_with_recovery(
                operation=execute_func,
                component=component,
                operation_name=operation_name,
                context={"args_count": len(args), "kwargs_keys": list(kwargs.keys())},
                retry_config_key=retry_config
            )
        
        return wrapper
    
    return decorator


def with_fallback(component: str, operation: str = None):
    """Decorator for automatic fallback execution"""
    
    def decorator(func: Callable) -> Callable:
        operation_name = operation or func.__name__
        
        @wraps(func)
        @traceable(name=f"fallback_enabled_{func.__name__}")
        async def wrapper(*args, **kwargs):
            async def execute_func():
                return await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
            
            return await error_handler.execute_with_fallback(
                primary_operation=execute_func,
                component=component,
                operation=operation_name,
                context={"args_count": len(args), "kwargs_keys": list(kwargs.keys())}
            )
        
        return wrapper
    
    return decorator


# Fallback strategies for critical SUBFRACTURE components
async def strategy_swarm_fallback(context: Dict[str, Any]) -> Dict[str, Any]:
    """Fallback strategy for strategy swarm failures"""
    return {
        "strategic_insights": {
            "core_truths": [
                "Authentic brand positioning creates sustainable competitive advantage",
                "Strategic clarity drives operational efficiency and market success",
                "Human-centered approach differentiates in automated marketplace"
            ],
            "strategic_summary": {
                "competitive_advantage": "Distinctive methodology and authentic human insight",
                "market_opportunity": "Growing demand for human-centered brand development",
                "strategic_recommendation": "Focus on authentic differentiation and systematic delivery"
            }
        },
        "fallback_used": True,
        "fallback_reason": "Primary strategy analysis unavailable"
    }


async def creative_swarm_fallback(context: Dict[str, Any]) -> Dict[str, Any]:
    """Fallback strategy for creative swarm failures"""
    return {
        "creative_directions": {
            "target_insights": [
                "Seeking authentic connection over superficial engagement",
                "Values depth and substance in business relationships",
                "Appreciates sophisticated yet accessible communication"
            ],
            "creative_territories": [
                "Professional authenticity and human-centered expertise",
                "Sophisticated methodology with warm, approachable delivery",
                "Strategic depth combined with practical implementation"
            ],
            "human_breakthroughs": [
                "Recognition that authentic human insight cannot be automated",
                "Understanding that strategic depth requires human wisdom and experience"
            ]
        },
        "fallback_used": True,
        "fallback_reason": "Primary creative analysis unavailable"
    }


# Register fallback strategies
error_handler.register_fallback("strategy_swarm", "strategic_truth_discovery", strategy_swarm_fallback)
error_handler.register_fallback("creative_swarm", "creative_insight_discovery", creative_swarm_fallback)