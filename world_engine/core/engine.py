"""Main Engine Class - Orchestrates all modules and layers."""
import logging
from typing import Any, Dict, List, Optional
from world_engine.core.base import ModuleBase, Layer
from world_engine.core.registry import ModuleRegistry


logger = logging.getLogger(__name__)


class Engine:
    """Main engine class that orchestrates all modules and layers.
    
    The Engine is responsible for:
    - Managing module lifecycle (initialization, execution, shutdown)
    - Processing data through the module pipeline
    - Coordinating between different layers
    - Providing a unified interface for users
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the engine with optional configuration.
        
        Args:
            config: Optional dictionary containing engine configuration
        """
        self.config = config or {}
        self._modules: List[ModuleBase] = []
        self._registry = ModuleRegistry()
        self._running = False
        self._initialized = False
        
        logger.info("Engine initialized with config: %s", self.config)
    
    def add_module(self, module: ModuleBase) -> 'Engine':
        """Add a module to the engine.
        
        Args:
            module: Module instance to add
            
        Returns:
            Self for method chaining
        """
        self._modules.append(module)
        logger.info("Added module: %s (layer: %s)", module.name, module.layer.value)
        return self
    
    def remove_module(self, name: str) -> bool:
        """Remove a module by name.
        
        Args:
            name: Name of the module to remove
            
        Returns:
            True if module was removed, False if not found
        """
        for i, module in enumerate(self._modules):
            if module.name == name:
                removed = self._modules.pop(i)
                removed.shutdown()
                logger.info("Removed module: %s", name)
                return True
        logger.warning("Module not found: %s", name)
        return False
    
    def get_module(self, name: str) -> Optional[ModuleBase]:
        """Get a module by name.
        
        Args:
            name: Name of the module
            
        Returns:
            Module instance if found, None otherwise
        """
        for module in self._modules:
            if module.name == name:
                return module
        return None
    
    def list_modules(self) -> List[Dict[str, Any]]:
        """List all loaded modules with their metadata.
        
        Returns:
            List of module metadata dictionaries
        """
        return [module.get_metadata() for module in self._modules]
    
    def initialize(self) -> bool:
        """Initialize all modules in the engine.
        
        Returns:
            True if all modules initialized successfully, False otherwise
        """
        logger.info("Initializing engine...")
        
        success = True
        for module in self._modules:
            try:
                if not module.initialize():
                    logger.error("Failed to initialize module: %s", module.name)
                    success = False
            except Exception as e:
                logger.error("Error initializing module %s: %s", module.name, str(e))
                success = False
        
        if success:
            self._initialized = True
            logger.info("Engine initialized successfully")
        else:
            logger.warning("Engine initialized with errors")
        
        return success
    
    def shutdown(self) -> None:
        """Shutdown all modules and clean up resources."""
        logger.info("Shutting down engine...")
        
        for module in reversed(self._modules):
            try:
                module.shutdown()
                logger.info("Shutdown module: %s", module.name)
            except Exception as e:
                logger.error("Error shutting down module %s: %s", module.name, str(e))
        
        self._modules.clear()
        self._running = False
        self._initialized = False
        logger.info("Engine shutdown complete")
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data through all modules.
        
        Args:
            data: Input data dictionary
            
        Returns:
            Processed data dictionary
        """
        if not self._initialized:
            logger.warning("Engine not initialized, initializing now...")
            self.initialize()
        
        result = data.copy()
        
        for module in self._modules:
            if not module.is_initialized:
                logger.warning("Module %s not initialized, skipping...", module.name)
                continue
            
            try:
                logger.debug("Processing with module: %s", module.name)
                result = module.process(result)
            except Exception as e:
                logger.error("Error in module %s: %s", module.name, str(e))
                # Continue processing with other modules
        
        return result
    
    def run(self) -> None:
        """Run the engine in continuous mode.
        
        This method blocks until stop() is called.
        """
        if not self._initialized:
            self.initialize()
        
        self._running = True
        logger.info("Engine running...")
        
        # Default run loop - can be overridden by subclasses
        while self._running:
            # Placeholder for continuous processing
            pass
    
    def stop(self) -> None:
        """Stop the engine's run loop."""
        self._running = False
        logger.info("Engine stop requested")
    
    @property
    def is_running(self) -> bool:
        """Check if engine is running."""
        return self._running
    
    @property
    def is_initialized(self) -> bool:
        """Check if engine is initialized."""
        return self._initialized
    
    def get_status(self) -> Dict[str, Any]:
        """Get current engine status.
        
        Returns:
            Dictionary containing engine status information
        """
        return {
            "running": self._running,
            "initialized": self._initialized,
            "module_count": len(self._modules),
            "modules": self.list_modules()
        }
