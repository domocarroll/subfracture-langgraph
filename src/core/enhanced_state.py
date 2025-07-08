"""
SUBFRACTURE Enhanced State Management

Extended state models that add memory, swarm coordination, and research intelligence
capabilities while maintaining backward compatibility with existing SUBFRACTURE workflows.
"""

from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel, Field
from enum import Enum

from .state import SubfractureGravityState, WorkshopPhase, GravityType
from ..memory.memory_models import BrandMemoryContext, BrandInsight


class SwarmCoordinationMode(str, Enum):
    """Modes for swarm coordination"""
    SEQUENTIAL = "sequential"      # Traditional linear workflow
    PARALLEL = "parallel"          # Agents work simultaneously
    DYNAMIC = "dynamic"            # Agents hand off based on need
    COLLABORATIVE = "collaborative"  # Agents work together on tasks


class AgentStatus(str, Enum):
    """Status of individual agents in the swarm"""
    IDLE = "idle"
    ACTIVE = "active"
    WAITING = "waiting"
    COMPLETED = "completed"
    ERROR = "error"
    HANDED_OFF = "handed_off"


class ResearchIntelligenceMode(str, Enum):
    """Modes for research intelligence"""
    DISABLED = "disabled"
    BASIC = "basic"               # Basic competitive monitoring
    ENHANCED = "enhanced"         # Full research automation
    CONTINUOUS = "continuous"     # Real-time intelligence updates


class SwarmAgent(BaseModel):
    """Individual agent in the swarm"""
    
    agent_id: str = Field(..., description="Unique agent identifier")
    agent_type: str = Field(..., description="Type of agent (strategy, creative, etc.)")
    agent_name: str = Field(..., description="Human-readable agent name")
    status: AgentStatus = Field(default=AgentStatus.IDLE, description="Current agent status")
    capabilities: List[str] = Field(default_factory=list, description="Agent capabilities")
    
    # Coordination
    current_task: Optional[str] = Field(None, description="Current task assignment")
    handoff_context: Dict[str, Any] = Field(default_factory=dict, description="Context for handoffs")
    dependencies: List[str] = Field(default_factory=list, description="Dependent agent IDs")
    
    # Performance
    task_history: List[Dict[str, Any]] = Field(default_factory=list, description="Task execution history")
    performance_metrics: Dict[str, Any] = Field(default_factory=dict, description="Agent performance data")
    last_active: Optional[datetime] = Field(None, description="Last activity timestamp")
    
    # Memory integration
    memory_context: Dict[str, Any] = Field(default_factory=dict, description="Agent's memory context")
    learned_patterns: List[str] = Field(default_factory=list, description="Patterns learned by agent")


class SwarmCoordinationState(BaseModel):
    """State for coordinating multiple agents"""
    
    coordination_mode: SwarmCoordinationMode = Field(default=SwarmCoordinationMode.SEQUENTIAL)
    active_agents: Dict[str, SwarmAgent] = Field(default_factory=dict, description="Currently active agents")
    
    # Task coordination
    task_queue: List[Dict[str, Any]] = Field(default_factory=list, description="Pending tasks")
    completed_tasks: List[Dict[str, Any]] = Field(default_factory=list, description="Completed tasks")
    active_handoffs: Dict[str, Any] = Field(default_factory=dict, description="Active agent handoffs")
    
    # Workflow orchestration
    current_orchestrator: Optional[str] = Field(None, description="Current orchestrating agent")
    workflow_context: Dict[str, Any] = Field(default_factory=dict, description="Shared workflow context")
    collaboration_patterns: List[str] = Field(default_factory=list, description="Observed collaboration patterns")
    
    # Performance tracking
    coordination_metrics: Dict[str, Any] = Field(default_factory=dict, description="Coordination performance")
    efficiency_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Coordination efficiency")
    parallelization_opportunities: List[str] = Field(default_factory=list, description="Identified parallelization opportunities")


