import pygame, time, random
from pygame.locals import *
from pytmx.util_pygame import load_pygame
from utils import blit_all_tiles, update_enemies
from entities import Entity
from enemies import Enemy
from hud import drawHud

BASE_IMG_PATH = "data/images/"
PIXELS_IN_TILE = 32
HEALTH = 100
POINTS = 0

pygame.font.init()
FONT = pygame.font.SysFont("Arial", 18)


class Game:
    def __init__(self):  # Constructor
        # *************** Initialize & run the game **************
        pygame.init()
        # pygame.mixer.init()
        pygame.display.set_caption("Jhonny C")
        width, height = 1200, 640
        self.current_map_path = "data\maps\map.tmx"
        self.current_map_verbose = "map"
        
        # string
        # list - iter []
        # tuple - (1, 2, {1:2}, [])
        # dict - iter {"key":"value"}

        self.location_maps = {
            "map" : "data\maps\map.tmx",
            "cave" : "data\maps\cave.tmx",
        }

        # self.tmxdata = load_pygame("data\maps\map.tmx")
        # Window / Surface
        self.window = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

        self.x = 400
        self.y_ground = self.window.get_height() - 234  # 640-234
        self.y = self.y_ground

        # change from camera original setting (x,y)
        self.world_offset = [0, 0]
        self.enemies_group = []
        # self.animations_group = pygame.sprite.Group()

        self.player = Entity(self)
        self.enemy = Enemy(self, 120, 120, ["stand", "right", "stand", "left"])
        self.enemy2 = Enemy(self, 600, 200)
        # self.player2 = Entity(self,600)

        self.player_group = pygame.sprite.GroupSingle(self.player)

        self.enemy: Enemy = Enemy(self, 1050, 149)
        self.enemy2: Enemy = Enemy(self, 600, 200)

        self.enemies_group.append(self.enemy)
        self.enemies_group.append(self.enemy2)

    def main(self):
        self.tmxdata = load_pygame(self.current_map_path)
        self.quit = False
        # x = 400
        # y = y_ground
        self.health = HEALTH
        self.points = POINTS

        # *************** Start game loop ***************
        while not self.quit:
            self.window.fill((3, 194, 252))
            blit_all_tiles(self.window, self.tmxdata, self.world_offset)

            drawHud(self.window, self.player, self.enemy2, self.health, self.points)
            # ******* Proccess events **********

            for event in pygame.event.get():
                # print(event)  # Useful for debug
                if event.type == QUIT:
                    self.quit = True

            # World Moves - Handle world offset
            # print(f"{self.player.y,self.player.x}")
            if self.player.y < 134:
                self.player.y = 134
                self.world_offset[1] += 10

            if self.player.y > self.y_ground:
                self.player.y = self.y_ground
                self.world_offset[1] -= 10

            if self.player.x < 340:
                self.player.x = 340
                self.world_offset[0] += 10

            if self.player.x > self.window.get_width() - 340 - 50:
                self.player.x = self.window.get_width() - 340 - 50
                self.world_offset[0] -= 10

            # ************** Update screen ****************

            # enemy calculated without world offset and printed with
            self.player.update(self.tmxdata, self.window)  # window only used for debug
            self.player.render(self.tmxdata, self.window)

            update_enemies(self, self.tmxdata, self.window, self.world_offset)
            # self.enemy.update(self.tmxdata, self.window)
            # self.enemy.render(self.window, self.world_offset)

            # self.enemy2.update(self.tmxdata, self.window)
            # self.enemy2.render(self.window, self.world_offset)

            enemy_index = self.player.rect.collidelist(self.enemies_group)
            if enemy_index >= 0:
                enemy = self.enemies_group[enemy_index]
                print(f"enemy {enemy_index} : rect {enemy.rect}")
                print(f"colided with enemy {enemy_index}")
                print(f"player rect {self.player.rect}")

            # self.player2.update(self.tmxdata, self.window)
            # self.player2.render(self.tmxdata, self.window)

            pygame.display.update()  # Actually does the screen update
            self.clock.tick(30)  # Run at 30 frames per second


Game().main()
pygame.quit()
