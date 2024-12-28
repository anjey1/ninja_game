# Sword class
import pygame

from utils import load_image


class Shovel(pygame.sprite.Sprite):
    def __init__(self, entity):
        super().__init__()
        # self.image = pygame.Surface((30, 100))
        # self.image.fill((150, 75, 0))  # Brown color for the sword
        self.width = 30
        self.height = 60
        self.detached = False
        self.attack_direction = ""
        self.entity = None

        try:
            self.image = load_image("shovel.png")
        except pygame.error as e:
            print(f"Failed to load image: {e}")
            self.image = None

        if self.image is not None:
            self.image_original = pygame.transform.scale(
                self.image, (self.width, self.height)
            )

            self.rect = self.image.get_rect()
            self.vector = pygame.Vector2(self.rect.center)

            # Link sword to the player
            self.entity = entity
            self.update_position()

    def update_position(self, entity_direction="right"):

        if self.detached == False:
            if entity_direction == "right":
                self.image = pygame.transform.rotate(self.image_original, 90)
                self.rect = self.image.get_rect()

                # Adjust the rect for horizontal alignment
                self.rect.width, self.rect.height = self.rect.height, self.rect.width

                # Position the sword to the right of the player
                self.rect.midleft = (
                    self.entity.rect.midbottom[0] + 50,
                    self.entity.rect.midbottom[1],
                )
            elif entity_direction == "left":
                self.image = pygame.transform.rotate(self.image_original, 270)
                self.rect = self.image.get_rect()

                # Adjust the rect for horizontal alignment
                self.rect.width, self.rect.height = self.rect.height, self.rect.width

                self.rect.midleft = (
                    self.entity.rect.midbottom[0] - 50,
                    self.entity.rect.midbottom[1],
                )
            else:
                self.image = pygame.transform.rotate(
                    self.image_original, 0
                )  # Horizontal as default
                self.rect = self.image.get_rect()
                self.rect.width, self.rect.height = self.rect.height, self.rect.width
                self.rect.center = self.entity.rect.center

            self.last_direction = entity_direction

        # move weapon
        elif self.detached == True:

            if self.entity.name == "enemy2":
                print(
                    f"entity: {self.entity.name} , self.LAS_DIRECTION: {entity_direction}"
                )

            self.rect.x = (
                self.rect.x - 15 if self.last_direction == "left" else self.rect.x + 15
            )

            self.rect.y = self.entity.rect.midbottom[1]

        self.vector = pygame.Vector2(self.rect.center)

    # update_position is in charge of weapon movment
    def attack(self, last_direction="right"):
        if self.detached == False:
            if last_direction == "right":
                self.image = pygame.transform.rotate(self.image_original, 90)
                self.rect = self.image.get_rect()

                # Position the sword to the right of the player
                self.rect.midleft = (
                    self.entity.rect.midbottom[0] + 40,
                    self.entity.rect.midbottom[1],
                )

                print(f"fired:{last_direction}")
            elif last_direction == "left":
                self.image = pygame.transform.rotate(self.image_original, 270)
                self.rect = self.image.get_rect()

                self.rect.midleft = (
                    self.entity.rect.midbottom[0] - 50,
                    self.entity.rect.midbottom[1],
                )

                print(f"fired:{last_direction}")


class Sword(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        # self.image = pygame.Surface((30, 100))
        # self.image.fill((150, 75, 0))  # Brown color for the sword
        self.current_angle = 45
        self.direction = 1
        self.width = 30
        self.height = 60
        self.angle = 0

        try:
            self.image = load_image("sword3.png")
        except pygame.error as e:
            print(f"Failed to load image: {e}")
            self.image = None

        if self.image is not None:
            self.image_original = pygame.transform.scale(
                self.image, (self.width, self.height)
            )

            self.rect = self.image.get_rect()

            # Link sword to the player
            self.player = player
            self.update_position()

        # self.image = pygame.transform.rotate(
        #     self.image, -self.current_angle
        # )  # Rotate by 45 degrees

    def update_position(self, last_direction="left"):

        self.image = pygame.transform.rotate(
            self.image_original, self.angle
        )  # Horizontal as default
        self.rect = self.image.get_rect()

        self.angle = 110 if last_direction == "left" else 250

        self.rect.center = (
            self.player.rect.midbottom[0] + 25,
            self.player.rect.midbottom[1] + 30,
        )

        # Update the angle
        # self.current_angle += 5 * self.direction
        # if self.current_angle >= 85 or self.current_angle <= 45:
        #     self.direction *= -1  # Reverse direction at the bounds

        return self.current_angle

    def attack(self, last_direction="left"):
        if last_direction == "right":
            self.image = pygame.transform.rotate(self.image_original, 90)
            self.rect = self.image.get_rect()

            # Position the sword to the right of the player
            self.rect.midleft = (
                self.player.rect.midbottom[0] + 40,
                self.player.rect.midbottom[1],
            )

        elif last_direction == "left":
            self.image = pygame.transform.rotate(self.image_original, 270)
            self.rect = self.image.get_rect()

            self.rect.midleft = (
                self.player.rect.midbottom[0] - 50,
                self.player.rect.midbottom[1],
            )
