# Sword class
import pygame

from utils import load_image


class Sword(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        # self.image = pygame.Surface((30, 100))
        # self.image.fill((150, 75, 0))  # Brown color for the sword

        self.image = load_image("sword.png")
        self.image = pygame.transform.scale(self.image, (30, 100))
        self.image = pygame.transform.rotate(self.image, 45)  # Rotate by 45 degrees
        self.rect = self.image.get_rect()

        # Link sword to the player
        self.player = player
        self.update_position()

    def update_position(self):
        # Position the sword to the right of the player
        self.rect.midleft = self.player.rect.midright
