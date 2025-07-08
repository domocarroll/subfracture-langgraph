"""
SUBFRACTURE Async Optimization & Parallel Execution Engine

Advanced async optimization for SUBFRACTURE workflows to maximize performance,
reduce latency, and enable concurrent processing of brand development tasks.

Features:
- Intelligent task parallelization
- Dependency-aware execution ordering
- Resource pool management
- Adaptive concurrency limiting
- Performance monitoring and optimization
- Memory-efficient async operations
"""

import asyncio
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable, Tuple, Set
from dataclasses import dataclass
from enum import Enum
import structlog
from concurrent.futures import ThreadPoolExecutor
import threading

from langsmith import traceable

from .error_handling import with_error_handling, ErrorSeverity

logger = structlog.get_logger()


class TaskPriority(Enum):
    """Task priority levels for execution ordering"""
    CRITICAL = 0    # Must execute first (dependencies)
    HIGH = 1       # Important for workflow success
    MEDIUM = 2     # Standard priority
    LOW = 3        # Can be delayed if needed


class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class AsyncTask:
    """Async task definition for parallel execution"""
    task_id: str
    function: Callable
    args: Tuple
    kwargs: Dict[str, Any]
    priority: TaskPriority
    dependencies: List[str]
    estimated_duration: float
    timeout: Optional[float]
    retry_count: int = 0
    max_retries: int = 3
    status: TaskStatus = TaskStatus.PENDING
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    result: Any = None
    error: Optional[Exception] = None
    
    def __post_init__(self):
        if self.timeout is None:
            self.timeout = max(30.0, self.estimated_duration * 3)  # Default timeout


@dataclass
class ExecutionPlan:
    """Optimized execution plan for parallel task execution"""
    execution_phases: List[List[AsyncTask]]
    total_estimated_duration: float
    parallelization_factor: float
    critical_path_duration: float
    optimization_score: float


