import pygame, time, random
from pygame.locals import *
from pytmx.util_pygame import load_pygame
from utils import blit_all_tiles, load_image, get_tile_properties
from entities import Entity

BASE_IMG_PATH = "data/images/"
PIXELS_IN_TILE = 32

pygame.font.init()
FONT = pygame.font.SysFont("Arial",18)

class Game:
    def __init__(self):
        #*************** Initialize & run the game **************
        pygame.init()
        # pygame.mixer.init()
        pygame.display.set_caption("Jhonny C")
        width, height = 1200, 640

        # Window / Surface
        self.window = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

        self.x = 400
        self.y_ground = self.window.get_height() - 234 # 640-234
        self.y = self.y_ground

        # change from camera original setting (x,y)
        self.world_offset = [0,0]

        self.player = Entity(self)
        self.player2 = Entity(self,600)

    def main(self):
        
        tmxdata = load_pygame('data\maps\map.tmx')
#        y_ground = 
        quit = False
        #x = 400
        #y = y_ground

        


        #*************** Start game loop ***************
        while not quit:
            self.window.fill((164,164,164))
            blit_all_tiles(self.window, tmxdata, self.world_offset)

            PLAYER_LOCATION = FONT.render(f"x, y: {self.player.x, self.player.y}", 1, (255,255,255))
            self.window.blit(PLAYER_LOCATION, (50,50))

            #******* Proccess events **********
            
            for event in pygame.event.get():
                # print(event)  # Useful for debug
                if event.type == QUIT:
                    quit = True
            
            # World Moves - Handle world offset
            print(f"{self.player.y,self.player.x}")
            if self.player.y < 134:                 
                self.player.y = 134
                self.world_offset[1] += 10

            if self.player.y > self.y_ground:       
                self.player.y = self.y_ground       
                self.world_offset[1] -= 10

            if self.player.x < 140:
                self.player.x = 140
                self.world_offset[0] += 10

            if self.player.x > self.window.get_width() - 140 - 50:
                self.player.x = self.window.get_width() - 140 - 50
                self.world_offset[0] -= 10
            
        
            #************** Update screen ****************

            self.player.update(tmxdata, self.window)
            self.player.render(tmxdata, self.window)

            self.player2.update(tmxdata, self.window)
            self.player2.render(tmxdata, self.window)

            pygame.display.update()                             # Actually does the screen update
            self.clock.tick(30)                                      # Run at 30 frames per second


Game().main()
pygame.quit()
