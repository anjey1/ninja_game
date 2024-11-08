import pygame
from entities import Entity
from enemies import Enemy

pygame.font.init()
FONT = pygame.font.SysFont("Arial", 18)


def drawHud(
    window: pygame.Surface, player: Entity, enemy: Enemy, health: int = 0, points=0
):
    """Draws game hood

    Args:
        window (pygame.Surface): _description_
        player (Entity): _description_
        enemy (Enemy): _description_
        health (int, optional): _description_. Defaults to 0.
        points (int, optional): _description_. Defaults to 0.
    """

    POINTS_HUD = FONT.render(f"points: {points}", 1, (255, 255, 255))
    window.blit(POINTS_HUD, (50, 10))

    HEALTH_HUD = FONT.render(f"health: {health}", 1, (255, 255, 255))
    window.blit(HEALTH_HUD, (50, 30))

    PLAYER_LOCATION = FONT.render(f"x, y: {player.x, player.y}", 1, (255, 255, 255))
    window.blit(PLAYER_LOCATION, (50, 50))

    ENEMY_LOCATION = FONT.render(f"Enemy x, y: {enemy.x, enemy.y}", 1, (255, 255, 255))
    window.blit(ENEMY_LOCATION, (50, 70))

    ENEMY_STANDING_ON = FONT.render(
        f"Enemy Standing ON: {enemy.standing_on}", 1, (255, 255, 255)
    )
    window.blit(ENEMY_STANDING_ON, (50, 90))

    ENEMY_TOUCHING = FONT.render(
        f"Enemy Touching ON: {enemy.touching}", 1, (255, 255, 255)
    )
    window.blit(ENEMY_TOUCHING, (50, 110))
