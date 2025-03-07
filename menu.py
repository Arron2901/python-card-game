import pygame as pygame
from variables import *
import sys
import time
import random

pygame.init()
clock = pygame.time.Clock()

# Initialising Display
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Main Menu')
gameDisplay.fill(background_color)
pygame.draw.rect(gameDisplay, grey, pygame.Rect(0, 0, 250, 700))

### Function for Text Objects
def text_objects(text, font, colour=black):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()

def end_text_objects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()


# Functions to Display Text
def game_texts(text, x, y, colour=black):
    TextSurf, TextRect = text_objects(text, textfont, colour)
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()

def game_finish(text, x, y, colour):
    TextSurf, TextRect = end_text_objects(text, game_end, colour)
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()

class GenericButton():
    def __init__(self, msg, x, y, w, h, ic, ac):
        self.msg = msg
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.ic = ic
        self.ac = ac

    # Function to draw the button
    def draw(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.x + self.w > mouse[0] > self.x and self.y + self.h > mouse[1] > self.y:
            pygame.draw.rect(gameDisplay, self.ac, (self.x, self.y, self.w, self.h))
            if click[0] == 1:
                return True
        else:
            pygame.draw.rect(gameDisplay, self.ic, (self.x, self.y, self.w, self.h))

        TextSurf, TextRect = text_objects(self.msg, font)
        TextRect.center = ((self.x + (self.w/2)), (self.y + (self.h/2)))
        gameDisplay.blit(TextSurf, TextRect)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
        game_finish('A Card Game!', 600, 200, black)
        quit_game = GenericButton('Quit!', 625, 350, 100, 50, red, dark_red)
        play = GenericButton('Play!', 375, 350, 100, 50, green, dark_green)

        if quit_game.draw():
            running = False
        elif play.draw():
            exec(open('game.py').read())