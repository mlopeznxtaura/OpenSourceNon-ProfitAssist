"""
World Engine - A modular cognitive engine for distributed intelligent systems.
"""

__version__ = "1.0.0"
__author__ = "World Engine Contributors"
__license__ = "MIT"

from world_engine.core.base import ModuleBase, Layer
from world_engine.core.engine import Engine
from world_engine.core.registry import ModuleRegistry

__all__ = [
    "ModuleBase",
    "Layer", 
    "Engine",
    "ModuleRegistry",
]
