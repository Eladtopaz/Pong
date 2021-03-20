import pygame

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
MY_FONT = r'documents\Roboto-Bold.ttf'
SCORE_FONT = pygame.font.Font(r'documents\Roboto-Bold.ttf', 60)
BUTTONS_FONT = pygame.font.Font(r'documents\Roboto-Bold.ttf', 50)

# Sound
PONG_SOUND = pygame.mixer.Sound(r'documents\pong.wav')  # Initialize the pong sound

# Image
PONG_ICON = pygame.image.load(r"documents/pong_icon.jpeg")
