"""
SUBFRACTURE LangGraph State Management

Core state models for the brand intelligence workflow integrating
SUBFRACTURE v1 four-pillar methodology with gravity system.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class WorkshopPhase(str, Enum):
    """Workshop execution phases"""
    SETUP = "setup"
    STRATEGY = "strategy"
    CREATIVE = "creative"
    DESIGN = "design"
    TECHNOLOGY = "technology"
    GRAVITY_ANALYSIS = "gravity_analysis"
    HUMAN_VALIDATION = "human_validation"
    VESICA_PISCES = "vesica_pisces"
    BRAND_WORLD = "brand_world"
    COMPLETED = "completed"


class GravityType(str, Enum):
    """Five gravity types from SUBFRACTURE v1"""
    RECOGNITION = "recognition"      # Visual distinctiveness
    COMPREHENSION = "comprehension"  # Message clarity
    ATTRACTION = "attraction"        # Cultural relevance
    AMPLIFICATION = "amplification"  # Partnership synergy
    TRUST = "trust"                 # Experiential consistency


class SubfractureGravityState(BaseModel):
    """
    Core state for SUBFRACTURE brand intelligence workflow
    Integrates v1 four-pillar system with gravity rules
    """
    
    # Session Context
    session_id: str = Field(default="", description="Unique session identifier")
    timestamp: datetime = Field(default_factory=datetime.now, description="Session start time")
    current_phase: WorkshopPhase = Field(default=WorkshopPhase.SETUP, description="Current workflow phase")
    
    # Input Context: Brand Operator Brief
    brand_brief: str = Field(default="", description="Core brand challenge description")
    operator_context: Dict[str, Any] = Field(
        default_factory=dict,
        description="Brand operator context (founder/executive personal investment)"
    )
    target_outcome: str = Field(
        default="",
        description="Desired end state - 'start with end in mind'"
    )
    
    # Four Pillar Outputs (SUBFRACTURE v1 Core)
    strategy_insights: Dict[str, Any] = Field(
        default_factory=dict,
        description="Strategy swarm outputs - truth mining results"
    )
    creative_directions: Dict[str, Any] = Field(
        default_factory=dict,
        description="Creative swarm outputs - insight hunting results"
    )
    design_synthesis: Dict[str, Any] = Field(
        default_factory=dict,
        description="Design swarm outputs - visual weaving with gravity points"
    )
    technology_roadmap: Dict[str, Any] = Field(
        default_factory=dict,
        description="Technology swarm outputs - experience building with funnel physics"
    )
    
    # Gravity System Integration (v1 Framework)
    gravity_analysis: Dict[GravityType, float] = Field(
        default_factory=dict,
        description="Five gravity types scoring (0-1 scale)"
    )
    funnel_physics: Dict[str, Any] = Field(
        default_factory=dict,
        description="Friction, velocity, momentum analysis"
    )
    world_rules: Dict[str, str] = Field(
        default_factory=dict,
        description="Brand world physics and governing principles"
    )
    gravity_mechanics: Dict[str, str] = Field(
        default_factory=dict,
        description="Attraction, retention, amplification mechanics"
    )
    gravity_index: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Overall brand gravitational strength"
    )
    
    # Human Validation ("The Heart Knows")
    intuitive_validation: Dict[str, Any] = Field(
        default_factory=dict,
        description="Human intuition validation results"
    )
    emotional_resonance: Dict[str, float] = Field(
        default_factory=dict,
        description="Authenticity and emotional alignment scores"
    )
    premium_value_validation: Dict[str, Any] = Field(
        default_factory=dict,
        description="$50k value proposition validation"
    )
    
    # Vesica Pisces Breakthrough Discovery
    vesica_pisces_moments: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Truth + Insight intersection discoveries"
    )
    primary_breakthrough: Dict[str, Any] = Field(
        default_factory=dict,
        description="Selected primary breakthrough for implementation"
    )
    
    # Final Brand World Output
    brand_world: Dict[str, Any] = Field(
        default_factory=dict,
        description="Comprehensive brand world deliverable"
    )
    implementation_plan: Dict[str, Any] = Field(
        default_factory=dict,
        description="Tactical next steps and roadmap"
    )
    
    # Workflow Metadata
    participant_feedback: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Human feedback collected throughout workflow"
    )
    validation_checkpoints: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Human validation checkpoint results"
    )
    execution_metrics: Dict[str, Any] = Field(
        default_factory=dict,
        description="Performance and quality metrics"
    )
    
    class Config:
        """Pydantic configuration"""
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class BrandOperatorProfile(BaseModel):
    """Brand operator context model"""
    
    participant_id: str = Field(..., description="Unique participant identifier")
    role: str = Field(..., description="Founder, CEO, CMO, etc.")
    company_stage: str = Field(..., description="Startup, growth, mature, etc.")
    industry: str = Field(..., description="Industry sector")
    personal_investment: str = Field(..., description="Personal connection to brand")
    vision: str = Field(..., description="Personal vision for the brand")
    challenges: List[str] = Field(default_factory=list, description="Current brand challenges")
    success_metrics: List[str] = Field(default_factory=list, description="How they measure success")


class GravityCalculationResult(BaseModel):
    """Results from gravity analysis"""
    
    gravity_scores: Dict[GravityType, float] = Field(
        ...,
        description="Individual gravity type scores"
    )
    overall_index: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Combined gravity index"
    )
    strongest_gravity: GravityType = Field(
        ...,
        description="Highest performing gravity type"
    )
    weakest_gravity: GravityType = Field(
        ...,
        description="Lowest performing gravity type"
    )
    investment_priority: str = Field(
        ...,
        description="Recommended investment focus"
    )
    business_correlation: Dict[str, Any] = Field(
        default_factory=dict,
        description="Predicted business impact metrics"
    )


class VesicaPiscesDiscovery(BaseModel):
    """Vesica pisces breakthrough discovery"""
    
    truth_component: Dict[str, Any] = Field(
        ...,
        description="Strategic truth element"
    )
    insight_component: Dict[str, Any] = Field(
        ...,
        description="Target insight element"
    )
    intersection_potential: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Breakthrough potential score"
    )
    big_idea: str = Field(
        ...,
        description="Generated big idea from intersection"
    )
    implementation_path: Dict[str, Any] = Field(
        default_factory=dict,
        description="How to implement the big idea"
    )
    business_impact: Dict[str, Any] = Field(
        default_factory=dict,
        description="Predicted business outcomes"
    )


class HumanValidationResult(BaseModel):
    """Human validation checkpoint result"""
    
    checkpoint_type: str = Field(..., description="Type of validation")
    participant_id: str = Field(..., description="Validator identifier")
    feedback: Dict[str, Any] = Field(..., description="Human feedback")
    resonance_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Emotional resonance assessment"
    )
    decision: str = Field(..., description="proceed, refine, or reject")
    reasoning: str = Field(..., description="Human reasoning for decision")
    timestamp: datetime = Field(default_factory=datetime.now)