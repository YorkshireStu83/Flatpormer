import pygame


class Character():
    """Create a character - inherits from the Sprite class"""
    def __init__(self, screen, game_settings):
        self.screen = screen
        self.settings = game_settings

        # Load the character image and get its rect
        self.image = pygame.image.load("images/Robot.png")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start the character at the bottom-left of the screen
        self.rect.left = self.screen_rect.left
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for the character's center
        self.centerx = float(self.rect.centerx)
        self.bottom = float(self.rect.bottom)
        self.start_y = 0.0

        # Movement flags
        self.moving_right = False
        self.moving_left = False
        self.jumping = False
        self.falling = False

        # Get width of character for entering and exiting screen
        self.width = self.rect.width
        self.height = self.rect.height

    def update(self):
        """Update the character's position on the screen"""
        # Update center for float value
        if self.moving_right and self.rect.right < self.screen_rect.right + self.width:
            self.centerx += self.settings.movement_speed
        if self.moving_left and self.rect.left > 0:
            self.centerx -= self.settings.movement_speed
        if self.jumping:
            self.bottom -= self.settings.jumping_speed
            if self.bottom <= (self.start_y - self.settings.jump_height):
                self.jumping = False
        if self.falling:
            self.bottom += self.settings.gravity

        # Update rect using new centerx and bottom values
        self.rect.centerx = self.centerx
        self.rect.bottom = self.bottom

    def reset(self):
        """Reset the character to the bottom-left of the screen"""
        self.centerx = self.width / 2
        self.bottom = self.screen_rect.bottom

    def blitme(self):
        """Draw the character at its present location"""
        self.screen.blit(self.image, self.rect)
