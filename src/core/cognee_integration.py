"""
SUBFRACTURE Cognee Integration

Advanced knowledge management and memory persistence using Cognee framework.
Provides sophisticated memory operations, knowledge graphs, and semantic search
for SUBFRACTURE brand intelligence workflows.

Features:
- Semantic memory storage and retrieval
- Knowledge graph construction for brand insights
- Intelligent context management
- Brand knowledge persistence across sessions
- Semantic search and similarity matching
- Memory consolidation and optimization
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
import structlog
from pathlib import Path

try:
    import cognee
    from cognee import add, search, prune, status
    from cognee.modules.data.processing import Document
    COGNEE_AVAILABLE = True
except ImportError:
    COGNEE_AVAILABLE = False
    cognee = None

from langsmith import traceable

from .state import SubfractureGravityState
from .error_handling import with_error_handling, ErrorSeverity

logger = structlog.get_logger()


class SubfractureCogneeManager:
    """
    Advanced memory management using Cognee for SUBFRACTURE workflows
    """
    
    def __init__(self):
        self.logger = logger.bind(component="cognee_memory_manager")
        self.initialized = False
        self.knowledge_base_id = "subfracture_brand_intelligence"
        
        # Memory categories for organization
        self.memory_categories = {
            "strategic_insights": "Strategic brand truths and competitive analysis",
            "creative_directions": "Creative insights and breakthrough concepts", 
            "design_synthesis": "Visual and verbal brand systems",
            "technology_roadmap": "User experience and technical architecture",
            "gravity_analysis": "Brand gravity measurements and optimization",
            "validation_results": "Human validation and quality assessments",
            "breakthrough_discoveries": "Vesica Pisces breakthrough moments",
            "brand_worlds": "Complete brand universe outputs",
            "session_context": "Workflow session metadata and progress"
        }
        
        if not COGNEE_AVAILABLE:
            self.logger.warning("Cognee not available - falling back to basic memory management")
    
    async def initialize(self, vector_db_url: Optional[str] = None, graph_db_url: Optional[str] = None):
        """Initialize Cognee memory management system"""
        
        if not COGNEE_AVAILABLE:
            self.logger.warning("Cognee not available - memory features limited")
            return False
        
        try:
            # Configure Cognee
            config = {}
            if vector_db_url:
                config["vector_db_url"] = vector_db_url
            if graph_db_url:
                config["graph_db_url"] = graph_db_url
            
            # Initialize Cognee with configuration
            await cognee.config.configure(**config)
            
            # Test connection
            status_info = await status()
            self.logger.info("Cognee initialized successfully", status=status_info)
            
            self.initialized = True
            return True
            
        except Exception as e:
            self.logger.error("Cognee initialization failed", error=str(e))
            self.initialized = False
            return False
    
    @traceable(name="store_brand_knowledge")
    @with_error_handling("cognee_manager", "knowledge_storage", severity=ErrorSeverity.MEDIUM)
    async def store_brand_knowledge(
        self,
        session_id: str,
        knowledge_type: str,
        content: Dict[str, Any],
        metadata: Dict[str, Any] = None
    ) -> str:
        """Store brand knowledge in Cognee memory system"""
        
        if not self.initialized:
            self.logger.warning("Cognee not initialized - skipping knowledge storage")
            return f"fallback_{session_id}_{knowledge_type}"
        
        try:
            # Prepare knowledge document
            knowledge_id = f"{session_id}_{knowledge_type}_{int(datetime.now().timestamp())}"
            
            # Convert content to searchable text
            searchable_content = await self._prepare_searchable_content(knowledge_type, content)
            
            # Prepare metadata
            full_metadata = {
                "session_id": session_id,
                "knowledge_type": knowledge_type,
                "category": self.memory_categories.get(knowledge_type, "general"),
                "timestamp": datetime.now().isoformat(),
                "knowledge_base": self.knowledge_base_id,
                **(metadata or {})
            }
            
            # Create document
            document = Document(
                id=knowledge_id,
                text=searchable_content,
                metadata=full_metadata
            )
            
            # Store in Cognee
            await add([document])
            
            self.logger.info("Brand knowledge stored",
                           knowledge_id=knowledge_id,
                           knowledge_type=knowledge_type,
                           session_id=session_id)
            
            return knowledge_id
            
        except Exception as e:
            self.logger.error("Brand knowledge storage failed", error=str(e))
            raise
    
    @traceable(name="retrieve_brand_knowledge")
    async def retrieve_brand_knowledge(
        self,
        query: str,
        knowledge_types: List[str] = None,
        session_id: str = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant brand knowledge using semantic search"""
        
        if not self.initialized:
            self.logger.warning("Cognee not initialized - returning empty results")
            return []
        
        try:
            # Prepare search filters
            filters = {"knowledge_base": self.knowledge_base_id}
            
            if session_id:
                filters["session_id"] = session_id
            
            if knowledge_types:
                filters["knowledge_type"] = {"$in": knowledge_types}
            
            # Perform semantic search
            search_results = await search(
                query=query,
                limit=limit,
                filters=filters
            )
            
            # Process results
            processed_results = []
            for result in search_results:
                processed_result = {
                    "knowledge_id": result.get("id"),
                    "content": result.get("text"),
                    "metadata": result.get("metadata", {}),
                    "relevance_score": result.get("score", 0.0),
                    "knowledge_type": result.get("metadata", {}).get("knowledge_type"),
                    "session_id": result.get("metadata", {}).get("session_id")
                }
                processed_results.append(processed_result)
            
            self.logger.info("Brand knowledge retrieved",
                           query_length=len(query),
                           results_count=len(processed_results),
                           knowledge_types=knowledge_types)
            
            return processed_results
            
        except Exception as e:
            self.logger.error("Brand knowledge retrieval failed", error=str(e))
            return []
    
    @traceable(name="store_workflow_state")
    async def store_workflow_state(
        self,
        session_id: str,
        state: SubfractureGravityState,
        workflow_phase: str
    ) -> Dict[str, str]:
        """Store complete workflow state as structured knowledge"""
        
        if not self.initialized:
            return {"status": "cognee_not_available"}
        
        knowledge_ids = {}
        
        try:
            # Store different aspects of the state
            if state.strategy_insights:
                knowledge_ids["strategy"] = await self.store_brand_knowledge(
                    session_id=session_id,
                    knowledge_type="strategic_insights",
                    content=state.strategy_insights,
                    metadata={"workflow_phase": workflow_phase}
                )
            
            if state.creative_directions:
                knowledge_ids["creative"] = await self.store_brand_knowledge(
                    session_id=session_id,
                    knowledge_type="creative_directions",
                    content=state.creative_directions,
                    metadata={"workflow_phase": workflow_phase}
                )
            
            if state.design_synthesis:
                knowledge_ids["design"] = await self.store_brand_knowledge(
                    session_id=session_id,
                    knowledge_type="design_synthesis",
                    content=state.design_synthesis,
                    metadata={"workflow_phase": workflow_phase}
                )
            
            if state.technology_roadmap:
                knowledge_ids["technology"] = await self.store_brand_knowledge(
                    session_id=session_id,
                    knowledge_type="technology_roadmap",
                    content=state.technology_roadmap,
                    metadata={"workflow_phase": workflow_phase}
                )
            
            if state.gravity_analysis:
                knowledge_ids["gravity"] = await self.store_brand_knowledge(
                    session_id=session_id,
                    knowledge_type="gravity_analysis",
                    content=dict(state.gravity_analysis),
                    metadata={"workflow_phase": workflow_phase, "gravity_index": state.gravity_index}
                )
            
            if state.primary_breakthrough:
                knowledge_ids["breakthrough"] = await self.store_brand_knowledge(
                    session_id=session_id,
                    knowledge_type="breakthrough_discoveries",
                    content=state.primary_breakthrough,
                    metadata={"workflow_phase": workflow_phase}
                )
            
            # Store session context
            session_context = {
                "brand_brief": state.brand_brief,
                "operator_context": state.operator_context,
                "target_outcome": state.target_outcome,
                "workflow_phase": workflow_phase,
                "gravity_index": state.gravity_index
            }
            
            knowledge_ids["session"] = await self.store_brand_knowledge(
                session_id=session_id,
                knowledge_type="session_context",
                content=session_context,
                metadata={"workflow_phase": workflow_phase}
            )
            
            self.logger.info("Workflow state stored in Cognee",
                           session_id=session_id,
                           workflow_phase=workflow_phase,
                           knowledge_items=len(knowledge_ids))
            
            return knowledge_ids
            
        except Exception as e:
            self.logger.error("Workflow state storage failed", error=str(e))
            return {"error": str(e)}
    
    @traceable(name="retrieve_similar_brand_insights")
    async def retrieve_similar_brand_insights(
        self,
        current_brand_brief: str,
        insight_types: List[str] = None,
        similarity_threshold: float = 0.7,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Retrieve similar brand insights from previous sessions"""
        
        if not self.initialized:
            return []
        
        try:
            # Search for similar brand contexts
            similar_insights = await self.retrieve_brand_knowledge(
                query=current_brand_brief,
                knowledge_types=insight_types or ["strategic_insights", "creative_directions"],
                limit=limit * 2  # Get more to filter by threshold
            )
            
            # Filter by similarity threshold
            relevant_insights = [
                insight for insight in similar_insights
                if insight["relevance_score"] >= similarity_threshold
            ][:limit]
            
            self.logger.info("Similar brand insights retrieved",
                           total_found=len(similar_insights),
                           relevant_count=len(relevant_insights),
                           similarity_threshold=similarity_threshold)
            
            return relevant_insights
            
        except Exception as e:
            self.logger.error("Similar brand insights retrieval failed", error=str(e))
            return []
    
    @traceable(name="consolidate_brand_knowledge")
    async def consolidate_brand_knowledge(
        self,
        session_id: str,
        consolidation_type: str = "session_summary"
    ) -> Dict[str, Any]:
        """Consolidate and synthesize brand knowledge from a session"""
        
        if not self.initialized:
            return {"status": "cognee_not_available"}
        
        try:
            # Retrieve all knowledge for the session
            session_knowledge = await self.retrieve_brand_knowledge(
                query="*",  # Get all
                session_id=session_id,
                limit=100
            )
            
            # Group by knowledge type
            knowledge_by_type = {}
            for item in session_knowledge:
                knowledge_type = item["knowledge_type"]
                if knowledge_type not in knowledge_by_type:
                    knowledge_by_type[knowledge_type] = []
                knowledge_by_type[knowledge_type].append(item)
            
            # Create consolidation summary
            consolidation = {
                "session_id": session_id,
                "consolidation_type": consolidation_type,
                "timestamp": datetime.now().isoformat(),
                "knowledge_types_found": list(knowledge_by_type.keys()),
                "total_knowledge_items": len(session_knowledge),
                "knowledge_summary": {}
            }
            
            # Summarize each knowledge type
            for knowledge_type, items in knowledge_by_type.items():
                consolidation["knowledge_summary"][knowledge_type] = {
                    "item_count": len(items),
                    "latest_timestamp": max(item["metadata"].get("timestamp", "") for item in items),
                    "key_insights": self._extract_key_insights(items, knowledge_type)
                }
            
            # Store consolidation as new knowledge
            consolidation_id = await self.store_brand_knowledge(
                session_id=session_id,
                knowledge_type="session_consolidation",
                content=consolidation,
                metadata={"consolidation_type": consolidation_type}
            )
            
            consolidation["consolidation_id"] = consolidation_id
            
            self.logger.info("Brand knowledge consolidated",
                           session_id=session_id,
                           knowledge_types=len(knowledge_by_type),
                           total_items=len(session_knowledge))
            
            return consolidation
            
        except Exception as e:
            self.logger.error("Brand knowledge consolidation failed", error=str(e))
            return {"error": str(e)}
    
    async def _prepare_searchable_content(self, knowledge_type: str, content: Dict[str, Any]) -> str:
        """Convert structured content to searchable text"""
        
        searchable_parts = [f"Knowledge Type: {knowledge_type}"]
        
        def extract_text(obj, prefix=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if isinstance(value, (dict, list)):
                        extract_text(value, f"{prefix}{key}: ")
                    else:
                        searchable_parts.append(f"{prefix}{key}: {str(value)}")
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    if isinstance(item, (dict, list)):
                        extract_text(item, f"{prefix}[{i}] ")
                    else:
                        searchable_parts.append(f"{prefix}[{i}]: {str(item)}")
            else:
                searchable_parts.append(f"{prefix}{str(obj)}")
        
        extract_text(content)
        
        return "\n".join(searchable_parts)
    
    def _extract_key_insights(self, knowledge_items: List[Dict[str, Any]], knowledge_type: str) -> List[str]:
        """Extract key insights from knowledge items"""
        
        insights = []
        
        for item in knowledge_items:
            content = item.get("content", "")
            
            # Extract key phrases based on knowledge type
            if knowledge_type == "strategic_insights":
                if "core_truths" in content:
                    insights.append("Strategic truths identified")
                if "competitive_advantage" in content:
                    insights.append("Competitive advantages analyzed")
            
            elif knowledge_type == "creative_directions":
                if "target_insights" in content:
                    insights.append("Target audience insights discovered")
                if "breakthrough" in content.lower():
                    insights.append("Creative breakthrough achieved")
            
            elif knowledge_type == "gravity_analysis":
                metadata = item.get("metadata", {})
                gravity_index = metadata.get("gravity_index")
                if gravity_index:
                    insights.append(f"Gravity index: {gravity_index:.2f}")
            
            # Generic insight extraction
            if "insights" in content.lower():
                insights.append("Key insights documented")
        
        return list(set(insights))  # Remove duplicates
    
    async def cleanup_old_knowledge(self, days_old: int = 30) -> Dict[str, Any]:
        """Clean up old knowledge beyond retention period"""
        
        if not self.initialized:
            return {"status": "cognee_not_available"}
        
        try:
            # Calculate cutoff date
            cutoff_date = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
            
            # Use Cognee's prune functionality if available
            # This is a simplified example - actual implementation depends on Cognee's API
            cleanup_result = await prune(
                filters={
                    "knowledge_base": self.knowledge_base_id,
                    "timestamp": {"$lt": cutoff_date}
                }
            )
            
            self.logger.info("Old knowledge cleaned up",
                           days_old=days_old,
                           cleanup_result=cleanup_result)
            
            return {
                "status": "completed",
                "days_old": days_old,
                "cleanup_result": cleanup_result
            }
            
        except Exception as e:
            self.logger.error("Knowledge cleanup failed", error=str(e))
            return {"status": "failed", "error": str(e)}
    
    def get_memory_status(self) -> Dict[str, Any]:
        """Get current memory system status"""
        
        return {
            "cognee_available": COGNEE_AVAILABLE,
            "initialized": self.initialized,
            "knowledge_base_id": self.knowledge_base_id,
            "memory_categories": list(self.memory_categories.keys()),
            "features_available": [
                "semantic_search",
                "knowledge_graphs", 
                "memory_consolidation",
                "similarity_matching"
            ] if self.initialized else ["basic_fallback"]
        }


# Global Cognee manager instance
cognee_manager = SubfractureCogneeManager()


# Integration decorators and utilities
def with_cognee_memory(knowledge_type: str, store_result: bool = True):
    """Decorator for automatic Cognee knowledge storage"""
    
    def decorator(func):
        @traceable(name=f"cognee_memory_{func.__name__}")
        async def wrapper(*args, **kwargs):
            # Execute function
            result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
            
            # Extract session info
            session_id = "default_session"
            for arg in args:
                if hasattr(arg, 'session_id'):
                    session_id = arg.session_id
                    break
                elif isinstance(arg, SubfractureGravityState):
                    session_id = getattr(arg, 'session_id', 'default_session')
                    break
            
            # Store result in Cognee if enabled
            if store_result and isinstance(result, dict) and cognee_manager.initialized:
                try:
                    await cognee_manager.store_brand_knowledge(
                        session_id=session_id,
                        knowledge_type=knowledge_type,
                        content=result,
                        metadata={"function": func.__name__}
                    )
                except Exception as e:
                    logger.warning("Cognee storage failed", error=str(e))
            
            return result
        
        return wrapper
    
    return decorator


async def initialize_cognee_memory(vector_db_url: str = None, graph_db_url: str = None):
    """Initialize Cognee memory management"""
    return await cognee_manager.initialize(vector_db_url, graph_db_url)


async def enhance_state_with_memory(state: SubfractureGravityState, session_id: str) -> SubfractureGravityState:
    """Enhance state with relevant knowledge from memory"""
    
    if not cognee_manager.initialized:
        return state
    
    try:
        # Retrieve similar brand insights
        similar_insights = await cognee_manager.retrieve_similar_brand_insights(
            current_brand_brief=state.brand_brief,
            limit=3
        )
        
        # Add memory context to state (this would require extending the state model)
        if hasattr(state, 'memory_context'):
            state.memory_context = {
                "similar_insights": similar_insights,
                "memory_enhanced": True,
                "enhancement_timestamp": datetime.now().isoformat()
            }
        
        logger.info("State enhanced with memory",
                   session_id=session_id,
                   similar_insights_count=len(similar_insights))
        
        return state
        
    except Exception as e:
        logger.warning("State memory enhancement failed", error=str(e))
        return state