from collision import *


class PhysicsManager:
    def __init__(self):
        self.colliders = []
        self.response = Response()

    def AddCollider(self, topleft, topright, bottomright, bottomleft):
        """Create a collider polygon directly from the four provided points without sanitization.
        Caller is responsible for passing correct X,Z pairs and valid polygons.
        
        Points are in world coordinates. We pass them directly as vertices to the collision library.
        """
        pts = [topleft, topright, bottomright, bottomleft]

        # Attempt to construct Poly; catch library errors to avoid crashing
        try:
            # Create the polygon with position at (0,0) and world coordinates as vertices
            # The collision library will add position to vertices, so we use world coords directly
            polygon = Poly(Vector(0, 0), [Vector(float(p[0]), float(p[1])) for p in pts])
            
        except Exception as e:
            try:
                print(f"[PHYS ERROR] Failed to create Poly for points={pts}: {e}")
            except Exception:
                pass
            return None

        try:
            print(f"[PHYS DEBUG] Adding collider with points: {pts}")
        except Exception:
            pass
        self.colliders.append(polygon)
        try:
            print(f"[PHYS DEBUG] Collider count={len(self.colliders)}")
        except Exception:
            pass
        return polygon

    def CheckCollisions(self, playerPos):
        playerColliderWidth = 0.5
        playerColliderHeight = 0.5

        # Create player collider at position with relative vertices (0-based)
        # The collision library will store vertices with position added
        # So we need to pass (0,0) as position and absolute coords as vertices to match debug drawing
        x, z = playerPos
        playerCollider = Poly(Vector(0, 0), [
            Vector(x - playerColliderWidth / 2, z - playerColliderHeight / 2),
            Vector(x + playerColliderWidth / 2, z - playerColliderHeight / 2),
            Vector(x + playerColliderWidth / 2, z + playerColliderHeight / 2),
            Vector(x - playerColliderWidth / 2, z + playerColliderHeight / 2)
        ])

        self.response.reset()
        
        has_collision = False
        for collider in self.colliders:
            if collide(playerCollider, collider, self.response):
                has_collision = True
                print(f"Collision at {playerPos}!")
                break

        # Return the original position if colliding, otherwise return the position unchanged
        # This prevents the player from moving into walls
        return tuple(playerPos), has_collision


# physics manager singleton used by the game
physicsManager = PhysicsManager()

if __name__ == "__main__":
    # Example/test code only runs when this module is executed directly

    is_colliding, res = physicsManager.CheckCollisions((7, 7))
    if is_colliding:
        print("Collision detected in standalone test.")
    else:
        print("Safe! No collision in standalone test.")
