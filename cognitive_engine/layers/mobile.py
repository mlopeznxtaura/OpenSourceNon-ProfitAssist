"""Mobile Layer - Mobility, navigation, and spatial awareness."""
from typing import Any, Dict, List, Optional
from world_engine.core.base import ModuleBase, Layer


class MobileLayer(ModuleBase):
    """Base mobile layer module for movement and navigation.
    
    The mobile layer handles:
    - Path planning and navigation
    - Spatial awareness
    - Movement control
    - Position tracking
    """
    
    name = "mobile_layer"
    layer = Layer.MOBILE
    version = "1.0.0"
    description = "Base mobile layer for movement and navigation"
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the mobile layer.
        
        Args:
            config: Optional configuration dictionary
        """
        super().__init__(config)
        self._position = {"x": 0.0, "y": 0.0, "z": 0.0}
        self._velocity = {"x": 0.0, "y": 0.0, "z": 0.0}
        self._path = []
        self._destination = None
        self._obstacles = []
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process mobility tasks.
        
        Args:
            data: Input data containing movement commands or queries
            
        Returns:
            Processed data with movement results
        """
        result = data.copy()
        
        # Handle different types of mobility operations
        if "move_to" in data:
            result["path"] = self._plan_path(data["move_to"])
        
        if "set_velocity" in data:
            self._velocity = data["set_velocity"]
            result["velocity_set"] = True
        
        if "get_position" in data:
            result["position"] = self.get_position()
        
        if "obstacle_detected" in data:
            self._add_obstacle(data["obstacle_detected"])
            result["obstacle_registered"] = True
        
        if "update_position" in data:
            self._update_position(data["update_position"])
            result["position_updated"] = True
        
        return result
    
    def _plan_path(self, destination: Dict[str, float]) -> List[Dict[str, float]]:
        """Plan a path to a destination.
        
        Args:
            destination: Target position coordinates
            
        Returns:
            List of waypoints representing the path
        """
        # Placeholder implementation
        # Override in subclasses for specific pathfinding logic
        self._destination = destination
        self._path = [
            self._position.copy(),
            destination.copy()
        ]
        return self._path
    
    def _add_obstacle(self, obstacle: Dict[str, Any]) -> None:
        """Add an obstacle to the obstacle list.
        
        Args:
            obstacle: Obstacle description with position and size
        """
        self._obstacles.append(obstacle)
    
    def _update_position(self, new_position: Dict[str, float]) -> None:
        """Update current position.
        
        Args:
            new_position: New position coordinates
        """
        self._position.update(new_position)
    
    def get_position(self) -> Dict[str, float]:
        """Get current position.
        
        Returns:
            Current position coordinates
        """
        return self._position.copy()
    
    def get_velocity(self) -> Dict[str, float]:
        """Get current velocity.
        
        Returns:
            Current velocity vector
        """
        return self._velocity.copy()
    
    def set_velocity(self, velocity: Dict[str, float]) -> None:
        """Set velocity vector.
        
        Args:
            velocity: Velocity vector
        """
        self._velocity = velocity
    
    def stop(self) -> None:
        """Stop all movement."""
        self._velocity = {"x": 0.0, "y": 0.0, "z": 0.0}
    
    def get_path(self) -> List[Dict[str, float]]:
        """Get current planned path.
        
        Returns:
            List of waypoints
        """
        return self._path.copy()
    
    def clear_path(self) -> None:
        """Clear the current path."""
        self._path.clear()
        self._destination = None
    
    def get_obstacles(self) -> List[Dict[str, Any]]:
        """Get list of known obstacles.
        
        Returns:
            List of obstacles
        """
        return self._obstacles.copy()
