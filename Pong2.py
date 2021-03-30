import sys

from playsound import playsound

from Ball import Ball
from Buttons import Button, SpecialButton
from Player import Player
from anotherFunctions import *

"""
    Pong 2.0, OOP.
"""


class Game:
    """ Game class with 6 attributes:
        1. screen - the screen of the game.
        2. right_player - the right player in the game.
        3. left_player - the left player in the game.
        4. ball - the ball in the game.
        5. rand_ball - custom setting - if the ball is random size or not.

        The class represent a game.
    """
    # A constructor
    def __init__(self, screen, rand_ball=False):
        """ Create a new Game object.
        :param screen: the screen that game will be played on.
        :type screen: pygame.display
        :param rand_ball: boolean that represent the game setting, if the ball is random size or not, default is False.
        :type rand_ball: boolean
        :return: None
        """
        self.screen = screen  # Take the screen that was given

        # Create two players and a ball
        self.right_player = Player("right")
        self.left_player = Player("left")
        self.ball = Ball(rand_ball)

        # Save the settings of the game
        self.rand_ball = rand_ball  # Random size for the ball

    def start(self):
        """ This function will start a Pong game!
         :return: None
         """
        pygame.mixer.music.load(BACKGROUND_MUSIC)  # Initialize the background music

        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)   # Set mouse courser to normal

        # The -1 says it will keep the background song will keep forever
        pygame.mixer.music.play(-1)
        clock = pygame.time.Clock()          # Initialize a clock
        counter = 0                          # Count the frames, use for later
        players_boost = 0                    # "boost" for the players speed


        while True:

            # Handling input
            for event in pygame.event.get():

                # Handle the exit from game command
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # If clicked on a key
                if event.type == pygame.KEYDOWN:

                    # If it is the arrow-DOWN key
                    if event.key == pygame.K_DOWN:
                        self.right_player.key_down(players_boost, True)

                    # If it is the arrow-UP key
                    if event.key == pygame.K_UP:
                        self.right_player.key_down(players_boost, False)

                    # If it is the "W" key
                    if event.key == pygame.K_w:
                        self.left_player.key_up(players_boost, True)

                    # If it is the "S" key
                    if event.key == pygame.K_s:
                        self.left_player.key_up(players_boost, False)

                    """ Glitch!! Can't click on a key while click on "continue"
                    or "restart" option! Because when you leave the key it will keep -him
                    so the player will go to the other side all the time.
                    """
                    # If clicked on the "P" button
                    if event.key == pygame.K_p:
                        self.right_player.player_speed = 0  # If clicked on "P" and another key the same time
                        self.left_player.player_speed = 0   # It won't keep going there, it become 0.

                        # Pause the background music
                        pygame.mixer.music.pause()
                        pause(self.screen, self.rand_ball)
                        # unpause the background music
                        pygame.mixer.music.unpause()

                    # If clicked on the "R" key, restart the game!!
                    if event.key == pygame.K_r:
                        restart_game = Game(self.screen, self.rand_ball)
                        restart_game.start()

                # If stopped clicked on a key
                if event.type == pygame.KEYUP:

                    # Reverse what is done
                    if event.key == pygame.K_DOWN:
                        self.right_player.key_up(players_boost, True)

                    # Reverse what is done
                    if event.key == pygame.K_UP:
                        self.right_player.key_up(players_boost, False)

                    # Reverse what is done
                    if event.key == pygame.K_w:
                        self.left_player.key_down(players_boost, True)

                    # Reverse what is done
                    if event.key == pygame.K_s:
                        self.left_player.key_down(players_boost, False)

            # Constantly check if keys are pressed
            pressed = pygame.key.get_pressed()

            # Move the players if clicked on a key
            self.right_player.move()
            self.left_player.move()

            # Make the counter ++ every frame
            counter += 1
            """"Every 10sec the ball and players get faster only if 0 keys are pressed.
                Explain: Because every 600 sec the players_boost gets bigger, then might be the next glitch -
                Assume you clicked on W (+= (7 +n) ) and while you click on it n change.
                When you stop click on W, (-= (7 + n)) you will have 1 pixel less, which will
                Make the player move passively, because it won't get to player_speed 0
            """
            if counter % 600 == 0 and not any((pressed[pygame.K_w], pressed[pygame.K_s], pressed[pygame.K_UP], pressed[pygame.K_DOWN])):

                # Make the ball faster
                self.ball.speed_change()

                # Make the players faster
                players_boost += 1

            # Make the ball bounce up and down
            self.ball.flipy()

            # Check if the ball left the left side of the screen
            if self.ball.left_side():
                # Increase player score
                self.right_player.score += 1

                # Pause the background music
                pygame.mixer.music.pause()

                # Play "What a loser" (which will cause with pause the whole game)
                playsound(WHAT_A_LOSER)

                # Resume the background music
                pygame.mixer.music.unpause()

            # Check if the ball left the right side of the screen
            if self.ball.right_side():
                # Increase opponent score
                self.left_player.score += 1

                # Pause the background music
                pygame.mixer.music.pause()

                # Play "You Sucks" (which will cause with pause the whole game)
                playsound(YOU_SUCKS)

                # Resume the background music
                pygame.mixer.music.unpause()

            # Update players score every frame "black = (0, 0, 0)"
            right_player_score = SCORE_FONT.render(f'{self.right_player.score}', True, "black")
            left_player_score = SCORE_FONT.render(f'{self.left_player.score}', True, (0, 0, 0))

            # Make sure if collide down, get the ball to down
            if self.ball.ball.colliderect(self.left_player.down) or self.ball.ball.colliderect(self.right_player.down):
                # True = down
                self.ball.collide(True)
                pygame.mixer.Sound.play(PONG_SOUND)

            # Make sure if collide up, get the ball up
            if self.ball.ball.colliderect(self.left_player.up) or self.ball.ball.colliderect(self.right_player.up):
                # False = up
                self.ball.collide(False)
                pygame.mixer.Sound.play(PONG_SOUND)

            # Make sure if collide middle, ball will go forward
            if self.ball.ball.colliderect(self.right_player.middle):
                self.ball.collide_middle("right")

            # Make sure if collide middle, ball will go forward
            if self.ball.ball.colliderect(self.left_player.middle):
                self.ball.collide_middle("left")

            # Check for winner
            if self.right_player.score == 13:
                # Pause the background music
                pygame.mixer.music.pause()
                end_game(self.screen, self.right_player, self.rand_ball)
            if self.left_player.score == 13:
                # Pause the background music
                pygame.mixer.music.pause()
                end_game(self.screen, self.left_player, self.rand_ball)

            # Move the ball every frame
            self.ball.move()

            # Drawing
            self.screen.fill(SCREEN_COLOR)

            # Right player
            pygame.draw.rect(self.screen, RIGHT_PLAYER_COLOR, self.right_player.up)
            pygame.draw.rect(self.screen, RIGHT_PLAYER_COLOR, self.right_player.middle)
            pygame.draw.rect(self.screen, RIGHT_PLAYER_COLOR, self.right_player.down)
            # Left player
            pygame.draw.rect(self.screen, LEFT_PLAYER_COLOR, self.left_player.up)
            pygame.draw.rect(self.screen, LEFT_PLAYER_COLOR, self.left_player.middle)
            pygame.draw.rect(self.screen, LEFT_PLAYER_COLOR, self.left_player.down)
            # Ball
            pygame.draw.ellipse(self.screen, BALL_COLOR, self.ball.ball)
            # Draw the middle line
            draw_dashed_line(self.screen, "black", (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT), width=7, dash_length=8)
            # Draw the top line
            pygame.draw.line(self.screen, "black", (0, 0), (SCREEN_WIDTH, 0), 7)
            # Draw the bottom line
            pygame.draw.line(self.screen, "black", (0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT), 7)
            # Draw players score
            self.screen.blit(right_player_score, (SCREEN_WIDTH / 2 + 60, 0))
            self.screen.blit(left_player_score, (SCREEN_WIDTH / 2 - 33 - 60, 0))

            # Updating the window
            pygame.display.update()
            # Number of frames per sec
            clock.tick(60)


