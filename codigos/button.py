import pygame
from pygame.locals import *
from sys import exit


# class CreateImage():
#     def __init__(self):
#         self.image

class createImage():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# button class


class Button():
    def __init__(self, x, y, image, text=''):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False
        self.text = text
        self.font = pygame.font.Font(None, 36)  # Use uma fonte padrão ou carregue a sua
        self.text_color = (255, 255, 255) # Cor do texto (branco)

    def Click(self):
        # posição do mouse
        position = pygame.mouse.get_pos()

        # verificar se o botão foi clicado
        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                return True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        return False

    def draw(self, surface):
        # Desenha o botão
        surface.blit(self.image, (self.rect.x, self.rect.y))

        # Se houver texto, renderiza e centraliza no botão
        if self.text != '':
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)
