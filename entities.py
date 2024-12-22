import pygame
from pytmx.util_pygame import load_pygame
from utils import get_tile_properties, load_images, drawInticator
from weapons import Sword

PIXELS_IN_TILE = 32


class Entity(pygame.sprite.Sprite):
    def __init__(self, game, x=0, y=0):
        from main import Game

        """Player Object

        Args:
            game (_type_): _description_
            x (int, optional): Initital X position. Defaults to 400.
            y (int, optional): Initital Y position. Defaults to 200.
        """
        super().__init__()  # init sprite parent class for collisions
        self.player_width = 50
        self.player_height = 70
        self.x = x
        self.y = y
        self.game: Game = game
        self.moving_x_direction = 0
        self.assets = {
            "player_stand": load_images("entities/player/idle"),
            "player_jump": load_images("entities/player/jump"),
            "player_land": load_images("entities/player/slide"),
            "player_right": load_images("entities/player/run"),
            "player_left": load_images("entities/player/run", True),
        }

        # Add rectangle for collisions - maybe there is a better way to handle collisions
        self.image = pygame.Surface((self.player_width, self.player_height))
        self.rect = self.image.get_rect()
        self.vector = pygame.Vector2(self.rect.center)

        # Adding the sword as an attribute
        self.sword = Sword(self)

        self.player_stand_frame = 0
        self.player_right_frame = 0
        self.player_left_frame = 0
        self.player_jump_frame = 0

        self.LAST_DIRECTION = "right"

        # Maintain our direction
        self.direction = "stand"

        self.image = pygame.Surface((self.player_width, self.player_height))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self, tmxdata, window: pygame.Surface):

        keypressed = pygame.key.get_pressed()

        # ******** Collisions ********

        # Bottom Center Player Sprite
        # -----
        # |   | <<--
        # |   | -->>
        # -----
        # Get Tile Below - Check for ground - Axis Y
        standing_on = get_tile_properties(
            tmxdata,
            self.x + int(self.player_width / 2),
            self.y + self.player_height + 2,
            self.game.world_offset,
        )

        # standing on
        drawInticator(
            window,
            self.x + int(self.player_width / 2),
            self.y + self.player_height,
            (255, 0, 255),
        )

        # Monitor x Movment (Direction)
        # ******** Your LEFT/RIGHT  logic here **************
        if keypressed[ord("a")]:
            left_tile = get_tile_properties(
                tmxdata,
                self.x,  # - LR_MOVMENT_OFFSET
                self.y + self.player_height - 16,
                self.game.world_offset,
            )  # center middle +10 on x

            if left_tile["solid"] == 0:
                self.x = self.x - 30
                self.LAST_DIRECTION = self.direction = "left"

        if keypressed[ord("d")]:
            right_tile = get_tile_properties(
                tmxdata,
                self.x + self.player_width,  # - LR_MOVMENT_OFFSET
                self.y + self.player_height - 16,
                self.game.world_offset,
            )  # center middle +10 on x

            if right_tile["solid"] == 0:
                self.x = self.x + 30
                self.LAST_DIRECTION = self.direction = "right"

        if keypressed[ord(" ")]:
            if standing_on["ground"] == 1:
                self.player_jump_frame = 40

        if sum(keypressed) == 0:  # No key is pressed
            if self.direction != "stand":
                self.direction = "stand"

        # ******** Your JUMP/FALL  logic here **************
        # Understand how landing works... something there
        if self.player_jump_frame > 0:  # Jumping in progresss

            # Get Tile Above - Check for ground - Axis Y
            above_tile = get_tile_properties(
                tmxdata,
                self.x + int(self.player_width / 2),
                self.y + int(self.player_height / 2),
                self.game.world_offset,
            )

            if above_tile["ground"] == 0:
                self.y = self.y - 10
                self.direction = "jump"
                self.player_jump_frame -= 1  # 20 - 1
            else:
                self.player_jump_frame = 0

        elif standing_on["ground"] == 0:
            self.y = self.y + 10
            self.direction = "land"

        # Update the sword position to follow the player
        self.sword.update_position(self.LAST_DIRECTION)

        if keypressed[ord("s")]:
            # Update the sword position to follow the player
            self.sword.attack(self.LAST_DIRECTION)

        # Touching logic x axis

        touchingX = self.x + self.moving_x_direction
        touchingY = self.y + self.player_height - 20

        if self.direction == "right":
            self.moving_x_direction = self.player_width // 2
        if self.direction == "left":
            self.moving_x_direction = 0

        # Get Tile Aside - Check for solid - Axis X
        touching = get_tile_properties(
            tmxdata,
            touchingX,
            touchingY,
            self.game.world_offset,
        )

        # touching
        # render -> self.x
        drawInticator(
            window,
            touchingX,
            touchingY,
            (255, 0, 255),
        )

        # ememy object top corner - self.x
        pygame.draw.rect(
            window,
            (0, 0, 255),
            (
                # Where
                self.x,
                self.y,
                # What
                self.player_width,
                self.player_height,
            ),
            2,
        )

        if touching.get("id") != None:
            pass
            # print(touching['id'])

        if touching.get("health") != None:
            self.game.health += touching["health"]
            if self.game.health < 0:
                self.game.quit = True

        if touching.get("points") != None:
            self.game.points += touching["points"]
            if touching.get("remove") is not None and touching["remove"] == True:
                tile_x = (touchingX - self.game.world_offset[0]) // PIXELS_IN_TILE
                tile_y = (touchingY - self.game.world_offset[1]) // PIXELS_IN_TILE
                print(f"Tile Removed{tile_x,tile_y}")
                tmxdata.layers[0].data[tile_y][tile_x] = 0

        if touching.get("teleport") != None:
            if self.game.current_map_verbose == "map":
                self.game.tmxdata = load_pygame(self.game.location_maps["cave"])
                self.game.current_map_verbose = "cave"

            else:
                self.game.tmxdata = load_pygame(self.game.location_maps["map"])
                self.game.current_map_verbose = "map"

        # Update rect location
        self.rect.center = (self.x, self.y)
        self.vector = pygame.Vector2(self.rect.center)

    def render(self, tmxdata, window):
        # Draw the player
        if self.direction == "left":
            window.blit(
                self.assets["player_left"][self.player_left_frame], (self.x, self.y)
            )
            self.player_left_frame = (self.player_left_frame + 1) % len(
                self.assets["player_left"]
            )

        elif self.direction == "right":
            window.blit(
                self.assets["player_right"][self.player_right_frame], (self.x, self.y)
            )
            self.player_right_frame = (self.player_right_frame + 1) % len(
                self.assets["player_right"]
            )

        elif self.direction == "jump":
            if self.LAST_DIRECTION == "left":
                window.blit(
                    pygame.transform.flip(self.assets["player_jump"][0], True, False),
                    (self.x, self.y),
                )
            else:
                window.blit(self.assets["player_jump"][0], (self.x, self.y))

        elif self.direction == "land":
            if self.LAST_DIRECTION == "left":
                window.blit(
                    pygame.transform.flip(self.assets["player_land"][0], True, False),
                    (self.x, self.y),
                )
            else:
                window.blit(self.assets["player_land"][0], (self.x, self.y))

        else:  # stand
            if self.LAST_DIRECTION == "left":
                window.blit(
                    pygame.transform.flip(
                        self.assets["player_stand"][self.player_stand_frame],
                        True,
                        False,
                    ),
                    (self.x, self.y),
                )
                self.player_stand_frame = (self.player_stand_frame + 1) % len(
                    self.assets["player_stand"]
                )
            else:
                window.blit(
                    self.assets["player_stand"][self.player_stand_frame],
                    (self.x, self.y),
                )
                self.player_stand_frame = (self.player_stand_frame + 1) % len(
                    self.assets["player_stand"]
                )

        # Sword
        # self.sword.image = pygame.transform.rotate(
        #     self.sword.image, self.sword.current_angle
        # )  # Rotate by 45 degrees

        # touching
        drawInticator(
            window,
            self.sword.rect.x,
            self.sword.rect.y,
            (255, 0, 255),
            self.sword.rect.width,
            self.sword.rect.height,
        )

        window.blit(
            pygame.transform.flip(
                self.sword.image,
                True,
                False,
            ),
            (self.sword.rect.x, self.sword.rect.y),
        )
