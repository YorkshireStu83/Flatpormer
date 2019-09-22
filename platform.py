import pygame


class Platform():
    """Represents platforms that appear on the screen"""

    def __init__(self, screen, settings, height, width, xposition, yposition, colour):
        self.screen = screen
        self.settings = settings

        # Set the dimensions of the platform based on the given arguments"""
        self.height = height
        self.width = width
        self.xposition = xposition
        self.yposition = yposition
        self.colour = colour

        # Build the platform's rect and position it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.left = self.xposition
        self.rect.top = self.yposition

    def draw_platform(self):
        """Draw the platform to the screen"""
        self.screen.fill(self.colour, self.rect)
