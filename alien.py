from pygame.sprite import Sprite
import pygame

class Alien(Sprite):
    """Class to manage aliens"""
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = pygame.image.load('images/alien.bmp')
        self.screen_rect = self.screen.get_rect()
        self.rect = self.image.get_rect()
        self.rect.bottomleft= self.screen_rect.bottomleft

        self.x = float(self.rect.x)

    def update(self):
        self.x += self.settings.alien_speed
        self.rect.x = self.x

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True