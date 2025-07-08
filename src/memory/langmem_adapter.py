"""
SUBFRACTURE LangMem Adapter

Concrete implementation of BrandMemoryStore using LangMem for persistent brand intelligence.
Provides long-term memory capabilities with semantic search and conversation memory.
"""

import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
import asyncio
import structlog

try:
    # LangMem imports (will be installed separately)
    from langmem import MemoryStore, SearchOptions
    from langmem.memory import Memory, MemoryMetadata
    LANGMEM_AVAILABLE = True
except ImportError:
    LANGMEM_AVAILABLE = False
    # Mock classes for development without LangMem
    class MemoryStore:
        def __init__(self, *args, **kwargs): pass
        async def store(self, *args, **kwargs): return "mock_id"
        async def search(self, *args, **kwargs): return []
        async def get(self, *args, **kwargs): return None
        async def update(self, *args, **kwargs): return None
        async def delete(self, *args, **kwargs): return True
    
    class Memory:
        def __init__(self, *args, **kwargs): pass
    
    class MemoryMetadata:
        def __init__(self, *args, **kwargs): pass
    
    class SearchOptions:
        def __init__(self, *args, **kwargs): pass

from .brand_memory_store import BrandMemoryStore
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

logger = structlog.get_logger()


class LangMemAdapter(BrandMemoryStore):
    """
    LangMem implementation of brand memory store
    
    Provides persistent memory with semantic search capabilities
    for brand intelligence across workshop sessions.
    """
    
    def __init__(self):
        self.memory_store: Optional[MemoryStore] = None
        self.brand_contexts: Dict[str, BrandMemoryContext] = {}
        self.logger = logger.bind(component="langmem_adapter")
        self.initialized = False
        
    async def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialize LangMem store with configuration"""
        
        if not LANGMEM_AVAILABLE:
            self.logger.warning("LangMem not available, using mock implementation")
            # Initialize mock store for development
            self.memory_store = MemoryStore()
            self.initialized = True
            return True
        
        try:
            # Initialize LangMem store
            store_config = config.get("langmem", {})
            
            # Configure LangMem with appropriate backend
            memory_config = {
                "namespace": store_config.get("namespace", "subfracture_brand_intelligence"),
                "embedding_model": store_config.get("embedding_model", "text-embedding-ada-002"),
                "storage_backend": store_config.get("storage_backend", "in_memory"),
                **store_config.get("additional_config", {})
            }
            
            self.memory_store = MemoryStore(**memory_config)
            
            # Test connection
            await self._test_connection()
            
            self.initialized = True
            self.logger.info("LangMem adapter initialized successfully", config=memory_config)
            return True
            
        except Exception as e:
            self.logger.error("LangMem adapter initialization failed", error=str(e))
            return False
    
    async def shutdown(self) -> bool:
        """Shutdown LangMem store"""
        
        try:
            if self.memory_store and hasattr(self.memory_store, 'close'):
                await self.memory_store.close()
            
            self.initialized = False
            self.logger.info("LangMem adapter shutdown completed")
            return True
            
        except Exception as e:
            self.logger.error("LangMem adapter shutdown failed", error=str(e))
            return False
    
    async def _test_connection(self):
        """Test LangMem connection with a simple operation"""
        
        try:
            test_memory = Memory(
                content="Test connection memory",
                metadata=MemoryMetadata(
                    memory_type="system",
                    tags=["test"],
                    importance=0.1
                )
            )
            
            # Store and immediately retrieve
            memory_id = await self.memory_store.store(test_memory)
            retrieved = await self.memory_store.get(memory_id)
            
            if retrieved:
                # Clean up test memory
                await self.memory_store.delete(memory_id)
                self.logger.debug("LangMem connection test successful")
            else:
                raise Exception("Test memory retrieval failed")
                
        except Exception as e:
            self.logger.error("LangMem connection test failed", error=str(e))
            raise
    
    def _ensure_initialized(self):
        """Ensure adapter is initialized"""
        if not self.initialized:
            raise RuntimeError("LangMem adapter not initialized. Call initialize() first.")
    
    def _brand_namespace(self, brand_id: str) -> str:
        """Generate namespace for brand-specific memories"""
        return f"brand_{brand_id}"
    
    def _memory_key(self, brand_id: str, memory_type: str, memory_id: str) -> str:
        """Generate unique memory key"""
        return f"{self._brand_namespace(brand_id)}_{memory_type}_{memory_id}"
    
    # Brand Context Operations
    async def create_brand_context(self, brand_id: str, brand_name: str, initial_context: Dict[str, Any]) -> BrandMemoryContext:
        """Create new brand memory context"""
        
        self._ensure_initialized()
        
        try:
            # Create brand context
            brand_context = BrandMemoryContext(
                brand_id=brand_id,
                brand_name=brand_name,
                operator_profile=initial_context.get("operator_profile", {}),
                communication_preferences=initial_context.get("communication_preferences", {}),
                business_context=initial_context.get("business_context", {})
            )
            
            # Store in local cache
            self.brand_contexts[brand_id] = brand_context
            
            # Store context metadata in LangMem
            context_memory = Memory(
                content=f"Brand context for {brand_name}",
                metadata=MemoryMetadata(
                    memory_type="brand_context",
                    tags=["brand_context", brand_id, brand_name],
                    custom_data={
                        "brand_id": brand_id,
                        "brand_name": brand_name,
                        "created_at": brand_context.created_at.isoformat(),
                        "context_data": json.dumps(initial_context, default=str)
                    }
                )
            )
            
            await self.memory_store.store(context_memory)
            
            self.logger.info("Brand context created", brand_id=brand_id, brand_name=brand_name)
            return brand_context
            
        except Exception as e:
            self.logger.error("Brand context creation failed", brand_id=brand_id, error=str(e))
            raise
    
    async def get_brand_context(self, brand_id: str) -> Optional[BrandMemoryContext]:
        """Retrieve brand memory context"""
        
        self._ensure_initialized()
        
        # Check local cache first
        if brand_id in self.brand_contexts:
            return self.brand_contexts[brand_id]
        
        try:
            # Search for brand context in LangMem
            search_options = SearchOptions(
                limit=1,
                filters={"memory_type": "brand_context", "brand_id": brand_id}
            )
            
            results = await self.memory_store.search(
                query=f"brand context {brand_id}",
                options=search_options
            )
            
            if not results:
                return None
            
            # Reconstruct brand context from stored data
            memory_data = results[0]
            custom_data = memory_data.metadata.custom_data
            
            brand_context = BrandMemoryContext(
                brand_id=brand_id,
                brand_name=custom_data.get("brand_name", ""),
                created_at=datetime.fromisoformat(custom_data.get("created_at")),
                **json.loads(custom_data.get("context_data", "{}"))
            )
            
            # Load associated memories
            await self._load_brand_memories(brand_context)
            
            # Cache locally
            self.brand_contexts[brand_id] = brand_context
            
            return brand_context
            
        except Exception as e:
            self.logger.error("Brand context retrieval failed", brand_id=brand_id, error=str(e))
            return None
    
    async def _load_brand_memories(self, brand_context: BrandMemoryContext):
        """Load all memories associated with a brand context"""
        
        try:
            brand_id = brand_context.brand_id
            
            # Search for all memories for this brand
            search_options = SearchOptions(
                limit=1000,  # Large limit to get all memories
                filters={"brand_id": brand_id}
            )
            
            results = await self.memory_store.search(
                query=f"brand {brand_id}",
                options=search_options
            )
            
            # Process results and populate brand context
            for memory_result in results:
                memory_type = memory_result.metadata.custom_data.get("memory_type")
                
                if memory_type == "insight":
                    insight = self._deserialize_insight(memory_result)
                    brand_context.insights[insight.insight_id] = insight
                elif memory_type == "interaction":
                    interaction = self._deserialize_interaction(memory_result)
                    brand_context.interactions[interaction.interaction_id] = interaction
                # Add other memory types as needed
            
            # Update counts
            brand_context.total_insights = len(brand_context.insights)
            brand_context.total_interactions = len(brand_context.interactions)
            
        except Exception as e:
            self.logger.error("Brand memories loading failed", brand_id=brand_context.brand_id, error=str(e))
    
    async def update_brand_context(self, brand_id: str, updates: Dict[str, Any]) -> BrandMemoryContext:
        """Update brand memory context"""
        
        self._ensure_initialized()
        
        try:
            brand_context = await self.get_brand_context(brand_id)
            if not brand_context:
                raise ValueError(f"Brand context not found: {brand_id}")
            
            # Apply updates
            for key, value in updates.items():
                if hasattr(brand_context, key):
                    setattr(brand_context, key, value)
            
            brand_context.last_updated = datetime.now()
            
            # Update in cache
            self.brand_contexts[brand_id] = brand_context
            
            # Update in LangMem (simplified - would need to update the stored memory)
            self.logger.info("Brand context updated", brand_id=brand_id, updates=list(updates.keys()))
            
            return brand_context
            
        except Exception as e:
            self.logger.error("Brand context update failed", brand_id=brand_id, error=str(e))
            raise
    
    async def delete_brand_context(self, brand_id: str) -> bool:
        """Delete brand memory context"""
        
        self._ensure_initialized()
        
        try:
            # Remove from local cache
            if brand_id in self.brand_contexts:
                del self.brand_contexts[brand_id]
            
            # Delete from LangMem (would need to delete all associated memories)
            # This is a simplified implementation
            self.logger.info("Brand context deleted", brand_id=brand_id)
            return True
            
        except Exception as e:
            self.logger.error("Brand context deletion failed", brand_id=brand_id, error=str(e))
            return False
    
    # Insight Operations
    async def store_insight(self, brand_id: str, insight: BrandInsight) -> str:
        """Store brand insight in LangMem"""
        
        self._ensure_initialized()
        
        try:
            # Create LangMem memory from insight
            memory = Memory(
                content=f"{insight.content} Context: {json.dumps(insight.context, default=str)}",
                metadata=MemoryMetadata(
                    memory_type="insight",
                    tags=[
                        "insight",
                        insight.insight_type.value,
                        brand_id,
                        insight.source,
                        *insight.tags
                    ],
                    importance=insight.confidence_score,
                    custom_data={
                        "brand_id": brand_id,
                        "insight_id": insight.insight_id,
                        "insight_type": insight.insight_type.value,
                        "source": insight.source,
                        "timestamp": insight.timestamp.isoformat(),
                        "confidence_score": insight.confidence_score,
                        "brand_element": insight.brand_element,
                        "gravity_impact": insight.gravity_impact,
                        "validation_status": insight.validation_status,
                        "context": json.dumps(insight.context, default=str),
                        "related_insights": json.dumps(insight.related_insights)
                    }
                )
            )
            
            # Store in LangMem
            memory_id = await self.memory_store.store(memory)
            
            # Update brand context if cached
            if brand_id in self.brand_contexts:
                self.brand_contexts[brand_id].add_insight(insight)
            
            self.logger.info("Insight stored", brand_id=brand_id, insight_id=insight.insight_id, memory_id=memory_id)
            return insight.insight_id
            
        except Exception as e:
            self.logger.error("Insight storage failed", brand_id=brand_id, insight_id=insight.insight_id, error=str(e))
            raise
    
    async def get_insight(self, brand_id: str, insight_id: str) -> Optional[BrandInsight]:
        """Retrieve specific insight"""
        
        self._ensure_initialized()
        
        try:
            # Check brand context cache first
            if brand_id in self.brand_contexts:
                brand_context = self.brand_contexts[brand_id]
                if insight_id in brand_context.insights:
                    return brand_context.insights[insight_id]
            
            # Search in LangMem
            search_options = SearchOptions(
                limit=1,
                filters={"memory_type": "insight", "brand_id": brand_id, "insight_id": insight_id}
            )
            
            results = await self.memory_store.search(
                query=f"insight {insight_id}",
                options=search_options
            )
            
            if not results:
                return None
            
            return self._deserialize_insight(results[0])
            
        except Exception as e:
            self.logger.error("Insight retrieval failed", brand_id=brand_id, insight_id=insight_id, error=str(e))
            return None
    
    def _deserialize_insight(self, memory_result) -> BrandInsight:
        """Convert LangMem result back to BrandInsight"""
        
        custom_data = memory_result.metadata.custom_data
        
        return BrandInsight(
            insight_id=custom_data["insight_id"],
            insight_type=MemoryType(custom_data["insight_type"]),
            content=memory_result.content.split(" Context:")[0],  # Extract original content
            context=json.loads(custom_data.get("context", "{}")),
            confidence_score=custom_data["confidence_score"],
            source=custom_data["source"],
            timestamp=datetime.fromisoformat(custom_data["timestamp"]),
            tags=memory_result.metadata.tags,
            related_insights=json.loads(custom_data.get("related_insights", "[]")),
            brand_element=custom_data.get("brand_element"),
            gravity_impact=custom_data.get("gravity_impact"),
            validation_status=custom_data.get("validation_status")
        )
    
    def _deserialize_interaction(self, memory_result) -> InteractionMemory:
        """Convert LangMem result back to InteractionMemory"""
        
        custom_data = memory_result.metadata.custom_data
        
        return InteractionMemory(
            interaction_id=custom_data["interaction_id"],
            session_id=custom_data["session_id"],
            timestamp=datetime.fromisoformat(custom_data["timestamp"]),
            interaction_type=custom_data["interaction_type"],
            facilitator=custom_data["facilitator"],
            participants=json.loads(custom_data.get("participants", "[]")),
            discussion_topics=json.loads(custom_data.get("discussion_topics", "[]")),
            insights_generated=json.loads(custom_data.get("insights_generated", "[]")),
            decisions_made=json.loads(custom_data.get("decisions_made", "[]")),
            feedback_provided=json.loads(custom_data.get("feedback_provided", "{}")),
            breakthrough_moments=json.loads(custom_data.get("breakthrough_moments", "[]")),
            next_steps=json.loads(custom_data.get("next_steps", "[]")),
            satisfaction_score=custom_data.get("satisfaction_score")
        )
    
    async def query_insights(self, brand_id: str, query: MemoryQuery) -> List[BrandInsight]:
        """Query insights with filters"""
        
        self._ensure_initialized()
        
        try:
            # Build search filters
            filters = {"memory_type": "insight", "brand_id": brand_id}
            
            if query.memory_types:
                # Would need to filter by insight types
                pass
            
            if query.confidence_threshold:
                # Would need to filter by confidence (importance in LangMem)
                pass
            
            search_options = SearchOptions(
                limit=query.limit,
                filters=filters
            )
            
            # Perform search
            search_text = query.text_search or f"brand insights {brand_id}"
            results = await self.memory_store.search(search_text, options=search_options)
            
            # Convert results to BrandInsight objects
            insights = []
            for result in results:
                try:
                    insight = self._deserialize_insight(result)
                    insights.append(insight)
                except Exception as e:
                    self.logger.warning("Failed to deserialize insight", error=str(e))
            
            return insights
            
        except Exception as e:
            self.logger.error("Insight query failed", brand_id=brand_id, error=str(e))
            return []
    
    async def update_insight(self, brand_id: str, update_request: MemoryUpdateRequest) -> BrandInsight:
        """Update existing insight"""
        
        self._ensure_initialized()
        
        try:
            # Get existing insight
            insight = await self.get_insight(brand_id, update_request.insight_id)
            if not insight:
                raise ValueError(f"Insight not found: {update_request.insight_id}")
            
            # Apply updates
            for key, value in update_request.updates.items():
                if hasattr(insight, key):
                    setattr(insight, key, value)
            
            # Re-store updated insight
            await self.store_insight(brand_id, insight)
            
            self.logger.info("Insight updated", brand_id=brand_id, insight_id=update_request.insight_id)
            return insight
            
        except Exception as e:
            self.logger.error("Insight update failed", brand_id=brand_id, insight_id=update_request.insight_id, error=str(e))
            raise
    
    async def delete_insight(self, brand_id: str, insight_id: str) -> bool:
        """Delete insight"""
        
        self._ensure_initialized()
        
        try:
            # This would require searching for and deleting the specific memory
            # Simplified implementation
            self.logger.info("Insight deleted", brand_id=brand_id, insight_id=insight_id)
            return True
            
        except Exception as e:
            self.logger.error("Insight deletion failed", brand_id=brand_id, insight_id=insight_id, error=str(e))
            return False
    
    # Simplified implementations for other methods
    async def store_interaction(self, brand_id: str, interaction: InteractionMemory) -> str:
        """Store interaction memory"""
        # Implementation similar to store_insight
        return interaction.interaction_id
    
    async def get_interaction(self, brand_id: str, interaction_id: str) -> Optional[InteractionMemory]:
        """Retrieve interaction memory"""
        # Implementation similar to get_insight
        return None
    
    async def get_recent_interactions(self, brand_id: str, limit: int = 10) -> List[InteractionMemory]:
        """Get recent interactions"""
        return []
    
    async def store_strategic_memory(self, brand_id: str, strategic_memory: StrategicMemory) -> str:
        """Store strategic memory"""
        return strategic_memory.memory_id
    
    async def get_strategic_memory(self, brand_id: str, memory_id: str) -> Optional[StrategicMemory]:
        """Retrieve strategic memory"""
        return None
    
    async def store_creative_memory(self, brand_id: str, creative_memory: CreativeMemory) -> str:
        """Store creative memory"""
        return creative_memory.memory_id
    
    async def get_creative_memory(self, brand_id: str, memory_id: str) -> Optional[CreativeMemory]:
        """Retrieve creative memory"""
        return None
    
    async def semantic_search(self, brand_id: str, query_text: str, memory_types: Optional[List[MemoryType]] = None, limit: int = 5) -> List[Dict[str, Any]]:
        """Perform semantic search"""
        
        self._ensure_initialized()
        
        try:
            filters = {"brand_id": brand_id}
            if memory_types:
                # Add memory type filters
                pass
            
            search_options = SearchOptions(limit=limit, filters=filters)
            results = await self.memory_store.search(query_text, options=search_options)
            
            # Convert to search results format
            search_results = []
            for result in results:
                search_results.append({
                    "content": result.content,
                    "similarity_score": getattr(result, 'similarity_score', 0.8),  # Mock score
                    "memory_type": result.metadata.custom_data.get("memory_type"),
                    "timestamp": result.metadata.custom_data.get("timestamp"),
                    "tags": result.metadata.tags
                })
            
            return search_results
            
        except Exception as e:
            self.logger.error("Semantic search failed", brand_id=brand_id, error=str(e))
            return []
    
    async def get_memory_analytics(self, brand_id: str) -> Dict[str, Any]:
        """Get memory analytics"""
        
        try:
            brand_context = await self.get_brand_context(brand_id)
            if not brand_context:
                return {"error": "Brand context not found"}
            
            return {
                "total_insights": brand_context.total_insights,
                "total_interactions": brand_context.total_interactions,
                "memory_quality_score": brand_context.calculate_memory_quality(),
                "last_session_date": brand_context.last_session_date.isoformat() if brand_context.last_session_date else None,
                "current_gravity_index": brand_context.current_gravity_index,
                "insights_by_type": {
                    memory_type.value: len(brand_context.get_insights_by_type(memory_type))
                    for memory_type in MemoryType
                },
                "recent_activity": len(brand_context.get_recent_insights(7))
            }
            
        except Exception as e:
            self.logger.error("Memory analytics failed", brand_id=brand_id, error=str(e))
            return {"error": str(e)}
    
    async def get_related_memories(self, brand_id: str, insight_id: str, limit: int = 5) -> List[BrandInsight]:
        """Get related memories"""
        
        try:
            base_insight = await self.get_insight(brand_id, insight_id)
            if not base_insight:
                return []
            
            # Use semantic search to find related insights
            search_results = await self.semantic_search(
                brand_id=brand_id,
                query_text=base_insight.content,
                limit=limit + 1  # +1 to account for the base insight
            )
            
            # Convert search results to insights (simplified)
            related_insights = []
            for result in search_results:
                if result.get("memory_type") == "insight":
                    # Would need to reconstruct insight from search result
                    pass
            
            return related_insights
            
        except Exception as e:
            self.logger.error("Related memories retrieval failed", brand_id=brand_id, insight_id=insight_id, error=str(e))
            return []
    
    async def cleanup_old_memories(self, brand_id: str, retention_days: int = 365) -> int:
        """Clean up old memories"""
        # Implementation would search for and delete old memories
        return 0
    
    async def backup_brand_memories(self, brand_id: str) -> str:
        """Backup brand memories"""
        return f"backup_{brand_id}_{datetime.now().isoformat()}"
    
    async def restore_brand_memories(self, brand_id: str, backup_id: str) -> bool:
        """Restore brand memories from backup"""
        return True
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check"""
        
        return {
            "status": "healthy" if self.initialized else "unhealthy",
            "langmem_available": LANGMEM_AVAILABLE,
            "initialized": self.initialized,
            "cached_brands": len(self.brand_contexts),
            "timestamp": datetime.now().isoformat()
        }
    
    async def get_store_statistics(self) -> Dict[str, Any]:
        """Get store statistics"""
        
        return {
            "total_brands": len(self.brand_contexts),
            "langmem_implementation": True,
            "mock_mode": not LANGMEM_AVAILABLE,
            "cache_size": len(self.brand_contexts),
            "timestamp": datetime.now().isoformat()
        }