from os.path import isfile

import pygame
import sys
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from random import randint
from game_stats import GameStats
from time import sleep
import sound_effects as se
from button import Button
from scoreboard import Scoreboard
from explosion import Explosion

class SidewaysShooter:
    """New class to define new game"""

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((1600, 900), pygame.RESIZABLE)
        self.caption = pygame.display.set_caption("Sideways shooter")
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.explosion = Explosion(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, "Play")

    def run_game(self):
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self.update_screen()

    def update_screen(self):
        self.screen.blit(self.settings.background, (0, 0))
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            se.explosion_sound.play()
            self.explosion.blitme()
            sleep(0.5)
        else:
            self.stats.game_active = False

    def _update_aliens(self):
        self.aliens.update()
        self._check_fleet_edges()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            self._check_aliens_bottom()

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.aliens.remove(alien)

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        ship_height = self.ship.rect.height
        ship_width = self.ship.rect.width
        avaiable_space_y = self.settings.screen_height - alien_height
        number_rows = avaiable_space_y // ship_height
        avaiable_space_x = self.settings.screen_width - ship_width - 3 * alien_width
        number_aliens_x = avaiable_space_x // (int(1 * alien_width))
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        random_number = randint(0, row_number)
        random_number_x = randint(0, alien_number)
        alien.x = (int(2 * alien_width)) * random_number_x
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + (int(2 * alien.rect.height)) * random_number
        self.aliens.add(alien)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._fire_bullet()
            elif event.type == pygame.QUIT:
                    sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            if isfile('./Current_HighScore.txt'):
                with open('./Current_HighScore.txt', 'a') as file:
                    file.truncate(0)
                    file.write(str(self.stats.high_score))
            elif not isfile('./Current_HighScore.txt'):
                with open('./Current_HighScore.txt', 'w') as file:
                    file.write(str(self.stats.high_score))
            # if q is pressed quit the game
            sys.exit()

        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_RETURN:
            self._check_play_button()

    def _check_play_button(self):
        """Start a new game when the player clicks Play."""
        button_clicked = pygame.K_RETURN
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_images()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
            elif bullet.rect.left <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            self._start_new_level()
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
            se.alien_sound.play()

    def _start_new_level(self):
        self._create_fleet()
        self.bullets.empty()
        self.settings.increase_speed()
        self.stats.level += 1
        self.sb.prep_level()



    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.right > screen_rect.right:
                self._ship_hit()
                break

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            se.bullet_sound.play()


if __name__ in '__main__':
    ai = SidewaysShooter()
    ai.run_game()
