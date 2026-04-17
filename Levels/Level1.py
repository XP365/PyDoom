from ObjectManager import *
from TextureManager import textures

WallTex = textures.GetTexture("Wall")
ui_tex = textures.GetTexture("UI_Main")

create_wall((1, 1, 1), (7, 5, 0), WallTex, tile_u=0.2, tile_v=0.2)
create_wall((10, 0, 10), (5, 5, 10), WallTex, tile_u=0.2, tile_v=0.2)