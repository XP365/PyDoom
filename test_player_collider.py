#!/usr/bin/env python3
"""Test to verify player collider position matches between physics and debug"""

from Camera import camera
from collision import Poly, Vector

# Simulate player at camera position
test_pos = (camera.x, camera.z)
print(f"Camera position: x={camera.x}, z={camera.z}")
print(f"Player position for collision: {test_pos}")

# Check what the collision library does
playerColliderWidth = 0.5
playerColliderHeight = 0.5

# NEW: position at (0,0) with absolute world coordinates as vertices
x, z = test_pos
playerCollider = Poly(Vector(0, 0), [
    Vector(x, z),
    Vector(x, z + playerColliderHeight),
    Vector(x + playerColliderWidth, z + playerColliderHeight),
    Vector(x + playerColliderWidth, z)
])

print(f"\nPlayer collider (physics - new method):")
print(f"  Position: ({playerCollider.pos.x}, {playerCollider.pos.y})")
print(f"  Points (world coordinates after library adds position):")
for i, pt in enumerate(playerCollider.points):
    print(f"    {i}: ({pt.x}, {pt.y})")

print(f"\nExpected debug drawing:")
print(f"  Corner 0: ({x}, {z})")
print(f"  Corner 1: ({x}, {z + playerColliderHeight})")
print(f"  Corner 2: ({x + playerColliderWidth}, {z + playerColliderHeight})")
print(f"  Corner 3: ({x + playerColliderWidth}, {z})")

print(f"\nFirst point match: ({playerCollider.points[0].x}, {playerCollider.points[0].y}) vs ({x}, {z})")
print(f"Match: {abs(playerCollider.points[0].x - x) < 0.01 and abs(playerCollider.points[0].y - z) < 0.01}")
