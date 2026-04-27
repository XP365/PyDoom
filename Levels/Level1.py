from ObjectManager import *
from TextureManager import textures

WallTex = textures.GetTexture("Wall")
ui_tex = textures.GetTexture("UI_Main")

def CreateObjects():
    create_wall((0, 0, 0), (7, 5, 0), WallTex, tile_u=0.2, tile_v=0.2)
    create_wall((5, 0, 5), (5, 5, 10), WallTex, tile_u=0.2, tile_v=0.2)
    create_wall((0, 0, 5), (12, 5, 12), WallTex, tile_u=0.2, tile_v=0.2)


    # floors
    floor_width = 10
    create_floor((-floor_width, 0, -floor_width), (floor_width, 0, floor_width), WallTex, tile_u=0.2, tile_v=0.2)
