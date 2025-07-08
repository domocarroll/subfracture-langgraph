"""
SUBFRACTURE Enhanced Configuration

Extended configuration system for enhanced features including memory integration,
swarm coordination, and research intelligence capabilities.
"""

import os
from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel, Field, validator
from dotenv import load_dotenv

from .config import SubfractureConfig, LangGraphConfig, LangSmithConfig, LLMConfig

# Load environment variables
load_dotenv()


class LangMemConfig(BaseModel):
    """Configuration for LangMem integration"""
    
    # Core LangMem settings
    enabled: bool = Field(
        default_factory=lambda: os.getenv("LANGMEM_ENABLED", "true").lower() == "true",
        description="Enable LangMem memory integration"
    )
    
    namespace: str = Field(
        default="subfracture_brand_intelligence",
        description="LangMem namespace for brand memories"
    )
    
    storage_backend: str = Field(
        default_factory=lambda: os.getenv("LANGMEM_STORAGE_BACKEND", "in_memory"),
        description="LangMem storage backend (in_memory, redis, postgresql)"
    )
    
    embedding_model: str = Field(
        default_factory=lambda: os.getenv("LANGMEM_EMBEDDING_MODEL", "text-embedding-ada-002"),
        description="Embedding model for semantic search"
    )
    
    # Memory management settings
    memory_retention_days: int = Field(
        default=365,
        ge=1,
        description="Days to retain memories before cleanup"
    )
    
    max_memories_per_brand: int = Field(
        default=10000,
        ge=100,
        description="Maximum memories to store per brand"
    )
    
    semantic_search_limit: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Maximum results for semantic search"
    )
    
    # Performance settings
    batch_size: int = Field(
        default=100,
        ge=1,
        le=1000,
        description="Batch size for memory operations"
    )
    
    cache_enabled: bool = Field(
        default=True,
        description="Enable memory caching"
    )
    
    cache_ttl_seconds: int = Field(
        default=3600,  # 1 hour
        ge=60,
        description="Cache TTL in seconds"
    )
    
    # Integration settings
    auto_store_insights: bool = Field(
        default=True,
        description="Automatically store insights in memory"
    )
    
    auto_enrich_context: bool = Field(
        default=True,
        description="Automatically enrich context with relevant memories"
    )
    
    relevance_threshold: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Minimum relevance score for memory retrieval"
    )
    
    # Storage backend specific settings
    redis_config: Dict[str, Any] = Field(
        default_factory=lambda: {
            "host": os.getenv("REDIS_HOST", "localhost"),
            "port": int(os.getenv("REDIS_PORT", "6379")),
            "db": int(os.getenv("REDIS_DB", "0")),
            "password": os.getenv("REDIS_PASSWORD")
        },
        description="Redis configuration for LangMem"
    )
    
    postgresql_config: Dict[str, Any] = Field(
        default_factory=lambda: {
            "host": os.getenv("POSTGRES_HOST", "localhost"),
            "port": int(os.getenv("POSTGRES_PORT", "5432")),
            "database": os.getenv("POSTGRES_DB", "langmem"),
            "username": os.getenv("POSTGRES_USER", "langmem"),
            "password": os.getenv("POSTGRES_PASSWORD")
        },
        description="PostgreSQL configuration for LangMem"
    )


class SwarmConfig(BaseModel):
    """Configuration for LangGraph Swarm coordination"""
    
    # Core swarm settings
    enabled: bool = Field(
        default_factory=lambda: os.getenv("SWARM_ENABLED", "false").lower() == "true",
        description="Enable swarm coordination"
    )
    
    coordination_mode: str = Field(
        default="sequential",
        description="Default coordination mode (sequential, parallel, dynamic, collaborative)"
    )
    
    max_concurrent_agents: int = Field(
        default=4,
        ge=1,
        le=20,
        description="Maximum concurrent agents"
    )
    
    # Agent management
    agent_timeout_seconds: int = Field(
        default=300,  # 5 minutes
        ge=30,
        description="Timeout for individual agent tasks"
    )
    
    handoff_timeout_seconds: int = Field(
        default=60,
        ge=10,
        description="Timeout for agent handoffs"
    )
    
    max_handoff_attempts: int = Field(
        default=3,
        ge=1,
        description="Maximum handoff attempts before failure"
    )
    
    # Coordination intelligence
    auto_optimize_coordination: bool = Field(
        default=True,
        description="Automatically optimize coordination patterns"
    )
    
    learn_handoff_patterns: bool = Field(
        default=True,
        description="Learn optimal handoff patterns"
    )
    
    parallel_when_possible: bool = Field(
        default=True,
        description="Use parallel execution when tasks are independent"
    )
    
    # Performance monitoring
    track_agent_performance: bool = Field(
        default=True,
        description="Track individual agent performance"
    )
    
    efficiency_threshold: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="Minimum efficiency threshold for coordination"
    )
    
    # Swarm-specific agent configurations
    agent_configs: Dict[str, Dict[str, Any]] = Field(
        default_factory=lambda: {
            "strategy_swarm": {
                "max_parallel_tasks": 2,
                "memory_enabled": True,
                "research_integration": True
            },
            "creative_swarm": {
                "max_parallel_tasks": 3,
                "memory_enabled": True,
                "research_integration": True
            },
            "design_swarm": {
                "max_parallel_tasks": 2,
                "memory_enabled": True,
                "research_integration": False
            },
            "technology_swarm": {
                "max_parallel_tasks": 2,
                "memory_enabled": True,
                "research_integration": True
            },
            "gravity_analyzer": {
                "max_parallel_tasks": 1,
                "memory_enabled": True,
                "research_integration": True
            }
        },
        description="Agent-specific configurations"
    )


