


class Camera:
    def __init__(self):
        CAMERA_OFFSET = (-2,-2,-2)
        self.x = CAMERA_OFFSET[0]
        self.y = CAMERA_OFFSET[1]
        self.z = CAMERA_OFFSET[2]

        self.rotationX = 0.0
        self.rotationY = 0.0
        self.rotationZ = 0.0

        self.forward_vector = (0,0)
        self.camera_pos_2d = (0,0)


camera = Camera()