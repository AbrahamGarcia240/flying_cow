#!/home/abraham/anaconda3/bin/python
#
#   MY FIRST GAME in Python
#
#   This is intended to be a tutorial on how to create a game using
#   the PyGame library
#
#   NOTES:
#       This is a quick 'avoid obstacles' game with the following constraints
#         - The player starts on the left side of the screen
#         - Obstacles enter randomly form the right and move in straigh line
#         - Player can move L, R, U, D
#         - Player cannot move off the screen
#         - Game ends when the player hits an obstacle or user closes the
#           window
#
#       The names of the following attributes and methods SHOULD NOT BE CHANGED
#       as pygame assumes such attributes and methods exist
#           - Enemy.rect
#           - Player.rect
#           - Enemy.update()
#           - Player.update()

import os
import random
import pygame
import time
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN,
                           QUIT, RLEACCEL)
from typing import Dict

# ------------------------------ CONSTANTS ---------------------------------- #

# Size of the screen of the game in pixels
SCREEN_WIDTH    = 800 # X
SCREEN_HEIGHT   = 600 # Y

# Colors
COLOR_BLACK     = (0, 0, 0)
COLOR_WHITE     = (255, 255, 255)

# New enemy interval
# Interval in miniseconds to add a new enemy
NEW_ENEMY_INTERVAL = 250

# Event to constantly add enemies
# The index of last event that the user has defined is stored in
# the attribute pygame.USEREVENT
ADD_ENEMY = pygame.USEREVENT + 1

# Speed of the game
FRAME_RATE = 30

# Sprites dir
SPRITES_DIR = os.path.join(os.getcwd(), "sprites")
assert os.path.exists(SPRITES_DIR)

# Music dir
MUSIC_DIR = os.path.join(os.getcwd(), "sounds")
assert os.path.exists(MUSIC_DIR)

# Background image
BACKGROUND = os.path.join(SPRITES_DIR, "background.png")
assert os.path.exists(BACKGROUND)
BACKGROUND = pygame.image.load(BACKGROUND)

# Background music
BACKGROUND_MUSIC = os.path.join(MUSIC_DIR, "bg.mp3")
assert os.path.exists(BACKGROUND_MUSIC)

# Collision music
COLLISION_MUSIC = os.path.join(MUSIC_DIR, "collision.mp3")
assert os.path.exists(COLLISION_MUSIC)

# ------------------------------ GLOBALS ------------------------------------ #

# Screen for the game
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Variable to ensure the game is running, i.e. to control the
# gameloop. If False, the game will stop
running = True


# Setup for sounds
pygame.mixer.init()

# Set background music
pygame.mixer.music.load(BACKGROUND_MUSIC)
pygame.mixer.music.play(loops=-1)

# Set music for collision
collision_sound = pygame.mixer.Sound(COLLISION_MUSIC)

# ------------------------------- CLASSES ----------------------------------- #

# -------------------------------- Enemy ------------------------------------ #
#   DESCRIPTION:
#       Object representation of an Enemy
#
#   NOTES:
#       In pygame, everything is a surface (usually a rectangle), thus,
#       the player is a rectangle with a defined area
#
class Enemy(pygame.sprite.Sprite):

    # --------------------------- ATTRIBUTES -------------------------------- #
    # Default shape of the enemy
    width  = 20
    height = 10

    # Sprite image for the enemy
    image = os.path.join(SPRITES_DIR, "bullet2.png")
    assert os.path.exists(image)


    # ---------------------------- METHODS ---------------------------------- #

    # -------------------------- __ init __ --------------------------------- #
    #
    #   DESCRIPTION:
    #       Creates a new Enemy
    #
    #   PARAMETERS:
    #       None
    #
    #   RETURNS:
    #       None
    #
    def __init__(self):
        # Call the superclass constructor
        super(Enemy, self).__init__()

        # Define a new surface (a.k.a. area) for this sprite
        self.surface = pygame.image.load(self.image).convert_alpha()

        # Define the initial position of the Enemy
        # The enemies should appear on the right side of the screen
        x = random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100)
        # The enemies can appear at any altitude as long as they are inside
        # the screen
        y = random.randint(0, SCREEN_HEIGHT)

        # Get the representation of the player
        self.rect = self.surface.get_rect(center = (x, y))

        # Set the speed of this enemy
        self.speed = random.randint(5, 20)


    # ----------------------------- update ---------------------------------- #
    #
    #   DESCRIPTION:
    #       Updates the position of the enemy
    #
    #   PARAMETERS:
    #       None
    #
    #   RETURNS:
    #       None
    #
    def update(self):
        # Move as fast as our speed can
        self.rect.move_ip(-self.speed, 0)

        # If we hit the left corner of the screen, commit suicide
        if self.rect.right < 0:
            # This will remove this object from the list of all_sprites and
            # enemies
            self.kill()



