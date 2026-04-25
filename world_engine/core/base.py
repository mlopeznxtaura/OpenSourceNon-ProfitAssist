"""Module Base Class - All modules inherit from this."""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from enum import Enum


class Layer(Enum):
    """Enumeration of engine layers."""
    COGNITIVE = "cognitive"
    MOBILE = "mobile"
    HOST = "host"
    ALL = "all"


class ModuleBase(ABC):
    """Abstract base class for all World Engine modules.
    
    All custom modules must inherit from this class and implement
    the required methods to integrate with the engine.
    """
    
    name: str = "base_module"
    layer: Layer = Layer.ALL
    version: str = "1.0.0"
    description: str = "Base module"

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the module with optional configuration.
        
        Args:
            config: Optional dictionary containing module configuration
        """
        self.config = config or {}
        self._initialized = False

    @abstractmethod
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data and return results.
        
        This method must be implemented by all subclasses.
        
        Args:
            data: Input data dictionary
            
        Returns:
            Processed data dictionary
        """
        pass

    def initialize(self) -> bool:
        """Initialize module resources.
        
        Override this method to set up resources needed by the module.
        
        Returns:
            True if initialization successful, False otherwise
        """
        self._initialized = True
        return True

    def shutdown(self) -> None:
        """Shutdown module and cleanup resources.
        
        Override this method to clean up resources when the module stops.
        """
        self._initialized = False

    def get_metadata(self) -> Dict[str, Any]:
        """Get module metadata.
        
        Returns:
            Dictionary containing module name, layer, and version
        """
        return {
            "name": self.name,
            "layer": self.layer.value,
            "version": self.version,
            "description": self.description
        }

    @property
    def is_initialized(self) -> bool:
        """Check if module is initialized."""
        return self._initialized
