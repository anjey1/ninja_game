import pygame
from dialog import FONT
from utils import load_images, PIXELS_IN_TILE, get_tile_properties, get_tile_properties_enemy




class Enemy(pygame.sprite.Sprite):
    def __init__(self, x=710, y=222,  tile_x = 21, tile_y = 16, debug=False):
        super().__init__()
        self.directions = ["stand", "right", "stand", "right", "stand"]
        # self.directions = ["stand"]
        self.tile_x = tile_x
        self.tile_y = tile_y
        
        self.width = 40
        self.height = 60
        self.x = x
        self.y = y

        # Add rectangle for collisions - maybe use the tile print coords x,y,widht,height
        self.image = pygame.Surface((self.width,self.height))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)

        self.last_update = pygame.time.get_ticks()
        self.last_direction_index = 0
        self.last_direction = "stand"
        self.world_offset = [0,0]
        self.last_stand = 0
        self.assets = {
            "enemy_stand": load_images("entities/enemy/idle"),
            "enemy_right": load_images("entities/enemy/run"),
            "enemy_left": load_images("entities/enemy/run", True),
        }

        self.enemy_left_frame = 0
        self.enemy_right_frame = 0
        self.enemy_stand_frame = 0 

    def destroy(self):
        pass 
        # add destroy enemy when falling of grid
        # add remove from enemies array

    def update(self, tmxdata, window, world_offset=(0,0)):
        

        now = pygame.time.get_ticks()
        
         # ******** Collisions ********

        # bottom center player sprite
        try:
            standing_on = get_tile_properties_enemy(
                tmxdata, self.x + int(self.width / 2), self.y + self.height, world_offset
            )
        except Exception as e:
            print(f'exception error standing on {self.x + int(self.width / 2),self.y + self.height}')                    

        
        # middle center player sprite
        try:
            touching = get_tile_properties_enemy(
                tmxdata, self.x + int(self.width / 2), self.y + int(self.height / 2), world_offset
            )
        except Exception as e:
            print(f'exception error standing at {self.x + int(self.width / 2),self.y + self.height}')


        if now - self.last_update > 1000:
            self.last_update = now
            self.last_direction_index = (self.last_direction_index + 1) % len(self.directions)
            self.last_direction = self.directions[self.last_direction_index]

        if self.last_stand != standing_on['id']:
            #print(f'standing on {standing_on}')
            self.last_stand = standing_on['id']

        try: 
            if standing_on["ground"] == 0 and standing_on["climable"] == 0:  # Landing/Falling in progress
                self.y = self.y + 10
                self.direction = "land"
                #print(f'standing on {standing_on}')
                
        except KeyError:
            if standing_on is not None:
                print(f'KeyError falling error {standing_on['ground'],standing_on['climable']}')
            else:
                print(f'KeyError standing one = None')
        except UnboundLocalError:
            if standing_on is not None:
                print(f'Unbound falling error {standing_on['ground'],standing_on['climable']}')
            else:
                print(f'Unbound standing one = None')


        if self.last_direction == "right":
            self.x = self.x  + 3      
            self.render(window, 'right')
        elif self.last_direction == "left":
            self.x = self.x - 3
            self.render(window, 'left')
        elif self.last_direction == "stand":
            self.render(window, 'stand')
        
        self.world_offset = world_offset
        self.rect.update(self.x, self.y, self.width, self.height)

        # Add frame to enemy
        pygame.draw.rect(window,(255,0,0),(self.x  + self.world_offset[0], self.y  + self.world_offset[1], self.width, self.height),2)

        # self.destroy()

        # Returning to update in enemies array - maybe there is a better update way
        return self

    def render(self, window, direction='none'):

        if direction == "left":
            window.blit(self.assets["enemy_left"][self.enemy_left_frame], (self.x + self.world_offset[0], self.y + self.world_offset[1]))
            self.enemy_left_frame = (self.enemy_left_frame + 1) % len(self.assets["enemy_left"])
        elif direction == "right":
            window.blit(self.assets["enemy_right"][self.enemy_right_frame], (self.x + self.world_offset[0], self.y + self.world_offset[1]))
            self.enemy_right_frame = (self.enemy_right_frame + 1) % len(self.assets["enemy_right"])
        else:
            window.blit(self.assets["enemy_stand"][self.enemy_stand_frame], (self.x + self.world_offset[0], self.y + self.world_offset[1]))
            self.enemy_stand_frame = (self.enemy_stand_frame + 1) % len(self.assets["enemy_stand"])
        
        ENEMY_LOCATION = FONT.render(
                f"Enemy Location: {self.x//PIXELS_IN_TILE, self.y//PIXELS_IN_TILE}", 1, (255, 255, 255)
        )

        ENEMY_X_Y = FONT.render(
                f"Enemy XY: {self.x, self.y}", 1, (255, 255, 255)
        )

        ENEMY_WORLD_OFFSET = FONT.render(
                f"Enemy WOFFSET: {self.world_offset[0], self.world_offset[1]}", 1, (255, 255, 255)
        )
    
        window.blit(ENEMY_LOCATION, (50, 80))
        window.blit(ENEMY_X_Y, (50, 110))
        window.blit(ENEMY_WORLD_OFFSET, (50, 140))



