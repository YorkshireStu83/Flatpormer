class GameStats():
    """A class to track stats for the game"""

    def __init__(self, game_settings, high_score):
        self.game_settings = game_settings
        self.reset_stats()
        self.high_score = high_score

        # Start game in inactive state
        self.game_active = False

    def reset_stats(self):
        """Initialise stats that can change during the game"""
        self.score = 0
        self.game_settings.lives = 3
