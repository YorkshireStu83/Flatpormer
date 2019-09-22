import pygame.font


class ScoreBoard():
    """A class to report scoring information"""

    def __init__(self, game_settings, screen, stats):
        """Initialise scoring attributes"""
        self.game_settings = game_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats

        # Font settings for scorning information
        self.text_colour = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_all_images()

    def prep_all_images(self):
        """Prep all images on game start up"""
        self.prep_score()
        self.prep_lives_image()
        self.prep_lives_indicator()
        self.prep_high_score()

    def prep_score(self):
        """Turn the score into a rendered image"""
        rounded_score = round(self.stats.score, -1)
        score_str = "Score: " + "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_colour)

        # Display the score at the top of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.centerx = self.screen_rect.centerx
        self.score_rect.top = 30

    def prep_lives_image(self):
        """show an image of the player next to the remaining lives"""
        self.lives_image = pygame.image.load("images/Robot.png")
        self.lives_image_rect = self.lives_image.get_rect()
        self.lives_image_rect.right = 50
        self.lives_image_rect.top = 10

    def prep_lives_indicator(self):
        """Turn the number of remaining lives into a rendered image"""
        lives = self.game_settings.lives
        lives_str = " x " + str(lives)
        self.lives = self.font.render(lives_str, True, self.text_colour)

        # Display the remaining lives in the top-left of the screen
        self.lives_rect = self.lives.get_rect()
        self.lives_rect.centerx = self.lives_image_rect.right + (self.lives_rect.width / 2)
        self.lives_rect.top = 30

    def prep_high_score(self):
        """Turn the current high score into a rendered image"""
        high_score = self.stats.high_score
        high_score_str = "High: " + "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_colour)

        # Display the high score in the top-right of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.top = 30
        self.high_score_rect.right = self.screen_rect.right - 20

    def show_images(self):
        """Draw all the images to the screen"""
        self.show_score()
        self.show_lives()
        self.show_high_score()

    def show_score(self):
        """Draw the score to the screen"""
        self.screen.blit(self.score_image, self.score_rect)

    def show_lives(self):
        """Draw the lives image and the number of lives to the screen"""
        self.screen.blit(self.lives_image, self.lives_image_rect)
        self.screen.blit(self.lives, self.lives_rect)

    def show_high_score(self):
        """Draw the high score to the screen"""
        self.screen.blit(self.high_score_image, self.high_score_rect)
