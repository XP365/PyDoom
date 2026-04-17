from collision import *


class PhysicsManager:
    def __init__(self):
        self.colliders = []
        self.response = Response()
        self.last_valid_pos = (0.0, 0.0)

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

    def CheckCollisions(self, playerPos, lastPos=None):
        """Check collisions and attempt to slide along walls.
        
        Args:
            playerPos: Current player position (x, z)
            lastPos: Previous player position for calculating movement direction
            
        Returns:
            (adjusted_position, has_collision)
        """
        playerColliderWidth = 0.5
        playerColliderHeight = 0.5

        x, z = playerPos
        playerCollider = Poly(Vector(0, 0), [
            Vector(x - playerColliderWidth / 2, z - playerColliderHeight / 2),
            Vector(x + playerColliderWidth / 2, z - playerColliderHeight / 2),
            Vector(x + playerColliderWidth / 2, z + playerColliderHeight / 2),
            Vector(x - playerColliderWidth / 2, z + playerColliderHeight / 2)
        ])

        self.response.reset()
        
        has_collision = False
        collision_normal = None
        
        # Check collisions
        for collider in self.colliders:
            if collide(playerCollider, collider, self.response):
                has_collision = True
                collision_normal = self.response.overlap_n
                break

        # If no collision, just return the current position
        if not has_collision:
            return tuple(playerPos), False
        
        # If we have collision but no lastPos, just reject the movement
        if lastPos is None:
            return tuple(lastPos) if lastPos else tuple(playerPos), True
        
        # Try to slide along the wall
        movement_x = playerPos[0] - lastPos[0]
        movement_z = playerPos[1] - lastPos[1]
        
        # Get the wall tangent (perpendicular to the normal)
        # If normal is (nx, nz), tangent is (-nz, nx) or (nz, -nx)
        if collision_normal:
            # Calculate tangent vector (perpendicular to normal)
            tangent_x = -collision_normal.y
            tangent_z = collision_normal.x
            
            # Project movement onto the tangent vector
            dot_product = movement_x * tangent_x + movement_z * tangent_z
            
            # Calculate the slide movement (movement projected onto tangent)
            slide_x = tangent_x * dot_product * 0.9  # 0.9 = slight friction/damping
            slide_z = tangent_z * dot_product * 0.9
            
            # Try the slide position
            slide_pos = (lastPos[0] + slide_x, lastPos[1] + slide_z)
            
            # Verify the slide position doesn't collide
            slide_collider = Poly(Vector(0, 0), [
                Vector(slide_pos[0] - playerColliderWidth / 2, slide_pos[1] - playerColliderHeight / 2),
                Vector(slide_pos[0] + playerColliderWidth / 2, slide_pos[1] - playerColliderHeight / 2),
                Vector(slide_pos[0] + playerColliderWidth / 2, slide_pos[1] + playerColliderHeight / 2),
                Vector(slide_pos[0] - playerColliderWidth / 2, slide_pos[1] + playerColliderHeight / 2)
            ])
            
            slide_has_collision = False
            for collider in self.colliders:
                self.response.reset()
                if collide(slide_collider, collider, self.response):
                    slide_has_collision = True
                    break
            
            # If slide position is safe, use it; otherwise stay at last position
            if not slide_has_collision:
                return slide_pos, True
            else:
                print(f"Slide blocked, staying at {lastPos}")
        
        return tuple(lastPos), True


# physics manager singleton used by the game
physicsManager = PhysicsManager()

if __name__ == "__main__":
    # Example/test code only runs when this module is executed directly

    is_colliding, res = physicsManager.CheckCollisions((7, 7))
    if is_colliding:
        print("Collision detected in standalone test.")
    else:
        print("Safe! No collision in standalone test.")