class MainMenu:
    """ Main menu class with 6 attributes:
    1. screen - the screen of the main menu.
    2. start_game_button - a button to start a game.
    3. rand_button - a button for the custom option random ball size.
    4. how_to_play_button - a button for the how to play screen.

    The class represent a main menu.
    """
    # A constructor
    def __init__(self):
        """ Create a new MainMenu object.
        :return: None
        """
        # Setting up the main window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Create the start button and the settings button    
        self.start_game_button = Button("white", SCREEN_WIDTH / 2 - 170, SCREEN_HEIGHT / 2 - 70, 350, 100,
                                        "Start A Game")
        self.rand_button = SpecialButton(SCREEN_COLOR, 650, 366, 350, 100, "Disabled")
        self.how_to_play_button = Button("white", SCREEN_WIDTH / 2 - 170, SCREEN_HEIGHT / 2 - 170, 350, 100, "How to play")

    def start(self):
        """ This function will open the main menu.
        :return: None
        """
        # General setup
        pygame.init()

        # Initialize the icon picture
        pygame.display.set_icon(PONG_ICON)
        pygame.display.set_caption("Pong")    # Chose the name on the window
        clock = pygame.time.Clock()           # Initialize a clock

        while True:

            # stores the (x,y) coordinates into the variable as a tuple 
            mouse = pygame.mouse.get_pos()

            # Handling input
            for event in pygame.event.get():

                # Handle the exit from game command
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Check if the mouse is over A button
                if self.start_game_button.is_over(mouse) or self.rand_button.is_over(mouse) or self.how_to_play_button.is_over(mouse):

                    # If so - change the mouse cursor
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)

                    # Check if the mouse left button is pressed and is on the start button
                    if pygame.mouse.get_pressed()[0] and self.start_game_button.is_over(mouse):

                        # If so - bring back the mouse cursor and start a game
                        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

                        # If the random option selected - make a game with random option
                        if self.rand_button.text_color == "green":
                            game = Game(self.screen, rand_ball=True)

                        # If not - make a game without the random option
                        else:
                            game = Game(self.screen)
                        game.start()

                    # Check if the mouse left button is pressed and is on the rand button
                    if pygame.mouse.get_pressed()[0] and self.rand_button.is_over(mouse):
                        # If so - change the text and color
                        self.rand_button.change_mode()

                    # Check if the mouse left button is pressed and is on the how to play button
                    if pygame.mouse.get_pressed()[0] and self.how_to_play_button.is_over(mouse):
                        # If so - open how to play screen
                        how_to_play(self.screen)

                # Else - bring back the mouse cursor to normal
                else:
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

            # Fill the bg color
            self.screen.fill(SCREEN_COLOR)

            # Draw the buttons
            self.start_game_button.draw(self.screen, (0, 0, 0))
            self.how_to_play_button.draw(self.screen, (0, 0, 0))
            self.rand_button.draw(self.screen)
            # Message to screen with what is the setting to chose.
            message_to_screen(self.screen, "Random ball size: ", 50, "black", (320, 385))

            # Updating the window
            pygame.display.flip()
            # Number of frames per sec
            clock.tick(60)