class AsyncOptimizer:
    """
    Advanced async optimization engine for SUBFRACTURE workflows
    """
    
    def __init__(self, max_concurrent_tasks: int = 8):
        self.max_concurrent_tasks = max_concurrent_tasks
        self.logger = logger.bind(component="async_optimizer")
        
        # Resource management
        self.semaphore = asyncio.Semaphore(max_concurrent_tasks)
        self.thread_pool = ThreadPoolExecutor(max_workers=4)
        
        # Performance tracking
        self.execution_history: List[Dict[str, Any]] = []
        self.performance_metrics: Dict[str, float] = {}
        
        # Task management
        self.active_tasks: Dict[str, AsyncTask] = {}
        self.completed_tasks: Dict[str, AsyncTask] = {}
        
        # Adaptive optimization
        self.optimal_concurrency_level = max_concurrent_tasks // 2
        self.performance_window = 10  # Last 10 executions for optimization
    
    @traceable(name="create_execution_plan")
    async def create_execution_plan(self, tasks: List[AsyncTask]) -> ExecutionPlan:
        """Create optimized execution plan with dependency resolution"""
        
        try:
            # Validate dependencies
            await self._validate_dependencies(tasks)
            
            # Topological sort for dependency resolution
            execution_phases = await self._resolve_dependencies(tasks)
            
            # Calculate execution metrics
            total_estimated_duration = sum(task.estimated_duration for task in tasks)
            critical_path_duration = await self._calculate_critical_path(execution_phases)
            parallelization_factor = total_estimated_duration / critical_path_duration if critical_path_duration > 0 else 1.0
            optimization_score = await self._calculate_optimization_score(execution_phases)
            
            execution_plan = ExecutionPlan(
                execution_phases=execution_phases,
                total_estimated_duration=total_estimated_duration,
                parallelization_factor=parallelization_factor,
                critical_path_duration=critical_path_duration,
                optimization_score=optimization_score
            )
            
            self.logger.info("Execution plan created",
                           phases=len(execution_phases),
                           total_tasks=len(tasks),
                           parallelization_factor=parallelization_factor,
                           optimization_score=optimization_score)
            
            return execution_plan
            
        except Exception as e:
            self.logger.error("Execution plan creation failed", error=str(e))
            raise
    
    @traceable(name="execute_parallel_workflow")
    async def execute_parallel_workflow(self, execution_plan: ExecutionPlan) -> Dict[str, Any]:
        """Execute workflow with optimized parallel processing"""
        
        start_time = time.time()
        results = {}
        
        try:
            self.logger.info("Starting parallel workflow execution",
                           phases=len(execution_plan.execution_phases),
                           estimated_duration=execution_plan.total_estimated_duration)
            
            # Execute phases sequentially, tasks within phases in parallel
            for phase_idx, phase_tasks in enumerate(execution_plan.execution_phases):
                phase_start = time.time()
                
                self.logger.info(f"Executing phase {phase_idx + 1}",
                               tasks_in_phase=len(phase_tasks))
                
                # Execute all tasks in current phase concurrently
                phase_results = await self._execute_phase_parallel(phase_tasks)
                results.update(phase_results)
                
                phase_duration = time.time() - phase_start
                self.logger.info(f"Phase {phase_idx + 1} completed",
                               duration=phase_duration,
                               tasks_completed=len(phase_results))
            
            total_duration = time.time() - start_time
            
            # Record execution metrics
            execution_record = {
                "execution_id": f"exec_{int(time.time())}",
                "start_time": datetime.fromtimestamp(start_time),
                "duration": total_duration,
                "tasks_executed": sum(len(phase) for phase in execution_plan.execution_phases),
                "phases": len(execution_plan.execution_phases),
                "parallelization_achieved": execution_plan.total_estimated_duration / total_duration if total_duration > 0 else 1.0,
                "optimization_score": execution_plan.optimization_score
            }
            
            self.execution_history.append(execution_record)
            
            # Update performance metrics
            await self._update_performance_metrics(execution_record)
            
            self.logger.info("Parallel workflow execution completed",
                           total_duration=total_duration,
                           tasks_executed=len(results),
                           parallelization_achieved=execution_record["parallelization_achieved"])
            
            return {
                "results": results,
                "execution_metrics": execution_record,
                "performance_improvement": await self._calculate_performance_improvement()
            }
            
        except Exception as e:
            self.logger.error("Parallel workflow execution failed", error=str(e))
            raise
    
    async def _validate_dependencies(self, tasks: List[AsyncTask]):
        """Validate task dependencies for circular references"""
        
        task_ids = {task.task_id for task in tasks}
        
        for task in tasks:
            # Check if all dependencies exist
            for dep in task.dependencies:
                if dep not in task_ids:
                    raise ValueError(f"Task {task.task_id} depends on non-existent task {dep}")
            
            # Check for self-dependency
            if task.task_id in task.dependencies:
                raise ValueError(f"Task {task.task_id} has circular dependency on itself")
        
        # Check for circular dependencies using DFS
        visited = set()
        rec_stack = set()
        
        def has_cycle(task_id: str, task_map: Dict[str, AsyncTask]) -> bool:
            visited.add(task_id)
            rec_stack.add(task_id)
            
            task = task_map[task_id]
            for dep in task.dependencies:
                if dep not in visited:
                    if has_cycle(dep, task_map):
                        return True
                elif dep in rec_stack:
                    return True
            
            rec_stack.remove(task_id)
            return False
        
        task_map = {task.task_id: task for task in tasks}
        
        for task in tasks:
            if task.task_id not in visited:
                if has_cycle(task.task_id, task_map):
                    raise ValueError(f"Circular dependency detected involving task {task.task_id}")
    
    async def _resolve_dependencies(self, tasks: List[AsyncTask]) -> List[List[AsyncTask]]:
        """Resolve dependencies and create execution phases"""
        
        task_map = {task.task_id: task for task in tasks}
        phases = []
        remaining_tasks = set(task.task_id for task in tasks)
        completed_tasks = set()
        
        while remaining_tasks:
            # Find tasks that can be executed (all dependencies completed)
            current_phase_tasks = []
            
            for task_id in list(remaining_tasks):
                task = task_map[task_id]
                if all(dep in completed_tasks for dep in task.dependencies):
                    current_phase_tasks.append(task)
                    remaining_tasks.remove(task_id)
            
            if not current_phase_tasks:
                # This shouldn't happen if dependencies are valid
                raise ValueError("Unable to resolve dependencies - possible circular dependency")
            
            # Sort current phase by priority
            current_phase_tasks.sort(key=lambda t: t.priority.value)
            phases.append(current_phase_tasks)
            
            # Mark phase tasks as completed for dependency resolution
            completed_tasks.update(task.task_id for task in current_phase_tasks)
        
        return phases
    
    async def _execute_phase_parallel(self, phase_tasks: List[AsyncTask]) -> Dict[str, Any]:
        """Execute all tasks in a phase concurrently"""
        
        # Limit concurrency based on optimal level
        concurrency_limit = min(len(phase_tasks), self.optimal_concurrency_level)
        semaphore = asyncio.Semaphore(concurrency_limit)
        
        async def execute_single_task(task: AsyncTask) -> Tuple[str, Any]:
            async with semaphore:
                return await self._execute_task_with_monitoring(task)
        
        # Execute all tasks concurrently
        task_coroutines = [execute_single_task(task) for task in phase_tasks]
        
        try:
            # Use asyncio.gather with return_exceptions to handle individual task failures
            results = await asyncio.gather(*task_coroutines, return_exceptions=True)
            
            # Process results and handle exceptions
            phase_results = {}
            for i, result in enumerate(results):
                task = phase_tasks[i]
                
                if isinstance(result, Exception):
                    task.status = TaskStatus.FAILED
                    task.error = result
                    self.logger.error(f"Task {task.task_id} failed",
                                    error=str(result),
                                    task_duration=task.estimated_duration)
                    
                    # Use fallback result if available
                    fallback_result = await self._get_fallback_result(task)
                    if fallback_result is not None:
                        phase_results[task.task_id] = fallback_result
                else:
                    task_id, task_result = result
                    phase_results[task_id] = task_result
                    task.status = TaskStatus.COMPLETED
                    task.result = task_result
            
            return phase_results
            
        except Exception as e:
            self.logger.error("Phase execution failed", error=str(e))
            raise
    
    @with_error_handling("async_optimizer", "task_execution", severity=ErrorSeverity.MEDIUM)
    async def _execute_task_with_monitoring(self, task: AsyncTask) -> Tuple[str, Any]:
        """Execute individual task with monitoring and timeout"""
        
        task.status = TaskStatus.RUNNING
        task.start_time = datetime.now()
        self.active_tasks[task.task_id] = task
        
        try:
            # Execute task with timeout
            result = await asyncio.wait_for(
                self._execute_task_function(task),
                timeout=task.timeout
            )
            
            task.end_time = datetime.now()
            task.result = result
            task.status = TaskStatus.COMPLETED
            
            # Move to completed tasks
            self.completed_tasks[task.task_id] = task
            if task.task_id in self.active_tasks:
                del self.active_tasks[task.task_id]
            
            execution_time = (task.end_time - task.start_time).total_seconds()
            self.logger.info(f"Task {task.task_id} completed",
                           duration=execution_time,
                           estimated_duration=task.estimated_duration)
            
            return task.task_id, result
            
        except asyncio.TimeoutError:
            task.status = TaskStatus.FAILED
            task.error = Exception(f"Task {task.task_id} timed out after {task.timeout}s")
            self.logger.error(f"Task {task.task_id} timed out",
                            timeout=task.timeout,
                            estimated_duration=task.estimated_duration)
            raise task.error
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = e
            task.end_time = datetime.now()
            
            if task.task_id in self.active_tasks:
                del self.active_tasks[task.task_id]
            
            self.logger.error(f"Task {task.task_id} failed",
                            error=str(e),
                            retry_count=task.retry_count)
            raise e
    
    async def _execute_task_function(self, task: AsyncTask) -> Any:
        """Execute the actual task function"""
        
        function = task.function
        args = task.args
        kwargs = task.kwargs
        
        # Handle both async and sync functions
        if asyncio.iscoroutinefunction(function):
            return await function(*args, **kwargs)
        else:
            # Run sync function in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(self.thread_pool, lambda: function(*args, **kwargs))
    
    async def _get_fallback_result(self, task: AsyncTask) -> Any:
        """Get fallback result for failed task"""
        
        # Define fallback strategies for different task types
        fallback_strategies = {
            "strategy_swarm": lambda: {
                "strategic_insights": {
                    "core_truths": ["Authentic positioning creates advantage"],
                    "strategic_summary": {"status": "fallback_used"}
                }
            },
            "creative_swarm": lambda: {
                "creative_directions": {
                    "target_insights": ["Seeking authentic connection"],
                    "creative_territories": ["Professional authenticity"]
                }
            },
            "design_swarm": lambda: {
                "design_synthesis": {
                    "visual_languages": ["Professional clarity"],
                    "verbal_frameworks": ["Clear communication"]
                }
            },
            "technology_swarm": lambda: {
                "technology_roadmap": {
                    "user_journeys": ["Discovery to engagement"],
                    "friction_analysis": {"status": "fallback_used"}
                }
            },
            "gravity_analyzer": lambda: {
                "gravity_analysis": {f"gravity_{i}": 0.6 for i in range(5)},
                "gravity_index": 0.6
            }
        }
        
        # Extract component from task_id (assumes format like "component_operation")
        component = task.task_id.split('_')[0]
        
        if component in fallback_strategies:
            self.logger.info(f"Using fallback strategy for {task.task_id}")
            return fallback_strategies[component]()
        
        return None
    
    async def _calculate_critical_path(self, execution_phases: List[List[AsyncTask]]) -> float:
        """Calculate critical path duration"""
        
        total_duration = 0.0
        
        for phase in execution_phases:
            # Critical path is the longest task in each phase
            phase_duration = max(task.estimated_duration for task in phase) if phase else 0.0
            total_duration += phase_duration
        
        return total_duration
    
    async def _calculate_optimization_score(self, execution_phases: List[List[AsyncTask]]) -> float:
        """Calculate optimization score for execution plan"""
        
        if not execution_phases:
            return 0.0
        
        # Factors for optimization score
        total_tasks = sum(len(phase) for phase in execution_phases)
        avg_tasks_per_phase = total_tasks / len(execution_phases)
        
        # Better parallelization = higher score
        parallelization_score = min(1.0, avg_tasks_per_phase / 3.0)  # Normalize to 0-1
        
        # Fewer phases with more tasks per phase = better optimization
        phase_efficiency_score = min(1.0, avg_tasks_per_phase / len(execution_phases))
        
        # Combine scores
        optimization_score = (parallelization_score * 0.6 + phase_efficiency_score * 0.4)
        
        return optimization_score
    
    async def _update_performance_metrics(self, execution_record: Dict[str, Any]):
        """Update performance metrics for adaptive optimization"""
        
        # Update average metrics
        self.performance_metrics["avg_duration"] = self._calculate_moving_average(
            "duration", execution_record["duration"]
        )
        self.performance_metrics["avg_parallelization"] = self._calculate_moving_average(
            "parallelization_achieved", execution_record["parallelization_achieved"]
        )
        
        # Adaptive concurrency optimization
        if execution_record["parallelization_achieved"] > 2.0:
            # High parallelization achieved, can increase concurrency
            self.optimal_concurrency_level = min(
                self.max_concurrent_tasks,
                self.optimal_concurrency_level + 1
            )
        elif execution_record["parallelization_achieved"] < 1.2:
            # Low parallelization, reduce concurrency to avoid overhead
            self.optimal_concurrency_level = max(2, self.optimal_concurrency_level - 1)
        
        self.logger.debug("Performance metrics updated",
                         optimal_concurrency=self.optimal_concurrency_level,
                         avg_duration=self.performance_metrics.get("avg_duration"),
                         avg_parallelization=self.performance_metrics.get("avg_parallelization"))
    
    def _calculate_moving_average(self, metric_name: str, new_value: float) -> float:
        """Calculate moving average for performance metrics"""
        
        # Get recent values for moving average
        recent_executions = self.execution_history[-self.performance_window:]
        recent_values = [exec_record.get(metric_name, 0) for exec_record in recent_executions]
        recent_values.append(new_value)
        
        return sum(recent_values) / len(recent_values)
    
    async def _calculate_performance_improvement(self) -> Dict[str, float]:
        """Calculate performance improvement over baseline"""
        
        if len(self.execution_history) < 2:
            return {"improvement": 0.0, "baseline_duration": 0.0}
        
        # Compare recent performance to earlier baseline
        baseline_executions = self.execution_history[:min(5, len(self.execution_history) // 2)]
        recent_executions = self.execution_history[-5:]
        
        baseline_avg_duration = sum(e["duration"] for e in baseline_executions) / len(baseline_executions)
        recent_avg_duration = sum(e["duration"] for e in recent_executions) / len(recent_executions)
        
        improvement = (baseline_avg_duration - recent_avg_duration) / baseline_avg_duration if baseline_avg_duration > 0 else 0.0
        
        return {
            "improvement": improvement,
            "baseline_duration": baseline_avg_duration,
            "recent_duration": recent_avg_duration,
            "improvement_percentage": improvement * 100
        }
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary"""
        
        return {
            "execution_count": len(self.execution_history),
            "optimal_concurrency_level": self.optimal_concurrency_level,
            "performance_metrics": self.performance_metrics,
            "active_tasks": len(self.active_tasks),
            "completed_tasks": len(self.completed_tasks),
            "recent_executions": self.execution_history[-5:],
            "performance_trends": self._calculate_performance_trends()
        }
    
    def _calculate_performance_trends(self) -> Dict[str, str]:
        """Calculate performance trends"""
        
        if len(self.execution_history) < 3:
            return {"trend": "insufficient_data"}
        
        recent_durations = [e["duration"] for e in self.execution_history[-5:]]
        
        # Simple trend analysis
        if len(recent_durations) >= 3:
            early_avg = sum(recent_durations[:2]) / 2
            late_avg = sum(recent_durations[-2:]) / 2
            
            if late_avg < early_avg * 0.9:
                trend = "improving"
            elif late_avg > early_avg * 1.1:
                trend = "degrading"
            else:
                trend = "stable"
        else:
            trend = "stable"
        
        return {"trend": trend, "data_points": len(recent_durations)}


# Global async optimizer instance
async_optimizer = AsyncOptimizer()


# Helper functions for creating optimized async tasks
def create_async_task(
    task_id: str,
    function: Callable,
    args: Tuple = (),
    kwargs: Dict[str, Any] = None,
    priority: TaskPriority = TaskPriority.MEDIUM,
    dependencies: List[str] = None,
    estimated_duration: float = 30.0,
    timeout: Optional[float] = None
) -> AsyncTask:
    """Create an async task with optimization metadata"""
    
    return AsyncTask(
        task_id=task_id,
        function=function,
        args=args,
        kwargs=kwargs or {},
        priority=priority,
        dependencies=dependencies or [],
        estimated_duration=estimated_duration,
        timeout=timeout
    )


@traceable(name="optimize_subfracture_workflow")
async def optimize_subfracture_workflow(
    strategy_task: Callable,
    creative_task: Callable,
    design_task: Callable,
    technology_task: Callable,
    gravity_task: Callable,
    validation_tasks: List[Callable],
    synthesis_tasks: List[Callable],
    args: Tuple = (),
    kwargs: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Optimize complete SUBFRACTURE workflow for parallel execution
    """
    
    kwargs = kwargs or {}
    
    # Define optimized task execution plan
    tasks = [
        # Phase 1: Independent foundational work (can run in parallel)
        create_async_task(
            task_id="strategy_swarm",
            function=strategy_task,
            args=args,
            kwargs=kwargs,
            priority=TaskPriority.CRITICAL,
            dependencies=[],
            estimated_duration=180.0
        ),
        create_async_task(
            task_id="creative_swarm",
            function=creative_task,
            args=args,
            kwargs=kwargs,
            priority=TaskPriority.CRITICAL,
            dependencies=[],
            estimated_duration=180.0
        ),
        
        # Phase 2: Dependent on Phase 1 (can run in parallel after Phase 1)
        create_async_task(
            task_id="design_swarm",
            function=design_task,
            args=args,
            kwargs=kwargs,
            priority=TaskPriority.HIGH,
            dependencies=["strategy_swarm", "creative_swarm"],
            estimated_duration=150.0
        ),
        create_async_task(
            task_id="technology_swarm",
            function=technology_task,
            args=args,
            kwargs=kwargs,
            priority=TaskPriority.HIGH,
            dependencies=["strategy_swarm", "creative_swarm"],
            estimated_duration=150.0
        ),
        
        # Phase 3: Requires all pillars (sequential)
        create_async_task(
            task_id="gravity_analyzer",
            function=gravity_task,
            args=args,
            kwargs=kwargs,
            priority=TaskPriority.CRITICAL,
            dependencies=["strategy_swarm", "creative_swarm", "design_swarm", "technology_swarm"],
            estimated_duration=120.0
        )
    ]
    
    # Add validation tasks (can run in parallel after gravity analysis)
    for i, validation_task in enumerate(validation_tasks):
        tasks.append(create_async_task(
            task_id=f"validation_{i}",
            function=validation_task,
            args=args,
            kwargs=kwargs,
            priority=TaskPriority.MEDIUM,
            dependencies=["gravity_analyzer"],
            estimated_duration=90.0
        ))
    
    # Add synthesis tasks (require validation completion)
    validation_deps = [f"validation_{i}" for i in range(len(validation_tasks))]
    for i, synthesis_task in enumerate(synthesis_tasks):
        tasks.append(create_async_task(
            task_id=f"synthesis_{i}",
            function=synthesis_task,
            args=args,
            kwargs=kwargs,
            priority=TaskPriority.HIGH,
            dependencies=validation_deps,
            estimated_duration=120.0
        ))
    
    # Create and execute optimized plan
    execution_plan = await async_optimizer.create_execution_plan(tasks)
    results = await async_optimizer.execute_parallel_workflow(execution_plan)
    
    return results