class ResearchInsight(BaseModel):
    """Research intelligence insight"""
    
    insight_id: str = Field(..., description="Unique insight identifier")
    insight_type: str = Field(..., description="Type of research insight")
    content: str = Field(..., description="Insight content")
    source: str = Field(..., description="Research source")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence level")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # Research context
    search_query: Optional[str] = Field(None, description="Original search query")
    data_sources: List[str] = Field(default_factory=list, description="Data sources used")
    methodology: Optional[str] = Field(None, description="Research methodology")
    
    # Business relevance
    relevance_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Relevance to brand")
    impact_potential: float = Field(default=0.0, ge=0.0, le=1.0, description="Potential business impact")
    actionability: float = Field(default=0.0, ge=0.0, le=1.0, description="How actionable the insight is")


class ResearchIntelligenceState(BaseModel):
    """State for research intelligence operations"""
    
    intelligence_mode: ResearchIntelligenceMode = Field(default=ResearchIntelligenceMode.BASIC)
    research_active: bool = Field(default=False, description="Whether research is currently active")
    
    # Research insights
    competitive_insights: List[ResearchInsight] = Field(default_factory=list, description="Competitive intelligence")
    market_insights: List[ResearchInsight] = Field(default_factory=list, description="Market research insights")
    trend_insights: List[ResearchInsight] = Field(default_factory=list, description="Trend analysis insights")
    opportunity_insights: List[ResearchInsight] = Field(default_factory=list, description="Market opportunity insights")
    
    # Research coordination
    active_research_tasks: List[Dict[str, Any]] = Field(default_factory=list, description="Active research tasks")
    research_queue: List[Dict[str, Any]] = Field(default_factory=list, description="Queued research tasks")
    research_history: List[Dict[str, Any]] = Field(default_factory=list, description="Research execution history")
    
    # Intelligence metrics
    research_coverage: Dict[str, float] = Field(default_factory=dict, description="Coverage by research domain")
    intelligence_freshness: Dict[str, datetime] = Field(default_factory=dict, description="Last update by domain")
    research_effectiveness: float = Field(default=0.0, ge=0.0, le=1.0, description="Research effectiveness score")


class MemoryIntegrationState(BaseModel):
    """State for memory system integration"""
    
    memory_enabled: bool = Field(default=True, description="Whether memory integration is enabled")
    brand_memory_id: Optional[str] = Field(None, description="Associated brand memory context ID")
    
    # Memory operations
    stored_insights: List[str] = Field(default_factory=list, description="Insight IDs stored in memory")
    retrieved_insights: List[str] = Field(default_factory=list, description="Insight IDs retrieved from memory")
    memory_queries: List[Dict[str, Any]] = Field(default_factory=list, description="Memory query history")
    
    # Memory intelligence
    contextual_memories: List[BrandInsight] = Field(default_factory=list, description="Relevant contextual memories")
    memory_suggestions: List[str] = Field(default_factory=list, description="Memory-based suggestions")
    learning_patterns: List[str] = Field(default_factory=list, description="Identified learning patterns")
    
    # Memory performance
    memory_retrieval_time: float = Field(default=0.0, description="Average memory retrieval time")
    memory_relevance_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Relevance of retrieved memories")
    memory_quality_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Quality of stored memories")


