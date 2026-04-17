#!/usr/bin/env python3
"""Test collision library directly to understand its behavior"""

from collision import Poly, Vector

# Test 1: Create a simple polygon with absolute position and relative vertices
print("Test 1: Poly at (0, 0) with relative vertices")
p1 = Poly(Vector(0, 0), [Vector(0, 0), Vector(5, 0), Vector(5, 5), Vector(0, 5)])
print(f"  Position: ({p1.pos.x}, {p1.pos.y})")
print(f"  Points:")
for i, pt in enumerate(p1.points):
    print(f"    {i}: ({pt.x}, {pt.y})")

# Test 2: Create same polygon but at different position
print("\nTest 2: Poly at (3, 3) with same relative vertices")
p2 = Poly(Vector(3, 3), [Vector(0, 0), Vector(5, 0), Vector(5, 5), Vector(0, 5)])
print(f"  Position: ({p2.pos.x}, {p2.pos.y})")
print(f"  Points:")
for i, pt in enumerate(p2.points):
    print(f"    {i}: ({pt.x}, {pt.y})")

# Test 3: Create polygon with pre-offset vertices (what we might be doing wrong)
print("\nTest 3: Poly at (3, 3) with pre-offset vertices (0-based)")
p3 = Poly(Vector(3, 3), [Vector(0, 0), Vector(5, 0), Vector(5, 5), Vector(0, 5)])
print(f"  Position: ({p3.pos.x}, {p3.pos.y})")
print(f"  Points:")
for i, pt in enumerate(p3.points):
    print(f"    {i}: ({pt.x}, {pt.y})")

# Test 4: What happens if position and vertices don't align
print("\nTest 4: Poly at (3, 3) with vertices starting at absolute (3, 3)")
p4 = Poly(Vector(3, 3), [Vector(3, 3), Vector(8, 3), Vector(8, 8), Vector(3, 8)])
print(f"  Position: ({p4.pos.x}, {p4.pos.y})")
print(f"  Points:")
for i, pt in enumerate(p4.points):
    print(f"    {i}: ({pt.x}, {pt.y})")

print("\n" + "="*60)
print("CONCLUSION: Do points include the position offset or not?")
print("="*60)
print(f"Test 1 point 2: ({p1.points[2].x}, {p1.points[2].y})")
print(f"Test 3 point 2: ({p3.points[2].x}, {p3.points[2].y})")
print("If these are the same, points are stored as-is (not adjusted)")
print("If they differ, the library adjusts them somehow")
