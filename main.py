import sys
import pygame, time, random
from pygame.locals import *
from pytmx.util_pygame import load_pygame
from npc import NPC
from utils import blit_all_tiles, moveWindow, update_enemies
from entities import Entity
from enemies import Enemy
from hud import drawHud
from dialog import Dialog

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
        self.current_map_path = "data/maps/map.tmx"
        self.current_map_verbose = "map"

        # string
        # list - iter []
        # tuple - (1, 2, {1:2}, [])
        # dict - iter {"key":"value"}

        self.location_maps = {
            "map": "data\maps\map.tmx",
            "cave": "data\maps\cave.tmx",
        }

        # self.tmxdata = load_pygame("data\maps\map.tmx")
        # Window / Surface
        self.window = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

        self.x = 0

        # Horizon
        self.y = (
            self.window.get_height() - 400
        )  # see 400 below player when standing on surface

        # Dialog
        self.dialog_active = False
        self.dialog_view = Dialog(self.window)

        # change from camera original setting (x,y)
        self.world_offset = [0, 0]  # [340, 130] = [0,0]
        self.enemies_group = []
        self.npc_group = []
        # self.animations_group = pygame.sprite.Group()

        self.player = Entity(self)
        self.enemy: Enemy = Enemy(self, 120, 120, ["stand", "right", "stand", "left"])
        self.enemy2: Enemy = Enemy(self, 1300, 20)
        self.enemy3: Enemy = Enemy(self, 1600, 100)
        self.npc: NPC = NPC(self, 400, 200)
        self.npc.__name__ = "albert"
        # self.player2 = Entity(self,600)

        self.player_group = pygame.sprite.GroupSingle(self.player)

        # self.enemy: Enemy = Enemy(self, 1050, 149)
        # self.enemy2: Enemy = Enemy(self, 600, 200)
        self.enemy.__name__ = "Random Enemy"
        self.enemies_group.insert(len(self.enemies_group), self.enemy)
        # Add group position index for future deletion
        self.enemy.group_index = len(self.enemies_group) - 1

        self.enemies_group.insert(len(self.enemies_group), self.enemy2)
        self.enemy2.group_index = len(self.enemies_group) - 1

        self.enemies_group.insert(len(self.enemies_group), self.enemy3)
        self.enemy3.group_index = len(self.enemies_group) - 1

        self.npc_group.insert(len(self.npc_group), self.npc)
        self.npc.group_index = len(self.npc_group) - 1

    def main(self):
        if not pygame.display.get_init():
            print("Pygame display not initialized. Exiting program.")
            pygame.quit()  # Optional: Clean up any pygame resources
            sys.exit()  # Exit the program

        self.tmxdata = load_pygame(self.current_map_path)
        self.quit = False

        self.health = HEALTH
        self.points = POINTS

        # *************** Start game loop ***************
        while not self.quit:
            self.window.fill((3, 194, 252))
            blit_all_tiles(self.window, self.tmxdata, self.world_offset)

            drawHud(self.window, self.player, self.enemy, self.health, self.points)
            # ******* Proccess events **********

            for event in pygame.event.get():
                # print(event)  # Useful for debug
                if event.type == QUIT:
                    self.quit = True

            moveWindow(self, self.window, self.player)

            # ************** Update screen ****************

            # USE - pygame.sprite.Group.draw(self.active_sprites, self.gameboard)
            # to draw all groups

            # Для правильной работы функции pygame.sprite.Group.draw
            # self.rect = self.image.get_rect()
            # self.rect.center = pos

            # enemy calculated without world offset and printed with
            self.player.update(self.tmxdata, self.window)  # window only used for debug
            self.player.render(self.tmxdata, self.window)

            update_enemies(self, self.tmxdata, self.window, self.world_offset)
            # self.enemy.update(self.tmxdata, self.window)
            # self.enemy.render(self.window, self.world_offset)

            self.npc.update(self.tmxdata, self.window)
            self.npc.render(self.window, self.world_offset)

            # return enemy index from enemy group
            enemy_index = self.player.sword.rect.collidelist(self.enemies_group)
            npc_index = self.player.rect.collidelist(self.npc_group)

            # use enemy index to deal damage
            if enemy_index >= 0:
                enemy: Enemy = self.enemies_group[enemy_index]
                enemy.takeDamage(50)
                print(
                    f"enemy {enemy_index} : rect {enemy.rect} : is_alive {enemy.is_alive}"
                )
                print(f"colided with enemy {enemy_index}")

            # use enemy index to deal damage
            if npc_index >= 0:
                npc: NPC = self.npc_group[npc_index]
                # if npc.spoke_to_hero != True:
                self.dialog_active = True
                print(
                    f"npc {npc_index} : rect {npc.rect.x, npc.rect.y} : is_alive {npc.is_alive} : spoken_to {npc.spoke_to_hero}"
                )
                print(f"colided with npc {npc_index}")
            else:
                self.dialog_active = False

            if self.dialog_active == True:
                self.dialog_view.render(self.window)

            # self.player2.update(self.tmxdata, self.window)
            # self.player2.render(self.tmxdata, self.window)

            pygame.display.update()  # Actually does the screen update
            self.clock.tick(30)  # Run at 30 frames per second


Game().main()
pygame.quit()
