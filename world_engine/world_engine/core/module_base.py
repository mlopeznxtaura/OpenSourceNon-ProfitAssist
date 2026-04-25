"""Module Base Class - All modules inherit from this."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from enum import Enum

class Layer(Enum):
    COGNITIVE = "cognitive"
    MOBILE = "mobile"
    HOST = "host"
    ALL = "all"

class ModuleBase(ABC):
    name: str = "base_module"
    layer: Layer = Layer.ALL
    version: str = "1.0.0"
    description: str = "Base module"
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self._initialized = False
    
    @abstractmethod
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    def initialize(self) -> bool:
        self._initialized = True
        return True
    
    def shutdown(self) -> None:
        self._initialized = False
    
    def get_metadata(self) -> Dict[str, Any]:
        return {"name": self.name, "layer": self.layer.value, "version": self.version}
