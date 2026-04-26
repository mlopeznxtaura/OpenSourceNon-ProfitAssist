"""
Modular Engine - A modular engine for distributed intelligent systems.
"""

__version__ = "1.0.0"
__author__ = "Modular Engine Contributors"
__license__ = "MIT"

from modular_engine.core.base import ModuleBase, Layer
from modular_engine.core.engine import Engine
from modular_engine.core.registry import ModuleRegistry

__all__ = [
    "ModuleBase",
    "Layer", 
    "Engine",
    "ModuleRegistry",
]