def pause(screen, rand_ball=False):
    """ This function will pause the game and give some options:
    1. continue 2. restart 3. main menu
    :param screen: the screen the options will be drawn on.
    :type screen: pygame.display
    :param rand_ball: the custom setting for the random ball size, default is False
    :type rand_ball: boolean
    :return: None
    """
    # Create the 3 buttons, one on top of the other
    continue_button = Button("white", SCREEN_WIDTH / 2 - 170, SCREEN_HEIGHT / 2 - 150, 350, 100, "Continue")
    restart_button = Button("white", SCREEN_WIDTH / 2 - 170, SCREEN_HEIGHT / 2 - 50, 350, 100, "Restart")
    main_menu_button = Button("white", SCREEN_WIDTH / 2 - 170, SCREEN_HEIGHT / 2 + 50, 350, 100, "Main Menu")
    be_careful_text = """Don't click on w/s/up/down keys when 
clicking on the continue/restart, will cause bags!"""

    paused = True                # Stop mark
    clock = pygame.time.Clock()  # Initialize a clock
    while paused:

        # stores the (x,y) coordinates into the variable as a tuple
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():

            # Handle the exit from game command
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # If the "P" button was clicked:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False

        # Check if the mouse is over A button
        if continue_button.is_over(mouse) or restart_button.is_over(mouse) or main_menu_button.is_over(mouse):

            # If so - change the mouse cursor
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)

            # Check if the mouse left button is pressed and is on the continue button
            if pygame.mouse.get_pressed()[0] and continue_button.is_over(mouse):
                # If so - bring back the mouse cursor and continue the game
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
                paused = False

            # Check if the mouse left button is pressed and is on the restart button
            if pygame.mouse.get_pressed()[0] and restart_button.is_over(mouse):
                # If so - create a new Game object and start it
                game = Game(screen, rand_ball)
                game.start()

            # Check if the mouse left button is pressed and is on the main_menu button
            if pygame.mouse.get_pressed()[0] and main_menu_button.is_over(mouse):
                # If so - create a new MainMenu object and start it
                main_menu_object = MainMenu()
                main_menu_object.start()

        # Else - bring the mouse cursor to normal
        else:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Fill the bg color
        screen.fill(SCREEN_COLOR)
        # Draw the buttons using their draw function
        continue_button.draw(screen, (0, 0, 0))
        restart_button.draw(screen, (0, 0, 0))
        main_menu_button.draw(screen, (0, 0, 0))

        message_to_screen(screen, be_careful_text, 25, "red", (350, 100), True)
        # Updating the window
        pygame.display.flip()
        # Number of frames per sec
        clock.tick(60)


