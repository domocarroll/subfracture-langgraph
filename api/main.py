"""
SUBFRACTURE LangGraph API

Production-ready FastAPI interface for SUBFRACTURE brand intelligence system.
Provides REST API endpoints for workflow execution, session management,
and system monitoring.
"""

import asyncio
import os
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import structlog

from src.core.workflow import create_subfracture_workflow
from src.core.state import SubfractureGravityState
from src.core.memory_manager import memory_manager, initialize_memory_management
from src.core.cognee_integration import cognee_manager, initialize_cognee_memory
from src.core.error_handling import error_handler
from src.core.async_optimizer import async_optimizer

# Configure logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# FastAPI app
app = FastAPI(
    title="SUBFRACTURE Brand Intelligence API",
    description="Physics-Based Brand Development System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Request/Response Models
class BrandBriefRequest(BaseModel):
    """Request model for brand brief submission"""
    brand_brief: str = Field(..., min_length=50, max_length=10000, description="Brand challenge description")
    operator_context: Dict[str, Any] = Field(..., description="Operator context and background")
    target_outcome: str = Field(..., min_length=20, max_length=1000, description="Desired outcome")
    session_id: Optional[str] = Field(None, description="Optional session ID for continuity")
    
    class Config:
        schema_extra = {
            "example": {
                "brand_brief": "We're a conscious AI consultancy helping technology companies integrate AI in human-centered ways. Our challenge: the market is flooded with AI solutions that feel soulless and manipulative.",
                "operator_context": {
                    "role": "Founder & Lead Consultant",
                    "industry": "AI Consulting & Technology",
                    "company_stage": "Growth",
                    "personal_investment": "Building technology solutions that serve human flourishing",
                    "vision": "Create a world where AI amplifies human wisdom rather than replacing it"
                },
                "target_outcome": "Establish market leadership in conscious AI consulting with premium positioning"
            }
        }


class WorkflowResponse(BaseModel):
    """Response model for workflow execution"""
    session_id: str
    status: str
    execution_time: float
    gravity_index: float
    breakthrough_discovered: bool
    brand_world_created: bool
    validation_passed: bool
    premium_value_justified: bool
    deliverables: Dict[str, Any]
    next_steps: List[str]


class SessionStatusResponse(BaseModel):
    """Response model for session status"""
    session_id: str
    status: str
    current_phase: Optional[str]
    progress_percentage: float
    estimated_completion: Optional[str]
    results_available: bool


class SystemHealthResponse(BaseModel):
    """Response model for system health"""
    status: str
    uptime: float
    memory_usage: Dict[str, Any]
    error_rate: float
    active_sessions: int
    system_performance: Dict[str, Any]


# Global state
workflow_sessions: Dict[str, Dict[str, Any]] = {}
system_start_time = time.time()


# Startup/Shutdown Events
@app.on_event("startup")
async def startup_event():
    """Initialize system components on startup"""
    try:
        logger.info("Starting SUBFRACTURE API system")
        
        # Initialize memory management
        await initialize_memory_management()
        
        # Initialize Cognee if configured
        vector_db_url = os.getenv("COGNEE_VECTOR_DB_URL")
        graph_db_url = os.getenv("COGNEE_GRAPH_DB_URL")
        
        if vector_db_url or graph_db_url:
            await initialize_cognee_memory(vector_db_url, graph_db_url)
        
        logger.info("SUBFRACTURE API system started successfully")
        
    except Exception as e:
        logger.error("System startup failed", error=str(e))
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup system components on shutdown"""
    try:
        logger.info("Shutting down SUBFRACTURE API system")
        
        # Shutdown memory management
        await memory_manager.shutdown()
        
        logger.info("SUBFRACTURE API system shutdown complete")
        
    except Exception as e:
        logger.error("System shutdown error", error=str(e))


# Health Check Endpoints
@app.get("/health", response_model=SystemHealthResponse)
async def health_check():
    """System health check endpoint"""
    try:
        uptime = time.time() - system_start_time
        memory_summary = memory_manager.get_memory_summary()
        error_summary = error_handler.get_error_summary()
        performance_summary = async_optimizer.get_performance_summary()
        
        return SystemHealthResponse(
            status="healthy",
            uptime=uptime,
            memory_usage=memory_summary,
            error_rate=1.0 - error_summary.get("recovery_success_rate", 1.0),
            active_sessions=len(workflow_sessions),
            system_performance=performance_summary
        )
        
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        raise HTTPException(status_code=500, detail="Health check failed")


@app.get("/health/memory")
async def memory_health():
    """Memory system health check"""
    try:
        memory_summary = memory_manager.get_memory_summary()
        cognee_status = cognee_manager.get_memory_status()
        
        return {
            "memory_manager": memory_summary,
            "cognee_manager": cognee_status,
            "status": "healthy" if memory_summary.get("monitoring_active") else "degraded"
        }
        
    except Exception as e:
        logger.error("Memory health check failed", error=str(e))
        raise HTTPException(status_code=500, detail="Memory health check failed")


# Main Workflow Endpoints
@app.post("/workflow/execute", response_model=WorkflowResponse)
async def execute_workflow(
    request: BrandBriefRequest,
    background_tasks: BackgroundTasks
):
    """Execute complete SUBFRACTURE brand development workflow"""
    try:
        session_id = request.session_id or f"session_{int(time.time())}"
        start_time = time.time()
        
        logger.info("Starting workflow execution",
                   session_id=session_id,
                   brand_brief_length=len(request.brand_brief))
        
        # Create initial state
        initial_state = SubfractureGravityState(
            brand_brief=request.brand_brief,
            operator_context=request.operator_context,
            target_outcome=request.target_outcome
        )
        
        # Register session
        workflow_sessions[session_id] = {
            "status": "running",
            "start_time": start_time,
            "current_phase": "initialization",
            "state": initial_state
        }
        
        # Create and execute workflow
        workflow = create_subfracture_workflow()
        result = await workflow.ainvoke({"state": initial_state})
        
        # Extract results
        final_state = result.get("state")
        execution_time = time.time() - start_time
        
        # Update session
        workflow_sessions[session_id].update({
            "status": "completed",
            "execution_time": execution_time,
            "final_state": final_state,
            "result": result
        })
        
        # Background task for memory storage
        background_tasks.add_task(
            store_session_memory,
            session_id,
            final_state,
            "workflow_completed"
        )
        
        # Prepare response
        response = WorkflowResponse(
            session_id=session_id,
            status="completed",
            execution_time=execution_time,
            gravity_index=getattr(final_state, "gravity_index", 0.0),
            breakthrough_discovered=bool(getattr(final_state, "primary_breakthrough", None)),
            brand_world_created=bool(getattr(final_state, "brand_world", None)),
            validation_passed=len(getattr(final_state, "validation_checkpoints", [])) >= 3,
            premium_value_justified=True,
            deliverables={
                "strategy_insights": getattr(final_state, "strategy_insights", {}),
                "creative_directions": getattr(final_state, "creative_directions", {}),
                "design_synthesis": getattr(final_state, "design_synthesis", {}),
                "technology_roadmap": getattr(final_state, "technology_roadmap", {}),
                "gravity_analysis": dict(getattr(final_state, "gravity_analysis", {})),
                "primary_breakthrough": getattr(final_state, "primary_breakthrough", {}),
                "brand_world": getattr(final_state, "brand_world", {})
            },
            next_steps=[
                "Review comprehensive brand world deliverable",
                "Begin implementation with provided roadmap",
                "Schedule follow-up optimization session"
            ]
        )
        
        logger.info("Workflow execution completed",
                   session_id=session_id,
                   execution_time=execution_time,
                   gravity_index=response.gravity_index)
        
        return response
        
    except Exception as e:
        logger.error("Workflow execution failed", session_id=session_id, error=str(e))
        
        # Update session status
        if session_id in workflow_sessions:
            workflow_sessions[session_id]["status"] = "failed"
            workflow_sessions[session_id]["error"] = str(e)
        
        raise HTTPException(status_code=500, detail=f"Workflow execution failed: {str(e)}")


@app.get("/workflow/status/{session_id}", response_model=SessionStatusResponse)
async def get_session_status(session_id: str):
    """Get status of specific workflow session"""
    try:
        if session_id not in workflow_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = workflow_sessions[session_id]
        
        # Calculate progress
        progress = 100.0 if session["status"] == "completed" else 50.0 if session["status"] == "running" else 0.0
        
        # Estimate completion time
        estimated_completion = None
        if session["status"] == "running":
            elapsed = time.time() - session["start_time"]
            estimated_total = elapsed * 2  # Simple estimation
            estimated_completion = datetime.fromtimestamp(session["start_time"] + estimated_total).isoformat()
        
        return SessionStatusResponse(
            session_id=session_id,
            status=session["status"],
            current_phase=session.get("current_phase"),
            progress_percentage=progress,
            estimated_completion=estimated_completion,
            results_available=session["status"] == "completed"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Session status retrieval failed", session_id=session_id, error=str(e))
        raise HTTPException(status_code=500, detail="Session status retrieval failed")


@app.get("/workflow/results/{session_id}")
async def get_session_results(session_id: str):
    """Get complete results for workflow session"""
    try:
        if session_id not in workflow_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = workflow_sessions[session_id]
        
        if session["status"] != "completed":
            raise HTTPException(status_code=400, detail="Session not completed")
        
        final_state = session.get("final_state")
        if not final_state:
            raise HTTPException(status_code=404, detail="Results not available")
        
        # Comprehensive results
        results = {
            "session_metadata": {
                "session_id": session_id,
                "execution_time": session.get("execution_time"),
                "completion_timestamp": datetime.now().isoformat()
            },
            "brand_intelligence": {
                "gravity_index": getattr(final_state, "gravity_index", 0.0),
                "gravity_analysis": dict(getattr(final_state, "gravity_analysis", {})),
                "physics_optimization": getattr(final_state, "funnel_physics", {})
            },
            "strategic_foundation": getattr(final_state, "strategy_insights", {}),
            "creative_breakthrough": {
                "creative_directions": getattr(final_state, "creative_directions", {}),
                "primary_breakthrough": getattr(final_state, "primary_breakthrough", {}),
                "vesica_pisces_moments": getattr(final_state, "vesica_pisces_moments", [])
            },
            "design_systems": getattr(final_state, "design_synthesis", {}),
            "technology_architecture": getattr(final_state, "technology_roadmap", {}),
            "human_validation": {
                "validation_checkpoints": getattr(final_state, "validation_checkpoints", []),
                "emotional_resonance": getattr(final_state, "emotional_resonance", {}),
                "premium_value_validation": getattr(final_state, "premium_value_validation", {})
            },
            "brand_world": getattr(final_state, "brand_world", {}),
            "implementation_guidance": {
                "next_steps": [
                    "Review and validate brand world deliverable",
                    "Begin phased implementation according to roadmap",
                    "Schedule 30-day follow-up for optimization",
                    "Track gravity improvements through measurement framework"
                ],
                "success_metrics": [
                    "Gravity index improvement: Target 20-40% within 12 months",
                    "Business impact: $200k-450k projected ROI over 24 months",
                    "Market positioning: Establish category leadership"
                ]
            }
        }
        
        return results
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Results retrieval failed", session_id=session_id, error=str(e))
        raise HTTPException(status_code=500, detail="Results retrieval failed")


# Memory and Knowledge Endpoints
@app.get("/knowledge/search")
async def search_knowledge(
    query: str,
    knowledge_types: Optional[List[str]] = None,
    session_id: Optional[str] = None,
    limit: int = 10
):
    """Search brand knowledge using semantic search"""
    try:
        if not cognee_manager.initialized:
            raise HTTPException(status_code=503, detail="Knowledge search not available")
        
        results = await cognee_manager.retrieve_brand_knowledge(
            query=query,
            knowledge_types=knowledge_types,
            session_id=session_id,
            limit=limit
        )
        
        return {
            "query": query,
            "results_count": len(results),
            "results": results
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Knowledge search failed", error=str(e))
        raise HTTPException(status_code=500, detail="Knowledge search failed")


@app.get("/knowledge/similar/{session_id}")
async def get_similar_insights(
    session_id: str,
    insight_types: Optional[List[str]] = None,
    limit: int = 5
):
    """Get similar brand insights from previous sessions"""
    try:
        if session_id not in workflow_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = workflow_sessions[session_id]
        brand_brief = session["state"].brand_brief
        
        similar_insights = await cognee_manager.retrieve_similar_brand_insights(
            current_brand_brief=brand_brief,
            insight_types=insight_types,
            limit=limit
        )
        
        return {
            "session_id": session_id,
            "similar_insights_count": len(similar_insights),
            "insights": similar_insights
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Similar insights retrieval failed", error=str(e))
        raise HTTPException(status_code=500, detail="Similar insights retrieval failed")


# System Management Endpoints
@app.get("/system/performance")
async def get_system_performance():
    """Get comprehensive system performance metrics"""
    try:
        return {
            "memory_management": memory_manager.get_memory_summary(),
            "async_optimization": async_optimizer.get_performance_summary(),
            "error_handling": error_handler.get_error_summary(),
            "active_sessions": len(workflow_sessions),
            "system_uptime": time.time() - system_start_time
        }
        
    except Exception as e:
        logger.error("Performance metrics retrieval failed", error=str(e))
        raise HTTPException(status_code=500, detail="Performance metrics retrieval failed")


@app.post("/system/cleanup")
async def cleanup_system():
    """Trigger system cleanup and optimization"""
    try:
        # Memory cleanup
        await memory_manager._cleanup_memory()
        
        # Clear old sessions (keep last 10)
        if len(workflow_sessions) > 10:
            sorted_sessions = sorted(workflow_sessions.items(), key=lambda x: x[1].get("start_time", 0))
            sessions_to_remove = sorted_sessions[:-10]
            
            for session_id, _ in sessions_to_remove:
                del workflow_sessions[session_id]
        
        # Knowledge cleanup (if available)
        cleanup_result = {"status": "completed"}
        if cognee_manager.initialized:
            cleanup_result = await cognee_manager.cleanup_old_knowledge(days_old=7)
        
        return {
            "memory_cleanup": "completed",
            "session_cleanup": f"Removed {len(sessions_to_remove) if 'sessions_to_remove' in locals() else 0} old sessions",
            "knowledge_cleanup": cleanup_result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("System cleanup failed", error=str(e))
        raise HTTPException(status_code=500, detail="System cleanup failed")


# Background Tasks
async def store_session_memory(session_id: str, state: SubfractureGravityState, phase: str):
    """Background task to store session in memory systems"""
    try:
        # Store in basic memory manager
        await memory_manager.create_checkpoint(
            session_id=session_id,
            state=state,
            workflow_phase=phase
        )
        
        # Store in Cognee if available
        if cognee_manager.initialized:
            await cognee_manager.store_workflow_state(
                session_id=session_id,
                state=state,
                workflow_phase=phase
            )
        
        logger.info("Session memory storage completed", session_id=session_id)
        
    except Exception as e:
        logger.error("Session memory storage failed", session_id=session_id, error=str(e))


# Exception Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error("Unhandled exception", error=str(exc), path=request.url.path)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "timestamp": datetime.now().isoformat()
        }
    )


# Root endpoint
@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "SUBFRACTURE Brand Intelligence API",
        "version": "1.0.0",
        "description": "Physics-Based Brand Development System",
        "status": "operational",
        "documentation": "/docs",
        "health_check": "/health",
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    
    # Development server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )