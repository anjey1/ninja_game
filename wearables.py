# Sword class
import pygame

from utils import load_image


class Band(pygame.sprite.Sprite):
    def __init__(self, entity):
        super().__init__()
        # self.image = pygame.Surface((30, 100))
        # self.image.fill((150, 75, 0))  # Brown color for the sword

        # Band
        # self.width = 8
        # self.height = 2

        # Helmet
        self.width = 70
        self.height = 60
        self.entity = None
        self.image = None
        self.entity_previous_direction = "right"

        try:
            # self.image = load_image("/wear/band.png")
            self.image = load_image("/wear/helmet.png")
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
        self.last_direction = (
            entity_direction if entity_direction != "" else self.last_direction
        )

        if entity_direction == "left" and self.entity_previous_direction != "left":
            self.image = pygame.transform.flip(self.image, True, False)
            self.entity_previous_direction = "left"
        elif entity_direction == "right" and self.entity_previous_direction != "right":
            self.image = pygame.transform.flip(self.image, True, False)
            self.entity_previous_direction = "right"

        self.rect = self.image.get_rect()

        self.rect.center = (
            self.entity.rect.midbottom[0] + 25,
            self.entity.rect.midbottom[1] - 18,
        )

        self.last_direction = entity_direction
