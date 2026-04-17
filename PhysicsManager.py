from collision import *


class PhysicsManager:
    def __init__(self):
        self.colliders = []
        self.response = Response()
        self.last_valid_pos = (0.0, 0.0)

    def AddCollider(self, topleft, topright, bottomright, bottomleft):
        #Create a collider polygon from four corner points.
        pts = [topleft, topright, bottomright, bottomleft]
        try:
            polygon = Poly(Vector(0, 0), [Vector(float(p[0]), float(p[1])) for p in pts])
        except Exception as e:
            print(f"Error creating collider: {e}")
            return None
        
        self.colliders.append(polygon)
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
        
        for collider in self.colliders:
            if collide(playerCollider, collider, self.response):
                has_collision = True
                collision_normal = self.response.overlap_n
                break

        if not has_collision:
            return tuple(playerPos), False
        
        if lastPos is None:
            return tuple(playerPos), True
        
        # Calculate movement vector
        movement_x = playerPos[0] - lastPos[0]
        movement_z = playerPos[1] - lastPos[1]
        
        # Calculate tangent vector (perpendicular to wall normal)
        tangent_x = -collision_normal.y
        tangent_z = collision_normal.x
        
        # Project movement onto tangent
        dot_product = movement_x * tangent_x + movement_z * tangent_z
        slide_x = tangent_x * dot_product * 0.9
        slide_z = tangent_z * dot_product * 0.9
        slide_pos = (lastPos[0] + slide_x, lastPos[1] + slide_z)
        
        # Check if slide position is valid
        slide_collider = Poly(Vector(0, 0), [
            Vector(slide_pos[0] - playerColliderWidth / 2, slide_pos[1] - playerColliderHeight / 2),
            Vector(slide_pos[0] + playerColliderWidth / 2, slide_pos[1] - playerColliderHeight / 2),
            Vector(slide_pos[0] + playerColliderWidth / 2, slide_pos[1] + playerColliderHeight / 2),
            Vector(slide_pos[0] - playerColliderWidth / 2, slide_pos[1] + playerColliderHeight / 2)
        ])
        
        for collider in self.colliders:
            self.response.reset()
            if collide(slide_collider, collider, self.response):
                return tuple(lastPos), True
        
        return slide_pos, True


# physics manager singleton used by the game
physicsManager = PhysicsManager()
