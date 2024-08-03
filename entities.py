import pygame
from pygame.image import load
from utils import get_tile_properties, load_image, load_images

class Entity:
    def __init__(self,game, x=400, y=200):
        self.player_width = 50
        self.player_height = 70
        self.x=x
        self.y=y
        self.game = game
        self.moving_x_direction = 0
        self.assets = {
            "player_stand": load_images("entities/player/idle"),
            "player_jump": load_images("entities/player/jump"),
            "player_land": load_images("entities/player/slide"),
            "player_right": load_images("entities/player/run"),
            "player_left": load_images("entities/player/run", True)
        }

        self.player_stand_frame = 0
        self.player_right_frame = 0
        self.player_left_frame = 0
        self.player_jump_frame = 0


        self.LAST_DIRECTION = ""

        # Maintain our direction
        self.direction = "stand"

    def update(self, tmxdata, window):

            keypressed = pygame.key.get_pressed()

            # ******** Collisions ********
            
            # Bottom Center Player Sprite
            #-----
            #|   | <<--
            #|   | -->>
            #-----
            standing_on = get_tile_properties(
                tmxdata, 
                self.x + int(self.player_width / 2), 
                self.y + self.player_height, 
                self.game.world_offset)
            

            # Monitor x Movment (Direction)
            #******** Your LEFT/RIGHT  logic here **************
            if keypressed[ord("a")]:
                left_tile = get_tile_properties(
                    tmxdata,
                    self.x, # - LR_MOVMENT_OFFSET
                    self.y + self.player_height - 16,
                    self.game.world_offset,
                ) # center middle +10 on x

                if left_tile["solid"] == 0:
                    self.x = self.x - 30
                    self.LAST_DIRECTION = self.direction = "left"
                    
            if keypressed[ord("d")]:
                right_tile = get_tile_properties(
                    tmxdata,
                    self.x + self.player_width, # - LR_MOVMENT_OFFSET
                    self.y + self.player_height - 16,
                    self.game.world_offset,
                ) # center middle +10 on x

                if right_tile["solid"] == 0:
                    self.x = self.x + 30
                    self.LAST_DIRECTION = self.direction = "right"

            if keypressed[ord("w")]:
                if standing_on["ground"] == 1:
                    self.player_jump_frame = 40
                
            if keypressed[ord("s")]:
                pass
            if sum(keypressed) == 0: # No key is pressed
                if self.direction != "stand":
                    self.direction = "stand"


            #******** Your JUMP/FALL  logic here **************
            if self.player_jump_frame > 0: # Jumping in progress
                above_tile = get_tile_properties(
                    tmxdata,
                    self.x + self.player_width, # - LR_MOVMENT_OFFSET
                    self.y + (self.player_height / 2),
                    self.game.world_offset,
                )
                if above_tile["solid"] == 0:
                    self.y = self.y - 10
                    self.direction = "jump"
                    self.player_jump_frame -=1 # 20 - 1
                else:
                    self.player_jump_frame = 0

            elif standing_on["ground"] == 0:
                self.y = self.y + 10
                self.direction = "land"

            
            # Touching logic x axis
            if(self.direction == 'right'):
                self.moving_x_direction = 0
            if(self.direction == 'left'):
                self.moving_x_direction = self.player_width
            
            touching = get_tile_properties(
                tmxdata, 
                self.x + self.moving_x_direction, 
                self.y + int(self.player_height / 2) + 10, 
                self.game.world_offset) 

            print(touching.get('health'))
            if touching.get('health') != None:
                self.game.health += touching["health"]

            if touching.get('points') != None:
                self.game.points += touching["points"]

    def render(self, tmxdata, window):
         # Draw the player
            if self.direction == "left":
                window.blit(self.assets["player_left"][self.player_left_frame], (self.x,self.y))
                self.player_left_frame = (self.player_left_frame + 1) % len(self.assets["player_left"])

            elif self.direction == "right":
                window.blit(self.assets["player_right"][self.player_right_frame], (self.x,self.y))
                self.player_right_frame = (self.player_right_frame + 1) % len(self.assets["player_right"])
                
            elif self.direction == "jump":
                if self.LAST_DIRECTION == "left":
                    window.blit(pygame.transform.flip(self.assets["player_jump"][0], True, False), (self.x,self.y))
                else:
                    window.blit(self.assets["player_jump"][0], (self.x,self.y))

            elif self.direction == "land":
                if self.LAST_DIRECTION == "left":
                    window.blit(pygame.transform.flip(self.assets["player_land"][0], True, False), (self.x,self.y))
                else:
                    window.blit(self.assets["player_land"][0], (self.x,self.y))


            else: #stand
                if self.LAST_DIRECTION == "left":
                    window.blit(pygame.transform.flip(self.assets["player_stand"][self.player_stand_frame], True, False), (self.x,self.y))
                    self.player_stand_frame = (self.player_stand_frame + 1) % len(self.assets["player_stand"])
                else:
                    window.blit(self.assets["player_stand"][self.player_stand_frame], (self.x,self.y))
                    self.player_stand_frame = (self.player_stand_frame + 1) % len(self.assets["player_stand"])