class ResearchConfig(BaseModel):
    """Configuration for Open Deep Research integration"""
    
    # Core research settings
    enabled: bool = Field(
        default_factory=lambda: os.getenv("RESEARCH_ENABLED", "false").lower() == "true",
        description="Enable research intelligence"
    )
    
    intelligence_mode: str = Field(
        default="basic",
        description="Research intelligence mode (disabled, basic, enhanced, continuous)"
    )
    
    # Research sources
    web_search_enabled: bool = Field(
        default=True,
        description="Enable web search research"
    )
    
    academic_search_enabled: bool = Field(
        default=False,
        description="Enable academic paper search"
    )
    
    news_search_enabled: bool = Field(
        default=True,
        description="Enable news search"
    )
    
    social_media_monitoring: bool = Field(
        default=False,
        description="Enable social media monitoring"
    )
    
    # Search API configurations
    search_apis: Dict[str, Dict[str, Any]] = Field(
        default_factory=lambda: {
            "tavily": {
                "enabled": os.getenv("TAVILY_API_KEY") is not None,
                "api_key": os.getenv("TAVILY_API_KEY"),
                "max_results": 10
            },
            "perplexity": {
                "enabled": os.getenv("PERPLEXITY_API_KEY") is not None,
                "api_key": os.getenv("PERPLEXITY_API_KEY"),
                "model": "llama-3.1-sonar-small-128k-online"
            },
            "arxiv": {
                "enabled": True,
                "max_results": 5
            },
            "pubmed": {
                "enabled": False,
                "max_results": 5
            }
        },
        description="Search API configurations"
    )
    
    # Research scheduling
    continuous_research_interval_hours: int = Field(
        default=24,
        ge=1,
        le=168,  # 1 week
        description="Interval for continuous research updates"
    )
    
    competitive_monitoring_interval_hours: int = Field(
        default=12,
        ge=1,
        le=72,
        description="Interval for competitive monitoring"
    )
    
    trend_analysis_interval_hours: int = Field(
        default=48,
        ge=6,
        le=168,
        description="Interval for trend analysis"
    )
    
    # Research quality settings
    min_confidence_threshold: float = Field(
        default=0.6,
        ge=0.0,
        le=1.0,
        description="Minimum confidence for research insights"
    )
    
    max_insights_per_domain: int = Field(
        default=50,
        ge=5,
        le=200,
        description="Maximum insights to store per research domain"
    )
    
    insight_freshness_days: int = Field(
        default=30,
        ge=1,
        le=365,
        description="Days after which insights are considered stale"
    )
    
    # Research domains
    research_domains: List[str] = Field(
        default_factory=lambda: [
            "competitive_landscape",
            "market_trends",
            "industry_analysis",
            "customer_insights",
            "technology_developments",
            "brand_positioning",
            "marketing_strategies"
        ],
        description="Research domains to monitor"
    )
    
    # Integration settings
    auto_integrate_insights: bool = Field(
        default=True,
        description="Automatically integrate research insights into workflows"
    )
    
    research_context_enrichment: bool = Field(
        default=True,
        description="Enrich brand context with research insights"
    )
    
    competitive_alerting: bool = Field(
        default=True,
        description="Send alerts for significant competitive changes"
    )