class EnhancedSubfractureState(SubfractureGravityState):
    """
    Enhanced SUBFRACTURE state with memory, swarm coordination, and research intelligence
    
    Extends the base SubfractureGravityState while maintaining full backward compatibility.
    New capabilities are optional and can be enabled/disabled as needed.
    """
    
    # Enhanced capabilities
    memory_integration: MemoryIntegrationState = Field(
        default_factory=MemoryIntegrationState,
        description="Memory system integration state"
    )
    
    swarm_coordination: SwarmCoordinationState = Field(
        default_factory=SwarmCoordinationState,
        description="Swarm coordination state"
    )
    
    research_intelligence: ResearchIntelligenceState = Field(
        default_factory=ResearchIntelligenceState,
        description="Research intelligence state"
    )
    
    # Enhanced workflow tracking
    enhancement_features_enabled: Dict[str, bool] = Field(
        default_factory=lambda: {
            "memory_integration": True,
            "swarm_coordination": False,
            "research_intelligence": False,
            "living_brand_world": False
        },
        description="Which enhancement features are enabled"
    )
    
    enhancement_metrics: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metrics for enhanced features"
    )
    
    # Backward compatibility helpers
    def to_base_state(self) -> SubfractureGravityState:
        """Convert to base SubfractureGravityState for backward compatibility"""
        
        base_fields = {}
        for field_name, field_info in SubfractureGravityState.__fields__.items():
            if hasattr(self, field_name):
                base_fields[field_name] = getattr(self, field_name)
        
        return SubfractureGravityState(**base_fields)
    
    @classmethod
    def from_base_state(cls, base_state: SubfractureGravityState) -> "EnhancedSubfractureState":
        """Create enhanced state from base state"""
        
        # Extract base state fields
        base_fields = base_state.dict()
        
        # Create enhanced state with base fields
        enhanced_state = cls(**base_fields)
        
        return enhanced_state
    
    # Enhanced functionality methods
    def enable_feature(self, feature_name: str) -> bool:
        """Enable an enhancement feature"""
        
        if feature_name in self.enhancement_features_enabled:
            self.enhancement_features_enabled[feature_name] = True
            return True
        return False
    
    def disable_feature(self, feature_name: str) -> bool:
        """Disable an enhancement feature"""
        
        if feature_name in self.enhancement_features_enabled:
            self.enhancement_features_enabled[feature_name] = False
            return True
        return False
    
    def is_feature_enabled(self, feature_name: str) -> bool:
        """Check if enhancement feature is enabled"""
        
        return self.enhancement_features_enabled.get(feature_name, False)
    
    def add_swarm_agent(self, agent: SwarmAgent):
        """Add agent to swarm coordination"""
        
        self.swarm_coordination.active_agents[agent.agent_id] = agent
    
    def get_swarm_agent(self, agent_id: str) -> Optional[SwarmAgent]:
        """Get swarm agent by ID"""
        
        return self.swarm_coordination.active_agents.get(agent_id)
    
    def update_agent_status(self, agent_id: str, status: AgentStatus, context: Optional[Dict[str, Any]] = None):
        """Update agent status"""
        
        if agent_id in self.swarm_coordination.active_agents:
            agent = self.swarm_coordination.active_agents[agent_id]
            agent.status = status
            agent.last_active = datetime.now()
            
            if context:
                agent.handoff_context.update(context)
    
    def add_research_insight(self, insight: ResearchInsight):
        """Add research insight to appropriate category"""
        
        if insight.insight_type == "competitive":
            self.research_intelligence.competitive_insights.append(insight)
        elif insight.insight_type == "market":
            self.research_intelligence.market_insights.append(insight)
        elif insight.insight_type == "trend":
            self.research_intelligence.trend_insights.append(insight)
        elif insight.insight_type == "opportunity":
            self.research_intelligence.opportunity_insights.append(insight)
    
    def get_research_insights_by_type(self, insight_type: str) -> List[ResearchInsight]:
        """Get research insights by type"""
        
        if insight_type == "competitive":
            return self.research_intelligence.competitive_insights
        elif insight_type == "market":
            return self.research_intelligence.market_insights
        elif insight_type == "trend":
            return self.research_intelligence.trend_insights
        elif insight_type == "opportunity":
            return self.research_intelligence.opportunity_insights
        else:
            return []
    
    def add_contextual_memory(self, memory: BrandInsight):
        """Add contextual memory from memory system"""
        
        self.memory_integration.contextual_memories.append(memory)
        self.memory_integration.retrieved_insights.append(memory.insight_id)
    
    def record_memory_query(self, query: str, results_count: int, retrieval_time: float):
        """Record memory query for performance tracking"""
        
        query_record = {
            "query": query,
            "results_count": results_count,
            "retrieval_time": retrieval_time,
            "timestamp": datetime.now().isoformat()
        }
        
        self.memory_integration.memory_queries.append(query_record)
        
        # Update average retrieval time
        if self.memory_integration.memory_queries:
            total_time = sum(q["retrieval_time"] for q in self.memory_integration.memory_queries)
            self.memory_integration.memory_retrieval_time = total_time / len(self.memory_integration.memory_queries)
    
    def calculate_enhancement_effectiveness(self) -> Dict[str, float]:
        """Calculate effectiveness scores for enhancement features"""
        
        effectiveness = {}
        
        # Memory effectiveness
        if self.is_feature_enabled("memory_integration"):
            memory_score = 0.0
            if self.memory_integration.contextual_memories:
                relevance_scores = [m.confidence_score for m in self.memory_integration.contextual_memories]
                memory_score = sum(relevance_scores) / len(relevance_scores)
            effectiveness["memory_integration"] = memory_score
        
        # Swarm effectiveness
        if self.is_feature_enabled("swarm_coordination"):
            swarm_score = self.swarm_coordination.efficiency_score
            effectiveness["swarm_coordination"] = swarm_score
        
        # Research effectiveness
        if self.is_feature_enabled("research_intelligence"):
            research_score = self.research_intelligence.research_effectiveness
            effectiveness["research_intelligence"] = research_score
        
        # Overall enhancement effectiveness
        if effectiveness:
            effectiveness["overall"] = sum(effectiveness.values()) / len(effectiveness)
        else:
            effectiveness["overall"] = 0.0
        
        # Store in enhancement metrics
        self.enhancement_metrics["effectiveness_scores"] = effectiveness
        
        return effectiveness
    
    def get_enhancement_summary(self) -> Dict[str, Any]:
        """Get summary of enhancement features and their status"""
        
        return {
            "features_enabled": self.enhancement_features_enabled,
            "memory_stats": {
                "stored_insights": len(self.memory_integration.stored_insights),
                "retrieved_insights": len(self.memory_integration.retrieved_insights),
                "contextual_memories": len(self.memory_integration.contextual_memories),
                "quality_score": self.memory_integration.memory_quality_score
            },
            "swarm_stats": {
                "active_agents": len(self.swarm_coordination.active_agents),
                "coordination_mode": self.swarm_coordination.coordination_mode.value,
                "efficiency_score": self.swarm_coordination.efficiency_score,
                "completed_tasks": len(self.swarm_coordination.completed_tasks)
            },
            "research_stats": {
                "intelligence_mode": self.research_intelligence.intelligence_mode.value,
                "competitive_insights": len(self.research_intelligence.competitive_insights),
                "market_insights": len(self.research_intelligence.market_insights),
                "research_effectiveness": self.research_intelligence.research_effectiveness
            },
            "effectiveness_scores": self.calculate_enhancement_effectiveness(),
            "enhancement_metrics": self.enhancement_metrics
        }