class Animate:
    def __init__(self, tmxdata, x=750, y=222, tile_x = 21, tile_y = 16):
        self.x = x
        self.y = y   #640 - 418
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.last_update = pygame.time.get_ticks()

        tile_props = tmxdata.get_tile_properties(tile_x, tile_y, 0)

        self.frames = [
             {
              'img':pygame.transform.scale(tmxdata.get_tile_image_by_gid(tile.gid),(PIXELS_IN_TILE,PIXELS_IN_TILE)) ,
              'duration': tile.duration,
              'index': index 
             }
             for index, tile in enumerate(tile_props['frames'])
        ] 
        
        # Init
        self.frame = self.frames[0]

        self.assets = {
            "frames": self.frames, # load animated tiles here...
        }

    def update(self, window, world_offset):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame['duration']:
            self.last_update = pygame.time.get_ticks()
            self.frame = self.frames[(self.frame['index'] + 1) % len(self.assets["frames"])]

        self.x = (self.tile_x * PIXELS_IN_TILE) + world_offset[0]
        self.y = (self.tile_y * PIXELS_IN_TILE) + world_offset[1]
        self.render(window)

    def render(self, window):
        window.blit(self.frame['img'], (self.x, self.y+10))
        

class PhysicsEntity(pygame.sprite.Sprite):

    def __init__(self, game, x=0, y=0, debug=False):
        super().__init__()
        self.x = x
        self.y = y   #640 - 418
        self.width = 40
        self.height = 56

        # Add rectangle for collisions - maybe there is a better way to handle collisions
        self.image = pygame.Surface((self.width,self.height))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)

        self.inventory = []
        self.points = 0
        self.direction = "stand"
        self.player_last_direction_x = "right"
        self.player_jump_frame = 0
        
        self.debug = debug

        self.assets = {
            "player_stand": load_images("entities/player/idle"),
            "player_jump": load_images("entities/player/jump"),
            "player_land": load_images("entities/player/slide"),
            "player_right": load_images("entities/player/run"),
            "player_left": load_images("entities/player/run", True),
        }

        self.player_left_frame = 0
        self.player_right_frame = 0
        self.player_stand_frame = 0 
        
        self.LR_MOVMENT_OFFSET = 15
        self.PLAYER_JUMP_HEIGHT = 23

        self.game = game

    def update(self, tmxdata, window):

        # ******** Collisions ********

        # bottom center player sprite
        try:
            standing_on = get_tile_properties(
                tmxdata, self.x + int(self.width / 2), self.y + self.height, self.game.world_offset
            )
        except Exception as e:
            print(f'exception error standing on {standing_on}')                    

        
        # middle center player sprite
        try:
            touching = get_tile_properties(
                tmxdata, self.x + int(self.width / 2), self.y + int(self.height / 2), self.game.world_offset
            )
        except Exception as e:
            print(f'exception error standing on {touching}')                    
        
        try:            
            if touching.get('health') != None:
                self.game.health += touching["health"]
            
            if touching.get('points') != None:
                self.points += touching["points"]

            # print(touching)

            tile_x = int(touching["x"])
            tile_y = int(touching["y"])

            if self.game.health < 0:
                quit = True

            # if touching['id'] == 73:
            if touching.get('remove') != None and touching["remove"] == True:
                tmxdata.layers[0].data[tile_y][tile_x] = 0

            if touching.get('provides') != None and touching["provides"] != '' and touching["provides"] != None:
                self.inventory.append(touching["provides"])
                print(f"got {touching["provides"]} !")
                tmxdata.layers[0].data[tile_y][tile_x] = 0

            if touching.get('requires') != None and touching["requires"] != '' and touching["requires"] != None:
                if touching["requires"] in self.inventory:
                    print(f"looking for {touching["requires"]} !")
                    if touching["requires"] == "key":
                        print(f"used {touching["requires"]} !")
                        self.inventory.remove(touching["requires"])
                        tmxdata.layers[0].data[tile_y][tile_x] = tmxdata.layers[1].data[tile_y][tile_x]
                        if tile_y == 29 and tile_x == 22: # 1st Door
                            #  print(world_offset)
                            self.game.world_offset[0] = self.game.world_offset[0] - 180 * 16 # move right 150 grids each 16
                            self.game.world_offset[1] = self.game.world_offset[1] - 1 * 16 # move up 1 grids each 16
                        elif tile_y == 30 and tile_x == 86: # 2st Door
                            #  print(self.game.world_offset)
                            self.game.world_offset[0] = self.game.world_offset[0] - 183 * 16 # move right 150 grids each 16
                            #  self.game.world_offset[1] = self.game.world_offset[1] - 20 # move up 2 grids each 16
                        elif tile_y == 18 and tile_x == 154: # 3st Door
                            #  print(self.game.world_offset)
                            self.game.world_offset[0] = self.game.world_offset[0] + 183 * 16 # move right 150 grids each 16
                            self.game.world_offset[1] = self.game.world_offset[1] + 5 * 16 # move up 2 grids each 16

            if touching.get('npc') != None:
                self.game.dialog = True
            else:
                self.game.dialog = False

        except KeyError:
            print(f'key error touching on {touching}')    
        
        
        # ******** Your LEFT & RIGHT game logic here **************
        keypressed = pygame.key.get_pressed()
        # print(keypressed)
        if keypressed[ord("a")]:
            left_tile = get_tile_properties(
                tmxdata,
                self.x,  # - LR_MOVMENT_OFFSET
                self.y + self.height - 16,
                self.game.world_offset,
            )  # center middle +10 on x
            if left_tile["solid"] == 0:
                self.x = self.x - self.LR_MOVMENT_OFFSET
                self.direction = "left"
                self.player_last_direction_x = "left"
                # print(left_tile)

        if keypressed[ord("d")]:
            right_tile = get_tile_properties(
                tmxdata,
                self.x + self.width,  # + self.LR_MOVMENT_OFFSET
                self.y + self.height - 16,
                self.game.world_offset,
            )  # center middle +10 on x
            if right_tile["solid"] == 0:
                self.x = self.x + self.LR_MOVMENT_OFFSET
                self.direction = "right"
                self.player_last_direction_x = "right"
                # print(right_tile)

        try:
            if keypressed[pygame.K_SPACE]:
                if standing_on["climable"] == 1:
                    self.y = self.y - 10
                if standing_on["ground"] == 1:
                    self.player_jump_frame = self.PLAYER_JUMP_HEIGHT

            if keypressed[ord("s")]:
                if standing_on["climable"] == 1:
                    self.y = self.y + 10
        except KeyError:
            print(f'key error standing on {standing_on}')    

        if sum(keypressed) == 0:  # No key is pressed
            if self.direction != "stand":
                # print(standing_on)
                # print(touching)
                self.direction = "stand"
        
        

        # ******** Your JUMP & FALL game logic here **************

        if self.player_jump_frame > 0:  # Jumping in progress after space pressed

            # center middle +10 on x
            above_tile = get_tile_properties(
                tmxdata, self.x + (self.width / 4), self.y + (self.height / 4), self.game.world_offset
            )
            try:
                if above_tile["solid"] == 0:
                    self.y = self.y - 10
                    self.direction = "jump"
                    self.player_jump_frame -= 1
                else:
                    self.player_jump_frame = 0
            except KeyError:
                print(f'above_tile error {above_tile}')
        else:
            try: 
                if standing_on["ground"] == 0 and standing_on["climable"] == 0:  # Landing/Falling in progress
                    self.y = self.y + 10
                    self.direction = "land"
            except KeyError:
                print(f'landing falling error {standing_on['ground'],standing_on['climable']}')

        self.rect.update(
                            self.x - self.game.world_offset[0], self.y - self.game.world_offset[1], self.width, self.height
                        )

        # Draw rect around enemy        
        pygame.draw.rect(window,(0,0,255),(self.x, self.y, self.width, self.height),2)


        self.render(window, self.direction)
        pass


        
    #def render(self, surf, offset =(0,0)):
    def render(self, window, direction):
        if direction == "left":
            window.blit(self.assets["player_left"][self.player_left_frame], (self.x, self.y))
            self.player_left_frame  = (self.player_left_frame + 1) % len(self.assets["player_left"])

        elif direction == "right":
            window.blit(self.assets["player_right"][self.player_right_frame], (self.x, self.y))
            self.player_right_frame = (self.player_right_frame + 1) % len(self.assets["player_right"])

        elif direction == "jump":
            if self.player_last_direction_x == "right":
                window.blit(self.assets["player_jump"][0], (self.x, self.y))
            else:
                window.blit(pygame.transform.flip(self.assets["player_jump"][0],True, False), (self.x, self.y))
            
        elif direction == "land":
            if self.player_last_direction_x == "right":
                window.blit(self.assets["player_land"][0], (self.x, self.y))
            else:
                window.blit(pygame.transform.flip(self.assets["player_land"][0],True, False), (self.x, self.y))

        else:
            if self.player_last_direction_x == "right":
                window.blit(self.assets["player_stand"][self.player_stand_frame], (self.x, self.y))
            else:
                window.blit(pygame.transform.flip(self.assets["player_stand"][self.player_stand_frame], True, False), (self.x, self.y))
            self.player_stand_frame = (self.player_stand_frame + 1) % len(self.assets["player_stand"])



