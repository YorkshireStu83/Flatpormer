import pygame
import random


class Enemy():
    """Create an enemy sprite"""

    def __init__(self, screen, character, game_settings, platforms):
        self.screen = screen
        self.character = character
        self.game_settings = game_settings
        self.moving = False

        # Load the enemy image and get its rect
        self.image = pygame.image.load("images/Enemy.png")
        self.rect = self.image.get_rect()
        self.screen_rect = self.image.get_rect()

        # Set movement flags
        self.moving_right = False
        self.moving_left = False

        # Set start position randomly
        # set x position
        minimum_centerx = (self.rect.width / 2) + 200
        maximum_centerx = self.character.screen_rect.width - (self.rect.width / 2)
        self.rect.centerx = random.randint(minimum_centerx, maximum_centerx)
        # set y position
        for platform in platforms:
            if self.rect.left >= platform.rect.left and self.rect.right <= platform.rect.right:
                self.rect.bottom = platform.rect.top
                self.floor_level = False
                self.my_platform = platform
                pass
            else:
                self.rect.bottom = character.screen_rect.bottom
                self.floor_level = True
        # Set direction
        direction = random.randint(1, 2)
        if direction == 1:
            self.moving_right = True
            self.image = pygame.image.load("images/Enemy.png")
        else:
            self.moving_left = True
            self.image = pygame.image.load("images/Enemy1.png")

        # Set a decimal value for the sprite centre
        self.centerx = float(self.rect.centerx)

    def update(self, platforms):
        """Update the position based on movement flags"""
        if self.floor_level:
            # Deal with the enemies on the floor
            if self.moving_left:
                if self.rect.left > 0:
                    self.centerx -= self.game_settings.enemy_speed
                else:
                    self.moving_left = False
                    self.moving_right = True
                    self.image = pygame.image.load("images/Enemy.png")
            elif self.moving_right:
                if self.rect.right < self.game_settings.screen_width:
                    self.centerx += self.game_settings.enemy_speed
                else:
                    self.moving_right = False
                    self.moving_left = True
                    self.image = pygame.image.load("images/Enemy1.png")
        else:
            if self.moving_left:
                if self.rect.left > self.my_platform.rect.left:
                    self.centerx -= self.game_settings.enemy_speed
                else:
                    self.moving_left = False
                    self.moving_right = True
                    self.image = pygame.image.load("images/Enemy.png")
            elif self.moving_right:
                if self.rect.right < self.my_platform.rect.right:
                    self.centerx += self.game_settings.enemy_speed
                else:
                    self.moving_right = False
                    self.moving_left = True
                    self.image = pygame.image.load("images/Enemy1.png")

        # Convert back to rect value
        self.rect.centerx = self.centerx

    def blitme(self):
        """Draw the sprite at its current position"""
        self.screen.blit(self.image, self.rect)
