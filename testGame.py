import pygame
from settings import Settings
from character import Character
import game_functions as gf
from level import Level
from game_stats import GameStats
from scoreboard import ScoreBoard
from button import Button


def run_game():
    # Initialise pygame, settings and screen object
    pygame.init()
    game_settings = Settings()
    screen = pygame.display.set_mode(
        (game_settings.screen_width, game_settings.screen_height))
    pygame.display.set_caption("Flatpormer")

    # Create the scoreboard for game information and stats
    high_score = gf.get_high_score()
    stats = GameStats(game_settings, high_score)
    scoreboard = ScoreBoard(game_settings, screen, stats)

    # Create a character instance
    character = Character(screen, game_settings)
    # Create a level with platforms and enemies
    level = Level(screen, character, game_settings)
    # Create the play button
    play_button = Button(game_settings, screen)
    # Initialise joystick
    pygame.joystick.init()
    gamepad = pygame.joystick.Joystick(0)
    gamepad.init()

    # load sounds
    sounds = gf.load_sounds()

    # Start the main loop for the game.
    while True:
        gf.check_events(screen, character, level, game_settings, stats, scoreboard, play_button, sounds, gamepad)
        if pygame.joystick.get_count() > 0:
            gf.check_gamepad_direction(gamepad, character)

        if stats.game_active:
            gf.check_platform_collisions(character, level.platforms)
            gf.check_gravity(character, level.platforms)
            character.update()
            gf.update_enemies(level)
            # Check for player-enemy collisions
            gf.check_enemy_collision(screen, character, game_settings, scoreboard, level, stats, sounds)
            # Check if player has completed the level
            gf.check_level_complete(screen, character, game_settings, level, scoreboard, stats, sounds)

        gf.update_screen(screen, character, game_settings, level, scoreboard, stats, play_button)


run_game()
