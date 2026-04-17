#!/usr/bin/env python3
"""Check actual collider vertex order in the game"""

from PhysicsManager import physicsManager
from ObjectManager import create_wall

# Mock texture
class MockTexture:
    pass

mock_tex = MockTexture()

print("Creating walls...")
create_wall((0, 0, 0), (7, 5, 0), mock_tex)
create_wall((5, 0, 5), (5, 5, 10), mock_tex)

print(f"\nCollider 0 (should be wall at X: 0-7, Z: -0.25-0.25):")
c = physicsManager.colliders[0]
print(f"  {len(c.points)} points:")
for i, pt in enumerate(c.points):
    print(f"    {i}: ({pt.x}, {pt.y})")

print(f"\nCollider 1 (should be wall at X: 4.75-5.25, Z: 5-10):")
c = physicsManager.colliders[1]
print(f"  {len(c.points)} points:")
for i, pt in enumerate(c.points):
    print(f"    {i}: ({pt.x}, {pt.y})")
