import random
from Permanent import *


class Ball:
    """ Ball class with 5 attributes:
        1. ball - a rectangle represent the ball.
        2. speed_x - a number represent the ball speed on the X axis.
        3. speed_y - a number represent the ball speed on the Y axis.
        4. last_speed_y - a number represent the ball last speed on the Y axis.
        5. rand_ball - a boolean represent if the game mode is random size for ball or not.

        The class represent a ball.
    """

    # A constructor
    def __init__(self, rand_ball=False):
        """ Create a new Ball object.
        :param rand_ball: boolean that represent if the random size for a ball is chosen.
                          default is False.
        :type rand_ball: boolean
        :return: None
        """
        # Setting up the rectangle
        self.ball = pygame.Rect(SCREEN_WIDTH / 2 - 15, SCREEN_HEIGHT / 2 - 15, 30, 30)

        # Chose the ball speed
        self.speed_x = 7 * random.choice((1, -1))  # Random, left/right
        self.speed_y = 7 * random.choice((1, -1))  # Random, up/down
        self.last_speed_y = self.speed_y  # Save the last speed
        self.rand_ball = rand_ball  # Save the rand option

    # Boost function
    def speed_change(self):
        """ Update the ball to be faster.
        :return: None
        """
        # Check the direction of the ball on the X axis
        if self.speed_x < 0:
            self.speed_x -= 1
        else:
            self.speed_x += 1

        # Check the direction of the ball on the Y axis
        if self.speed_y < 0:
            self.speed_y -= 1
        elif self.speed_y > 0:
            self.speed_y += 1

        # If equals to 0 means that hit the middle last time
        # Which means that if we make the y speed +/- 1 so next time it hits middle,
        # It will keep -1/+1 as last_speed_y!
        else:
            if self.last_speed_y < 0:
                self.last_speed_y -= 1
            else:
                self.last_speed_y += 1

    def flipy(self):
        """ Make sure the ball will bounce up and down on the screen.
        :return: None
        """
        # Make sure the ball will bounce up and down
        if self.ball.top <= 0 or self.ball.bottom >= SCREEN_HEIGHT:
            # Make ball speed negative/positive will make the ball go
            # The other side because it change by the x, y position
            self.speed_y *= -1

    # A restart option when a player score.
    def restart(self):
        """ Restart the ball to the middle position, and random his 
            direction. Also - random his size if rand_ball == True.
        :return: None
        """
        # Teleport him into the center
        self.ball.x = SCREEN_WIDTH / 2 - 15
        self.ball.y = SCREEN_HEIGHT / 2 - 15

        # Random the direction he will go on            
        self.speed_y = self.last_speed_y
        self.speed_y *= random.choice((1, -1))
        self.speed_x *= random.choice((1, -1))

        # If chose the rand option
        if self.rand_ball:
            ball_size = random.choice(range(5, 30))  # Get a SMALL random size
            self.ball = pygame.Rect(SCREEN_WIDTH / 2 - 15, SCREEN_HEIGHT / 2 - 15, ball_size,
                                    ball_size)  # Set up the new rectangle

    # Check function
    def left_side(self):
        """ Check if the ball left the left side of the field.
            If so - use restart and return True.
        :return: If the ball left the left side of the field.
        :rtype: bool
        """
        # If ball leave the left side of the field
        if self.ball.left <= 0:
            self.restart()
            return True

    # Check function
    def right_side(self):
        """ Check if the ball left the right side of the field.
            If so - use restart and return True.
        :return: If the ball left the right side of the field.
        :rtype: bool
        """
        # If the ball leave the right side of the field
        if self.ball.right >= SCREEN_WIDTH:
            self.restart()
            return True

    # Change the ball speed if collide with up/down players rectangles
    def collide(self, up_or_down):
        """ Update the ball speed, according to "hits" on the other players.
        :param up_or_down: boolean that represent which rectangle collide with the ball
        Get True when: The ball collide with one of the bottom
        Get False when: The ball collide with one of the top
        :type up_or_down: boolean 
        :return: None
        """
        if self.speed_y == 0:
            self.speed_y = self.last_speed_y

        # Collide with down, make the ball go down
        if up_or_down:
            if self.speed_y < 0:
                self.speed_y *= -1
            else:
                self.speed_y *= 1

        # Collide with up, make the ball go up
        else:
            if self.speed_y < 0:
                self.speed_y *= 1
            else:
                self.speed_y *= -1
        self.speed_x *= -1

    # Change the ball speed if collide with the middle of the players rectangles
    def collide_middle(self, right_or_left):
        """ Update the ball speed, if collide with the middle part of the players.
        :param right_or_left: string that represent which player collide with the ball
        :type right_or_left: string
        :return: None
        """
        # If the players use together the middle, one after another, the last_speed_y will be 0
        # We don't want that, so save only if not a 0
        if self.speed_y != 0:
            self.last_speed_y = self.speed_y
            self.speed_y = 0
        else:
            self.speed_y = 0

        if right_or_left == "right":

            # Writing this will stop the ball from passing the players if twice mid.
            if self.speed_x > 0:
                self.speed_x *= -1
        else:

            # Writing this will stop the ball from passing the players if twice mid.
            if self.speed_x < 0:
                self.speed_x *= -1

    # Move the ball every frame
    def move(self):
        """ Move the ball rectangle, using the current speed_x and speed_y.
        :return: None
        """
        # Move the ball every frame
        self.ball.x += self.speed_x
        self.ball.y += self.speed_y
