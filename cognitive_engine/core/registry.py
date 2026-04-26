"""Module Registry - Manages module registration and discovery."""
from typing import Dict, List, Optional, Type
from world_engine.core.base import ModuleBase, Layer


class ModuleRegistry:
    """Central registry for all available modules.
    
    Provides functionality to register, discover, and instantiate modules
    across different layers of the engine.
    """
    
    _instance: Optional['ModuleRegistry'] = None
    _modules: Dict[str, Type[ModuleBase]]
    
    def __new__(cls) -> 'ModuleRegistry':
        """Singleton pattern implementation."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._modules = {}
        return cls._instance
    
    def register(self, module_class: Type[ModuleBase]) -> None:
        """Register a module class with the registry.
        
        Args:
            module_class: The module class to register
        """
        name = module_class.name
        if name in self._modules:
            raise ValueError(f"Module '{name}' is already registered")
        self._modules[name] = module_class
    
    def unregister(self, name: str) -> bool:
        """Unregister a module by name.
        
        Args:
            name: Name of the module to unregister
            
        Returns:
            True if module was unregistered, False if not found
        """
        if name in self._modules:
            del self._modules[name]
            return True
        return False
    
    def get(self, name: str) -> Optional[Type[ModuleBase]]:
        """Get a module class by name.
        
        Args:
            name: Name of the module
            
        Returns:
            Module class if found, None otherwise
        """
        return self._modules.get(name)
    
    def get_all(self) -> Dict[str, Type[ModuleBase]]:
        """Get all registered modules.
        
        Returns:
            Dictionary of all registered modules
        """
        return self._modules.copy()
    
    def get_by_layer(self, layer: Layer) -> Dict[str, Type[ModuleBase]]:
        """Get all modules for a specific layer.
        
        Args:
            layer: The layer to filter by
            
        Returns:
            Dictionary of modules for the specified layer
        """
        if layer == Layer.ALL:
            return self._modules.copy()
        
        return {
            name: cls for name, cls in self._modules.items()
            if cls.layer == layer or cls.layer == Layer.ALL
        }
    
    def list_modules(self) -> List[str]:
        """List all registered module names.
        
        Returns:
            List of module names
        """
        return list(self._modules.keys())
    
    def is_registered(self, name: str) -> bool:
        """Check if a module is registered.
        
        Args:
            name: Name of the module
            
        Returns:
            True if module is registered, False otherwise
        """
        return name in self._modules
    
    def clear(self) -> None:
        """Clear all registered modules."""
        self._modules.clear()
    
    def create_instance(self, name: str, config: Optional[Dict] = None) -> Optional[ModuleBase]:
        """Create an instance of a registered module.
        
        Args:
            name: Name of the module to instantiate
            config: Optional configuration for the module
            
        Returns:
            Module instance if found, None otherwise
        """
        module_class = self.get(name)
        if module_class is None:
            return None
        return module_class(config=config)
