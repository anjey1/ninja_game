import pygame
from utils import load_images, PIXELS_IN_TILE, get_tile_properties


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
        
        self.frame = self.frames[0]

        self.assets = {
            "frames": self.frames, # load animated tiles here...
        }

    def update(self, window, world_offset):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame['duration']:
            self.last_update = pygame.time.get_ticks()
            self.frame = self.frames[(self.frame['index'] + 1) % len(self.assets["frames"])]

        self.x = self.tile_x * PIXELS_IN_TILE + world_offset[0]
        self.y = self.tile_y * PIXELS_IN_TILE + world_offset[1]
        self.render(window)

    def render(self, window):
        window.blit(self.frame['img'], (self.x, self.y))
        

class PhysicsEntity:

    def __init__(self, game, x=710, y=222, debug=False):
        self.x = x
        self.y = y   #640 - 418
        self.width = 40
        self.height = 56
        self.inventory = []
        self.points = 0
        self.direction = "stand"
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
        # self.type = e_type
        # self.pos = list(pos) # covert itirable into list
        # self.size = size
        # self.velocity = [0,0]
        # self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        # self.action = ''
        # self.anim_offset = (-3, -3) # overlay player image (8,15)
        # self.flip = False
        # self.set_action('idle')

    # def rect(self):
    #     return pygame.Rect(
    #         self.pos[0],
    #         self.pos[1],
    #         self.size[0],
    #         self.size[1],
    #         )

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()

    def update(self, tmxdata, window):

        # ******** Collisions ********

        # bottom center player sprite
        try:
            standing_on = get_tile_properties(
                tmxdata, self.x + int(self.width / 2), self.y + self.height, self.game.world_offset
            )
        except Exception as e:
            print(e)                    

        
        # middle center player sprite
        touching = get_tile_properties(
            tmxdata, self.x + int(self.width / 2), self.y + int(self.height / 2), self.game.world_offset
        )
        
        try:            
            self.game.health += touching["health"]
            self.points += touching["points"]
            # print(touching)

            tile_x = int(touching["x"])
            tile_y = int(touching["y"])

            if self.game.health < 0:
                quit = True

            # if touching['id'] == 73:
            if touching["remove"] == True:
                tmxdata.layers[0].data[tile_y][tile_x] = 0

            if touching["provides"] != '' and touching["provides"] != None:
                self.inventory.append(touching["provides"])
                print(f"got {touching["provides"]} !")
                tmxdata.layers[0].data[tile_y][tile_x] = 0

            if touching["requires"] != '' and touching["requires"] != None:
                if touching["requires"] in self.inventory:
                    print(f"looking for {touching["requires"]} !")
                    if touching["requires"] == "key":
                        print(f"used {touching["requires"]} !")
                        self.inventory.remove(touching["requires"])
                        tmxdata.layers[0].data[tile_y][tile_x] = tmxdata.layers[1].data[tile_y][tile_x]
                        if tile_y == 16 and tile_x == 22: # 1st Door
                            #  print(world_offset)
                            self.game.world_offset[0] = self.game.world_offset[0] - 180 * 16 # move right 150 grids each 16
                            self.game.world_offset[1] = self.game.world_offset[1] - 1 * 16 # move up 1 grids each 16
                        elif tile_y == 17 and tile_x == 86: # 2st Door
                            #  print(self.game.world_offset)
                            self.game.world_offset[0] = self.game.world_offset[0] - 183 * 16 # move right 150 grids each 16
                            #  self.game.world_offset[1] = self.game.world_offset[1] - 20 # move up 2 grids each 16
                        elif tile_y == 5 and tile_x == 154: # 3st Door
                            #  print(self.game.world_offset)
                            self.game.world_offset[0] = self.game.world_offset[0] + 183 * 16 # move right 150 grids each 16
                            self.game.world_offset[1] = self.game.world_offset[1] + 5 * 16 # move up 2 grids each 16
        except KeyError:
            print(touching)
        
        
        # ******** Player events **************
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
            print(standing_on)    

        if sum(keypressed) == 0:  # No key is pressed
            if self.direction != "stand":
                # print(standing_on)
                # print(touching)
                self.direction = "stand"
        
        

        # ******** Your game logic here **************

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
                print(above_tile)
        else:
            try: 
                if standing_on["ground"] == 0 and standing_on["climable"] == 0:  # Landing/Falling in progress
                    self.y = self.y + 10
                    self.direction = "land"
            except KeyError:
                print(standing_on)
    
        self.render(window, self.direction)
        pass


        
    #def render(self, surf, offset =(0,0)):
    def render(self, window, direction):
        # surf.blit(
        #     pygame.transform.flip(self.animation.img(), 
        #     self.flip, 
        #     False,
        #     (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1])
        # ))
        #surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))

        # Draw the player
        # print(f'x: {x} y: {y}')
        # print(direction)
        if direction == "left":
            window.blit(self.assets["player_left"][self.player_left_frame], (self.x, self.y))
            self.player_left_frame = (self.player_left_frame + 1) % len(self.assets["player_left"])
        elif direction == "right":
            window.blit(self.assets["player_right"][self.player_right_frame], (self.x, self.y))
            self.player_right_frame = (self.player_right_frame + 1) % len(self.assets["player_right"])
        elif direction == "jump":
            window.blit(self.assets["player_jump"][0], (self.x, self.y))
        elif direction == "land":
            window.blit(self.assets["player_land"][0], (self.x, self.y))
        else:
            window.blit(self.assets["player_stand"][self.player_stand_frame], (self.x, self.y))
            self.player_stand_frame = (self.player_stand_frame + 1) % len(self.assets["player_stand"])


class Player(PhysicsEntity):
    def __init__(self, game):
        super().__init__(game)

    def update(self):
        super().update()
        

