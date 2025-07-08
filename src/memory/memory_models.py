"""
SUBFRACTURE Enhanced Memory Models

Data models for persistent brand intelligence and memory operations.
Defines the structure for storing and retrieving brand knowledge across sessions.
"""

from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel, Field
from enum import Enum


class MemoryType(str, Enum):
    """Types of brand memories that can be stored"""
    STRATEGIC = "strategic"           # Strategic insights and positioning
    CREATIVE = "creative"             # Creative insights and concepts  
    DESIGN = "design"                 # Visual language and design principles
    TECHNOLOGY = "technology"         # Technical architecture and roadmaps
    GRAVITY = "gravity"               # Brand gravity analysis and optimization
    INTERACTION = "interaction"       # Workshop interactions and feedback
    BREAKTHROUGH = "breakthrough"     # Vesica pisces discoveries
    COMPETITIVE = "competitive"       # Competitive intelligence
    MARKET = "market"                 # Market trends and opportunities
    VALIDATION = "validation"         # Human validation results


class BrandInsight(BaseModel):
    """A specific brand insight stored in memory"""
    
    insight_id: str = Field(..., description="Unique insight identifier")
    insight_type: MemoryType = Field(..., description="Type of insight")
    content: str = Field(..., description="The insight content")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence in insight")
    source: str = Field(..., description="Source of insight (agent, human, research)")
    timestamp: datetime = Field(default_factory=datetime.now)
    tags: List[str] = Field(default_factory=list, description="Categorization tags")
    related_insights: List[str] = Field(default_factory=list, description="Related insight IDs")
    
    # Brand-specific metadata
    brand_element: Optional[str] = Field(None, description="Brand element this relates to")
    gravity_impact: Optional[float] = Field(None, description="Impact on brand gravity")
    validation_status: Optional[str] = Field(None, description="Human validation status")


class InteractionMemory(BaseModel):
    """Memory of a specific interaction or workshop session"""
    
    interaction_id: str = Field(..., description="Unique interaction identifier")
    session_id: str = Field(..., description="Workshop session ID")
    timestamp: datetime = Field(default_factory=datetime.now)
    interaction_type: str = Field(..., description="Type of interaction")
    
    # Participants
    facilitator: str = Field(..., description="Workshop facilitator")
    participants: List[str] = Field(default_factory=list, description="Session participants")
    
    # Content
    discussion_topics: List[str] = Field(default_factory=list)
    insights_generated: List[str] = Field(default_factory=list, description="Insight IDs generated")
    decisions_made: List[Dict[str, Any]] = Field(default_factory=list)
    feedback_provided: Dict[str, Any] = Field(default_factory=dict)
    
    # Outcomes
    breakthrough_moments: List[str] = Field(default_factory=list)
    next_steps: List[str] = Field(default_factory=list)
    satisfaction_score: Optional[float] = Field(None, ge=0.0, le=10.0)
    
    # Memory associations
    strategic_memories: List[str] = Field(default_factory=list)
    creative_memories: List[str] = Field(default_factory=list)
    validation_results: Dict[str, Any] = Field(default_factory=dict)


class StrategicMemory(BaseModel):
    """Strategic insights and positioning memory"""
    
    memory_id: str = Field(..., description="Unique memory identifier")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # Strategic elements
    positioning_statements: List[str] = Field(default_factory=list)
    competitive_advantages: List[str] = Field(default_factory=list)
    market_opportunities: List[str] = Field(default_factory=list)
    target_audiences: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Strategic frameworks
    frameworks_used: List[str] = Field(default_factory=list)
    success_metrics: List[str] = Field(default_factory=list)
    strategic_priorities: List[str] = Field(default_factory=list)
    
    # Evolution tracking
    confidence_evolution: List[Dict[str, Any]] = Field(default_factory=list)
    validation_history: List[Dict[str, Any]] = Field(default_factory=list)
    iteration_notes: List[str] = Field(default_factory=list)


class CreativeMemory(BaseModel):
    """Creative insights and concept memory"""
    
    memory_id: str = Field(..., description="Unique memory identifier")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # Creative elements
    brand_personality_traits: List[str] = Field(default_factory=list)
    creative_territories: List[Dict[str, Any]] = Field(default_factory=list)
    messaging_concepts: List[str] = Field(default_factory=list)
    emotional_drivers: List[str] = Field(default_factory=list)
    
    # Creative insights
    target_insights: List[Dict[str, Any]] = Field(default_factory=list)
    cultural_patterns: List[str] = Field(default_factory=list)
    breakthrough_concepts: List[str] = Field(default_factory=list)
    
    # Creative validation
    resonance_scores: Dict[str, float] = Field(default_factory=dict)
    feedback_themes: List[str] = Field(default_factory=list)
    refinement_notes: List[str] = Field(default_factory=list)