class LivingBrandConfig(BaseModel):
    """Configuration for Living Brand World features"""
    
    # Core living brand settings
    enabled: bool = Field(
        default_factory=lambda: os.getenv("LIVING_BRAND_ENABLED", "false").lower() == "true",
        description="Enable living brand world features"
    )
    
    stewardship_mode: str = Field(
        default="basic",
        description="Stewardship mode (basic, enhanced, autonomous)"
    )
    
    # Autonomous optimization
    auto_gravity_optimization: bool = Field(
        default=True,
        description="Automatically optimize brand gravity"
    )
    
    breakthrough_hunting: bool = Field(
        default=True,
        description="Continuously hunt for breakthrough opportunities"
    )
    
    adaptive_positioning: bool = Field(
        default=False,
        description="Adapt positioning based on market changes"
    )
    
    # Monitoring and alerting
    gravity_monitoring_enabled: bool = Field(
        default=True,
        description="Monitor brand gravity changes"
    )
    
    competitive_alerting_enabled: bool = Field(
        default=True,
        description="Alert on competitive threats"
    )
    
    opportunity_detection_enabled: bool = Field(
        default=True,
        description="Detect market opportunities"
    )
    
    # Optimization settings
    optimization_frequency_hours: int = Field(
        default=168,  # Weekly
        ge=24,
        le=720,  # Monthly
        description="Frequency of optimization cycles"
    )
    
    min_optimization_impact: float = Field(
        default=0.05,
        ge=0.01,
        le=0.5,
        description="Minimum impact threshold for optimizations"
    )
    
    # Assistant settings
    max_concurrent_assistants: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Maximum concurrent brand assistants"
    )
    
    assistant_specialization: Dict[str, List[str]] = Field(
        default_factory=lambda: {
            "brand_archaeologist": ["memory_management", "pattern_detection", "history_tracking"],
            "gravity_physicist": ["optimization", "physics_analysis", "performance_monitoring"],
            "cultural_curator": ["market_positioning", "trend_analysis", "competitive_intelligence"],
            "experience_architect": ["user_journey", "touchpoint_optimization", "friction_analysis"],
            "breakthrough_hunter": ["vesica_pisces", "opportunity_detection", "innovation_tracking"]
        },
        description="Assistant specializations and capabilities"
    )


class EnhancedSubfractureConfig(SubfractureConfig):
    """
    Enhanced SUBFRACTURE configuration with living brand world capabilities
    
    Extends the base SubfractureConfig while maintaining full backward compatibility.
    New configuration sections are optional and have sensible defaults.
    """
    
    # Enhanced configuration sections
    langmem: LangMemConfig = Field(default_factory=LangMemConfig)
    swarm: SwarmConfig = Field(default_factory=SwarmConfig)
    research: ResearchConfig = Field(default_factory=ResearchConfig)
    living_brand: LivingBrandConfig = Field(default_factory=LivingBrandConfig)
    
    # Feature flags
    enhancement_features: Dict[str, bool] = Field(
        default_factory=lambda: {
            "memory_integration": os.getenv("MEMORY_INTEGRATION", "true").lower() == "true",
            "swarm_coordination": os.getenv("SWARM_COORDINATION", "false").lower() == "true",
            "research_intelligence": os.getenv("RESEARCH_INTELLIGENCE", "false").lower() == "true",
            "living_brand_world": os.getenv("LIVING_BRAND_WORLD", "false").lower() == "true"
        },
        description="Enhancement feature flags"
    )
    
    # Integration settings
    integration_settings: Dict[str, Any] = Field(
        default_factory=lambda: {
            "memory_service_timeout": 30,
            "swarm_coordination_timeout": 60,
            "research_service_timeout": 120,
            "max_retry_attempts": 3,
            "fallback_to_base_functionality": True,
            "graceful_degradation": True
        },
        description="Integration and reliability settings"
    )
    
    # Performance monitoring
    performance_monitoring: Dict[str, Any] = Field(
        default_factory=lambda: {
            "enabled": True,
            "metrics_collection_interval": 60,  # seconds
            "alert_thresholds": {
                "memory_retrieval_time": 5.0,  # seconds
                "swarm_coordination_efficiency": 0.7,
                "research_insight_quality": 0.6
            },
            "dashboard_enabled": False,
            "metrics_retention_days": 30
        },
        description="Performance monitoring configuration"
    )
    
    @validator('enhancement_features')
    def validate_feature_dependencies(cls, v):
        """Validate feature dependencies"""
        
        # Living brand world requires other features
        if v.get("living_brand_world", False):
            if not v.get("memory_integration", False):
                raise ValueError("Living brand world requires memory integration")
        
        # Swarm coordination benefits from memory integration
        if v.get("swarm_coordination", False) and not v.get("memory_integration", False):
            # Log warning but don't fail
            import logging
            logging.warning("Swarm coordination is more effective with memory integration enabled")
        
        return v
    
    def is_feature_enabled(self, feature_name: str) -> bool:
        """Check if enhancement feature is enabled"""
        return self.enhancement_features.get(feature_name, False)
    
    def enable_feature(self, feature_name: str):
        """Enable enhancement feature"""
        if feature_name in self.enhancement_features:
            self.enhancement_features[feature_name] = True
    
    def disable_feature(self, feature_name: str):
        """Disable enhancement feature"""
        if feature_name in self.enhancement_features:
            self.enhancement_features[feature_name] = False
    
    def get_feature_config(self, feature_name: str) -> Optional[BaseModel]:
        """Get configuration for specific feature"""
        
        config_map = {
            "memory_integration": self.langmem,
            "swarm_coordination": self.swarm,
            "research_intelligence": self.research,
            "living_brand_world": self.living_brand
        }
        
        return config_map.get(feature_name)
    
    def to_base_config(self) -> SubfractureConfig:
        """Convert to base SubfractureConfig for backward compatibility"""
        
        base_fields = {}
        for field_name, field_info in SubfractureConfig.__fields__.items():
            if hasattr(self, field_name):
                base_fields[field_name] = getattr(self, field_name)
        
        return SubfractureConfig(**base_fields)
    
    def get_enhanced_summary(self) -> Dict[str, Any]:
        """Get summary of enhanced configuration"""
        
        return {
            "enhancement_features": self.enhancement_features,
            "langmem_enabled": self.langmem.enabled,
            "swarm_enabled": self.swarm.enabled,
            "research_enabled": self.research.enabled,
            "living_brand_enabled": self.living_brand.enabled,
            "integration_settings": self.integration_settings,
            "performance_monitoring": self.performance_monitoring["enabled"]
        }


