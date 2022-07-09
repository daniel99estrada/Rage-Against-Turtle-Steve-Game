import pygame
from pygame.locals import *
from settings import *


def draw_text(screen,message,x,y,size=30):

    font = pygame.font.SysFont(None, size)
    text = font.render(message, True, colorBLACK)
    text_rect = text.get_rect(center=(x,y))
    screen.blit(text, text_rect) 