def end_game(screen, winner_player, rand_ball=False):
    """ This function will end the game, show the winner and give 2 options:
    1. another game 2. main menu
    :param screen: the screen the options and the winner_player will be drawn on.
    :type screen: pygame.display
    :param winner_player: the player that won the game
    :type winner_player: Player
    :param rand_ball: the custom setting for the random ball size, default is False
    :type rand_ball: boolean
    :return: None
    """
    text = winner_player.side + " player is the winner!!"  # The text that will be displayed
    # Create a buttons
    another_game_button = Button("white", SCREEN_WIDTH / 2 - 170, SCREEN_HEIGHT / 2 - 50, 350, 100, "Another game")
    main_menu_button = Button("white", SCREEN_WIDTH / 2 - 170, SCREEN_HEIGHT / 2 + 50, 350, 100, "Main Menu")
    clock = pygame.time.Clock()  # Initialize a clock

    while True:

        # stores the (x,y) coordinates into the variable as a tuple
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():

            # Handle the exit from game command
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Check if the mouse is over A button
            if another_game_button.is_over(mouse) or main_menu_button.is_over(mouse):

                # If so - change the mouse cursor
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)

                # Check if the mouse left button is pressed and is on the another_game button
                if pygame.mouse.get_pressed()[0] and another_game_button.is_over(mouse):
                    # If so - bring back the mouse cursor and start a new game
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    game = Game(screen, rand_ball)
                    game.start()

                # Check if the mouse left button is pressed and is on the main_menu button
                if pygame.mouse.get_pressed()[0] and main_menu_button.is_over(mouse):
                    # If so - bring back the mouse cursor and open the main menu
                    main_menu_object = MainMenu()
                    main_menu_object.start()

            # Else - bring the mouse cursor to normal
            else:
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Fill the bg color
        screen.fill(SCREEN_COLOR)

        # Draw the buttons
        another_game_button.draw(screen, (0, 0, 0))
        main_menu_button.draw(screen, (0, 0, 0))
        message_to_screen(screen, text, 60, "black", (SCREEN_WIDTH / 2 - 340, SCREEN_HEIGHT / 2 - 180))

        # Updating the window
        pygame.display.update()
        # Number of frames per sec
        clock.tick(60)


def how_to_play(screen):
    """ This function will show how to play the game and give the option
    to get to the main menu.
    :param screen: the screen the options will be drawn on.
    :type screen: pygame.display
    :return: None
    """
    # Create the 1 button
    main_menu_button = Button("white", SCREEN_WIDTH / 2 - 170, SCREEN_HEIGHT / 2 + 50, 350, 100, "Main Menu")

    # Create text
    how_to_play_text = """The goal of the game is to make sure the ball \nwon't leave your side of the field, \nand leave the other player side of the field.
The winner is the first person to get to 13 points!!
Left player keys: W for up. S for down.
Right player keys: UP-arrow for up. DOWN-arrow for down.
P key for pause. R for restart."""

    # Position of the text
    x_pos = SCREEN_WIDTH / 2 - 300
    y_pos = SCREEN_HEIGHT / 2 - 200
    clock = pygame.time.Clock()  # Initialize a clock

    while True:

        # stores the (x,y) coordinates into the variable as a tuple
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():

            # Handle the exit from game command
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Check if the mouse is over the button
        if main_menu_button.is_over(mouse):

            # If so - change the mouse cursor
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)

            # Check if the mouse left button is pressed and is on the main_menu button
            if pygame.mouse.get_pressed()[0] and main_menu_button.is_over(mouse):
                # If so - create a new MainMenu object and start it
                main_menu_object = MainMenu()
                main_menu_object.start()

        # Else - bring the mouse cursor to normal
        else:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Fill the bg color
        screen.fill(SCREEN_COLOR)
        # Draw the button using it draw function
        main_menu_button.draw(screen, (0, 0, 0))

        # Messages the screen how to play
        message_to_screen(screen, how_to_play_text, 30, "black", (x_pos, y_pos), True)
        # Updating the window
        pygame.display.flip()
        # Number of frames per sec
        clock.tick(60)


# Activate only when this file is not imported
if __name__ == "__main__":
    main_menu = MainMenu()
    main_menu.start()
