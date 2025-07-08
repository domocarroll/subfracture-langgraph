"""
SUBFRACTURE Brand Memory Service

High-level service layer for brand memory operations.
Provides business logic and orchestration for memory management.
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
import asyncio
import structlog

from .brand_memory_store import BrandMemoryStore
from .langmem_adapter import LangMemAdapter
from .memory_models import (
    BrandMemoryContext,
    BrandInsight,
    InteractionMemory,
    StrategicMemory,
    CreativeMemory,
    MemoryType,
    MemoryQuery,
    MemoryUpdateRequest
)
from ..core.state import SubfractureGravityState, WorkshopPhase

logger = structlog.get_logger()


class BrandMemoryService:
    """
    Service layer for brand memory operations
    
    Provides high-level business logic for memory management,
    integrating with SUBFRACTURE workflows and state management.
    """
    
    def __init__(self, memory_store: Optional[BrandMemoryStore] = None):
        self.memory_store = memory_store or LangMemAdapter()
        self.logger = logger.bind(component="brand_memory_service")
        self.initialized = False
    
    async def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialize the memory service"""
        
        try:
            success = await self.memory_store.initialize(config)
            self.initialized = success
            
            if success:
                self.logger.info("Brand memory service initialized successfully")
            else:
                self.logger.error("Brand memory service initialization failed")
            
            return success
            
        except Exception as e:
            self.logger.error("Brand memory service initialization error", error=str(e))
            return False
    
    async def shutdown(self) -> bool:
        """Shutdown the memory service"""
        
        try:
            success = await self.memory_store.shutdown()
            self.initialized = False
            
            self.logger.info("Brand memory service shutdown completed")
            return success
            
        except Exception as e:
            self.logger.error("Brand memory service shutdown error", error=str(e))
            return False
    
    def _ensure_initialized(self):
        """Ensure service is initialized"""
        if not self.initialized:
            raise RuntimeError("Brand memory service not initialized. Call initialize() first.")
    
    # Brand Context Management
    async def create_brand_profile(
        self,
        brand_name: str,
        operator_context: Dict[str, Any],
        initial_brief: str = "",
        brand_id: Optional[str] = None
    ) -> BrandMemoryContext:
        """Create a new brand profile with initial context"""
        
        self._ensure_initialized()
        
        try:
            # Generate brand ID if not provided
            if not brand_id:
                brand_id = f"brand_{uuid.uuid4().hex[:12]}"
            
            # Prepare initial context
            initial_context = {
                "operator_profile": operator_context,
                "initial_brief": initial_brief,
                "communication_preferences": operator_context.get("communication_preferences", {}),
                "business_context": {
                    "industry": operator_context.get("industry", ""),
                    "company_stage": operator_context.get("company_stage", ""),
                    "role": operator_context.get("role", "")
                }
            }
            
            # Create brand context
            brand_context = await self.memory_store.create_brand_context(
                brand_id=brand_id,
                brand_name=brand_name,
                initial_context=initial_context
            )
            
            # Store initial brand brief as insight if provided
            if initial_brief:
                initial_insight = BrandInsight(
                    insight_id=f"initial_brief_{uuid.uuid4().hex[:8]}",
                    insight_type=MemoryType.STRATEGIC,
                    content=initial_brief,
                    context={"source": "initial_brief", "operator_context": operator_context},
                    confidence_score=0.8,
                    source="operator_input",
                    tags=["initial_brief", "strategic_foundation"]
                )
                
                await self.store_insight(brand_id, initial_insight)
            
            self.logger.info("Brand profile created",
                           brand_id=brand_id,
                           brand_name=brand_name,
                           operator_role=operator_context.get("role"))
            
            return brand_context
            
        except Exception as e:
            self.logger.error("Brand profile creation failed",
                            brand_name=brand_name,
                            error=str(e))
            raise
    
    async def get_brand_profile(self, brand_id: str) -> Optional[BrandMemoryContext]:
        """Retrieve brand profile with full context"""
        
        self._ensure_initialized()
        
        try:
            brand_context = await self.memory_store.get_brand_context(brand_id)
            
            if brand_context:
                # Update quality score
                brand_context.calculate_memory_quality()
                
                self.logger.debug("Brand profile retrieved",
                                brand_id=brand_id,
                                total_insights=brand_context.total_insights,
                                quality_score=brand_context.memory_quality_score)
            
            return brand_context
            
        except Exception as e:
            self.logger.error("Brand profile retrieval failed", brand_id=brand_id, error=str(e))
            return None
    
    async def update_brand_gravity(self, brand_id: str, gravity_index: float, gravity_breakdown: Dict[str, float]):
        """Update brand gravity tracking in memory"""
        
        self._ensure_initialized()
        
        try:
            # Create gravity update record
            gravity_update = {
                "timestamp": datetime.now().isoformat(),
                "gravity_index": gravity_index,
                "gravity_breakdown": gravity_breakdown,
                "improvement": 0.0  # Will calculate if previous data exists
            }
            
            brand_context = await self.get_brand_profile(brand_id)
            if brand_context:
                # Calculate improvement
                if brand_context.gravity_history:
                    previous_gravity = brand_context.gravity_history[-1]["gravity_index"]
                    gravity_update["improvement"] = gravity_index - previous_gravity
                
                # Update context
                updates = {
                    "current_gravity_index": gravity_index,
                    "gravity_history": brand_context.gravity_history + [gravity_update]
                }
                
                await self.memory_store.update_brand_context(brand_id, updates)
                
                # Store as insight
                gravity_insight = BrandInsight(
                    insight_id=f"gravity_update_{uuid.uuid4().hex[:8]}",
                    insight_type=MemoryType.GRAVITY,
                    content=f"Brand gravity index: {gravity_index:.3f}. Strongest gravity: {max(gravity_breakdown.items(), key=lambda x: x[1])[0]}",
                    context={
                        "gravity_breakdown": gravity_breakdown,
                        "improvement": gravity_update["improvement"],
                        "timestamp": gravity_update["timestamp"]
                    },
                    confidence_score=1.0,  # Gravity calculations are deterministic
                    source="gravity_analyzer",
                    tags=["gravity_analysis", "metrics", "optimization"],
                    gravity_impact=gravity_update["improvement"]
                )
                
                await self.store_insight(brand_id, gravity_insight)
                
                self.logger.info("Brand gravity updated",
                               brand_id=brand_id,
                               gravity_index=gravity_index,
                               improvement=gravity_update["improvement"])
            
        except Exception as e:
            self.logger.error("Brand gravity update failed", brand_id=brand_id, error=str(e))
            raise
    
    # Workshop Session Integration
    async def record_workshop_session(
        self,
        brand_id: str,
        session_state: SubfractureGravityState,
        facilitator: str = "Claude"
    ) -> str:
        """Record a complete workshop session in memory"""
        
        self._ensure_initialized()
        
        try:
            interaction_id = f"workshop_{session_state.session_id}_{uuid.uuid4().hex[:8]}"
            
            # Extract insights from session state
            insights_generated = []
            
            # Store strategic insights
            if session_state.strategy_insights:
                strategic_insight = await self._extract_strategic_insights(
                    brand_id, session_state.strategy_insights
                )
                insights_generated.append(strategic_insight.insight_id)
            
            # Store creative insights
            if session_state.creative_directions:
                creative_insight = await self._extract_creative_insights(
                    brand_id, session_state.creative_directions
                )
                insights_generated.append(creative_insight.insight_id)
            
            # Store design insights
            if session_state.design_synthesis:
                design_insight = await self._extract_design_insights(
                    brand_id, session_state.design_synthesis
                )
                insights_generated.append(design_insight.insight_id)
            
            # Store technology insights
            if session_state.technology_roadmap:
                tech_insight = await self._extract_technology_insights(
                    brand_id, session_state.technology_roadmap
                )
                insights_generated.append(tech_insight.insight_id)
            
            # Store breakthrough discoveries
            breakthrough_moments = []
            for moment in session_state.vesica_pisces_moments:
                breakthrough_id = await self._store_breakthrough_moment(brand_id, moment)
                breakthrough_moments.append(breakthrough_id)
            
            # Create interaction memory
            interaction = InteractionMemory(
                interaction_id=interaction_id,
                session_id=session_state.session_id,
                interaction_type="subfracture_workshop",
                facilitator=facilitator,
                participants=[session_state.operator_context.get("participant_id", "operator")],
                discussion_topics=[
                    "Strategic truth mining",
                    "Creative insight hunting",
                    "Design visual weaving",
                    "Technology experience building",
                    "Gravity analysis",
                    "Vesica pisces breakthrough discovery"
                ],
                insights_generated=insights_generated,
                breakthrough_moments=breakthrough_moments,
                feedback_provided={
                    "validation_checkpoints": len(session_state.validation_checkpoints),
                    "final_gravity_index": session_state.gravity_index,
                    "workflow_phase": session_state.current_phase.value
                },
                next_steps=session_state.implementation_plan.get("immediate_next_steps", []) if session_state.implementation_plan else []
            )
            
            # Store interaction
            stored_interaction_id = await self.memory_store.store_interaction(brand_id, interaction)
            
            # Update gravity if available
            if session_state.gravity_index > 0:
                await self.update_brand_gravity(
                    brand_id,
                    session_state.gravity_index,
                    dict(session_state.gravity_analysis)
                )
            
            self.logger.info("Workshop session recorded",
                           brand_id=brand_id,
                           session_id=session_state.session_id,
                           insights_count=len(insights_generated),
                           breakthrough_count=len(breakthrough_moments))
            
            return stored_interaction_id
            
        except Exception as e:
            self.logger.error("Workshop session recording failed",
                            brand_id=brand_id,
                            session_id=session_state.session_id,
                            error=str(e))
            raise
    
    async def _extract_strategic_insights(self, brand_id: str, strategy_data: Dict[str, Any]) -> BrandInsight:
        """Extract and store strategic insights from strategy swarm output"""
        
        insight = BrandInsight(
            insight_id=f"strategic_{uuid.uuid4().hex[:8]}",
            insight_type=MemoryType.STRATEGIC,
            content=f"Strategic foundation: {strategy_data.get('strategic_summary', {}).get('operator_strength', '')}. Market opportunity: {strategy_data.get('strategic_summary', {}).get('market_opportunity', '')}",
            context={
                "core_truths": strategy_data.get("core_truths", []),
                "strategic_frameworks": strategy_data.get("strategic_frameworks", {}),
                "outcome_pathway": strategy_data.get("outcome_pathway", [])
            },
            confidence_score=strategy_data.get("truth_confidence", 0.8),
            source="strategy_swarm",
            tags=["strategic_analysis", "truth_mining", "positioning"],
            brand_element="strategic_foundation"
        )
        
        await self.store_insight(brand_id, insight)
        return insight
    
    async def _extract_creative_insights(self, brand_id: str, creative_data: Dict[str, Any]) -> BrandInsight:
        """Extract and store creative insights from creative swarm output"""
        
        insight = BrandInsight(
            insight_id=f"creative_{uuid.uuid4().hex[:8]}",
            insight_type=MemoryType.CREATIVE,
            content=f"Creative insights: {creative_data.get('creative_summary', 'Creative direction developed')}",
            context={
                "target_insights": creative_data.get("target_insights", []),
                "creative_territories": creative_data.get("creative_territories", []),
                "emotional_drivers": creative_data.get("emotional_drivers", [])
            },
            confidence_score=creative_data.get("insight_confidence", 0.8),
            source="creative_swarm",
            tags=["creative_analysis", "insight_hunting", "target_mind"],
            brand_element="creative_direction"
        )
        
        await self.store_insight(brand_id, insight)
        return insight
    
    async def _extract_design_insights(self, brand_id: str, design_data: Dict[str, Any]) -> BrandInsight:
        """Extract and store design insights from design swarm output"""
        
        insight = BrandInsight(
            insight_id=f"design_{uuid.uuid4().hex[:8]}",
            insight_type=MemoryType.DESIGN,
            content=f"Design synthesis: {design_data.get('design_summary', 'Visual language developed')}",
            context={
                "visual_languages": design_data.get("visual_languages", []),
                "world_rules": design_data.get("world_rules", {}),
                "gravity_points": design_data.get("gravity_points", [])
            },
            confidence_score=design_data.get("design_confidence", 0.8),
            source="design_swarm",
            tags=["design_synthesis", "visual_weaving", "gravity_points"],
            brand_element="visual_identity"
        )
        
        await self.store_insight(brand_id, insight)
        return insight
    
    async def _extract_technology_insights(self, brand_id: str, tech_data: Dict[str, Any]) -> BrandInsight:
        """Extract and store technology insights from technology swarm output"""
        
        insight = BrandInsight(
            insight_id=f"technology_{uuid.uuid4().hex[:8]}",
            insight_type=MemoryType.TECHNOLOGY,
            content=f"Technology roadmap: {tech_data.get('tech_summary', 'Experience architecture developed')}",
            context={
                "user_journeys": tech_data.get("user_journeys", []),
                "friction_points": tech_data.get("friction_points", []),
                "amplification_strategies": tech_data.get("amplification_strategies", [])
            },
            confidence_score=tech_data.get("tech_confidence", 0.8),
            source="technology_swarm",
            tags=["technology_roadmap", "experience_building", "funnel_physics"],
            brand_element="user_experience"
        )
        
        await self.store_insight(brand_id, insight)
        return insight
    
    async def _store_breakthrough_moment(self, brand_id: str, breakthrough_data: Dict[str, Any]) -> str:
        """Store a vesica pisces breakthrough moment"""
        
        breakthrough_insight = BrandInsight(
            insight_id=f"breakthrough_{uuid.uuid4().hex[:8]}",
            insight_type=MemoryType.BREAKTHROUGH,
            content=f"Breakthrough discovery: {breakthrough_data.get('big_idea', 'Truth × Insight intersection discovered')}",
            context={
                "truth_component": breakthrough_data.get("truth_component", {}),
                "insight_component": breakthrough_data.get("insight_component", {}),
                "intersection_potential": breakthrough_data.get("intersection_potential", 0.0),
                "implementation_path": breakthrough_data.get("implementation_path", {})
            },
            confidence_score=breakthrough_data.get("intersection_potential", 0.8),
            source="vesica_pisces_engine",
            tags=["breakthrough", "vesica_pisces", "big_idea", "truth_insight_intersection"],
            brand_element="breakthrough_concept"
        )
        
        await self.store_insight(brand_id, breakthrough_insight)
        return breakthrough_insight.insight_id
    
    # Memory Intelligence Operations
    async def store_insight(self, brand_id: str, insight: BrandInsight) -> str:
        """Store brand insight with validation and enrichment"""
        
        self._ensure_initialized()
        
        try:
            # Enrich insight with related memories
            related_insights = await self.find_related_insights(brand_id, insight.content)
            insight.related_insights = [r.insight_id for r in related_insights[:3]]  # Top 3 related
            
            # Store insight
            insight_id = await self.memory_store.store_insight(brand_id, insight)
            
            self.logger.debug("Insight stored with enrichment",
                            brand_id=brand_id,
                            insight_id=insight_id,
                            related_count=len(insight.related_insights))
            
            return insight_id
            
        except Exception as e:
            self.logger.error("Insight storage with enrichment failed",
                            brand_id=brand_id,
                            insight_id=insight.insight_id,
                            error=str(e))
            raise
    
    async def find_related_insights(self, brand_id: str, query_text: str, limit: int = 5) -> List[BrandInsight]:
        """Find insights related to given text using semantic search"""
        
        self._ensure_initialized()
        
        try:
            search_results = await self.memory_store.semantic_search(
                brand_id=brand_id,
                query_text=query_text,
                limit=limit
            )
            
            # Convert search results to insights
            related_insights = []
            for result in search_results:
                if result.get("memory_type") == "insight":
                    # This would need to be implemented based on search result format
                    pass
            
            return related_insights
            
        except Exception as e:
            self.logger.error("Related insights search failed", brand_id=brand_id, error=str(e))
            return []
    
    async def get_brand_intelligence_summary(self, brand_id: str) -> Dict[str, Any]:
        """Get comprehensive brand intelligence summary"""
        
        self._ensure_initialized()
        
        try:
            # Get brand context
            brand_context = await self.get_brand_profile(brand_id)
            if not brand_context:
                return {"error": "Brand not found"}
            
            # Get memory analytics
            analytics = await self.memory_store.get_memory_analytics(brand_id)
            
            # Get recent insights by type
            insights_by_type = {}
            for memory_type in MemoryType:
                insights = brand_context.get_insights_by_type(memory_type)
                insights_by_type[memory_type.value] = {
                    "count": len(insights),
                    "latest": insights[-1].timestamp.isoformat() if insights else None,
                    "avg_confidence": sum(i.confidence_score for i in insights) / len(insights) if insights else 0.0
                }
            
            # Get recent activity
            recent_insights = brand_context.get_recent_insights(30)
            recent_interactions = await self.memory_store.get_recent_interactions(brand_id, limit=5)
            
            summary = {
                "brand_info": {
                    "brand_id": brand_id,
                    "brand_name": brand_context.brand_name,
                    "created_at": brand_context.created_at.isoformat(),
                    "last_updated": brand_context.last_updated.isoformat()
                },
                "memory_stats": analytics,
                "insights_by_type": insights_by_type,
                "recent_activity": {
                    "insights_last_30_days": len(recent_insights),
                    "interactions_last_5": len(recent_interactions),
                    "last_session": brand_context.last_session_date.isoformat() if brand_context.last_session_date else None
                },
                "brand_health": {
                    "gravity_index": brand_context.current_gravity_index,
                    "memory_quality": brand_context.memory_quality_score,
                    "knowledge_completeness": self._calculate_knowledge_completeness(insights_by_type),
                    "engagement_level": self._calculate_engagement_level(brand_context)
                }
            }
            
            return summary
            
        except Exception as e:
            self.logger.error("Brand intelligence summary failed", brand_id=brand_id, error=str(e))
            return {"error": str(e)}
    
    def _calculate_knowledge_completeness(self, insights_by_type: Dict[str, Dict]) -> float:
        """Calculate how complete the brand knowledge is across all memory types"""
        
        # Check if we have insights across key memory types
        key_types = [MemoryType.STRATEGIC, MemoryType.CREATIVE, MemoryType.DESIGN, MemoryType.TECHNOLOGY]
        covered_types = sum(1 for mem_type in key_types if insights_by_type.get(mem_type.value, {}).get("count", 0) > 0)
        
        return covered_types / len(key_types)
    
    def _calculate_engagement_level(self, brand_context: BrandMemoryContext) -> float:
        """Calculate engagement level based on recent activity"""
        
        # Factors: recent insights, interactions, gravity updates
        recent_insights = len(brand_context.get_recent_insights(30))
        total_interactions = brand_context.total_interactions
        has_recent_session = brand_context.last_session_date and (
            datetime.now() - brand_context.last_session_date
        ).days < 30
        
        # Simple scoring
        insight_score = min(1.0, recent_insights / 10)  # 10+ recent insights = max score
        interaction_score = min(1.0, total_interactions / 5)  # 5+ interactions = max score
        recency_score = 1.0 if has_recent_session else 0.0
        
        return (insight_score + interaction_score + recency_score) / 3
    
    # Utility Methods
    async def search_brand_knowledge(
        self,
        brand_id: str,
        query: str,
        memory_types: Optional[List[MemoryType]] = None,
        limit: int = 10
    ) -> Dict[str, Any]:
        """Search across all brand knowledge"""
        
        self._ensure_initialized()
        
        try:
            # Perform semantic search
            search_results = await self.memory_store.semantic_search(
                brand_id=brand_id,
                query_text=query,
                memory_types=memory_types,
                limit=limit
            )
            
            # Also search insights directly
            memory_query = MemoryQuery(
                memory_types=memory_types,
                text_search=query,
                limit=limit
            )
            
            insights = await self.memory_store.query_insights(brand_id, memory_query)
            
            return {
                "query": query,
                "semantic_results": search_results,
                "insight_results": [
                    {
                        "insight_id": insight.insight_id,
                        "content": insight.content,
                        "type": insight.insight_type.value,
                        "confidence": insight.confidence_score,
                        "timestamp": insight.timestamp.isoformat()
                    }
                    for insight in insights
                ],
                "total_results": len(search_results) + len(insights)
            }
            
        except Exception as e:
            self.logger.error("Brand knowledge search failed", brand_id=brand_id, error=str(e))
            return {"error": str(e)}
    
    async def get_health_status(self) -> Dict[str, Any]:
        """Get overall memory service health status"""
        
        try:
            store_health = await self.memory_store.health_check()
            store_stats = await self.memory_store.get_store_statistics()
            
            return {
                "service_status": "healthy" if self.initialized else "unhealthy",
                "store_health": store_health,
                "store_statistics": store_stats,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error("Health status check failed", error=str(e))
            return {"service_status": "error", "error": str(e)}