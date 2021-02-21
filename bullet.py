import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_game):
        """Create bullet object at current ship position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        #Create a bullet rect at (0,0) and the set correct position.
        self.rect = pygame.Rect(0,0, self.settings.bullet_width, self.settings.bullet_heigth)
        self.rect.center = ai_game.ship.rect.center

        #Store bullet position as decimal value
        self.x = float(self.rect.x)

    def update(self):
        """Move the bullet up the screen."""
        #Update the decimal possition of the bullet.
        self.x -= self.settings.bullet_speed
        #Update the rect position
        self.rect.x = self.x

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)