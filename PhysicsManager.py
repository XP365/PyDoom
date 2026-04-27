from collision import *
from OpenGL.GL import *
from glm import *
from numpy import atan2


class PhysicsManager:
    def __init__(self):
        self.colliders = []
        self.debug_colliders = []
        self.response = Response()
        self.last_valid_pos = (0.0, 0.0)
        self.debugManager = None  # Will be set by DebugManager for debug drawing

    def AddCollider(self, obj, topleft, topright, bottomright, bottomleft):
        #Create a collider polygon from four corner points.
        pts = [topleft, topright, bottomright, bottomleft]
        try:
            polygon = Poly(Vector(0, 0), [Vector(float(p[0]), float(p[1])) for p in pts])
        except Exception as e:
            print(f"Error creating collider: {e}")
            return None
        
        self.colliders.append((obj, polygon))
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
        
        for obj, collider in self.colliders:
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

        
        for obj, collider in self.colliders:
            self.response.reset()
            if collide(slide_collider, collider, self.response):
                return tuple(lastPos), True
        
        return slide_pos, True
    
    def Raycast(self, startPos : tuple, forwardVector : tuple):
        colliderWidth = 0.1
        colliderHeight = 0.1
        incfactor = 1

        x, z = startPos
        MAX_LOOPS = 20
        step_size = colliderHeight 
        total_distance = 0
        while total_distance < MAX_LOOPS:
            total_distance += step_size
            forward_x = forwardVector[0] * total_distance
            forward_z = forwardVector[1] * total_distance


            # 1. Define corners relative to local center (0,0)
            w2 = colliderWidth / 2
            h2 = colliderHeight / 2
            corners = [
                Vector(-w2, -h2),
                Vector(w2, -h2),
                Vector(w2, h2),
                Vector(-w2, h2)
            ]

            # 2. Calculate center
            center_x = x + forward_x
            center_y = z + forward_z
            rotation_angle = atan2(forwardVector[1], forwardVector[0])
            cos_a = cos(rotation_angle)
            sin_a = sin(rotation_angle)

            # 3. Rotate and Translate
            rotated_corners = []
            for p in corners:
                # Rotate
                rx = p.x * cos_a - p.y * sin_a
                ry = p.x * sin_a + p.y * cos_a
                # Translate
                rotated_corners.append(Vector(rx + center_x, ry + center_y))

            # 4. Create Poly with new rotated points
            raycastCollider = Poly(Vector(0 - 1, 0 - 1), rotated_corners)


            self.debug_colliders.append(raycastCollider)


            for obj, collider in self.colliders:
                if collide(raycastCollider, collider, self.response):
                    print(f"Collision at position: {self.response.overlap_v} with normal: {self.response.overlap_n}")
                    return obj
            else:
                continue
            break
        return None



    


# physics manager singleton used by the game
physicsManager = PhysicsManager()
