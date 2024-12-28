import pygame
from utils import get_tile_properties_enemies, load_images, drawInticator
from weapons import Shovel
from wearables import Band

PIXELS_IN_TILE = 32


class NPC(pygame.sprite.Sprite):
    def __init__(
        self,
        game,
        x=400,
        y=200,
        directions=["stand"],
        name="default",
    ):
        from main import Game

        """Enemy Object

        Args:
            game (_type_): _description_
            x (int, optional): _description_. Defaults to 400.
            y (int, optional): _description_. Defaults to 200.
            directions (list, optional): _description_. Defaults to ["stand", "left", "stand", "right"].
        """
        super().__init__()

        self.enemy_width = 50
        self.enemy_height = 70
        self.name = name
        self.x = x
        self.y = y
        self.is_alive = True
        self.game: Game = game
        self.health = 100
        self.moving_x_direction = 0
        self.assets = {
            "enemy_stand": load_images("entities/enemy/idle"),
            "enemy_right": load_images("entities/enemy/run"),
            "enemy_left": load_images("entities/enemy/run", True),
        }

        self.directions = directions
        self.last_update = pygame.time.get_ticks()
        self.last_direction_index = 0
        self.last_direction = "stand"
        self.group_index = 0

        self.enemy_stand_frame = 0
        self.enemy_right_frame = 0
        self.enemy_left_frame = 0
        self.enemy_jump_frame = 0

        self.LAST_DIRECTION = ""

        # Maintain our direction
        self.direction = "stand"
        self.standing_on = None
        self.touching = None
        self.ray_casting = None
        self.animate = True

        self.image = pygame.Surface((self.enemy_width, self.enemy_height))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.vector = pygame.Vector2(self.rect.center)

        # Adding the sword as an attribute
        self.shovel = Shovel(self)
        self.shovel.attack_direction = "right"
        self.last_fired = 0

        # Adding wearables
        self.band = Band(self)

        # Spoke to hero
        self.spoke_to_hero = False

    def update(self, tmxdata, window):

        now = pygame.time.get_ticks()

        # ******** Collisions ********

        # Bottom Center enemy Sprite
        # -----
        # |   | <<--
        # |   | -->>
        # -----

        # Stanging On Logic HERE ↓ (collision)
        self.standing_on = get_tile_properties_enemies(
            tmxdata,
            self.x + int(self.enemy_width / 2),
            self.y + self.enemy_height,
            self.game.world_offset,
        )

        # standing
        # drawInticator(
        #     window,
        #     self.x + int(self.enemy_width / 2) + self.game.world_offset[0],
        #     self.y + self.enemy_height + self.game.world_offset[1],
        #     (255, 0, 255),
        # )

        # Ray Casting Logic HERE ↓ (collision)
        self.ray_casting = get_tile_properties_enemies(
            tmxdata,
            self.x + self.moving_x_direction,
            self.y + self.enemy_height,
            self.game.world_offset,
        )

        # ray_casting
        drawInticator(
            window,
            self.x + self.moving_x_direction + self.game.world_offset[0],
            self.y + self.enemy_height + self.game.world_offset[1],
            (255, 0, 255),
        )

        # Animation - Select Direction ↓ (animation)
        if now - self.last_update > 1000 and self.animate == True:
            self.last_update = now
            self.last_direction_index = (self.last_direction_index + 1) % len(
                self.directions
            )
            self.last_direction = self.directions[self.last_direction_index]
            self.ray_casting = {"ground": 1}  # TODO: use the default array from utils

            # LEFT/RIGHT logic HERE ↓ (collision)
        if self.animate == True:
            if self.ray_casting["ground"] != 0:
                if self.last_direction == "left":
                    left_tile = get_tile_properties_enemies(
                        tmxdata,
                        self.x,  # - LR_MOVMENT_OFFSET
                        self.y + self.enemy_height - 16,
                        self.game.world_offset,
                    )  # center middle +10 on x

                    if left_tile["solid"] == 0:
                        self.x = self.x - 15
                        self.LAST_DIRECTION = self.direction = "left"

                if self.last_direction == "right":
                    right_tile = get_tile_properties_enemies(
                        tmxdata,
                        self.x + self.enemy_width,  # - LR_MOVMENT_OFFSET
                        self.y + self.enemy_height - 16,
                        self.game.world_offset,
                    )  # center middle +10 on x

                    if right_tile["solid"] == 0:
                        self.x = self.x + 15
                        self.LAST_DIRECTION = self.direction = "right"

                # if self.last_direction == "jump":
                #     if self.standing_on["ground"] == 1:
                #         self.enemy_jump_frame = 40

                # if keypressed[ord("s")]:
                #     pass

            if self.last_direction == "stand":  # No key is pressed
                if self.direction != "stand":
                    self.direction = "stand"

            # JUMP/FALL logic HERE ↓ (movment)

            if self.enemy_jump_frame > 0:  # Jumping in progress

                # Get Tile Above - Check for ground - Axis Y
                above_tile = get_tile_properties_enemies(
                    tmxdata,
                    self.x + (self.enemy_width / 2),  # - LR_MOVMENT_OFFSET
                    self.y + (self.enemy_height / 2),
                    self.game.world_offset,
                )

                pygame.draw.rect(
                    window,
                    (255, 0, 0),
                    (
                        # Where
                        self.x + self.game.world_offset[0] + (self.enemy_width / 2),
                        self.y + self.game.world_offset[1] + (self.enemy_height / 2),
                        # What
                        self.enemy_width,
                        self.enemy_height,
                    ),
                    2,
                )

                if above_tile["ground"] == 0:
                    self.y = self.y - 10
                    self.direction = "jump"
                    self.enemy_jump_frame -= 1  # 20 - 1
                else:
                    self.enemy_jump_frame = 0

        if self.standing_on["ground"] == 0:
            self.y = self.y + 10
            self.direction = "land"

        # Touching logic x axis HERE ↓ (collision)

        touchingX = self.x + self.moving_x_direction
        touchingY = self.y + self.enemy_height - 20

        if self.direction == "right":
            self.moving_x_direction = self.enemy_width
        if self.direction == "left":
            self.moving_x_direction = 0

        # Get Tile Aside - Check for solid - Axis X
        # Getting corrent tile using touchingX, touchingY without world offset
        self.touching = get_tile_properties_enemies(
            tmxdata, touchingX, touchingY, self.game.world_offset
        )

        # ememy object top corner - self.x
        pygame.draw.rect(
            window,
            (0, 0, 255),
            (
                # Where
                self.x + self.game.world_offset[0],
                self.y + self.game.world_offset[1],
                # What
                self.enemy_width,
                self.enemy_height,
            ),
            2,
        )

        # touching down - using touchingY + movment
        # render -> x = self.x + world_offset[0]
        drawInticator(
            window,
            touchingX + self.game.world_offset[0],
            touchingY + self.game.world_offset[1],
            (128, 128, 128),
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
                # Getting corrent tile using touchingX, touchingY without world offset
                tile_x = (touchingX) // PIXELS_IN_TILE
                tile_y = (touchingY) // PIXELS_IN_TILE
                print(f"Tile Removed{tile_x,tile_y}")
                tmxdata.layers[0].data[tile_y][tile_x] = 0

        self.rect.center = (
            self.x + self.game.world_offset[0],
            self.y + self.game.world_offset[1],
        )

        selfVector = pygame.Vector2(self.rect.center)
        enemyVector = pygame.Vector2(self.game.enemy.rect.center)
        distance = selfVector.distance_to(enemyVector)

        # print(distance)
        # print(self.shovel.detached)

        # Update the sword position to follow the enemy
        self.shovel.update_position(self.LAST_DIRECTION)
        self.band.update_position(self.LAST_DIRECTION)

        # if distance < 300:

        #     self.shovel.attack_direction = (
        #         "right" if enemyVector.x - selfVector.x > 0 else "left"
        #     )

        #     # Attach shovel if a in attack mode every second
        #     if now - self.last_fired > 1000 and self.shovel.detached == False:

        #         self.shovel.last_direction = self.shovel.attack_direction
        #         self.last_fired = now
        #         self.shovel.attack(self.last_direction)
        #         self.shovel.detached = True

        #         self.animate = False
        #         self.direction = "stand"

        #     # Detach shovel if a in attack mode every second
        #     if now - self.last_fired > 3000 and self.shovel.detached == True:
        #         # Adding the sword as an attribute
        #         self.shovel = Shovel(self)

        #     self.LAST_DIRECTION = self.shovel.attack_direction
        # else:
        #     self.animate = True

        # Update the sword position to follow the enemy
        self.shovel.update_position(self.LAST_DIRECTION)

    def render(self, window, world_offset):
        # Draw the enemy with offset - not to move with window
        x = self.x + world_offset[0]
        y = self.y + world_offset[1]
        if self.direction == "left":
            window.blit(self.assets["enemy_left"][self.enemy_left_frame], (x, y))
            self.enemy_left_frame = (self.enemy_left_frame + 1) % len(
                self.assets["enemy_left"]
            )

        elif self.direction == "right":
            window.blit(self.assets["enemy_right"][self.enemy_right_frame], (x, y))
            self.enemy_right_frame = (self.enemy_right_frame + 1) % len(
                self.assets["enemy_right"]
            )

        else:  # stand
            if self.LAST_DIRECTION == "left":
                window.blit(
                    pygame.transform.flip(
                        self.assets["enemy_stand"][self.enemy_stand_frame],
                        True,
                        False,
                    ),
                    (x, y),
                )
                self.enemy_stand_frame = (self.enemy_stand_frame + 1) % len(
                    self.assets["enemy_stand"]
                )
            else:
                window.blit(
                    self.assets["enemy_stand"][self.enemy_stand_frame],
                    (x, y),
                )
                self.enemy_stand_frame = (self.enemy_stand_frame + 1) % len(
                    self.assets["enemy_stand"]
                )

        # touching
        drawInticator(
            window,
            self.shovel.rect.x,
            self.shovel.rect.y,
            (255, 0, 255),
            self.shovel.rect.width,
            self.shovel.rect.height,
        )

        window.blit(
            pygame.transform.flip(
                self.shovel.image,
                True,
                False,
            ),
            (self.shovel.rect.x, self.shovel.rect.y),
        )

        window.blit(
            self.band.image,
            (self.band.rect.x, self.band.rect.y),
        )

    def takeDamage(self, damage: int = 10):
        self.health -= damage
        if self.health < 0 and self.is_alive == True:
            self.is_alive = False
            enemy_in_group = self.game.enemies_group[self.group_index]
            enemy_in_group.rect.x = enemy_in_group.x = 0
            enemy_in_group.rect.y = enemy_in_group.y = 0
