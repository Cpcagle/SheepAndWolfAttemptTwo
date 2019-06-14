import pygame


class InputBox:

    def __init__(self, x, y, width, height, FONT, type, DISPLAYSURF, text = ''):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.FONT = FONT
        self.COLOR_INACTIVE = pygame.Color('lightskyblue3')
        self.COLOR_ACTIVE = pygame.Color('dodgerblue2')
        self.color = self.COLOR_INACTIVE
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False
        self.input = 0
        self.screen = DISPLAYSURF
        self.type = type

    def handle_event(self, event):
        """
        Handles and event when the input box is clicked
        :param event: the event to be handled
        :return:
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # if the user clicked on the input box
            if self.rect.collidepoint(event.pos):
                # Change the active variable
                self.active = not self.active
            else:
                self.active = False
            # Change the color of the input box. This is to determine if you are ove the input box.
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.input = self.text
                    self.text = ''
                    # this clears the text box when return is pressed.
                    self.txt_surface.fill((0, 0, 0))
                    return self.input
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.FONT.render(self.text, True, self.color)

    def update(self):
        """
        updates the input box, will change lengths
        :return:
        """
        # Resize the box if the text is to long.
        width = max(60, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        """
        draws the input box to the screen
        :param screen:
        :return:
        """
        # Blit the text.
        self.screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(self.screen, self.color, self.rect, 2)



