import pygame
import sys
from time import sleep


def get_high_score():
    """Read the current high score"""
    filename = 'high_score.txt'
    with open(filename) as file_object:
        return int(file_object.read())


def check_high_score(stats, scoreboard):
    """Check the current score against the high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        scoreboard.prep_high_score()
        filename = 'high_score.txt'
        with open(filename, 'w') as file_object:
            score_str = str(stats.score)
            file_object.write(score_str)


def load_sounds():
    """Create a list of game sounds"""
    jump = pygame.mixer.Sound("sounds/jump.ogg")
    hit = pygame.mixer.Sound("sounds/hit.ogg")
    complete = pygame.mixer.Sound("sounds/complete.ogg")
    sounds = [jump, hit, complete]
    return sounds


def check_events(screen, character, level, game_settings, stats, scoreboard, play_button, sounds, gamepad):
    """Respond to key presses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit("Thanks for playing")
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(screen, event, character, level, game_settings, stats, scoreboard, sounds)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, character)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(screen, character, level, game_settings, stats, scoreboard, play_button,
                              mouse_x, mouse_y)
        # game pad events
        elif event.type == pygame.JOYBUTTONDOWN:
            check_gamepad_down_events(screen, character, level, game_settings, stats, scoreboard, sounds, gamepad)
        elif event.type == pygame.JOYBUTTONUP:
            check_gamepad_up_events(gamepad, character)


def check_keydown_events(screen, event, character, level, game_settings, stats, scoreboard, sounds):
    """Respond to keypresses"""
    if event.key == pygame.K_q:
        sys.exit("Thanks for playing!")
    # Controls for when game active
    elif stats.game_active:
        if event.key == pygame.K_RIGHT:
            character.moving_right = True
            character.image = pygame.image.load("images/Robot.png")
        elif event.key == pygame.K_LEFT:
            character.moving_left = True
            character.image = pygame.image.load("images/Robot1.png")
        elif event.key == pygame.K_SPACE:
            if not character.falling:
                pygame.mixer.Sound.play(sounds[0])
                character.jumping = True
                character.start_y = character.bottom
    # Controls for when game not active
    elif not stats.game_active:
        if event.key == pygame.K_p:
            start_game(screen, character, level, game_settings, stats, scoreboard)


def check_keyup_events(event, character):
    """Respond to key releases"""
    if event.key == pygame.K_RIGHT:
        character.moving_right = False
    elif event.key == pygame.K_LEFT:
        character.moving_left = False
    elif event.key == pygame.K_SPACE:
        character.jumping = False


def check_gamepad_down_events(screen, character, level, game_settings, stats, scoreboard, sounds, gamepad):
    """Respond to gamepad button presses"""
    if not stats.game_active:
        if gamepad.get_button(7) == 1:
            start_game(screen, character, level, game_settings, stats, scoreboard)
    elif stats.game_active:
        if gamepad.get_button(0) == 1 or gamepad.get_button(1) == 1:
            if not character.falling:
                pygame.mixer.Sound.play(sounds[0])
                character.jumping = True
                character.start_y = character.bottom


def check_gamepad_up_events(gamepad, character):
    """Respond to gamepad button releases"""
    if gamepad.get_button(0) == 0 and gamepad.get_button(1) == 0:
        character.jumping = False


def check_gamepad_direction(gamepad, character):
    """Check the direction controls on the gamepad"""
    if gamepad.get_axis(0) > 0.5:
        character.moving_right = True
        character.image = pygame.image.load("images/Robot.png")
    else:
        character.moving_right = False
    if gamepad.get_axis(0) < -0.5:
        character.moving_left = True
        character.image = pygame.image.load("images/Robot1.png")
    else:
        character.moving_left = False

def update_enemies(level):
    for enemy in level.enemies:
        enemy.update(level.platforms)


