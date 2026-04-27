from dataclasses import dataclass

from PhysicsManager import physicsManager
import glm
from math import sqrt

def getXZfromTupple(tuple):
    return tuple[0], tuple[2]

class Wall:
    def __init__(
        self,
        top_left : tuple[float, float, float],
        bottom_right : tuple[float, float, float],
        texture,
        uv_mode: str = "tile",   # "stretch" or "tile"
        tile_u: float = 5.0,     # repeats per world unit (U)
        tile_v: float = 5.0,     # repeats per world unit (V)
        u_offset: float = 0.0,
        v_offset: float = 0.0,
        double_sided: bool = False,
    ):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.texture = texture
        self.uv_mode = uv_mode
        self.tile_u = tile_u
        self.tile_v = tile_v
        self.u_offset = u_offset
        self.v_offset = v_offset

        self.top_right = (bottom_right[0], top_left[1], top_left[2])
        self.bottom_left = (top_left[0], bottom_right[1], top_left[2])

class Floor:
    def __init__(
        self,
        corner_a,
        corner_b,
        texture,
        uv_mode: str = "tile",   # "stretch" or "tile"
        tile_u: float = 5.0,     # repeats per world unit (U)
        tile_v: float = 5.0,     # repeats per world unit (V)
        u_offset: float = 0.0,
        v_offset: float = 0.0,
    ):
        # Two opposite corners in XZ; Y is taken from corner_a.
        self.corner_a = corner_a
        self.corner_b = corner_b
        self.texture = texture
        self.uv_mode = uv_mode
        self.tile_u = tile_u
        self.tile_v = tile_v
        self.u_offset = u_offset
        self.v_offset = v_offset


def create_wall(
    pos,
    inverse_pos,
    texture,
    uv_mode: str = "tile",
    tile_u: float = 5.0,
    tile_v: float = 5.0,
    u_offset: float = 0.0,
    v_offset: float = 0.0,
    collider_thickness: float = 0.5,
    double_sided: bool = False,
) -> Wall:
    wall = Wall(
        pos,
        inverse_pos,
        texture,
        uv_mode=uv_mode,
        tile_u=tile_u,
        tile_v=tile_v,
        u_offset=u_offset,
        v_offset=v_offset,
        double_sided=double_sided,
    )

    upper_pos = wall.top_left[1]

    # Create physics collider from the wall's XZ footprint
    # The wall is defined by top_left (x1, y, z1) and bottom_right (x2, y, z2)
    # We create a collider with a thickness parameter
    x1 = wall.top_left[0]
    z1 = wall.top_left[2]
    x2 = wall.bottom_right[0]
    z2 = wall.bottom_right[2]
    
    # Ensure we have a valid rectangle
    if x1 == x2 and z1 == z2:
        # Point, not a wall - skip collider
        return objectManager.addObject(wall)
    
    if x1 == x2:
        # Vertical line in XZ (constant X) - extend in Z with thickness in X
        corner_tl = (x1 - collider_thickness/2, z1)
        corner_tr = (x1 + collider_thickness/2, z1)
        corner_br = (x1 + collider_thickness/2, z2)
        corner_bl = (x1 - collider_thickness/2, z2)
    elif z1 == z2:
        # Horizontal line in XZ (constant Z) - extend in X with thickness in Z
        corner_tl = (x1, z1 - collider_thickness/2)
        corner_tr = (x2, z1 - collider_thickness/2)
        corner_br = (x2, z1 + collider_thickness/2)
        corner_bl = (x1, z1 + collider_thickness/2)
    else:
        # Diagonal wall segment: build a constant-thickness oriented rectangle around the segment.
        # The old implementation used an axis-aligned box from (x1,z1) to (x2,z2), which "sticks out"
        # for angled walls and makes them feel wider than intended.
        dx = x2 - x1
        dz = z2 - z1
        seg_len = sqrt(dx * dx + dz * dz)
        if seg_len == 0:
            return objectManager.addObject(wall)

        half_t = abs(collider_thickness) / 2.0
        # Unit perpendicular (left normal) in XZ.
        px = -dz / seg_len
        pz = dx / seg_len

        corner_tl = (x1 + px * half_t, z1 + pz * half_t)
        corner_tr = (x2 + px * half_t, z2 + pz * half_t)
        corner_br = (x2 - px * half_t, z2 - pz * half_t)
        corner_bl = (x1 - px * half_t, z1 - pz * half_t)
    
    physicsManager.AddCollider(wall, corner_tl, corner_tr, corner_br, corner_bl)
    return objectManager.addObject(wall)

def create_floor(
    pos,
    inverse_pos,
    texture,
    uv_mode: str = "tile",
    tile_u: float = 5.0,
    tile_v: float = 5.0,
    u_offset: float = 0.0,
    v_offset: float = 0.0,
) -> Floor:
    floor = Floor(
        pos,
        inverse_pos,
        texture,
        uv_mode=uv_mode,
        tile_u=tile_u,
        tile_v=tile_v,
        u_offset=u_offset,
        v_offset=v_offset,
    )
    return objectManager.addObject(floor)

def create_ui_rect(
    pos,
    inverse_pos,
    texture,
    uv_mode: str = "stretch", tile_u: float = 1.0, tile_v: float = 1.0, u_offset: float = 0.0, v_offset: float = 0.0) -> Wall:
    wall = Wall(
        pos,
        inverse_pos,
        texture,
        uv_mode=uv_mode,
        tile_u=tile_u,
        tile_v=tile_v,
        u_offset=u_offset,
        v_offset=v_offset,
    )

    return objectManager.addUiObject(wall)


class ObjectManager:
    def __init__(self):
        self.objects = []
        self.uiObjects = []
        self.camFacingObjects = []

    def addObject(self, obj):
        self.objects.append(obj)
        return obj

    def removeObject(self, obj):
        self.objects.remove(obj)


    def addUiObject(self, obj):
        self.uiObjects.append(obj)
        return obj

    def removeUiObject(self, obj):
        self.uiObjects.remove(obj)


objectManager = ObjectManager()
