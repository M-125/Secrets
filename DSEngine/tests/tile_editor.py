import pygame
from pygame import Vector2
from DSEngine import TileMap, Window, Image2D
import sys

# Initialize pygame
pygame.init()

# Configuration
WINDOW_SIZE = (1920, 1080)  # Full HD
TILE_SIZE = Vector2(32, 32)
FPS = 60

# Initialize main objects
window = Window(size=WINDOW_SIZE, fps=FPS)
window.no_update = True
tilemap = TileMap(tile_size=TILE_SIZE)

# Load tile images (you need to replace these paths with actual image paths)
tile_images = {
    1: "Test.png",  # Tile 1
    2: "Test1.png",  # Tile 2
    3: "default.icon.png",  # Tile 3
    # Add more tiles if needed
}

# Default selected tile and layer
selected_tile = 1
selected_layer = 1

# Setup grid position tracking
mouse_position = Vector2(0, 0)

# Load, Save, Add Tile helper functions
def load_tilemap(filename="tilemap.sav"):
    tilemap.import_tilemap(filename)

def save_tilemap(filename="tilemap.sav"):
    tilemap.save_tilemap(filename)

def add_tile_at_mouse():
    pos = Vector2(mouse_position.x // TILE_SIZE.x, mouse_position.y // TILE_SIZE.y)
    tilemap.add_tile(layer=selected_layer, tile_texture=tile_images[selected_tile], position=pos)

# UI for tile and layer selection
def draw_tile_selection(window):
    padding = 10
    tile_size = Vector2(50, 50)
    x_offset = padding
    y_offset = WINDOW_SIZE[1] - tile_size.y - padding  # Align at the bottom

    # Draw each tile as a selectable icon
    for tile_id, image_path in tile_images.items():
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (int(tile_size.x), int(tile_size.y)))

        # Highlight the selected tile
        if tile_id == selected_tile:
            pygame.draw.rect(window.surface, (255, 255, 0), (x_offset - 5, y_offset - 5, tile_size.x + 10, tile_size.y + 10), 3)

        window.surface.blit(image, (x_offset, y_offset))
        x_offset += tile_size.x + padding

def handle_tile_selection(mouse_pos):
    padding = 10
    tile_size = Vector2(50, 50)
    x_offset = padding
    y_offset = WINDOW_SIZE[1] - tile_size.y - padding

    for tile_id in tile_images.keys():
        tile_rect = pygame.Rect(x_offset, y_offset, tile_size.x, tile_size.y)
        if tile_rect.collidepoint(mouse_pos):
            return tile_id
        x_offset += tile_size.x + padding
    return None

# Layer button UI
def draw_layer_buttons(window):
    button_width = 50
    button_height = 30
    padding = 10
    x_offset = padding
    y_offset = WINDOW_SIZE[1] - button_height - padding * 2 - 70  # Above tile selection

    for layer in range(1, 11):
        button_rect = pygame.Rect(x_offset, y_offset, button_width, button_height)
        color = (0, 255, 0) if layer == selected_layer else (200, 200, 200)
        
        pygame.draw.rect(window.surface, color, button_rect)
        font = pygame.font.SysFont(None, 24)
        label = font.render(str(layer), True, (0, 0, 0))
        label_rect = label.get_rect(center=button_rect.center)
        window.surface.blit(label, label_rect)

        x_offset += button_width + padding

def handle_layer_button_click(mouse_pos):
    button_width = 50
    button_height = 30
    padding = 10
    x_offset = padding
    y_offset = WINDOW_SIZE[1] - button_height - padding * 2 - 70  # Above tile selection

    for layer in range(1, 11):
        button_rect = pygame.Rect(x_offset, y_offset, button_width, button_height)
        if button_rect.collidepoint(mouse_pos):
            return layer
        x_offset += button_width + padding
    return None

# Modify TileMap class to include boundaries rendering
class CustomTileMap(TileMap):
    def render(self, window):
        super().render(window)
        for y in range(0, int(WINDOW_SIZE[1] / TILE_SIZE.y)):
            for x in range(0, int(WINDOW_SIZE[0] / TILE_SIZE.x)):
                tile_rect = pygame.Rect(x * TILE_SIZE.x, y * TILE_SIZE.y, TILE_SIZE.x, TILE_SIZE.y)
                pygame.draw.rect(window.surface, (255, 0, 0), tile_rect, 1)

# Use CustomTileMap class
tilemap = CustomTileMap(tile_size=TILE_SIZE)

# Main loop
while window.running:
    window.frame()
    keys = pygame.key.get_pressed()
    mouse_position = window.get_mouse_pos()

    if pygame.mouse.get_pressed()[0]:  # Left mouse button
        clicked_tile = handle_tile_selection(mouse_position)
        clicked_layer = handle_layer_button_click(mouse_position)
        
        if clicked_tile is not None:
            selected_tile = clicked_tile
        elif clicked_layer is not None:
            selected_layer = clicked_layer
        else:
            add_tile_at_mouse()

    if keys[pygame.K_s]:
        save_tilemap("tilemap.sav")
        print("Tilemap saved!")
    if keys[pygame.K_l]:
        load_tilemap("tilemap.sav")
        print("Tilemap loaded!")

    tilemap.render(window)
    draw_tile_selection(window)
    draw_layer_buttons(window)

    pygame.display.flip()
    window.clock.tick(FPS)

pygame.quit()
sys.exit()