# Global enhanced configuration instance
enhanced_config = EnhancedSubfractureConfig()


def get_enhanced_config() -> EnhancedSubfractureConfig:
    """Get global enhanced configuration instance"""
    return enhanced_config


def update_enhanced_config(**kwargs) -> EnhancedSubfractureConfig:
    """Update enhanced configuration with new values"""
    global enhanced_config
    
    for key, value in kwargs.items():
        if hasattr(enhanced_config, key):
            setattr(enhanced_config, key, value)
    
    return enhanced_config


def create_development_config() -> EnhancedSubfractureConfig:
    """Create configuration optimized for development"""
    
    config = EnhancedSubfractureConfig()
    
    # Enable memory integration for development
    config.enable_feature("memory_integration")
    config.langmem.storage_backend = "in_memory"
    config.langmem.cache_enabled = True
    
    # Disable resource-intensive features by default
    config.disable_feature("swarm_coordination")
    config.disable_feature("research_intelligence")
    config.disable_feature("living_brand_world")
    
    # Development-friendly settings
    config.integration_settings.update({
        "fallback_to_base_functionality": True,
        "graceful_degradation": True,
        "max_retry_attempts": 1
    })
    
    config.performance_monitoring["enabled"] = True
    config.performance_monitoring["dashboard_enabled"] = True
    
    return config


def create_production_config() -> EnhancedSubfractureConfig:
    """Create configuration optimized for production"""
    
    config = EnhancedSubfractureConfig()
    
    # Enable all features for production (if API keys available)
    config.enable_feature("memory_integration")
    
    # Enable swarm coordination if configured
    if os.getenv("SWARM_ENABLED", "false").lower() == "true":
        config.enable_feature("swarm_coordination")
    
    # Enable research intelligence if API keys available
    if any(os.getenv(f"{provider.upper()}_API_KEY") for provider in ["TAVILY", "PERPLEXITY"]):
        config.enable_feature("research_intelligence")
    
    # Production storage backend
    if os.getenv("POSTGRES_HOST"):
        config.langmem.storage_backend = "postgresql"
    elif os.getenv("REDIS_HOST"):
        config.langmem.storage_backend = "redis"
    
    # Production settings
    config.langmem.memory_retention_days = 730  # 2 years
    config.langmem.max_memories_per_brand = 50000
    
    config.integration_settings.update({
        "memory_service_timeout": 60,
        "swarm_coordination_timeout": 120,
        "research_service_timeout": 300,
        "max_retry_attempts": 3
    })
    
    return config


def load_config_from_environment() -> EnhancedSubfractureConfig:
    """Load configuration from environment variables"""
    
    # Determine environment
    environment = os.getenv("ENVIRONMENT", "development").lower()
    
    if environment == "production":
        return create_production_config()
    else:
        return create_development_config()