# Sword class
import pygame

from utils import load_image


class Sword(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        # self.image = pygame.Surface((30, 100))
        # self.image.fill((150, 75, 0))  # Brown color for the sword
        self.current_angle = 45
        self.direction = 1
        self.width = 30
        self.height = 60

        self.image = load_image("sword3.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image = pygame.transform.rotate(
            self.image, -self.current_angle
        )  # Rotate by 45 degrees
        self.rect = self.image.get_rect()

        # Link sword to the player
        self.player = player
        self.update_position()

    def update_position(self, player_direction="left"):

        if player_direction == "right":
            # Position the sword to the right of the player
            self.rect.midleft = self.player.rect.midright
        elif player_direction == "left":
            self.rect.midleft = self.player.rect.midleft
        else:
            self.rect.midleft = self.player.rect.midright

        # Update the angle
        self.current_angle += 5 * self.direction
        if self.current_angle >= 85 or self.current_angle <= 45:
            self.direction *= -1  # Reverse direction at the bounds

        return self.current_angle
