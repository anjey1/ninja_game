import pygame
from utils import get_tile_properties_enemies, load_images, drawInticator

PIXELS_IN_TILE = 32


class Enemy:
    def __init__(
        self, game, x=400, y=200, directions=["stand", "left", "stand", "right"]
    ):
        """Enemy Object

        Args:
            game (_type_): _description_
            x (int, optional): _description_. Defaults to 400.
            y (int, optional): _description_. Defaults to 200.
            directions (list, optional): _description_. Defaults to ["stand", "left", "stand", "right"].
        """
        self.player_width = 50
        self.player_height = 70
        self.x = x
        self.y = y
        self.game = game
        self.moving_x_direction = 0
        self.assets = {
            "player_stand": load_images("entities/player/idle"),
            "player_jump": load_images("entities/player/jump"),
            "player_land": load_images("entities/player/slide"),
            "player_right": load_images("entities/player/run"),
            "player_left": load_images("entities/player/run", True),
        }

        self.directions = directions
        self.last_update = pygame.time.get_ticks()
        self.last_direction_index = 0
        self.last_direction = "stand"

        self.player_stand_frame = 0
        self.player_right_frame = 0
        self.player_left_frame = 0
        self.player_jump_frame = 0

        self.LAST_DIRECTION = ""

        # Maintain our direction
        self.direction = "stand"
        self.standing_on = None
        self.touching = None

    def update(self, tmxdata, window):

        now = pygame.time.get_ticks()

        # ******** Collisions ********

        # Bottom Center Player Sprite
        # -----
        # |   | <<--
        # |   | -->>
        # -----

        # Stanging On Logic HERE ↓ (collision)
        self.standing_on = standing_on = get_tile_properties_enemies(
            tmxdata,
            self.x + int(self.player_width / 2),
            self.y + self.player_height,
            self.game.world_offset,
        )

        # standing
        drawInticator(
            window,
            self.x + int(self.player_width / 2) + self.game.world_offset[0],
            self.y + self.player_height + self.game.world_offset[1],
            (255, 0, 255),
        )

        # Animation - Select Direction ↓ (animation)
        if now - self.last_update > 1000:
            self.last_update = now
            self.last_direction_index = (self.last_direction_index + 1) % len(
                self.directions
            )
            self.last_direction = self.directions[self.last_direction_index]

        # LEFT/RIGHT logic HERE ↓ (movment)

        if self.last_direction == "left":
            left_tile = get_tile_properties_enemies(
                tmxdata,
                self.x,  # - LR_MOVMENT_OFFSET
                self.y + self.player_height - 16,
                self.game.world_offset,
            )  # center middle +10 on x

            if left_tile["solid"] == 0:
                self.x = self.x - 15
                self.LAST_DIRECTION = self.direction = "left"

        if self.last_direction == "right":
            right_tile = get_tile_properties_enemies(
                tmxdata,
                self.x + self.player_width,  # - LR_MOVMENT_OFFSET
                self.y + self.player_height - 16,
                self.game.world_offset,
            )  # center middle +10 on x

            if right_tile["solid"] == 0:
                self.x = self.x + 15
                self.LAST_DIRECTION = self.direction = "right"

        # if keypressed[ord("w")]:
        #     if standing_on["ground"] == 1:
        #         self.player_jump_frame = 40

        # if keypressed[ord("s")]:
        #     pass

        if self.last_direction == "stand":  # No key is pressed
            if self.direction != "stand":
                self.direction = "stand"

        # JUMP/FALL logic HERE ↓ (movment)

        if self.player_jump_frame > 0:  # Jumping in progress

            # Get Tile Above - Check for ground - Axis Y
            above_tile = get_tile_properties_enemies(
                tmxdata,
                self.x + (self.player_width / 2),  # - LR_MOVMENT_OFFSET
                self.y + (self.player_height / 2),
                self.game.world_offset,
            )

            pygame.draw.rect(
                window,
                (255, 0, 0),
                (
                    # Where
                    self.x + self.game.world_offset[0] + (self.player_width / 2),
                    self.y + self.game.world_offset[1] + (self.player_height / 2),
                    # What
                    self.player_width,
                    self.player_height,
                ),
                2,
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

        # Touching logic x axis HERE ↓ (collision)

        if self.direction == "right":
            self.moving_x_direction = self.player_width
        if self.direction == "left":
            self.moving_x_direction = 0

        # Get Tile Aside - Check for solid - Axis X
        self.touching = get_tile_properties_enemies(
            tmxdata, self.x, self.y + self.player_height - 10, self.game.world_offset
        )

        pygame.draw.rect(
            window,
            (0, 0, 255),
            (
                # Where
                self.x + self.game.world_offset[0],
                self.y + self.game.world_offset[1],
                # What
                self.player_width,
                self.player_height,
            ),
            2,
        )

        # touching
        drawInticator(
            window,
            self.x + self.moving_x_direction + self.game.world_offset[0],
            self.y + self.player_height - 10 + self.game.world_offset[1],
            (255, 0, 255),
        )

        if self.touching.get("id") != None:
            pass
            # print(self.touching["id"])

        if self.touching.get("health") != None:
            self.game.health += self.touching["health"]
            if self.game.health < 0:
                self.game.quit = True

        if self.touching.get("points") != None:
            self.game.points += self.touching["points"]
            if (
                self.touching.get("remove") is not None
                and self.touching["remove"] == True
            ):
                tile_y = (self.y - self.game.world_offset[1] + 50) // PIXELS_IN_TILE
                tile_x = (self.x - self.game.world_offset[0]) // PIXELS_IN_TILE
                print(f"Tile Removed{tile_x,tile_y}")
                tmxdata.layers[0].data[tile_y][tile_x] = 0

    def render(self, window, world_offset):
        # Draw the player with offset - not to move with window
        x = self.x + world_offset[0]
        y = self.y + world_offset[1]
        if self.direction == "left":
            window.blit(self.assets["player_left"][self.player_left_frame], (x, y))
            self.player_left_frame = (self.player_left_frame + 1) % len(
                self.assets["player_left"]
            )

        elif self.direction == "right":
            window.blit(self.assets["player_right"][self.player_right_frame], (x, y))
            self.player_right_frame = (self.player_right_frame + 1) % len(
                self.assets["player_right"]
            )

        elif self.direction == "jump":
            if self.LAST_DIRECTION == "left":
                window.blit(
                    pygame.transform.flip(self.assets["player_jump"][0], True, False),
                    (x, y),
                )
            else:
                window.blit(self.assets["player_jump"][0], (x, y))

        elif self.direction == "land":
            if self.LAST_DIRECTION == "left":
                window.blit(
                    pygame.transform.flip(self.assets["player_land"][0], True, False),
                    (x, y),
                )
            else:
                window.blit(self.assets["player_land"][0], (x, y))

        else:  # stand
            if self.LAST_DIRECTION == "left":
                window.blit(
                    pygame.transform.flip(
                        self.assets["player_stand"][self.player_stand_frame],
                        True,
                        False,
                    ),
                    (x, y),
                )
                self.player_stand_frame = (self.player_stand_frame + 1) % len(
                    self.assets["player_stand"]
                )
            else:
                window.blit(
                    self.assets["player_stand"][self.player_stand_frame],
                    (x, y),
                )
                self.player_stand_frame = (self.player_stand_frame + 1) % len(
                    self.assets["player_stand"]
                )
