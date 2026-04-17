#!/usr/bin/env python3
"""Debug script to compare physics collider positions with expected positions"""

from PhysicsManager import physicsManager
from ObjectManager import create_wall, objectManager

# Mock texture
class MockTexture:
    pass

mock_tex = MockTexture()

print("=" * 60)
print("WALL 1: (0, 0, 0) to (7, 5, 0)")
print("=" * 60)
wall1 = create_wall((0, 0, 0), (7, 5, 0), mock_tex)

print("\nWall 1 Details:")
print(f"  top_left: {wall1.top_left}")
print(f"  bottom_right: {wall1.bottom_right}")

if len(physicsManager.colliders) > 0:
    c = physicsManager.colliders[0]
    print(f"\nCollider 0:")
    print(f"  Position: ({c.pos.x}, {c.pos.y})")
    print(f"  Points (relative to pos):")
    for i, pt in enumerate(c.points):
        print(f"    {i}: ({pt.x}, {pt.y}) -> World: ({c.pos.x + pt.x}, {c.pos.y + pt.y})")

print("\n" + "=" * 60)
print("WALL 2: (5, 0, 5) to (5, 5, 10)")
print("=" * 60)
wall2 = create_wall((5, 0, 5), (5, 5, 10), mock_tex)

print("\nWall 2 Details:")
print(f"  top_left: {wall2.top_left}")
print(f"  bottom_right: {wall2.bottom_right}")

if len(physicsManager.colliders) > 1:
    c = physicsManager.colliders[1]
    print(f"\nCollider 1:")
    print(f"  Position: ({c.pos.x}, {c.pos.y})")
    print(f"  Points (relative to pos):")
    for i, pt in enumerate(c.points):
        print(f"    {i}: ({pt.x}, {pt.y}) -> World: ({c.pos.x + pt.x}, {c.pos.y + pt.y})")

print("\n" + "=" * 60)
print("EXPECTED vs ACTUAL")
print("=" * 60)
print("\nWall 1 (0,0) to (7,0) in XZ:")
print(f"  Expected corners:")
print(f"    TL: (0, 0)")
print(f"    TR: (7, 0)")
print(f"    BR: (7, 0.25)")  # After thickness applied
print(f"    BL: (0, 0.25)")
if len(physicsManager.colliders) > 0:
    c = physicsManager.colliders[0]
    print(f"  Actual (world coords):")
    for i, pt in enumerate(c.points):
        print(f"    {i}: ({c.pos.x + pt.x}, {c.pos.y + pt.y})")

print("\nWall 2 (5,5) to (5,10) in XZ:")
print(f"  Expected corners:")
print(f"    TL: (4.75, 5)")
print(f"    TR: (5.25, 5)")
print(f"    BR: (5.25, 10)")
print(f"    BL: (4.75, 10)")
if len(physicsManager.colliders) > 1:
    c = physicsManager.colliders[1]
    print(f"  Actual (world coords):")
    for i, pt in enumerate(c.points):
        print(f"    {i}: ({c.pos.x + pt.x}, {c.pos.y + pt.y})")
