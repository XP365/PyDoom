from dataclasses import dataclass



class Wall:
    def __init__(
        self,
        top_left,
        bottom_right,
        texture,
        uv_mode: str = "tile",   # "stretch" or "tile"
        tile_u: float = 5.0,     # repeats per world unit (U)
        tile_v: float = 5.0,     # repeats per world unit (V)
        u_offset: float = 0.0,
        v_offset: float = 0.0,
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


def create_wall(
    pos,
    inverse_pos,
    texture,
    uv_mode: str = "tile",
    tile_u: float = 5.0,
    tile_v: float = 5.0,
    u_offset: float = 0.0,
    v_offset: float = 0.0,
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
    )

    return objectManager.addObject(wall)

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
