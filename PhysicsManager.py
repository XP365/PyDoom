from collision import *


class PhysicsManager:
    def __init__(self):
        self.colliders = []
        self.response = Response()

    def AddCollider(self, topleft, topright, bottomright, bottomleft):
        """Create a collider polygon directly from the four provided points without sanitization.
        Caller is responsible for passing correct X,Z pairs and valid polygons.
        """
        pts = [topleft, topright, bottomright, bottomleft]

        # Attempt to construct Poly; catch library errors to avoid crashing
        try:
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

        # Note: Vector(playerPos[0], playerPos[1]) sets the CENTER/START point
        playerCollider = Poly(Vector(playerPos[0], playerPos[1]), [
            Vector(0, 0),
            Vector(0, playerColliderHeight),
            Vector(playerColliderWidth, playerColliderHeight),
            Vector(playerColliderWidth, 0)
        ])

        self.response.reset()

        for collider in self.colliders:

            if collide(playerCollider, collider, self.response):
                # Print inside the loop so you see the result

                print(f"Collision at {playerPos}! Overlap: {self.response.overlap}")
                return True, self.response

        return False, None


# physics manager singleton used by the game
physicsManager = PhysicsManager()

if __name__ == "__main__":
    # Example/test code only runs when this module is executed directly

    is_colliding, res = physicsManager.CheckCollisions((7, 7))
    if is_colliding:
        print("Collision detected in standalone test.")
    else:
        print("Safe! No collision in standalone test.")
