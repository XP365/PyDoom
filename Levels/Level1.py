from ObjectManager import *
from TextureManager import textures

RedWall = textures.GetTexture("Red_Wall")
WallTex = textures.GetTexture("Wall")
ui_tex = textures.GetTexture("UI_Main")

def CreateObjects():
    """create_wall((0, 0, 0), (7, 5, 0), WallTex, tile_u=0.2, tile_v=0.2)
    create_wall((5, 0, 5), (5, 5, 10), WallTex, tile_u=0.2, tile_v=0.2)"""
    create_wall((-20, 0, -20), (20, 5, -20), WallTex, tile_u=0.2, tile_v=0.2)
    create_wall((20, 0, -20), (20, 5, 20), WallTex, tile_u=0.2, tile_v=0.2)
    create_wall((20, 0, 20), (-20, 5, 20), WallTex, tile_u=0.2, tile_v=0.2)
    create_wall((-20, 0, 20), (-20, 5, -20), RedWall, tile_u=0.2, tile_v=0.2)
    create_wall((15, 0, 10), (15, 5, 15), ui_tex, tile_u=0.2, tile_v=0.2)
    create_wall((15, 0, 10), (10, 5, 10), ui_tex, tile_u=0.2, tile_v=0.2)
    create_wall((10, 0, 15), (10, 5, 10), ui_tex, tile_u=0.2, tile_v=0.2)
    create_wall((10, 0, 15), (5, 5, 15), ui_tex, tile_u=0.2, tile_v=0.2)
    create_wall((5, 0, 10), (5, 5, 15), ui_tex, tile_u=0.2, tile_v=0.2)





    
    # floors
    floor_width = 20
    create_floor((-floor_width, 0, -floor_width), (floor_width, 0, floor_width), WallTex, tile_u=0.2, tile_v=0.2)
