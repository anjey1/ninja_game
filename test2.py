import pygame, time, random
from pygame.locals import *
from pytmx.util_pygame import load_pygame
from scripts.utils import load_images

BASE_IMG_PATH = 'data/images/'

def blit_all_tiles(window, tmxdata, world_offset):
    for layer in tmxdata:
        try:
            # layer['type'] != 'objectgroup': # and layer['name'] == 'Collision Layer':
            if layer.id in [1,2]:
                for tile in layer.tiles():
                # tile[0] .... x grid location
                # tile[1] .... y grid location
                # tile[2] .... image data for blitting
                    pixels_in_image = 32
                    tile_img = pygame.transform.scale(tile[2], (32,32))
                    x_pixel = tile[0] * pixels_in_image + world_offset[0]
                    y_pixel = tile[1] * pixels_in_image + world_offset[1]
                    # draw the image according to world offset
                    window.blit(tile_img, (x_pixel,y_pixel))
            # else:
            #     for obj in layer:
            #         col_rect = pygame.Rect(obj['x'], obj['y'], obj['width'], obj['height'])
            #     collision_rects.append(col_rect)
        except:
            print('Error getting tiles from layer !')



def get_tile_properties(tmxdata, x, y, world_offset):
    world_x = x - world_offset[0]
    world_y = y - world_offset[1]
    tile_x = world_x // 32 # pixels in tile
    tile_y = world_y // 32 # pixels in tile

    #*********** Handle tile properties**************
    try:
        properties = tmxdata.get_tile_properties(tile_x, tile_y, 0)
    except ValueError:
        # Fill in missing tiles with default values and kill on sight
        properties = {"climable":0, "ground":0, "health":-9999, "points":0, "provides":"", "requires":"", "solid":0}

    if properties is None:
        properties = {"climable":0, "ground":0, "health":0, "points":0, "provides":"", "requires":"", "solid":0}
    return properties

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0,0,0))
    return img

def main():

    # Loading State
    tmxdata = load_pygame("beta_map.tmx")
    y_ground = window.get_height() - 118
    player_width = 40
    player_height = 56
    quit = False
    x = 400
    y = y_ground


    # Load a single image for standing still
    player_stand = load_images("entities/player/idle")
    player_stand = [ pygame.transform.scale(image, (player_width,player_height)) for image in player_stand]
    player_stand_frame = 0

    # Jumping
    player_jump =  load_image("entities/player/jump/0.png")
    player_jump = pygame.transform.scale(player_jump, (player_width,player_height))
    player_jump_frame = 0
    # Landing
    player_land = load_image("entities/player/slide/0.png")
    player_land = pygame.transform.scale(player_land, (player_width,player_height))
    # Create List Of Images
    player_right = load_images("entities/player/run")
    
    # Resize all images in the list to 50*70
    player_right = [ pygame.transform.scale(image, (player_width,player_height)) for image in player_right]

    # Variable to remember which frame from the list we las displayed
    player_right_frame = 0

    # Creating moving left images by flipping the right facing ones on the horizontal axis
    player_left = [pygame.transform.flip(image, True, False) for image in player_right]
    player_left_frame = 0

    # Looking Left
    player_stand_left = [pygame.transform.flip(image, True, False) for image in player_stand]
    player_stand_left_frame = 0

    # Maintain our direction
    direction = "stand"

    world_offset = [0,0]

    #*************** Start game loop ***************
    while not quit:
        window.fill((176, 188, 209))
        blit_all_tiles(window, tmxdata, world_offset)

        #******* Proccess events **********
        keypressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            # print(event)  # Useful for debug
            if event.type == QUIT:
                quit = True


        # Collisions

        standing_on = get_tile_properties(tmxdata, x+20, y+56, world_offset) # bottom center player sprite
        print(standing_on)


        if keypressed[ord("a")]:
            left_tile = get_tile_properties(tmxdata, x - 10, y + (player_height / 2), world_offset) # center middle +10 on x
            if left_tile['solid'] == 0:
                x = x - 10
                direction = "left"
        if keypressed[ord("d")]:
            right_tile = get_tile_properties(tmxdata, x + player_width + 10, y + (player_height / 2), world_offset) # center middle +10 on x
            if right_tile['solid'] == 0:
                x = x + 10
                direction = "right"

        if keypressed[pygame.K_SPACE]:
            if standing_on['ground'] == 1:
                player_jump_frame = 13
        if keypressed[ord("s")]:
            pass

        if sum(keypressed) == 0: # No key is pressed
            direction = "stand"


        #******** Your game logic here **************
        if player_jump_frame > 0: # Jumping in progress
            above_tile = get_tile_properties(tmxdata, x - 10, y + (player_height / 2), world_offset) # center middle +10 on x
            y = y - 10
            direction = "jump"
            player_jump_frame -=1
        elif standing_on['ground'] == 0: # Landing/Falling in progress
            y = y + 10
            direction = "land"


        
    # Keep Player within screen limits

    # World Still
        # if y < 0:
        #     y = 0
        # if y >= y_ground:
        #     y = y_ground
        # if x < 0:
        #     x = 0
        # if x >= window.get_width() - 50:
        #     x = window.get_width() - 50

    # World Moves
        if y < 134:                 
            y = 134
            world_offset[1] += 10
        if y > y_ground:       
            y = y_ground       
            world_offset[1] -= 10
        
        if x < 140:
            x = 140
            world_offset[0] += 10
        if x > window.get_width() - 140 - 20:
            x = window.get_width() - 140 - 20
            world_offset[0] -= 10
        
    # Draw the player
        if direction == "left":
            window.blit(player_left[player_left_frame], (x,y))
            player_left_frame = (player_left_frame + 1) % len(player_left)
        elif direction == "right":
            window.blit(player_right[player_right_frame], (x,y))
            player_right_frame = (player_right_frame + 1) % len(player_right)
        elif direction == "jump":
            window.blit(player_jump, (x,y))
        elif direction == "land":
            window.blit(player_land, (x,y))
        else:
            window.blit(player_stand[player_stand_frame], (x,y))
            player_stand_frame = (player_stand_frame + 1) % len(player_stand)
        

        #************** Update screen ****************
        pygame.display.update()                             # Actually does the screen update
        clock.tick(30)                                      # Run at 30 frames per second

#*************** Initialize & run the game **************
if __name__ == "__main__":
    width, height = 1200, 640
    pygame.init()
    # pygame.mixer.init()
    pygame.display.set_caption("Jhonny B")
    window = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    main()
    pygame.quit()