class BrandMemoryContext(BaseModel):
    """Complete brand memory context for a client"""
    
    brand_id: str = Field(..., description="Unique brand identifier")
    brand_name: str = Field(..., description="Brand name")
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    
    # Memory collections
    insights: Dict[str, BrandInsight] = Field(default_factory=dict)
    interactions: Dict[str, InteractionMemory] = Field(default_factory=dict)
    strategic_memories: Dict[str, StrategicMemory] = Field(default_factory=dict)
    creative_memories: Dict[str, CreativeMemory] = Field(default_factory=dict)
    
    # Brand state
    current_gravity_index: float = Field(default=0.0, ge=0.0, le=1.0)
    gravity_history: List[Dict[str, Any]] = Field(default_factory=list)
    active_sessions: List[str] = Field(default_factory=list)
    
    # Operator context
    operator_profile: Dict[str, Any] = Field(default_factory=dict)
    communication_preferences: Dict[str, Any] = Field(default_factory=dict)
    business_context: Dict[str, Any] = Field(default_factory=dict)
    
    # Memory metadata
    total_insights: int = Field(default=0)
    total_interactions: int = Field(default=0)
    last_session_date: Optional[datetime] = Field(None)
    memory_quality_score: float = Field(default=0.0, ge=0.0, le=1.0)
    
    def add_insight(self, insight: BrandInsight):
        """Add new insight to memory"""
        self.insights[insight.insight_id] = insight
        self.total_insights = len(self.insights)
        self.last_updated = datetime.now()
    
    def add_interaction(self, interaction: InteractionMemory):
        """Add new interaction to memory"""
        self.interactions[interaction.interaction_id] = interaction
        self.total_interactions = len(self.interactions)
        self.last_session_date = interaction.timestamp
        self.last_updated = datetime.now()
    
    def get_insights_by_type(self, memory_type: MemoryType) -> List[BrandInsight]:
        """Get insights filtered by memory type"""
        return [
            insight for insight in self.insights.values()
            if insight.insight_type == memory_type
        ]
    
    def get_recent_insights(self, days: int = 30) -> List[BrandInsight]:
        """Get insights from the last N days"""
        cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
        return [
            insight for insight in self.insights.values()
            if insight.timestamp.timestamp() > cutoff_date
        ]
    
    def calculate_memory_quality(self) -> float:
        """Calculate the quality score of stored memories"""
        if not self.insights:
            return 0.0
        
        # Quality factors
        insight_confidence = sum(insight.confidence_score for insight in self.insights.values()) / len(self.insights)
        validation_ratio = len([i for i in self.insights.values() if i.validation_status == "validated"]) / len(self.insights)
        recency_factor = min(1.0, len(self.get_recent_insights(30)) / max(1, len(self.insights)))
        
        quality_score = (insight_confidence * 0.4 + validation_ratio * 0.4 + recency_factor * 0.2)
        self.memory_quality_score = quality_score
        return quality_score


class MemoryQuery(BaseModel):
    """Query structure for memory retrieval"""
    
    memory_types: Optional[List[MemoryType]] = Field(None, description="Filter by memory types")
    tags: Optional[List[str]] = Field(None, description="Filter by tags")
    date_range: Optional[Dict[str, datetime]] = Field(None, description="Date range filter")
    confidence_threshold: Optional[float] = Field(None, ge=0.0, le=1.0)
    text_search: Optional[str] = Field(None, description="Text search in content")
    limit: int = Field(default=10, ge=1, le=100, description="Maximum results")
    sort_by: str = Field(default="timestamp", description="Sort field")
    sort_order: str = Field(default="desc", description="Sort order")


class MemoryUpdateRequest(BaseModel):
    """Request structure for memory updates"""
    
    insight_id: str = Field(..., description="Insight ID to update")
    updates: Dict[str, Any] = Field(..., description="Fields to update")
    reason: str = Field(..., description="Reason for update")
    updated_by: str = Field(..., description="Who made the update")