# -------------------------------- Player ----------------------------------- #
#
#   DESCRIPTION:
#       Object representation of a player
#
#   NOTES:
#       In pygame, everything is a surface (usually a rectangle), thus,
#       the player is a rectangle with a defined area
#
class Player(pygame.sprite.Sprite):

    # --------------------------- ATTRIBUTES -------------------------------- #
    # Default shape of the player
    width  = 75
    height = 25

    # Sprite image for this player
    image = os.path.join(SPRITES_DIR, "player2.png")
    assert os.path.exists(image)

    # ---------------------------- METHODS ---------------------------------- #

    # -------------------------- __ init __ --------------------------------- #
    #
    #   DESCRIPTION:
    #       Creates a new player
    #
    #   PARAMETERS:
    #       None
    #
    #   RETURNS:
    #       None
    #
    def __init__(self):
        # Call the superclass constructor
        super(Player, self).__init__()

        # Define a new surface (a.k.a. area) for this sprite using
        # the image
        #
        # image.load returns a surface and .convert_alpha() optimizes the
        # surface to make .blint() calls faster
        self.surface = pygame.image.load(self.image).convert_alpha()
        # Set the image for this player
        self.surface.set_colorkey(COLOR_WHITE, RLEACCEL)

        # Get the representation of the player
        self.rect = self.surface.get_rect()


    # ----------------------------- update ---------------------------------- #
    #
    #   DESCRIPTION:
    #       Updates the position of the player
    #
    #   PARAMETERS:
    #       pressed_keys    Dict - A dictionary mapping the key identifier
    #                              to a boolean
    #
    #   RETURNS:
    #       None
    #
    def update(self, pressed_keys):
        # Define addtion we will do to both coordenates
        x, y = 0, 0

        if pressed_keys[K_UP]:
            y = -5
        if pressed_keys[K_DOWN]:
            y = 5
        if pressed_keys[K_LEFT]:
            x = -5
        if pressed_keys[K_RIGHT]:
            x = 5

        # Update the position of the player
        # move_ip sums the X, Y values to the current position of the player
        self.rect.move_ip(x, y)

        # Ensure we are not getting out of the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# ------------------------------ FUNCTIONS ---------------------------------- #

# -------------------------------- main ------------------------------------- #
#
#   DESCRIPTION:
#       This is what gets excuted when the script starts
#
#   PARAMETERS:
#       None
#
#   RETURNS:
#       None
#
def main():
    global running

    # Initialize a new game
    pygame.init()

    # Set up a clock to control the speed of the game
    clock = pygame.time.Clock()

    # Intanciate a player
    player = Player()

    # Keep track of both player and enemies using sprite groups
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    # Add our player to the group that keeps track of all sprites
    all_sprites.add(player)

    # Have the event ADD_ENEMY to be added to the event queue every
    # NEW_ENEMY_INTERVAL miliseconds
    pygame.time.set_timer(ADD_ENEMY, NEW_ENEMY_INTERVAL)

    # Here is the gameloop.
    # A gameloop does the following:
    #   - Processes the user input
    #   - Updates the state of all objects in the game
    #   - UPdates the display and audio input
    #   - Sets the speed of the game
    #
    # Every cycle in the loop is called FRAME
    while running:
        # Check for a new event, an event can be either an user input or
        # a change in the environment of the game (i.e. the window of the
        # game is closed)
        #
        # Every event is enqueued inside pygame's event queue
        for event in pygame.event.get():

            # Check if we should end up the game
            if event.type == QUIT or \
               (event.type == KEYDOWN and event.key == K_ESCAPE):
                # If control reached this point, the window of the game
                # got closed or the player pressed ESC.
                # we should quit the game
                running = False

            # Check if we should add a new enemy
            if event.type == ADD_ENEMY:
                # Create a new enemy and add it to the sprite groups
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

            # Get all pressed keys
            pressed_keys = pygame.key.get_pressed()

        # Update the position of the player
        player.update(pressed_keys)

        # Update the position of all enemies inside the group
        enemies.update()

        # Once we retrieved all events for this frame, render the screen
        # with all changes
        #
        # Paint the background of the screen
        screen.blit(BACKGROUND, (0,0))

        # Draw all sprites on the screen
        for sprite in all_sprites:
            screen.blit(sprite.surface, sprite.rect)

        # Check if our play has collied with any enemy
        if pygame.sprite.spritecollideany(player, enemies):
            # If control reached this point, we were hit by an enemy
            # kill the player
            player.kill()

            # Play the collision sound
            collision_sound.play()

            running = False

        # Render the screen
        pygame.display.flip()

        # Ensure the game maintains a rate of FRAME_RATE frames per second
        #
        # The argument passed to tick established the desired rate, to do this,
        # tick() calculates the number of milliseconds each frame should take,
        # based on the desired frame rate, then it compares the milliseconds
        # it has passed since the last time .tick() was called.
        #
        # If not enought time has passed, tick() delays the processing
        clock.tick(FRAME_RATE)

    time.sleep(3)
    # End the music
    pygame.mixer.music.stop()
    pygame.mixer.quit()

if __name__ == '__main__':
    main()
