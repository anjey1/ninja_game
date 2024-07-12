import pygame, time, random
from pygame.locals import *
from pytmx.util_pygame import load_pygame
from utils import load_images, blit_all_tiles, get_tile_properties

LR_MOVMENT_OFFSET = 15
PLAYER_JUMP_HEIGHT = 23
HEALTH = 100
POINTS = 0

pygame.font.init()
FONT = pygame.font.SysFont("Arial", 18)


def main():
    global HEALTH
    global POINTS

    # Loading State
    tmxdata = load_pygame("map4.tmx")
    y_ground = window.get_height() - 418

    quit = False
    x = 710
    y = y_ground
    player_width = 40
    player_height = 56
    health = HEALTH
    points = POINTS
    player_stand_frame = 0
    player_jump_frame = 0
    player_right_frame = 0
    player_left_frame = 0

    assets = {
        "player_stand": load_images("entities/player/idle"),
        "player_jump": load_images("entities/player/jump"),
        "player_land": load_images("entities/player/slide"),
        "player_right": load_images("entities/player/run"),
        "player_left": load_images("entities/player/run", True),
    }

    inventory = []

    # Maintain our direction
    direction = "stand"

    world_offset = [0, 0]

    # *************** Start game loop ***************
    while not quit:
        window.fill((33, 33, 33))
        blit_all_tiles(window, tmxdata, world_offset)
        POINTS_IMG = FONT.render(f"Points: {points}", 1, (255, 255, 255))
        HEALTH_IMG = FONT.render(f"HEALTH: {health}", 1, (255, 255, 255))
        window.blit(POINTS_IMG, (50, 10))
        window.blit(HEALTH_IMG, (50, 30))

        # ******* Proccess events **********

        for event in pygame.event.get():
            # print(event)  # Useful for debug
            if event.type == QUIT:
                quit = True

        # ******** Collisions ********

        # bottom center player sprite
        standing_on = get_tile_properties(
            tmxdata, x + (player_width / 2), y + player_height, world_offset
        )

        touching = get_tile_properties(
            tmxdata, x + (player_width / 2), y + (player_height / 2), world_offset
        )

        health += touching["health"]
        points += touching["points"]
        # print(touching)

        tile_x = int(touching["x"])
        tile_y = int(touching["y"])

        if health < 0:
            quit = True

        # if touching['id'] == 73:
        if touching["remove"] == True:
            tmxdata.layers[0].data[tile_y][tile_x] = 0

        if touching["provides"] != '' and touching["provides"] != None:
            inventory.append(touching["provides"])
            print(f"got {touching["provides"]} !")
            tmxdata.layers[0].data[tile_y][tile_x] = 0

        if touching["requires"] != '' and touching["requires"] != None:
            if touching["requires"] in inventory:
                print(f"looking for {touching["requires"]} !")
                if touching["requires"] == "key":
                    print(f"used {touching["requires"]} !")
                    inventory.remove(touching["requires"])
                    tmxdata.layers[0].data[tile_y][tile_x] = tmxdata.layers[1].data[tile_y][tile_x]
                    if tile_y == 16 and tile_x == 22: # 1st Door
                        #  print(world_offset)
                         world_offset[0] = world_offset[0] - 180 * 16 # move right 150 grids each 16
                         world_offset[1] = world_offset[1] - 1 * 16 # move up 1 grids each 16
                    elif tile_y == 17 and tile_x == 86: # 2st Door
                        #  print(world_offset)
                         world_offset[0] = world_offset[0] - 183 * 16 # move right 150 grids each 16
                        #  world_offset[1] = world_offset[1] - 20 # move up 2 grids each 16
                    elif tile_y == 5 and tile_x == 154: # 3st Door
                        #  print(world_offset)
                         world_offset[0] = world_offset[0] + 183 * 16 # move right 150 grids each 16
                         world_offset[1] = world_offset[1] + 5 * 16 # move up 2 grids each 16

        # ******** Player events **************
        keypressed = pygame.key.get_pressed()

        if keypressed[ord("a")]:
            left_tile = get_tile_properties(
                tmxdata,
                x,  # - LR_MOVMENT_OFFSET
                y + player_height - 16,
                world_offset,
            )  # center middle +10 on x
            if left_tile["solid"] == 0:
                x = x - LR_MOVMENT_OFFSET
                direction = "left"
                # print(left_tile)

        if keypressed[ord("d")]:
            right_tile = get_tile_properties(
                tmxdata,
                x + player_width,  # + LR_MOVMENT_OFFSET
                y + player_height - 16,
                world_offset,
            )  # center middle +10 on x
            if right_tile["solid"] == 0:
                x = x + LR_MOVMENT_OFFSET
                direction = "right"
                # print(right_tile)

        if keypressed[pygame.K_SPACE]:
            if standing_on["climable"] == 1:
                y = y - 10
            if standing_on["ground"] == 1:
                player_jump_frame = PLAYER_JUMP_HEIGHT

        if keypressed[ord("s")]:
            if standing_on["climable"] == 1:
                y = y + 10

        if sum(keypressed) == 0:  # No key is pressed
            if direction != "stand":
                # print(standing_on)
                # print(touching)
                direction = "stand"

        # ******** Your game logic here **************

        if player_jump_frame > 0:  # Jumping in progress after space pressed

            # center middle +10 on x
            above_tile = get_tile_properties(
                tmxdata, x + (player_width / 4), y + (player_height / 4), world_offset
            )

            if above_tile["solid"] == 0:
                y = y - 10
                direction = "jump"
                player_jump_frame -= 1
            else:
                player_jump_frame = 0

        elif (
            standing_on["ground"] == 0 and standing_on["climable"] == 0
        ):  # Landing/Falling in progress
            y = y + 10
            direction = "land"

        # ******** World Offset logic **************
        if y < 134:
            y = 134
            world_offset[1] += 10
        if y > y_ground:
            y = y_ground
            world_offset[1] -= 10

        if x < 340:
            x = 340
            world_offset[0] += 10
        if x > window.get_width() - 155:
            x = window.get_width() - 155
            world_offset[0] -= 10

        # Draw the player
        # print(f'x: {x} y: {y}')

        if direction == "left":
            window.blit(assets["player_left"][player_left_frame], (x, y))
            player_left_frame = (player_left_frame + 1) % len(assets["player_left"])
        elif direction == "right":
            window.blit(assets["player_right"][player_right_frame], (x, y))
            player_right_frame = (player_right_frame + 1) % len(assets["player_right"])
        elif direction == "jump":
            window.blit(assets["player_jump"][0], (x, y))
        elif direction == "land":
            window.blit(assets["player_land"][0], (x, y))
        else:
            window.blit(assets["player_stand"][player_stand_frame], (x, y))
            player_stand_frame = (player_stand_frame + 1) % len(assets["player_stand"])

        PLAYER_LOCATION = FONT.render(f"x,y: {x, y}", 1, (255, 255, 255))
        window.blit(PLAYER_LOCATION, (50, 50))

        # ************** Update screen ****************
        pygame.display.update()  # Actually does the screen update
        clock.tick(30)  # Run at 30 frames per second


# *************** Initialize & run the game **************
if __name__ == "__main__":
    width, height = 1200, 640
    pygame.init()
    # pygame.mixer.init()
    pygame.display.set_caption("Jhonny B")
    window = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    main()
    pygame.quit()
