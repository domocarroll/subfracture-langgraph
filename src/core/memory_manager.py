"""
SUBFRACTURE Memory Management & State Persistence

Advanced memory management, state persistence, and checkpoint recovery
for production SUBFRACTURE workflows. Ensures efficient resource usage
and reliable state recovery across sessions.

Features:
- Intelligent memory optimization and cleanup
- State checkpointing and recovery
- Session persistence across restarts
- Memory usage monitoring and alerts
- Garbage collection optimization
- State compression and serialization
"""

import asyncio
import gc
import pickle
import gzip
import json
import os
import psutil
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from pathlib import Path
import structlog
from functools import wraps

from langsmith import traceable

from .state import SubfractureGravityState
from .error_handling import with_error_handling, ErrorSeverity

logger = structlog.get_logger()


@dataclass
class MemoryMetrics:
    """Memory usage metrics"""
    timestamp: datetime
    process_memory_mb: float
    system_memory_percent: float
    python_objects_count: int
    gc_collections: Dict[int, int]
    checkpoint_size_mb: float
    state_objects_count: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            **asdict(self),
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class StateCheckpoint:
    """State checkpoint for persistence"""
    checkpoint_id: str
    timestamp: datetime
    workflow_phase: str
    state_data: Dict[str, Any]
    metadata: Dict[str, Any]
    compressed_size_bytes: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "checkpoint_id": self.checkpoint_id,
            "timestamp": self.timestamp.isoformat(),
            "workflow_phase": self.workflow_phase,
            "metadata": self.metadata,
            "compressed_size_bytes": self.compressed_size_bytes
            # Note: state_data excluded from dict for size reasons
        }


