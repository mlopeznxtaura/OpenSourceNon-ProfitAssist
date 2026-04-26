"""Test suite for Modular Cognitive Engine."""

import unittest
from cognitive_engine.core.base import ModuleBase, Layer
from cognitive_engine.core.engine import Engine
from cognitive_engine.core.registry import ModuleRegistry


class TestModuleBase(unittest.TestCase):
    """Tests for ModuleBase class."""
    
    def test_module_initialization(self):
        """Test module initialization."""
        module = DummyModule()
        self.assertFalse(module.is_initialized)
    
    def test_module_initialize(self):
        """Test module initialize method."""
        module = DummyModule()
        result = module.initialize()
        self.assertTrue(result)
        self.assertTrue(module.is_initialized)
    
    def test_module_shutdown(self):
        """Test module shutdown method."""
        module = DummyModule()
        module.initialize()
        module.shutdown()
        self.assertFalse(module.is_initialized)
    
    def test_module_metadata(self):
        """Test module metadata."""
        module = DummyModule()
        metadata = module.get_metadata()
        
        self.assertEqual(metadata["name"], "dummy_module")
        self.assertEqual(metadata["layer"], "cognitive")
        self.assertEqual(metadata["version"], "1.0.0")
    
    def test_module_with_config(self):
        """Test module with configuration."""
        config = {"key": "value"}
        module = DummyModule(config=config)
        self.assertEqual(module.config, config)


class TestEngine(unittest.TestCase):
    """Tests for Engine class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = Engine()
    
    def test_engine_initialization(self):
        """Test engine initialization."""
        self.assertFalse(self.engine.is_initialized)
        self.assertFalse(self.engine.is_running)
    
    def test_add_module(self):
        """Test adding modules."""
        module = DummyModule()
        self.engine.add_module(module)
        
        modules = self.engine.list_modules()
        self.assertEqual(len(modules), 1)
        self.assertEqual(modules[0]["name"], "dummy_module")
    
    def test_remove_module(self):
        """Test removing modules."""
        module = DummyModule()
        self.engine.add_module(module)
        
        result = self.engine.remove_module("dummy_module")
        self.assertTrue(result)
        
        modules = self.engine.list_modules()
        self.assertEqual(len(modules), 0)
    
    def test_process_data(self):
        """Test data processing."""
        module = DummyModule()
        self.engine.add_module(module)
        
        input_data = {"input": "test"}
        result = self.engine.process(input_data)
        
        self.assertIn("processed", result)
        self.assertTrue(result["processed"])
    
    def test_initialize_engine(self):
        """Test engine initialization."""
        module = DummyModule()
        self.engine.add_module(module)
        
        result = self.engine.initialize()
        self.assertTrue(result)
        self.assertTrue(self.engine.is_initialized)
    
    def test_shutdown_engine(self):
        """Test engine shutdown."""
        module = DummyModule()
        self.engine.add_module(module)
        self.engine.initialize()
        
        self.engine.shutdown()
        self.assertFalse(self.engine.is_initialized)
    
    def test_get_status(self):
        """Test getting engine status."""
        status = self.engine.get_status()
        
        self.assertIn("running", status)
        self.assertIn("initialized", status)
        self.assertIn("module_count", status)
        self.assertIn("modules", status)


class TestModuleRegistry(unittest.TestCase):
    """Tests for ModuleRegistry class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.registry = ModuleRegistry()
        self.registry.clear()
    
    def test_register_module(self):
        """Test registering a module."""
        self.registry.register(DummyModule)
        
        self.assertTrue(self.registry.is_registered("dummy_module"))
    
    def test_unregister_module(self):
        """Test unregistering a module."""
        self.registry.register(DummyModule)
        result = self.registry.unregister("dummy_module")
        
        self.assertTrue(result)
        self.assertFalse(self.registry.is_registered("dummy_module"))
    
    def test_get_module(self):
        """Test getting a module."""
        self.registry.register(DummyModule)
        
        module_class = self.registry.get("dummy_module")
        self.assertEqual(module_class, DummyModule)
    
    def test_create_instance(self):
        """Test creating module instance."""
        self.registry.register(DummyModule)
        
        instance = self.registry.create_instance("dummy_module")
        self.assertIsInstance(instance, DummyModule)
    
    def test_list_modules(self):
        """Test listing modules."""
        self.registry.register(DummyModule)
        
        modules = self.registry.list_modules()
        self.assertIn("dummy_module", modules)
    
    def test_get_by_layer(self):
        """Test getting modules by layer."""
        self.registry.register(DummyModule)
        
        modules = self.registry.get_by_layer(Layer.COGNITIVE)
        self.assertIn("dummy_module", modules)


class DummyModule(ModuleBase):
    """Dummy module for testing."""
    
    name = "dummy_module"
    layer = Layer.COGNITIVE
    version = "1.0.0"
    description = "Dummy module for testing"
    
    def process(self, data):
        """Process data."""
        result = data.copy()
        result["processed"] = True
        return result


if __name__ == "__main__":
    unittest.main()
