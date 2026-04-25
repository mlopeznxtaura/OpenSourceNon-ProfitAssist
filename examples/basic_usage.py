"""Example usage of World Engine."""

from world_engine import Engine, ModuleBase, Layer
from world_engine.layers import CognitiveLayer, MobileLayer, HostLayer


def basic_example():
    """Basic example of using World Engine."""
    print("=== Basic Example ===\n")
    
    # Create engine
    engine = Engine()
    
    # Add layer modules
    engine.add_module(CognitiveLayer())
    engine.add_module(HostLayer())
    
    # Initialize
    engine.initialize()
    
    # Process some data
    result = engine.process({
        "observe": {"temperature": 25, "humidity": 60},
        "query": "temperature"
    })
    
    print(f"Result: {result}")
    
    # Shutdown
    engine.shutdown()
    print("\n=== Example Complete ===\n")


def cognitive_example():
    """Example using cognitive layer."""
    print("=== Cognitive Example ===\n")
    
    engine = Engine()
    cognitive = CognitiveLayer()
    
    engine.add_module(cognitive)
    engine.initialize()
    
    # Add a goal
    cognitive.add_goal("Navigate to location A")
    
    # Process goal
    result = engine.process({
        "goal": "Find optimal path"
    })
    
    print(f"Plan: {result.get('plan')}")
    
    # Query knowledge
    cognitive._update_knowledge({"location_a": "north", "location_b": "south"})
    result = engine.process({
        "query": "location_a"
    })
    
    print(f"Knowledge query result: {result.get('answer')}")
    
    engine.shutdown()
    print("\n=== Example Complete ===\n")


def mobile_example():
    """Example using mobile layer."""
    print("=== Mobile Example ===\n")
    
    engine = Engine()
    mobile = MobileLayer()
    
    engine.add_module(mobile)
    engine.initialize()
    
    # Plan a path
    result = engine.process({
        "move_to": {"x": 10.0, "y": 20.0, "z": 0.0}
    })
    
    print(f"Path: {result.get('path')}")
    
    # Get position
    result = engine.process({
        "get_position": True
    })
    
    print(f"Position: {result.get('position')}")
    
    engine.shutdown()
    print("\n=== Example Complete ===\n")


def host_example():
    """Example using host layer."""
    print("=== Host Example ===\n")
    
    engine = Engine()
    host = HostLayer()
    
    engine.add_module(host)
    engine.initialize()
    
    # Get system info
    result = engine.process({
        "get_system_info": True
    })
    
    print(f"System Info: {result.get('system_info')}")
    
    # Environment variable
    engine.process({
        "env_set": {"key": "MY_VAR", "value": "test_value"}
    })
    
    result = engine.process({
        "env_get": "MY_VAR"
    })
    
    print(f"Environment Variable: {result.get('env_value')}")
    
    engine.shutdown()
    print("\n=== Example Complete ===\n")


def custom_module_example():
    """Example creating a custom module."""
    print("=== Custom Module Example ===\n")
    
    from typing import Any, Dict
    
    class CustomModule(ModuleBase):
        name = "custom_processor"
        layer = Layer.COGNITIVE
        version = "1.0.0"
        description = "A custom processing module"
        
        def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
            result = data.copy()
            result["custom_processed"] = True
            result["timestamp"] = "2024-01-01"
            return result
    
    engine = Engine()
    engine.add_module(CustomModule())
    engine.initialize()
    
    result = engine.process({"input": "test_data"})
    
    print(f"Custom Result: {result}")
    
    engine.shutdown()
    print("\n=== Example Complete ===\n")


if __name__ == "__main__":
    basic_example()
    cognitive_example()
    mobile_example()
    host_example()
    custom_module_example()
    
    print("All examples completed successfully!")
