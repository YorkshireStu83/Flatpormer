import pygame
import random
from platform import Platform
from enemy import Enemy


class Level():
    """A class to represent the platforms in the level"""

    def __init__(self, screen, character, game_settings):
        """Initialise the platform object"""
        self.platforms = self.create_platforms(screen, character, game_settings)
        self.enemies = self.create_enemies(screen, character, game_settings)

    def create_platforms(self, screen, character, game_settings):
        """Create random objects for the level"""

        # Empty the platforms list
        self.platforms = []

        # Set level colour
        red = random.randint(50, 255)
        green = random.randint(50, 255)
        blue = random.randint(50, 255)
        colour = [red, green, blue]

        # Create between 2 and 7 platforms
        number_platforms = random.randint(2, 7)

        x = 0
        while x < number_platforms:
            platform = self.get_platform(screen, game_settings, character, colour)
            # Check doesn't overlap with others
            overlap = False
            if x == 0:
                # First platform - cannot overlap
                pass
            else:
                # Loop through existing platforms. If collide, discard; if not, add to list
                y = 0
                z = len(self.platforms)
                while y < z:
                    if pygame.Rect.colliderect(platform.rect, self.platforms[y].rect):
                        overlap = True
                    y = y + 1
            if not overlap:
                self.platforms.append(platform)
                x = x + 1

        return self.platforms

    def get_platform(self, screen, game_settings, character, colour):
        """Create a new platform"""
        # any x-axis values are multiples of movement speed
        # any y-axis values are multiples of gravity value
        height = random.randrange(50, 400, game_settings.gravity)
        width = random.randrange(48, 702, game_settings.movement_speed)
        # Adjust character width
        adjusted_width = self.get_adjusted_character_width(character, game_settings)
        xposition = random.randrange(adjusted_width, character.screen_rect.width,
                                     game_settings.movement_speed)
        yposition = random.randrange(0, character.screen_rect.height - height - character.rect.height,
                                     game_settings.gravity)
        platform = Platform(screen, game_settings, height, width, xposition, yposition, colour)

        return platform

    def get_adjusted_character_width(self, character, game_settings):
        """Get a character width for building platforms that is a multiple of the movement speed"""
        adjusted_width = character.rect.width
        while True:
            if adjusted_width % game_settings.movement_speed == 0:
                return adjusted_width
            else:
                adjusted_width += 1

    def create_enemies(self, screen, character, game_settings):
        """Create a list of three enemies"""
        self.enemies = []
        x = 1
        while x <= 3:
            new_enemy = Enemy(screen, character, game_settings, self.platforms)
            self.enemies.append(new_enemy)
            x += 1

        return self.enemies
