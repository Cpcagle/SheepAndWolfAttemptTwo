import pygame

class button():
    def __init__(self, color, x, y, width, height, win, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.win = win

    def draw(self, outline=None):
        """
        Draws the button to the screen.
        :param win: DISPLAYSURF
        :param outline: the color of the outline
        """
        if outline:
            pygame.draw.rect(self.win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(self.win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('freesansbold', 30)
            text = font.render(self.text, 1, (0, 0, 0))
            self.win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))


    def isOver(self, pos):
        """
        Determines if the mouse is over a certain position. 
        :param pos: is the mouse or an x, y coordinate.
        :return: True if the mouse is over the position.
        """
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False