# Utility functions for state management
def create_enhanced_state_from_inputs(
    brand_brief: str,
    operator_context: Dict[str, Any],
    target_outcome: str = "",
    enable_features: Optional[Dict[str, bool]] = None
) -> EnhancedSubfractureState:
    """Create enhanced state with initial inputs and feature configuration"""
    
    # Create base state
    state = EnhancedSubfractureState(
        brand_brief=brand_brief,
        operator_context=operator_context,
        target_outcome=target_outcome
    )
    
    # Configure enhancement features
    if enable_features:
        for feature, enabled in enable_features.items():
            if enabled:
                state.enable_feature(feature)
            else:
                state.disable_feature(feature)
    
    return state


def migrate_base_state_to_enhanced(base_state: SubfractureGravityState) -> EnhancedSubfractureState:
    """Migrate existing base state to enhanced state with default settings"""
    
    enhanced_state = EnhancedSubfractureState.from_base_state(base_state)
    
    # Set up default enhancement configuration
    enhanced_state.enable_feature("memory_integration")  # Enable memory by default
    
    return enhanced_state


def create_swarm_agent(
    agent_type: str,
    agent_name: str,
    capabilities: List[str],
    agent_id: Optional[str] = None
) -> SwarmAgent:
    """Create a new swarm agent with default configuration"""
    
    if not agent_id:
        agent_id = f"{agent_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    return SwarmAgent(
        agent_id=agent_id,
        agent_type=agent_type,
        agent_name=agent_name,
        capabilities=capabilities,
        performance_metrics={
            "tasks_completed": 0,
            "average_execution_time": 0.0,
            "success_rate": 1.0,
            "handoff_efficiency": 1.0
        }
    )