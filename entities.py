import pygame
from utils import get_tile_properties, load_image

class Entity:
    def __init__(self,game, x=400, y=200):
        self.player_width = 50
        self.player_height = 70
        self.x=x
        self.y=y
        self.game = game
        
        # Load a single image for standing still
        self.player_stand = load_image("entities/player/idle/00.png")
        self.player_stand = pygame.transform.scale(self.player_stand, (self.player_width,self.player_height))
        
        # Jumping
        self.player_jump =  load_image("entities/player/jump/0.png")
        self.player_jump = pygame.transform.scale(self.player_jump, (self.player_width,self.player_height))
        self.player_jump_frame = 0
        
        # Landing
        self.player_land = load_image("entities/player/slide/0.png")
        self.player_land = pygame.transform.scale(self.player_land, (self.player_width,self.player_height))
        
        # Create List Of Images
        self.player_right = [
            load_image("entities/player/run/0.png"),
            load_image("entities/player/run/1.png"),
            load_image("entities/player/run/2.png"),
            load_image("entities/player/run/3.png"),
            load_image("entities/player/run/4.png"),
            load_image("entities/player/run/5.png"),
        ]
        
        
        # Resize all images in the list to 50*70
        self.player_right = [ pygame.transform.scale(image, (self.player_width,self.player_height)) for image in self.player_right]

        # Variable to remember which frame from the list we las displayed
        self.player_right_frame = 0

        # Creating moving left images by flipping the right facing ones on the horizontal axis
        self.player_left = [pygame.transform.flip(image, True, False) for image in self.player_right]
        self.player_left_frame = 0

        self.LAST_DIRECTION = ""

        # Maintain our direction
        self.direction = "stand"

    def update(self, tmxdata, window):

            keypressed = pygame.key.get_pressed()

            # ******** Collisions ********
            
            standing_on = get_tile_properties(tmxdata, self.x + (self.player_width / 2), self.y + self.player_height, self.game.world_offset) # bottom center player sprite
            # print(standing_on)

            # Monitor x Movment (Direction)
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


            #******** Your game logic here **************
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

    def render(self, tmxdata, window):
         # Draw the player
            if self.direction == "left":
                window.blit(self.player_left[self.player_left_frame], (self.x,self.y))
                self.player_left_frame = (self.player_left_frame + 1) % len(self.player_left)
            elif self.direction == "right":
                window.blit(self.player_right[self.player_right_frame], (self.x,self.y))
                self.player_right_frame = (self.player_right_frame + 1) % len(self.player_right)

            elif self.direction == "jump":
                if self.LAST_DIRECTION == "left":
                    window.blit(pygame.transform.flip(self.player_jump, True, False), (self.x,self.y))
                else:
                    window.blit(self.player_jump, (self.x,self.y))

            elif self.direction == "land":
                if self.LAST_DIRECTION == "left":
                    window.blit(pygame.transform.flip(self.player_land, True, False), (self.x,self.y))
                else:
                    window.blit(self.player_land, (self.x,self.y))

            else:
                if self.LAST_DIRECTION == "left":
                    window.blit(pygame.transform.flip(self.player_stand, True, False), (self.x,self.y))
                else:
                    window.blit(self.player_stand, (self.x,self.y))






