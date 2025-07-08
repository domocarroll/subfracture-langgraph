"""
SUBFRACTURE LangGraph Configuration

Configuration management for LangGraph workflow and LangSmith integration
"""

import os
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LangGraphConfig(BaseModel):
    """LangGraph workflow configuration"""
    
    # LangGraph Settings
    workflow_name: str = Field(
        default="SUBFRACTURE-Brand-Intelligence-v2",
        description="Workflow identifier"
    )
    max_iterations: int = Field(
        default=50,
        description="Maximum workflow iterations"
    )
    checkpoint_storage: Optional[str] = Field(
        default=None,
        description="Checkpoint storage backend"
    )
    
    # Parallelization Settings
    max_concurrent_agents: int = Field(
        default=4,
        description="Maximum concurrent agent executions"
    )
    agent_timeout: int = Field(
        default=300,  # 5 minutes
        description="Agent execution timeout in seconds"
    )
    
    # Human-in-the-Loop Settings
    human_timeout: int = Field(
        default=1800,  # 30 minutes
        description="Human validation timeout in seconds"
    )
    require_human_validation: bool = Field(
        default=True,
        description="Require human validation checkpoints"
    )


class LangSmithConfig(BaseModel):
    """LangSmith observability configuration"""
    
    # LangSmith API Settings
    api_key: Optional[str] = Field(
        default_factory=lambda: os.getenv("LANGSMITH_API_KEY"),
        description="LangSmith API key"
    )
    endpoint: str = Field(
        default="https://api.smith.langchain.com",
        description="LangSmith API endpoint"
    )
    project_name: str = Field(
        default="subfracture-brand-intelligence",
        description="LangSmith project name"
    )
    
    # Tracing Settings
    trace_enabled: bool = Field(
        default=True,
        description="Enable LangSmith tracing"
    )
    trace_sample_rate: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Trace sampling rate"
    )
    
    # Evaluation Settings
    enable_evaluations: bool = Field(
        default=True,
        description="Enable automatic evaluations"
    )
    evaluation_criteria: List[str] = Field(
        default_factory=lambda: [
            "gravity_coherence",
            "human_resonance",
            "business_correlation",
            "premium_value_justification"
        ],
        description="Evaluation criteria for brand intelligence"
    )


class LLMConfig(BaseModel):
    """LLM provider configuration"""
    
    # Primary LLM (for main agents)
    primary_provider: str = Field(
        default="anthropic",
        description="Primary LLM provider"
    )
    primary_model: str = Field(
        default="claude-3-5-sonnet-20241022",
        description="Primary model name"
    )
    primary_api_key: Optional[str] = Field(
        default_factory=lambda: os.getenv("ANTHROPIC_API_KEY"),
        description="Primary LLM API key"
    )
    
    # Secondary LLM (for validation/evaluation)
    secondary_provider: str = Field(
        default="openai",
        description="Secondary LLM provider"
    )
    secondary_model: str = Field(
        default="gpt-4",
        description="Secondary model name"
    )
    secondary_api_key: Optional[str] = Field(
        default_factory=lambda: os.getenv("OPENAI_API_KEY"),
        description="Secondary LLM API key"
    )
    
    # Generation Settings
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Temperature for creative tasks"
    )
    max_tokens: int = Field(
        default=4000,
        description="Maximum tokens per generation"
    )


class GravityConfig(BaseModel):
    """Gravity system configuration"""
    
    # Gravity Calculation Settings
    gravity_weights: Dict[str, float] = Field(
        default_factory=lambda: {
            "recognition": 0.25,      # Visual impact
            "comprehension": 0.20,    # Message clarity
            "attraction": 0.20,       # Cultural relevance
            "amplification": 0.15,    # Partnership power
            "trust": 0.20            # Consistency
        },
        description="Gravity type weighting for overall index"
    )
    
    # Physics Analysis Settings
    friction_threshold: float = Field(
        default=0.3,
        description="Threshold for identifying friction points"
    )
    velocity_target: float = Field(
        default=0.7,
        description="Target velocity for user journeys"
    )
    momentum_decay_rate: float = Field(
        default=0.1,
        description="Rate of momentum decay without reinforcement"
    )
    
    # Business Correlation Settings
    enable_roi_predictions: bool = Field(
        default=True,
        description="Enable ROI predictions based on gravity"
    )
    baseline_conversion_rate: float = Field(
        default=0.02,
        description="Baseline conversion rate for predictions"
    )


class ValidationConfig(BaseModel):
    """Human validation configuration"""
    
    # Validation Requirements
    required_checkpoints: List[str] = Field(
        default_factory=lambda: [
            "strategy_creative_synthesis",
            "design_technology_integration", 
            "gravity_validation",
            "final_brand_world"
        ],
        description="Required human validation checkpoints"
    )
    
    # Validation Criteria
    minimum_resonance_score: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Minimum emotional resonance for approval"
    )
    
    # Premium Value Validation
    premium_value_threshold: float = Field(
        default=50000.0,
        description="Minimum value demonstration for premium positioning"
    )
    roi_prediction_confidence: float = Field(
        default=0.8,
        description="Required confidence level for ROI predictions"
    )


class SubfractureConfig(BaseModel):
    """Complete SUBFRACTURE configuration"""
    
    langgraph: LangGraphConfig = Field(default_factory=LangGraphConfig)
    langsmith: LangSmithConfig = Field(default_factory=LangSmithConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    gravity: GravityConfig = Field(default_factory=GravityConfig)
    validation: ValidationConfig = Field(default_factory=ValidationConfig)
    
    # Environment Settings
    environment: str = Field(
        default_factory=lambda: os.getenv("ENVIRONMENT", "development"),
        description="Runtime environment"
    )
    debug_mode: bool = Field(
        default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true",
        description="Enable debug mode"
    )
    log_level: str = Field(
        default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"),
        description="Logging level"
    )


# Global configuration instance
config = SubfractureConfig()


def get_config() -> SubfractureConfig:
    """Get global configuration instance"""
    return config


def update_config(**kwargs) -> SubfractureConfig:
    """Update configuration with new values"""
    global config
    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)
    return config