class MemoryManager:
    """
    Advanced memory management system for SUBFRACTURE workflows
    """
    
    def __init__(self, max_memory_mb: int = 2048, checkpoint_dir: str = "checkpoints"):
        self.max_memory_mb = max_memory_mb
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(exist_ok=True)
        
        self.logger = logger.bind(component="memory_manager")
        
        # Memory tracking
        self.memory_history: List[MemoryMetrics] = []
        self.memory_alerts_enabled = True
        self.memory_cleanup_threshold = 0.8  # 80% of max memory
        
        # State management
        self.active_states: Dict[str, SubfractureGravityState] = {}
        self.checkpoints: Dict[str, StateCheckpoint] = {}
        self.checkpoint_retention_hours = 24
        
        # Optimization settings
        self.gc_optimization_enabled = True
        self.state_compression_enabled = True
        self.automatic_cleanup_enabled = True
        
        # Background monitoring
        self.monitoring_task: Optional[asyncio.Task] = None
        self.monitoring_interval = 30  # seconds
        
    async def initialize(self):
        """Initialize memory management system"""
        
        try:
            # Start background monitoring
            if self.monitoring_task is None:
                self.monitoring_task = asyncio.create_task(self._background_monitoring())
            
            # Load existing checkpoints
            await self._load_checkpoints()
            
            # Initial memory metrics
            await self._record_memory_metrics()
            
            self.logger.info("Memory manager initialized",
                           max_memory_mb=self.max_memory_mb,
                           checkpoint_dir=str(self.checkpoint_dir),
                           existing_checkpoints=len(self.checkpoints))
            
        except Exception as e:
            self.logger.error("Memory manager initialization failed", error=str(e))
            raise
    
    async def shutdown(self):
        """Shutdown memory management system"""
        
        try:
            # Cancel background monitoring
            if self.monitoring_task:
                self.monitoring_task.cancel()
                try:
                    await self.monitoring_task
                except asyncio.CancelledError:
                    pass
            
            # Final cleanup
            await self._cleanup_memory()
            
            self.logger.info("Memory manager shutdown completed")
            
        except Exception as e:
            self.logger.error("Memory manager shutdown failed", error=str(e))
    
    @traceable(name="create_checkpoint")
    @with_error_handling("memory_manager", "checkpoint_creation", severity=ErrorSeverity.HIGH)
    async def create_checkpoint(
        self,
        session_id: str,
        state: SubfractureGravityState,
        workflow_phase: str,
        metadata: Dict[str, Any] = None
    ) -> str:
        """Create state checkpoint for persistence"""
        
        try:
            checkpoint_id = f"{session_id}_{workflow_phase}_{int(time.time())}"
            metadata = metadata or {}
            
            # Serialize state
            state_data = await self._serialize_state(state)
            
            # Compress if enabled
            if self.state_compression_enabled:
                compressed_data = await self._compress_data(state_data)
                compressed_size = len(compressed_data)
            else:
                compressed_data = state_data
                compressed_size = len(json.dumps(state_data).encode())
            
            # Create checkpoint
            checkpoint = StateCheckpoint(
                checkpoint_id=checkpoint_id,
                timestamp=datetime.now(),
                workflow_phase=workflow_phase,
                state_data=state_data,
                metadata=metadata,
                compressed_size_bytes=compressed_size
            )
            
            # Save to disk
            await self._save_checkpoint_to_disk(checkpoint, compressed_data)
            
            # Store in memory (without state_data to save memory)
            self.checkpoints[checkpoint_id] = StateCheckpoint(
                checkpoint_id=checkpoint_id,
                timestamp=checkpoint.timestamp,
                workflow_phase=workflow_phase,
                state_data={},  # Empty to save memory
                metadata=metadata,
                compressed_size_bytes=compressed_size
            )
            
            self.logger.info("Checkpoint created",
                           checkpoint_id=checkpoint_id,
                           workflow_phase=workflow_phase,
                           compressed_size_mb=compressed_size / 1024 / 1024)
            
            return checkpoint_id
            
        except Exception as e:
            self.logger.error("Checkpoint creation failed", error=str(e))
            raise
    
    @traceable(name="restore_checkpoint")
    @with_error_handling("memory_manager", "checkpoint_restoration", severity=ErrorSeverity.HIGH)
    async def restore_checkpoint(self, checkpoint_id: str) -> SubfractureGravityState:
        """Restore state from checkpoint"""
        
        try:
            if checkpoint_id not in self.checkpoints:
                raise ValueError(f"Checkpoint {checkpoint_id} not found")
            
            # Load checkpoint from disk
            checkpoint_data = await self._load_checkpoint_from_disk(checkpoint_id)
            
            # Decompress if needed
            if self.state_compression_enabled:
                state_data = await self._decompress_data(checkpoint_data)
            else:
                state_data = checkpoint_data
            
            # Deserialize state
            restored_state = await self._deserialize_state(state_data)
            
            self.logger.info("Checkpoint restored",
                           checkpoint_id=checkpoint_id,
                           workflow_phase=self.checkpoints[checkpoint_id].workflow_phase)
            
            return restored_state
            
        except Exception as e:
            self.logger.error("Checkpoint restoration failed", 
                            checkpoint_id=checkpoint_id, error=str(e))
            raise
    
    @traceable(name="register_active_state")
    async def register_active_state(self, session_id: str, state: SubfractureGravityState):
        """Register active state for memory monitoring"""
        
        self.active_states[session_id] = state
        
        # Check memory usage after adding state
        await self._check_memory_usage()
        
        self.logger.debug("Active state registered",
                         session_id=session_id,
                         total_active_states=len(self.active_states))
    
    async def unregister_active_state(self, session_id: str):
        """Unregister active state to free memory"""
        
        if session_id in self.active_states:
            del self.active_states[session_id]
            
            # Trigger garbage collection
            if self.gc_optimization_enabled:
                gc.collect()
            
            self.logger.debug("Active state unregistered",
                             session_id=session_id,
                             remaining_active_states=len(self.active_states))
    
    async def _serialize_state(self, state: SubfractureGravityState) -> Dict[str, Any]:
        """Serialize state to dictionary"""
        
        try:
            # Convert Pydantic model to dict
            state_dict = state.dict()
            
            # Handle special serialization for complex objects
            for key, value in state_dict.items():
                if hasattr(value, 'dict'):  # Pydantic model
                    state_dict[key] = value.dict()
                elif isinstance(value, datetime):
                    state_dict[key] = value.isoformat()
                elif not isinstance(value, (str, int, float, bool, list, dict, type(None))):
                    # Convert complex objects to string representation
                    state_dict[key] = str(value)
            
            return state_dict
            
        except Exception as e:
            self.logger.error("State serialization failed", error=str(e))
            raise
    
    async def _deserialize_state(self, state_data: Dict[str, Any]) -> SubfractureGravityState:
        """Deserialize state from dictionary"""
        
        try:
            # Create new state instance from dict
            restored_state = SubfractureGravityState(**state_data)
            return restored_state
            
        except Exception as e:
            self.logger.error("State deserialization failed", error=str(e))
            # Try to create minimal valid state
            minimal_state = SubfractureGravityState(
                brand_brief=state_data.get("brand_brief", ""),
                operator_context=state_data.get("operator_context", {}),
                target_outcome=state_data.get("target_outcome", "")
            )
            self.logger.warning("Using minimal state due to deserialization error")
            return minimal_state
    
    async def _compress_data(self, data: Dict[str, Any]) -> bytes:
        """Compress data for storage"""
        
        try:
            # Convert to JSON bytes
            json_data = json.dumps(data, default=str).encode('utf-8')
            
            # Compress with gzip
            compressed_data = gzip.compress(json_data)
            
            compression_ratio = len(compressed_data) / len(json_data)
            self.logger.debug("Data compressed",
                            original_size=len(json_data),
                            compressed_size=len(compressed_data),
                            compression_ratio=compression_ratio)
            
            return compressed_data
            
        except Exception as e:
            self.logger.error("Data compression failed", error=str(e))
            raise
    
    async def _decompress_data(self, compressed_data: bytes) -> Dict[str, Any]:
        """Decompress data from storage"""
        
        try:
            # Decompress
            json_data = gzip.decompress(compressed_data)
            
            # Convert back to dict
            data = json.loads(json_data.decode('utf-8'))
            
            return data
            
        except Exception as e:
            self.logger.error("Data decompression failed", error=str(e))
            raise
    
    async def _save_checkpoint_to_disk(self, checkpoint: StateCheckpoint, data: Union[Dict, bytes]):
        """Save checkpoint to disk"""
        
        try:
            checkpoint_file = self.checkpoint_dir / f"{checkpoint.checkpoint_id}.pkl"
            metadata_file = self.checkpoint_dir / f"{checkpoint.checkpoint_id}.json"
            
            # Save compressed data
            with open(checkpoint_file, 'wb') as f:
                if isinstance(data, bytes):
                    f.write(data)
                else:
                    pickle.dump(data, f)
            
            # Save metadata
            with open(metadata_file, 'w') as f:
                json.dump(checkpoint.to_dict(), f, indent=2)
            
        except Exception as e:
            self.logger.error("Checkpoint disk save failed", error=str(e))
            raise
    
    async def _load_checkpoint_from_disk(self, checkpoint_id: str) -> Union[Dict, bytes]:
        """Load checkpoint from disk"""
        
        try:
            checkpoint_file = self.checkpoint_dir / f"{checkpoint_id}.pkl"
            
            if not checkpoint_file.exists():
                raise FileNotFoundError(f"Checkpoint file not found: {checkpoint_file}")
            
            with open(checkpoint_file, 'rb') as f:
                if self.state_compression_enabled:
                    return f.read()  # Return bytes for decompression
                else:
                    return pickle.load(f)  # Return dict directly
            
        except Exception as e:
            self.logger.error("Checkpoint disk load failed", error=str(e))
            raise
    
    async def _load_checkpoints(self):
        """Load existing checkpoints from disk"""
        
        try:
            checkpoint_files = list(self.checkpoint_dir.glob("*.json"))
            
            for metadata_file in checkpoint_files:
                try:
                    with open(metadata_file, 'r') as f:
                        checkpoint_data = json.load(f)
                    
                    checkpoint_id = checkpoint_data["checkpoint_id"]
                    
                    # Create checkpoint object (without state_data to save memory)
                    checkpoint = StateCheckpoint(
                        checkpoint_id=checkpoint_id,
                        timestamp=datetime.fromisoformat(checkpoint_data["timestamp"]),
                        workflow_phase=checkpoint_data["workflow_phase"],
                        state_data={},  # Empty to save memory
                        metadata=checkpoint_data.get("metadata", {}),
                        compressed_size_bytes=checkpoint_data.get("compressed_size_bytes", 0)
                    )
                    
                    self.checkpoints[checkpoint_id] = checkpoint
                    
                except Exception as e:
                    self.logger.warning("Failed to load checkpoint metadata",
                                      file=str(metadata_file), error=str(e))
            
            # Clean up old checkpoints
            await self._cleanup_old_checkpoints()
            
            self.logger.info("Checkpoints loaded",
                           total_checkpoints=len(self.checkpoints))
            
        except Exception as e:
            self.logger.error("Checkpoint loading failed", error=str(e))
    
    async def _cleanup_old_checkpoints(self):
        """Clean up old checkpoints beyond retention period"""
        
        try:
            cutoff_time = datetime.now() - timedelta(hours=self.checkpoint_retention_hours)
            old_checkpoints = []
            
            for checkpoint_id, checkpoint in self.checkpoints.items():
                if checkpoint.timestamp < cutoff_time:
                    old_checkpoints.append(checkpoint_id)
            
            # Remove old checkpoints
            for checkpoint_id in old_checkpoints:
                await self._remove_checkpoint(checkpoint_id)
            
            if old_checkpoints:
                self.logger.info("Old checkpoints cleaned up",
                               removed_count=len(old_checkpoints))
            
        except Exception as e:
            self.logger.error("Checkpoint cleanup failed", error=str(e))
    
    async def _remove_checkpoint(self, checkpoint_id: str):
        """Remove checkpoint from memory and disk"""
        
        try:
            # Remove from memory
            if checkpoint_id in self.checkpoints:
                del self.checkpoints[checkpoint_id]
            
            # Remove from disk
            checkpoint_file = self.checkpoint_dir / f"{checkpoint_id}.pkl"
            metadata_file = self.checkpoint_dir / f"{checkpoint_id}.json"
            
            if checkpoint_file.exists():
                checkpoint_file.unlink()
            
            if metadata_file.exists():
                metadata_file.unlink()
            
        except Exception as e:
            self.logger.warning("Checkpoint removal failed",
                              checkpoint_id=checkpoint_id, error=str(e))
    
    async def _background_monitoring(self):
        """Background memory monitoring task"""
        
        while True:
            try:
                await asyncio.sleep(self.monitoring_interval)
                
                # Record memory metrics
                await self._record_memory_metrics()
                
                # Check memory usage and cleanup if needed
                await self._check_memory_usage()
                
                # Cleanup old checkpoints periodically
                if len(self.memory_history) % 20 == 0:  # Every 20 intervals
                    await self._cleanup_old_checkpoints()
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error("Background monitoring error", error=str(e))
                await asyncio.sleep(5)  # Brief pause before retrying
    
    async def _record_memory_metrics(self):
        """Record current memory metrics"""
        
        try:
            # Get process memory info
            process = psutil.Process()
            process_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            # Get system memory info
            system_memory = psutil.virtual_memory()
            system_memory_percent = system_memory.percent
            
            # Get Python object count
            python_objects = len(gc.get_objects())
            
            # Get garbage collection stats
            gc_stats = {i: gc.get_count()[i] for i in range(3)}
            
            # Calculate checkpoint sizes
            total_checkpoint_size = sum(
                checkpoint.compressed_size_bytes 
                for checkpoint in self.checkpoints.values()
            ) / 1024 / 1024  # MB
            
            # Create metrics
            metrics = MemoryMetrics(
                timestamp=datetime.now(),
                process_memory_mb=process_memory,
                system_memory_percent=system_memory_percent,
                python_objects_count=python_objects,
                gc_collections=gc_stats,
                checkpoint_size_mb=total_checkpoint_size,
                state_objects_count=len(self.active_states)
            )
            
            # Store metrics (keep last 100 measurements)
            self.memory_history.append(metrics)
            if len(self.memory_history) > 100:
                self.memory_history = self.memory_history[-100:]
            
            self.logger.debug("Memory metrics recorded",
                            process_memory_mb=process_memory,
                            system_memory_percent=system_memory_percent,
                            python_objects=python_objects,
                            active_states=len(self.active_states))
            
        except Exception as e:
            self.logger.error("Memory metrics recording failed", error=str(e))
    
    async def _check_memory_usage(self):
        """Check memory usage and trigger cleanup if needed"""
        
        try:
            if not self.memory_history:
                return
            
            latest_metrics = self.memory_history[-1]
            
            # Check process memory usage
            memory_usage_ratio = latest_metrics.process_memory_mb / self.max_memory_mb
            
            if memory_usage_ratio > self.memory_cleanup_threshold:
                self.logger.warning("High memory usage detected",
                                  current_mb=latest_metrics.process_memory_mb,
                                  max_mb=self.max_memory_mb,
                                  usage_ratio=memory_usage_ratio)
                
                if self.automatic_cleanup_enabled:
                    await self._cleanup_memory()
            
            # Check system memory usage
            if latest_metrics.system_memory_percent > 90:
                self.logger.warning("High system memory usage",
                                  system_memory_percent=latest_metrics.system_memory_percent)
                
                if self.automatic_cleanup_enabled:
                    await self._aggressive_cleanup()
            
        except Exception as e:
            self.logger.error("Memory usage check failed", error=str(e))
    
    async def _cleanup_memory(self):
        """Perform memory cleanup"""
        
        try:
            self.logger.info("Starting memory cleanup")
            
            # Force garbage collection
            if self.gc_optimization_enabled:
                collected = gc.collect()
                self.logger.debug("Garbage collection completed", objects_collected=collected)
            
            # Clean up old active states (keep only recent ones)
            if len(self.active_states) > 5:
                # Sort by activity (this is simplified - in real implementation, track last access time)
                excess_states = list(self.active_states.keys())[5:]
                for session_id in excess_states:
                    await self.unregister_active_state(session_id)
                
                self.logger.info("Excess active states cleaned up", removed_count=len(excess_states))
            
            # Trim memory history
            if len(self.memory_history) > 50:
                self.memory_history = self.memory_history[-50:]
            
            self.logger.info("Memory cleanup completed")
            
        except Exception as e:
            self.logger.error("Memory cleanup failed", error=str(e))
    
    async def _aggressive_cleanup(self):
        """Perform aggressive memory cleanup under pressure"""
        
        try:
            self.logger.warning("Starting aggressive memory cleanup")
            
            # Remove all but the most recent active state
            if len(self.active_states) > 1:
                session_ids = list(self.active_states.keys())
                for session_id in session_ids[:-1]:  # Keep only the last one
                    await self.unregister_active_state(session_id)
            
            # Force multiple garbage collection cycles
            for _ in range(3):
                gc.collect()
            
            # Clean up old checkpoints more aggressively
            cutoff_time = datetime.now() - timedelta(hours=self.checkpoint_retention_hours // 2)
            old_checkpoints = [
                checkpoint_id for checkpoint_id, checkpoint in self.checkpoints.items()
                if checkpoint.timestamp < cutoff_time
            ]
            
            for checkpoint_id in old_checkpoints:
                await self._remove_checkpoint(checkpoint_id)
            
            self.logger.warning("Aggressive memory cleanup completed",
                              states_removed=len(self.active_states) - 1,
                              checkpoints_removed=len(old_checkpoints))
            
        except Exception as e:
            self.logger.error("Aggressive memory cleanup failed", error=str(e))
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """Get comprehensive memory usage summary"""
        
        if not self.memory_history:
            return {"status": "no_data"}
        
        latest_metrics = self.memory_history[-1]
        
        # Calculate trends
        if len(self.memory_history) >= 2:
            previous_metrics = self.memory_history[-2]
            memory_trend = "increasing" if latest_metrics.process_memory_mb > previous_metrics.process_memory_mb else "decreasing"
            objects_trend = "increasing" if latest_metrics.python_objects_count > previous_metrics.python_objects_count else "decreasing"
        else:
            memory_trend = "stable"
            objects_trend = "stable"
        
        return {
            "current_metrics": latest_metrics.to_dict(),
            "memory_usage_ratio": latest_metrics.process_memory_mb / self.max_memory_mb,
            "memory_trend": memory_trend,
            "objects_trend": objects_trend,
            "active_states_count": len(self.active_states),
            "checkpoints_count": len(self.checkpoints),
            "total_checkpoint_size_mb": sum(c.compressed_size_bytes for c in self.checkpoints.values()) / 1024 / 1024,
            "memory_alerts_triggered": self._count_memory_alerts(),
            "automatic_cleanup_enabled": self.automatic_cleanup_enabled,
            "monitoring_active": self.monitoring_task is not None and not self.monitoring_task.done()
        }
    
    def _count_memory_alerts(self) -> int:
        """Count recent memory alerts"""
        
        if len(self.memory_history) < 5:
            return 0
        
        recent_metrics = self.memory_history[-5:]
        alerts = sum(
            1 for metrics in recent_metrics
            if metrics.process_memory_mb / self.max_memory_mb > self.memory_cleanup_threshold
        )
        
        return alerts


# Global memory manager instance
memory_manager = MemoryManager()


def with_memory_management(checkpoint_phase: str = None):
    """Decorator for automatic memory management and checkpointing"""
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        @traceable(name=f"memory_managed_{func.__name__}")
        async def wrapper(*args, **kwargs):
            # Extract state and session info
            state = None
            session_id = None
            
            for arg in args:
                if isinstance(arg, SubfractureGravityState):
                    state = arg
                    session_id = getattr(arg, 'session_id', 'default_session')
                    break
            
            # Register state if found
            if state and session_id:
                await memory_manager.register_active_state(session_id, state)
            
            try:
                # Execute function
                result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
                
                # Create checkpoint if phase specified and state modified
                if checkpoint_phase and state and session_id and isinstance(result, dict):
                    # Check if state was modified (simplified check)
                    if any(key in result for key in ['strategy_insights', 'creative_directions', 'design_synthesis', 'technology_roadmap', 'gravity_analysis']):
                        await memory_manager.create_checkpoint(
                            session_id=session_id,
                            state=state,
                            workflow_phase=checkpoint_phase,
                            metadata={"function": func.__name__, "result_keys": list(result.keys()) if isinstance(result, dict) else []}
                        )
                
                return result
                
            finally:
                # Cleanup happens automatically in background monitoring
                pass
        
        return wrapper
    
    return decorator


# Initialization function
async def initialize_memory_management():
    """Initialize the global memory manager"""
    await memory_manager.initialize()


# Shutdown function  
async def shutdown_memory_management():
    """Shutdown the global memory manager"""
    await memory_manager.shutdown()