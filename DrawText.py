import pygame

class DrawText:

    def __init__(self, FONT, SURF, text, width, height):
        self.font = FONT
        self.surf = SURF
        self.text = text
        self.width = width
        self.height = height
        self.WHITE = (255, 255, 255)
        self.color = (  30, 30, 30)

    def draw_color(self):
        """
        draws text to the screen in a different color
        :return:
        """
        surf = self.font.render(self.text, True, self.color)
        rect = surf.get_rect()
        rect.midtop = (self.width, self.height)
        self.surf.blit(surf, rect)

    def draw_text(self):
        """
        draws text to the screen
        :return:
        """
        surf = self.font.render(self.text, True, self.WHITE)
        rect = surf.get_rect()
        rect.midtop = (self.width, self.height)
        self.surf.blit(surf, rect)

    def draw_num(self, text):
        """
        draws a number to the screen
        :param text: number to be drawn
        :return:
        """
        self.text = text
        surf = self.font.render(str(self.text), True, self.WHITE)
        rect = surf.get_rect()
        rect.midtop = (self.width, self.height)
        self.surf.blit(surf, rect)

    '''
    def handle_event(self, event, surf, count):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                surf.fill((0, 0, 0))
    '''



