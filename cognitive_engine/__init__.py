"""
Modular Cognitive Engine - A modular cognitive engine for distributed intelligent systems.
"""

__version__ = "1.0.0"
__author__ = "Cognitive Engine Contributors"
__license__ = "MIT"

from cognitive_engine.core.base import ModuleBase, Layer
from cognitive_engine.core.engine import Engine
from cognitive_engine.core.registry import ModuleRegistry

__all__ = [
    "ModuleBase",
    "Layer", 
    "Engine",
    "ModuleRegistry",
]
