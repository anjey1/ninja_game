import pygame, time, random
from pygame.locals import *
from pytmx.util_pygame import load_pygame

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
                    img = pygame.transform.scale(tile[2], (32,32))
                    x_pixel = tile[0] * pixels_in_image + world_offset[0]
                    y_pixel = tile[1] * pixels_in_image + world_offset[1]
                    # draw the image according to world offset
                    window.blit(img, (x_pixel,y_pixel))
            # else:
            #     for obj in layer:
            #         col_rect = pygame.Rect(obj['x'], obj['y'], obj['width'], obj['height'])
            #     collision_rects.append(col_rect)
        except:
            print('Warning !')
            print(layer.tiles())

def main():
    tmxdata = load_pygame("beta_map.tmx")
    y_ground = window.get_height() - 134
    player_width = 50
    player_height = 70
    quit = False
    x = 400
    y = y_ground
    # Load a single image for standing still
    player_stand = pygame.image.load("data/images/entities/player/idle/00.png").convert_alpha()
    player_stand = pygame.transform.scale(player_stand, (player_width,player_height))
    # Jumping
    player_jump =  pygame.image.load("data/images/entities/player/jump/0.png").convert_alpha()
    player_jump = pygame.transform.scale(player_jump, (player_width,player_height))
    player_jump_frame = 0
    # Landing
    player_land = pygame.image.load("data/images/entities/player/slide/0.png")
    player_land.set_colorkey((0,0,0))
    player_land.convert_alpha()
    player_land = pygame.transform.scale(player_land, (player_width,player_height))
    # Create List Of Images
    player_right = [
        pygame.image.load("data/images/entities/player/run/0.png").convert_alpha(),
        pygame.image.load("data/images/entities/player/run/1.png").convert_alpha(),
        pygame.image.load("data/images/entities/player/run/2.png").convert_alpha(),
        pygame.image.load("data/images/entities/player/run/3.png").convert_alpha(),
    ]
    
    
    # Resize all images in the list to 50*70
    player_right = [ pygame.transform.scale(image, (player_width,player_height)) for image in player_right]

    # Variable to remember which frame from the list we las displayed
    player_right_frame = 0

    # Creating moving left images by flipping the right facing ones on the horizontal axis
    player_left = [pygame.transform.flip(image, True, False) for image in player_right]
    player_left_frame = 0

    # Maintain our direction
    direction = "stand"

    world_offset = [0,0]

    #*************** Start game loop ***************
    while not quit:
        window.fill((64,64,64))
        blit_all_tiles(window, tmxdata, world_offset)
        #******* Proccess events **********
        keypressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            # print(event)  # Useful for debug
            if event.type == QUIT:
                quit = True

        if keypressed[ord("a")]:
            x = x - 10
            direction = "left"
        if keypressed[ord("d")]:
            x = x + 10
            direction = "right"
        if keypressed[ord("w")]:
            y = y_ground
            player_jump_frame = 20
        if keypressed[ord("s")]:
            pass
        if sum(keypressed) == 0: # No key is pressed
            direction = "stand"


        #******** Your game logic here **************
        if player_jump_frame > 0: # Jumping in progress
            y = y - 10
            direction = "jump"
            player_jump_frame -=1
        elif y < y_ground:
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
            print(f'ssss')


        if x < 140:
            x = 140
            world_offset[0] += 10


        if x > window.get_width() - 140 - 50:
            x = window.get_width() - 140 - 50
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
            window.blit(player_stand, (x,y))
        

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
