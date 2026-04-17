#!/usr/bin/env python3
"""Test collision detection with fixed player collider"""

from PhysicsManager import physicsManager
from ObjectManager import create_wall
from Camera import camera

# Mock texture  
class MockTexture:
    pass

# Create a wall
wall = create_wall((0, 0, 0), (7, 5, 0), MockTexture())

# Test collisions at different positions
test_positions = [
    (0, 0),    # Should collide with wall
    (-1, 0),   # Should NOT collide (before wall)
    (3, 0),    # Should collide (middle of wall)
    (7, 0),    # Edge of wall
    (8, 0),    # Beyond wall
    (0, -1),   # Below wall
    (0, 0.5),  # Within wall thickness
]

for pos in test_positions:
    is_colliding, response = physicsManager.CheckCollisions(pos)
    status = "COLLIDING" if is_colliding else "CLEAR"
    print(f"Position {pos}: {status}")
