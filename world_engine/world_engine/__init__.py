"""
World Engine - Nonprofit Flywheel Dispatch System

A modular, open-source engine for classifying, compressing, and dispatching
nonprofit impact data across cognitive, mobile, and host compute layers.
"""

__version__ = "3.3.0"
__author__ = "World Engine Project"
__license__ = "MIT"

from .core.engine import WorldEngine
from .core.module_base import ModuleBase
from .core.pipeline import Pipeline, PipelineStep
from .core.manifest import Manifest, ManifestGenerator

__all__ = [
    "WorldEngine",
    "ModuleBase",
    "Pipeline",
    "PipelineStep",
    "Manifest",
    "ManifestGenerator",
]
