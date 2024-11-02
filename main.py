import pygame, time, random
from pygame.locals import *
from pytmx.util_pygame import load_pygame
from entities import PhysicsEntity
from utils import blit_all_tiles, update_animations, load_images, update_enemies
from scripts.clouds import Clouds
from dialog import DialogView

LR_MOVMENT_OFFSET = 15
PLAYER_JUMP_HEIGHT = 23
HEALTH = 100
POINTS = 0

pygame.font.init()
FONT = pygame.font.SysFont("Arial", 18)


class Game:
    def __init__(self):
        pygame.init()
        width, height = 1920, 1080
        # width, height = 1200, 640
        # pygame.mixer.init()
        pygame.display.set_caption("Jhonny B")
        self.window = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.animations = {}
        self.enemies = {}
        self.player = PhysicsEntity(self)

        # groups added for collisions
        self.animations_group = pygame.sprite.Group()
        self.enemies_group = []
        self.player_group = pygame.sprite.GroupSingle(self.player)

        self.dialog = False
        self.dialog_view = DialogView(self.window)
        self.clouds = Clouds(load_images("clouds", False, 300, 200), 9)
        # self.player2 = PhysicsEntity(self, 540, 250, True)

        self.elapsed_time = (
            pygame.time.get_ticks()
        )  # in charge of moving background aminations

    def main(self):
        global HEALTH
        global POINTS

        # Loading State
        tmxdata = load_pygame("map5.tmx")

        y_ground = self.window.get_height() - 418

        quit = False

        self.health = HEALTH
        self.points = POINTS

        self.world_offset = [0, 0]

        # *************** Start game loop ***************
        while not quit:
            self.elapsed_time = pygame.time.get_ticks()
            # self.window.fill((33, 33, 33))
            self.window.fill((3, 194, 252))

            self.clouds.update()
            self.clouds.render(
                self.window,
                # offset=(self.world_offset[0], self.world_offset[1]),
            )

            blit_all_tiles(self, self.window, tmxdata, self.world_offset)

            POINTS_IMG = FONT.render(
                f"Points: {self.player.points}", 1, (255, 255, 255)
            )
            HEALTH_IMG = FONT.render(f"HEALTH: {self.health}", 1, (255, 255, 255))

            self.window.blit(POINTS_IMG, (50, 10))
            self.window.blit(HEALTH_IMG, (50, 30))

            # ******* Proccess game events **********

            for event in pygame.event.get():
                # print(event)  # Useful for debug
                if event.type == QUIT:
                    quit = True
                if self.dialog:
                    keypressed = ""
                    keypressed = pygame.key.get_pressed()
                    if keypressed[ord("k")]:
                        self.dialog_view.next_line()

            # ******** World Offset logic **************
            if self.player.y < 134:
                self.player.y = 134
                self.world_offset[1] += 10
            if self.player.y > y_ground:
                self.player.y = y_ground
                self.world_offset[1] -= 10

            if self.player.x < 640:
                self.player.x = 640
                self.world_offset[0] += 10

            if self.player.x > self.window.get_width() - 640:
                self.player.x = self.window.get_width() - 640
                self.world_offset[0] -= 10

            PLAYER_LOCATION = FONT.render(
                f"x,y: {self.player.x, self.player.y}", 1, (255, 255, 255)
            )
            self.window.blit(PLAYER_LOCATION, (50, 50))

            update_animations(self, self.window, self.world_offset)
            # update_enemies(self, tmxdata, self.window, self.world_offset)

            if self.player.rect.collidelist(self.enemies_group) >= 0:
                print("colided with enemy")

            # self.player2.update(tmxdata, self.window)
            # self.player.render(self.window, direction)

            self.player.update(tmxdata, self.window)

            if self.dialog == True:
                self.dialog_view.render(self.window)
            # ************** Update screen ****************
            pygame.display.update()  # Actually does the screen update
            self.clock.tick(30)  # Run at 30 frames per second


Game().main()
pygame.quit()
