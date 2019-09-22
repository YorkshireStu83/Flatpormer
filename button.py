import pygame.font


class Button():
    """A class to represent the start button"""

    def __init__(self, game_settings, screen):
        """Initialise attributes of the button"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set the button dimensions
        self.width, self.height = 200, 50
        self.button_color = (100, 100, 100)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and centre it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self.prep_message()

    def prep_message(self):
        """Prep the message ready for writing to the screen"""
        msg = "Play"
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.screen_rect.center

    def draw_button(self):
        """Draw the button to the screen"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)