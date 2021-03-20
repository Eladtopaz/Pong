from Permanent import *


class Player:
    """ Player class with 6 attributes:
        1. side - side of the player, left or right
        2. up - a rectangle represent the upper part of the player
        3. middle - a rectangle represent the middle part of the player
        4. down - a rectangle represent the button part of the player
        5. player_speed - a number represent the current speed of the player
        6. score - a number represent the score of the player

        The class represent a player.
    """
    # A constructor
    def __init__(self, side):
        """ Create a new Player object.
        :param side: string that represent the side of the player (left or right)
        :type side: string
        :return: None
        """
        self.side = side  # Keep the player side

        if side == "right":  # If it is the right player
            # Create the Rects needed
            self.up = pygame.Rect(SCREEN_WIDTH - 20, SCREEN_HEIGHT / 2 - 70 + 1, 10, (PLAYERS_HEIGHT / 15) * 7)
            self.middle = pygame.Rect(SCREEN_WIDTH - 20, (SCREEN_HEIGHT / 2 - 70) + (PLAYERS_HEIGHT / 3) + 20, 10,
                                      (PLAYERS_HEIGHT / 15))
            self.down = pygame.Rect(SCREEN_WIDTH - 20, (SCREEN_HEIGHT / 2 - 70) + 2 * (PLAYERS_HEIGHT / 3) - 18, 10,
                                    (PLAYERS_HEIGHT / 15) * 7)
        else:  # If it is the left player
            # Create the Rects needed
            self.up = pygame.Rect(10, SCREEN_HEIGHT / 2 - 70 + 1, 10, (PLAYERS_HEIGHT / 15) * 7)
            self.middle = pygame.Rect(10, (SCREEN_HEIGHT / 2 - 70) + (PLAYERS_HEIGHT / 3) + 20, 10,
                                      (PLAYERS_HEIGHT / 15))
            self.down = pygame.Rect(10, (SCREEN_HEIGHT / 2 - 70) + 2 * (PLAYERS_HEIGHT / 3) - 18, 10,
                                    (PLAYERS_HEIGHT / 15) * 7)

            # Initialize the speed of the Rects to 0, score to 0.
        self.player_speed = 0
        self.score = 0

    # Key press handling
    def key_down(self, n, up_or_down):
        """ Update player current speed.
        :param n: integer that represent the "Bonus" speed boost.
        :type n: integer
        :param up_or_down: boolean that represent what key was pressed.
        Get True when:  1. right player click on down-arrow key
                        2. left player stopped click on "w" key
        Get False when: 1. right player click on up-arrow key
                        2. left player stopped click on "s" key
        :type up_or_down: boolean 
        :return: None
        """
        if up_or_down:
            self.player_speed += (7 + n)
        else:
            self.player_speed -= (7 + n)

            # Key press handling

    def key_up(self, n, up_or_down):
        """ Update player current speed.
        :param n: integer that represent the "Bonus" speed boost.
        :type n: integer
        :param up_or_down: boolean that represent what key was pressed.
        Get True when:  1. left player click on "w" key
                        2. right player stopped click on up-arrow key
        Get False when: 1. left player click on "s" key
                        2. right player stopped click on down-arrow key
        :type up_or_down: boolean 
        :return: None
        """
        if up_or_down:
            self.player_speed -= (7 + n)
        else:
            self.player_speed += (7 + n)

            # Move the players every frame

    def move(self):
        """ Move the player rectangle, using the current player speed.
        :return: None
        """
        # Move the rects with the speed
        self.up.y += self.player_speed
        self.middle.y += self.player_speed
        self.down.y += self.player_speed

        # Make sure the players won't be out of screen
        if self.up.top <= 0:
            self.up.top = 0
            self.middle.top = self.up.bottom
            self.down.top = self.middle.bottom

        if self.down.bottom >= SCREEN_HEIGHT:
            self.down.bottom = SCREEN_HEIGHT
            self.middle.bottom = self.down.top
            self.up.bottom = self.middle.top
