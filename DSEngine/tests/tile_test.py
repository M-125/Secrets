from DSEngine import *
from pygame import Vector2
from pygame.display import update
from os.path import exists

window = Window(fps=120, size=(1280, 720))
tilemap = TileMap(2, position=Vector2(0, 0), tile_size=Vector2(32, 32)) 
tile = Tile(tilemap, texture="Test.png")
image1 = Image2D(filename="Test.png", position=Vector2(150, 55))
image2 = Image2D(filename="Test1.png", position=Vector2(150, 55))
spritesheet1 = Spritesheet(image1, image1, image1, image1, image1, image2, image2, image2, image2, image2)
spritesheet2 = Spritesheet(image2, image1)
animationsheet = AnimationSheet(default=image1, normal=spritesheet1, back=spritesheet2)
sprite = AnimatedSprite2D(sheet=animationsheet, position=Vector2(500, 55), layer=2)
tilemap.init(window)
sprite.init(window)
tile_x = 0
tile_y = 0
saved = False
imported = False
while window.running:
    keys = window.frame()
    acc = Vector2(0.0, 0.0)
    acc.x = (keys[key_to_scancode("d")]-keys[key_to_scancode("a")])*window.delta
    acc.y = (keys[key_to_scancode("s")]-keys[key_to_scancode("w")])*window.delta
    sprite.move(acc)
    if exists("tilemap.sav"):
        #print("Exists")
        if not imported:
            tilemap.import_tilemap()
            imported = True
    else:
        if tile_y <= 10:
            tilemap.add_tile(1, "Test.png", Vector2(tile_x, tile_y))
            if tile_x >= 10:
                tile_x = 0
                tile_y += 1
            else:
                tile_x += 1
        else:
            if not saved:
                #d = tile.save_tile()
                #print(d)
                tilemap.save_tilemap()
                saved = True
    keys = window.frame()