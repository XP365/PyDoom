#!/usr/bin/env python3
"""Test script to check if colliders are being created properly"""

from PhysicsManager import physicsManager
from ObjectManager import create_wall, objectManager

# Mock texture
class MockTexture:
    pass

mock_tex = MockTexture()

# Test adding colliders like the game does
print("[TEST] Adding first wall collider (0,0,0) to (7,5,0)...")
wall1 = create_wall((0, 0, 0), (7, 5, 0), mock_tex)
print(f"Created wall, collider count: {len(physicsManager.colliders)}")

print("\n[TEST] Adding second wall collider (5,0,5) to (5,5,10)...")
wall2 = create_wall((5, 0, 5), (5, 5, 10), mock_tex)
print(f"Created wall, collider count: {len(physicsManager.colliders)}")

print(f"\n[TEST] Total colliders: {len(physicsManager.colliders)}")

# Check collider structure
for i, collider in enumerate(physicsManager.colliders):
    print(f"\nCollider {i}:")
    print(f"  Position: ({collider.pos.x}, {collider.pos.y})")
    print(f"  Points: {len(collider.points)}")
    for j, pt in enumerate(collider.points):
        print(f"    Point {j}: ({pt.x}, {pt.y})")
