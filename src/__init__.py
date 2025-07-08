"""
SUBFRACTURE LangGraph Platform Package
Core brand intelligence and strategic positioning system
"""

__version__ = "1.0.0"
__author__ = "SUBFRACTURE"

# Essential imports for package functionality
from .core.state import SubfractureGravityState
from .core.config import SubfractureConfig

__all__ = [
    "SubfractureGravityState",
    "SubfractureConfig",
]