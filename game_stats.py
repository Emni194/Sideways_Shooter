from os.path import isfile


class GameStats:

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False
        if isfile('./Current_HighScore.txt'):
            with open('./Current_HighScore.txt', 'r') as file:
                self.high_score = int(file.read())
        elif not isfile('./Current_HighScore.txt'):
            self.high_score = 0

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1