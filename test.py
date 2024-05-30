import pygame
import json

# Initialize Pygame
pygame.init()

# Load JSON map data
with open('data/maps/beta_map.json') as f:
    map_data = json.load(f)

# Map and Tileset properties
map_width = map_data['width']
map_height = map_data['height']
tile_width = map_data['tilewidth']
tile_height = map_data['tileheight']
tileset = map_data['tilesets'][0]
#tileset_image_path = tileset['source']  # Assuming the path is relative to the current working directory
tileset_image = pygame.image.load('tileset.png')

# Create Pygame display
screen = pygame.display.set_mode((map_width * tile_width, map_height * tile_height))

# Load the player sprite
player_image = pygame.image.load('data/images/entities/player/idle/00.png')
player_rect = player_image.get_rect()

# Function to get a tile from the tileset
def get_tile_image(tile_id):
    columns = tileset['tilewidth'] // tile_width
    x = (tile_id - 1) % columns
    y = (tile_id - 1) // columns
    rect = pygame.Rect(x * tile_width, y * tile_height, tile_width, tile_height)
    image = pygame.Surface((tile_width, tile_height), pygame.SRCALPHA)
    image.blit(tileset_image, (0, 0), rect)
    return image

# Function to check collision
def check_collision(rect, collision_rects):
    for col_rect in collision_rects:
        if rect.colliderect(col_rect):
            return True
    return False

# Parse collision objects
collision_rects = []
for layer in map_data['layers']:
    if layer['type'] == 'objectgroup' and layer['name'] == 'Collision Layer':
        for obj in layer['objects']:
            col_rect = pygame.Rect(obj['x'], obj['y'], obj['width'], obj['height'])
            collision_rects.append(col_rect)

# Player settings
player_speed = 5
player_color = (0, 255, 0)
player_rect.topleft = (0, 0)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= player_speed
        if check_collision(player_rect, collision_rects):
            player_rect.x += player_speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += player_speed
        if check_collision(player_rect, collision_rects):
            player_rect.x -= player_speed
    if keys[pygame.K_UP]:
        player_rect.y -= player_speed
        if check_collision(player_rect, collision_rects):
            player_rect.y += player_speed
    if keys[pygame.K_DOWN]:
        player_rect.y += player_speed
        if check_collision(player_rect, collision_rects):
            player_rect.y -= player_speed

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the map
    for layer in map_data['layers']:
        if layer['type'] == 'tilelayer':
            data = layer['data']
            for y in range(map_height):
                for x in range(map_width):
                    tile_id = data[y * map_width + x]
                    if tile_id > 0:
                        tile_image = get_tile_image(tile_id)
                        screen.blit(tile_image, (x * tile_width, y * tile_height))

    # Draw collision rectangles (for debugging purposes)
    for rect in collision_rects:
        pygame.draw.rect(screen, (255, 0, 0), rect, 2)

    # Draw player
    screen.blit(player_image, player_rect)

    pygame.display.flip()

pygame.quit()
