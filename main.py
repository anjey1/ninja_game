import pygame, time, random
from pygame.locals import *
from pytmx.util_pygame import load_pygame
from entities import PhysicsEntity
from utils import load_images, blit_all_tiles, get_tile_properties

LR_MOVMENT_OFFSET = 15
PLAYER_JUMP_HEIGHT = 23
HEALTH = 100
POINTS = 0

pygame.font.init()
FONT = pygame.font.SysFont("Arial", 18)


class Game:
    def __init__(self):
        pygame.init()
        width, height = 1200, 640
        # pygame.mixer.init()
        pygame.display.set_caption("Jhonny B")
        self.window = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

        self.player = PhysicsEntity(self)

    def main(self):
        global HEALTH
        global POINTS

        # Loading State
        tmxdata = load_pygame("map4.tmx")
        y_ground = self.window.get_height() - 418

        quit = False

        self.health = HEALTH
        self.points = POINTS

        self.world_offset = [0, 0]

        # *************** Start game loop ***************
        while not quit:
            self.window.fill((33, 33, 33))
            blit_all_tiles(self.window, tmxdata, self.world_offset)

            POINTS_IMG = FONT.render(
                f"Points: {self.player.points}", 1, (255, 255, 255)
            )
            HEALTH_IMG = FONT.render(f"HEALTH: {self.health}", 1, (255, 255, 255))

            self.window.blit(POINTS_IMG, (50, 10))
            self.window.blit(HEALTH_IMG, (50, 30))

            # ******* Proccess events **********

            for event in pygame.event.get():
                # print(event)  # Useful for debug
                if event.type == QUIT:
                    quit = True

            # ******** World Offset logic **************
            if self.player.y < 134:
                self.player.y = 134
                self.world_offset[1] += 10
            if self.player.y > y_ground:
                self.player.y = y_ground
                self.world_offset[1] -= 10

            if self.player.x < 340:
                self.player.x = 340
                self.world_offset[0] += 10

            if self.player.x > self.window.get_width() - 155:
                self.player.x = self.window.get_width() - 155
                self.world_offset[0] -= 10

            PLAYER_LOCATION = FONT.render(
                f"x,y: {self.player.x, self.player.y}", 1, (255, 255, 255)
            )
            self.window.blit(PLAYER_LOCATION, (50, 50))

            # self.player.update(self.tilemap,(self.movement[1] - self.movement[0],0))
            # self.player.render(self.display,  offset=render_scroll)

            self.player.update(tmxdata, self.window)
            # self.player.render(self.window, direction)

            # ************** Update screen ****************
            pygame.display.update()  # Actually does the screen update
            self.clock.tick(30)  # Run at 30 frames per second


Game().main()
pygame.quit()
