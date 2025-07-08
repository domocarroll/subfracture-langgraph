"""
SUBFRACTURE Brand Memory Store - Abstract Interface

Abstract base class defining the interface for brand memory operations.
Follows SOLID principles with dependency inversion for different memory backends.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union
from datetime import datetime

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


class BrandMemoryStore(ABC):
    """
    Abstract interface for brand memory operations
    
    Defines the contract for storing, retrieving, and managing brand intelligence
    across different memory backend implementations (LangMem, Redis, PostgreSQL, etc.)
    """
    
    @abstractmethod
    async def initialize(self, config: Dict[str, Any]) -> bool:
        """
        Initialize the memory store with configuration
        
        Args:
            config: Configuration dictionary for the memory store
            
        Returns:
            bool: True if initialization successful
        """
        pass
    
    @abstractmethod
    async def shutdown(self) -> bool:
        """
        Shutdown the memory store and cleanup resources
        
        Returns:
            bool: True if shutdown successful
        """
        pass
    
    # Brand Context Operations
    @abstractmethod
    async def create_brand_context(self, brand_id: str, brand_name: str, initial_context: Dict[str, Any]) -> BrandMemoryContext:
        """
        Create a new brand memory context
        
        Args:
            brand_id: Unique brand identifier
            brand_name: Brand name
            initial_context: Initial brand context data
            
        Returns:
            BrandMemoryContext: Created brand context
        """
        pass
    
    @abstractmethod
    async def get_brand_context(self, brand_id: str) -> Optional[BrandMemoryContext]:
        """
        Retrieve brand memory context
        
        Args:
            brand_id: Brand identifier
            
        Returns:
            Optional[BrandMemoryContext]: Brand context if found
        """
        pass
    
    @abstractmethod
    async def update_brand_context(self, brand_id: str, updates: Dict[str, Any]) -> BrandMemoryContext:
        """
        Update brand memory context
        
        Args:
            brand_id: Brand identifier
            updates: Context updates to apply
            
        Returns:
            BrandMemoryContext: Updated brand context
        """
        pass
    
    @abstractmethod
    async def delete_brand_context(self, brand_id: str) -> bool:
        """
        Delete brand memory context
        
        Args:
            brand_id: Brand identifier
            
        Returns:
            bool: True if deletion successful
        """
        pass
    
    # Insight Operations
    @abstractmethod
    async def store_insight(self, brand_id: str, insight: BrandInsight) -> str:
        """
        Store a brand insight
        
        Args:
            brand_id: Brand identifier
            insight: Brand insight to store
            
        Returns:
            str: Stored insight ID
        """
        pass
    
    @abstractmethod
    async def get_insight(self, brand_id: str, insight_id: str) -> Optional[BrandInsight]:
        """
        Retrieve a specific insight
        
        Args:
            brand_id: Brand identifier
            insight_id: Insight identifier
            
        Returns:
            Optional[BrandInsight]: Insight if found
        """
        pass
    
    @abstractmethod
    async def query_insights(self, brand_id: str, query: MemoryQuery) -> List[BrandInsight]:
        """
        Query insights with filters
        
        Args:
            brand_id: Brand identifier
            query: Query parameters
            
        Returns:
            List[BrandInsight]: Matching insights
        """
        pass
    
    @abstractmethod
    async def update_insight(self, brand_id: str, update_request: MemoryUpdateRequest) -> BrandInsight:
        """
        Update an existing insight
        
        Args:
            brand_id: Brand identifier
            update_request: Update request details
            
        Returns:
            BrandInsight: Updated insight
        """
        pass
    
    @abstractmethod
    async def delete_insight(self, brand_id: str, insight_id: str) -> bool:
        """
        Delete an insight
        
        Args:
            brand_id: Brand identifier
            insight_id: Insight identifier
            
        Returns:
            bool: True if deletion successful
        """
        pass
    
    # Interaction Memory Operations
    @abstractmethod
    async def store_interaction(self, brand_id: str, interaction: InteractionMemory) -> str:
        """
        Store an interaction memory
        
        Args:
            brand_id: Brand identifier
            interaction: Interaction memory to store
            
        Returns:
            str: Stored interaction ID
        """
        pass
    
    @abstractmethod
    async def get_interaction(self, brand_id: str, interaction_id: str) -> Optional[InteractionMemory]:
        """
        Retrieve a specific interaction
        
        Args:
            brand_id: Brand identifier
            interaction_id: Interaction identifier
            
        Returns:
            Optional[InteractionMemory]: Interaction if found
        """
        pass
    
    @abstractmethod
    async def get_recent_interactions(self, brand_id: str, limit: int = 10) -> List[InteractionMemory]:
        """
        Get recent interactions for a brand
        
        Args:
            brand_id: Brand identifier
            limit: Maximum number of interactions to return
            
        Returns:
            List[InteractionMemory]: Recent interactions
        """
        pass
    
    # Strategic Memory Operations
    @abstractmethod
    async def store_strategic_memory(self, brand_id: str, strategic_memory: StrategicMemory) -> str:
        """
        Store strategic memory
        
        Args:
            brand_id: Brand identifier
            strategic_memory: Strategic memory to store
            
        Returns:
            str: Stored memory ID
        """
        pass
    
    @abstractmethod
    async def get_strategic_memory(self, brand_id: str, memory_id: str) -> Optional[StrategicMemory]:
        """
        Retrieve strategic memory
        
        Args:
            brand_id: Brand identifier
            memory_id: Memory identifier
            
        Returns:
            Optional[StrategicMemory]: Strategic memory if found
        """
        pass
    
    # Creative Memory Operations
    @abstractmethod
    async def store_creative_memory(self, brand_id: str, creative_memory: CreativeMemory) -> str:
        """
        Store creative memory
        
        Args:
            brand_id: Brand identifier
            creative_memory: Creative memory to store
            
        Returns:
            str: Stored memory ID
        """
        pass
    
    @abstractmethod
    async def get_creative_memory(self, brand_id: str, memory_id: str) -> Optional[CreativeMemory]:
        """
        Retrieve creative memory
        
        Args:
            brand_id: Brand identifier
            memory_id: Memory identifier
            
        Returns:
            Optional[CreativeMemory]: Creative memory if found
        """
        pass
    
    # Search and Analytics
    @abstractmethod
    async def semantic_search(self, brand_id: str, query_text: str, memory_types: Optional[List[MemoryType]] = None, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Perform semantic search across memories
        
        Args:
            brand_id: Brand identifier
            query_text: Search query
            memory_types: Optional filter by memory types
            limit: Maximum results
            
        Returns:
            List[Dict[str, Any]]: Search results with similarity scores
        """
        pass
    
    @abstractmethod
    async def get_memory_analytics(self, brand_id: str) -> Dict[str, Any]:
        """
        Get analytics about stored memories
        
        Args:
            brand_id: Brand identifier
            
        Returns:
            Dict[str, Any]: Memory analytics and statistics
        """
        pass
    
    @abstractmethod
    async def get_related_memories(self, brand_id: str, insight_id: str, limit: int = 5) -> List[BrandInsight]:
        """
        Get memories related to a specific insight
        
        Args:
            brand_id: Brand identifier
            insight_id: Base insight identifier
            limit: Maximum related memories
            
        Returns:
            List[BrandInsight]: Related insights
        """
        pass
    
    # Maintenance Operations
    @abstractmethod
    async def cleanup_old_memories(self, brand_id: str, retention_days: int = 365) -> int:
        """
        Clean up old memories beyond retention period
        
        Args:
            brand_id: Brand identifier
            retention_days: Days to retain memories
            
        Returns:
            int: Number of memories cleaned up
        """
        pass
    
    @abstractmethod
    async def backup_brand_memories(self, brand_id: str) -> str:
        """
        Create backup of brand memories
        
        Args:
            brand_id: Brand identifier
            
        Returns:
            str: Backup identifier or path
        """
        pass
    
    @abstractmethod
    async def restore_brand_memories(self, brand_id: str, backup_id: str) -> bool:
        """
        Restore brand memories from backup
        
        Args:
            brand_id: Brand identifier
            backup_id: Backup identifier
            
        Returns:
            bool: True if restore successful
        """
        pass
    
    # Health and Status
    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform health check on memory store
        
        Returns:
            Dict[str, Any]: Health status information
        """
        pass
    
    @abstractmethod
    async def get_store_statistics(self) -> Dict[str, Any]:
        """
        Get overall store statistics
        
        Returns:
            Dict[str, Any]: Store statistics
        """
        pass