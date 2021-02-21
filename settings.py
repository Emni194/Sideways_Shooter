import pygame


class Settings:
    """Initialize settings for game"""

    def __init__(self):
        """Manage settings"""

        self.screen_width = 896
        self.screen_height = 672
        self.bg_color = (255, 255, 255)
        self.ship_speed = 10
        self.bullet_speed = 10
        self.bullet_color = (60, 60, 60)
        self.bullet_heigth = 120
        self.bullet_width = 80
        self.bullets_allowed = 40
        self.background = pygame.image.load('images/space.bmp')
        self.fleet_speed = 1
        self.alien_speed = 1
        self.ship_limit = 3
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 20
        self.bullet_speed = 20
        self.alien_speed = 1.0
        self.alien_points = 50


    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