def update_screen(screen, character, game_settings, level, scoreboard, stats, play_button):
    """Updates images on the screen and flip to the new screen"""
    screen.fill(game_settings.bg_colour)
    for platform in level.platforms:
        platform.draw_platform()
    character.blitme()
    for enemy in level.enemies:
        enemy.blitme()
    scoreboard.show_images()

    # Show play button if game not active
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recent game visible
    pygame.display.flip()


def check_platform_collisions(character, platforms):
    """Use the pygame colliderect to check if any platforms have been hit"""
    for platform in platforms:
        if pygame.Rect.colliderect(character.rect, platform.rect):
            top = platform.rect.top
            bottom = platform.rect.bottom
            left = platform.rect.left
            right = platform.rect.right

            # Check jumping flag
            if bottom > character.rect.top > top:
                character.jumping = False

            # Check horizontal movement flags
            if left < character.rect.right < left + 5:
                character.moving_right = False
            elif right > character.rect.left > right - 5:
                character.moving_left = False


def check_gravity(character, platforms):
    """Check if character should be falling"""
    if character.bottom >= character.screen_rect.bottom:
        character.falling = False
    if check_falling_blocked(character, platforms):
        character.falling = False
    elif character.jumping is False and character.bottom < character.screen_rect.bottom:
        character.falling = True


def check_falling_blocked(character, platforms):
    """Check the character hasn't landed on a platform"""
    blocked_list = []
    for platform in platforms:
        if character.rect.left > platform.rect.right or character.rect.right < platform.rect.left:
            blocked_list.append('no')
        elif character.rect.bottom < platform.rect.top:
            blocked_list.append('no')
        elif character.rect.bottom > platform.rect.top:
            blocked_list.append('no')
        else:
            blocked_list.append('yes')
    if 'yes' in blocked_list:
        return True
    else:
        return False


def check_enemy_collision(screen, character, game_settings, scoreboard, level, stats, sounds):
    """Check if the player has collided with an enemy"""
    if pygame.sprite.spritecollideany(character, level.enemies):
        # if lives left, start a new level
        pygame.mixer.Sound.play(sounds[1])
        if game_settings.lives > 0:
            start_new_level(screen, character, game_settings, scoreboard, level, stats)
        else:
            # If no lives left, end game
            stats.game_active = False
            pygame.mouse.set_visible(True)


def start_new_level(screen, character, game_settings, scoreboard, level, stats):
    """Take all actions for a new level"""
    character.reset()
    decrease_lives(game_settings, scoreboard)
    level.platforms = level.create_platforms(screen, character, game_settings)
    level.enemies = level.create_enemies(screen, character, game_settings)
    sleep(1)


def increase_score(stats, game_settings, scoreboard):
    """Increase the score by the amount specified in the settings"""
    stats.score += game_settings.score_increment
    scoreboard.prep_score()


def decrease_lives(game_settings, scoreboard):
    """Decrease the lives counter by one"""
    game_settings.lives -= 1
    if game_settings.lives > -1:
        scoreboard.prep_lives_indicator()


def start_game(screen, character, level, game_settings, stats, scoreboard):
    """Initialise all settings and run game"""
    stats.reset_stats()
    scoreboard.prep_all_images()
    pygame.mouse.set_visible(False)
    character.reset()
    level.platforms = level.create_platforms(screen, character, game_settings)
    level.enemies = level.create_enemies(screen, character, game_settings)
    stats.game_active = True


def check_play_button(screen, character, level, game_settings, stats, scoreboard, play_button,
                      mouse_x, mouse_y):
    """Start a new game when the player clicks play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_game(screen, character, level, game_settings, stats, scoreboard)


def check_level_complete(screen, character, game_settings, level, scoreboard, stats, sounds):
    if character.rect.left >= character.screen_rect.right:
        pygame.mixer.Sound.play(sounds[2])
        character.centerx = character.rect.width / 2
        level.platforms = level.create_platforms(screen, character, game_settings)
        level.enemies = level.create_enemies(screen, character, game_settings)
        increase_score(stats, game_settings, scoreboard)
        check_high_score(stats, scoreboard)
