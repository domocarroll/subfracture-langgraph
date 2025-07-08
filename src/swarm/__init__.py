"""
SUBFRACTURE Swarm Coordination System

Dynamic multi-agent coordination using LangGraph Swarm for collaborative brand intelligence.
Enables agents to work together, hand off tasks, and optimize workflow efficiency.
"""

from .swarm_coordinator import SwarmCoordinator
from .agent_handoff import AgentHandoffManager
from .swarm_state import SwarmStateManager
from .coordination_strategies import (
    SequentialStrategy,
    ParallelStrategy,
    DynamicStrategy,
    CollaborativeStrategy
)

__all__ = [
    "SwarmCoordinator",
    "AgentHandoffManager", 
    "SwarmStateManager",
    "SequentialStrategy",
    "ParallelStrategy",
    "DynamicStrategy",
    "CollaborativeStrategy"
]