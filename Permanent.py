import pygame
import os

# Initialize absolute path for later use
dirname = os.path.dirname(__file__)

# Window size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 650

# Height of the player, use for random
PLAYERS_HEIGHT = 140

# Colors
SCREEN_COLOR = "honeydew3"
RIGHT_PLAYER_COLOR = "blue"
LEFT_PLAYER_COLOR = "red"
BALL_COLOR = "lightsteelblue4"

# Initialize so we can use the Font and Sound.
pygame.init()

# Font
MY_FONT = os.path.join(dirname, r'documents\Roboto-Bold.ttf')
SCORE_FONT = pygame.font.Font(MY_FONT, 60)
BUTTONS_FONT = pygame.font.Font(MY_FONT, 50)

# Sound
PONG_SOUND = pygame.mixer.Sound(os.path.join(dirname, r'documents\pong.wav'))  # Initialize the pong sound
BACKGROUND_MUSIC = os.path.join(dirname, r"documents\jazz_bg.ogg")
WHAT_A_LOSER = os.path.join(dirname, r'documents\what_a_loser.mp3')
YOU_SUCKS = os.path.join(dirname, r'documents\You_sucks.mp3')

# Image
PONG_ICON = pygame.image.load(os.path.join(dirname, r"documents/pong_icon.jpeg"))
