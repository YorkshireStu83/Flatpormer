class Settings():
    """A class to store settings for the test game"""

    def __init__(self):
        """Initialise the game's settings"""
        self.screen_width = 1500
        self.screen_height = 780
        self.bg_colour = (0, 25, 0)

        self.movement_speed = 3
        self.jumping_speed = 2
        self.gravity = 2
        self.jump_height = 450
        self.enemy_speed = 1

        self.score_increment = 100
        self.lives = 3


