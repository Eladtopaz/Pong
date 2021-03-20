import pygame
from Permanent import BUTTONS_FONT


class Button:
    """ Button class with 6 attributes:
        1. color - background color of the button.
        2. x - x position for the most up left point of the rectangle.
        3. y - y position for the most up left point of the rectangle.
        4. width - the width of the button.
        5. height - the height of the button.
        6. text - the text that is written on the button.

        The class represent a button.
    """
    # A constructor
    def __init__(self, color, x, y, width, height, text):
        """ Create a new Button object.
        :param color: string that represent the background color of the button.
        :type color: string
        :param x: integer that represent the x position of the most up left corner.
        :type x: integer
        :param y: integer that represent the y position of the most up left corner.
        :type y: integer
        :param width: integer that represent the width of the button.
        :type width integer
        :param height: integer that represent the height of the button.
        :type height: integer
        :param text: string that will be written on the button
        :type text: string
        :return: None
        """
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen, outline=None):
        """ Draw the button on the given screen.
        :param screen: screen that the button will be drawn on.
        :type screen: pygame.display
        :param outline: tuple that represent the color of the outline. Default is None which means no outline.
        :type outline: tuple
        :return: None
        """
        # If there is an outline so create with outline, if not - without
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            text = BUTTONS_FONT.render(self.text, 1, (0, 0, 0))     # Color always black, (0,0,0)
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def is_over(self, pos):
        """ Check if the mouse is on the button.
        :param pos: tuple that represent the current place of the mouse.
        :type pos: tuple
        :return: If the mouse is on the button.
        :rtype: boolean.
        """
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width and pos[1] > self.y:
            if pos[1] < self.y + self.height:
                return True

        return False


class SpecialButton(Button):
    """ SpecialButton class with 7 attributes (inherit from Button):
        1. color - background color of the button.
        2. x - x position for the most up left point of the rectangle.
        3. y - y position for the most up left point of the rectangle.
        4. width - the width of the button.
        5. height - the height of the button.
        6. text - the text that is written on the button.
        7. text_color - the color of the text.

        The class represent a  settings button.
    """
    # A constructor
    def __init__(self, screen_color, x, y, width, height, text, text_color="red"):
        """ Create a new Button object.
           :param screen_color: string that represent the background color of the button.
           :type screen_color: string
           :param x: integer that represent the x position of the most up left corner.
           :type x: integer
           :param y: integer that represent the y position of the most up left corner.
           :type y: integer
           :param width: integer that represent the width of the button.
           :type width integer
           :param height: integer that represent the height of the button.
           :type height: integer
           :param text: string that will be written on the button
           :type text: string
           :param text_color: string that represent the color of the text. Default is red.
           :type text_color: string
           :return: None
        """
        super().__init__(screen_color, x, y, width, height, text)

        self.text_color = text_color
    
    def draw(self, screen):
        """ Draw the button on the given screen.
        :param screen: screen that the button will be drawn on.
        :type screen: pygame.display
        :return: None
        """
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        text = BUTTONS_FONT.render(self.text, 1, self.text_color)
        screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def change_mode(self):
        """ Change the mode of the button to Enable/Disable.
        :return: None
        """
        # If the current mode is red, it means the text is Disable, so change color and text.
        if self.text_color == "red":
            self.text_color = "green"
            self.text = "Enabled"
        else:
            self.text_color = 'red'
            self.text = "Disabled"
