import cv2
import numpy as np
from Vectors import Vector3

class Camera:
    def __init__(self, starttranslation, startrotation):
        self.pos = Vector3(starttranslation.x, starttranslation.y, starttranslation.z)
        self.pitch = float(startrotation.x)
        self.yaw = float(startrotation.y)
        self.roll = float(startrotation.z)
        self.rotation_matrix = np.identity(3, dtype=np.float32)
        self.rvec = np.zeros(3, dtype=np.float32)
        self.tvec = np.zeros(3, dtype=np.float32)
        self._sync_rotation()
        self._sync_translation()

    def moveCamera(self, vec3):
        self.pos.x += vec3.x
        self.pos.y += vec3.y
        self.pos.z += vec3.z
        self._sync_translation()

    def rotateCamera(self, vec3):
        self.pitch = float(np.clip(self.pitch + vec3.x, -1.55, 1.55))
        self.yaw = float((self.yaw + vec3.y) % (2 * np.pi))
        self.roll = float((self.roll + vec3.z) % (2 * np.pi))
        self._sync_rotation()
        self._sync_translation()

    def _sync_rotation(self):
        cx = np.cos(self.pitch)
        sx = np.sin(self.pitch)
        cy = np.cos(self.yaw)
        sy = np.sin(self.yaw)
        cz = np.cos(self.roll)
        sz = np.sin(self.roll)

        pitch_matrix = np.array(
            [[1, 0, 0], [0, cx, -sx], [0, sx, cx]],
            dtype=np.float32,
        )
        yaw_matrix = np.array(
            [[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]],
            dtype=np.float32,
        )
        roll_matrix = np.array(
            [[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]],
            dtype=np.float32,
        )

        self.rotation_matrix = yaw_matrix @ pitch_matrix @ roll_matrix
        self.rvec = cv2.Rodrigues(self.rotation_matrix)[0].reshape(3).astype(np.float32)

    def _rotation_matrix(self):
        return self.rotation_matrix

    def _view_rotation_matrix(self):
        return self._rotation_matrix().T

    def _sync_translation(self):
        camera_position = np.array([self.pos.x, self.pos.y, self.pos.z], dtype=np.float32)
        self.tvec = (-self._view_rotation_matrix() @ camera_position).astype(np.float32)

    def world_to_camera(self, point):
        world_point = np.array([point.x, point.y, point.z], dtype=np.float32)
        camera_point = (self._view_rotation_matrix() @ world_point) + self.tvec
        return Vector3(float(camera_point[0]), float(camera_point[1]), float(camera_point[2]))

    def get_forward_vector(self):
        direction = self._rotation_matrix() @ np.array([0.0, 0.0, 1.0], dtype=np.float32)
        return Vector3(float(direction[0]), float(0), float(direction[2]))

    def get_right_vector(self):
        direction = self._rotation_matrix() @ np.array([1.0, 0.0, 0.0], dtype=np.float32)
        return Vector3(float(direction[0]), float(direction[1]), float(direction[2]))

    def get_up_vector(self):
        direction = self._rotation_matrix() @ np.array([0.0, 1.0, 0.0], dtype=np.float32)
        return Vector3(float(direction[0]), float(direction[1]), float(direction[2]))


camera = Camera(Vector3(0, 0, 0), Vector3(0, 0, 0))
