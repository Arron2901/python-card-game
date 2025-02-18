import pygame as pygame
from variables import *
import sys
import time
import random

pygame.init()
clock = pygame.time.Clock()

# Initialising Display
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Card Game')
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


# Function to create buttons
def button(msg, x, y, w, h, ic, ac, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))


    TextSurf, TextRect = text_objects(msg, font)
    TextRect.center = ((x + (w/2)), (y + (h/2)))
    gameDisplay.blit(TextSurf, TextRect)

# Class for General Button
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

# Class for Button That Displays All Suits
class SuitButton():
    def __init__(self, suit, x, y, w, h, ic, ac):
        self.suit = suit
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.ic = ic
        self.ac = ac

    # Function to draw buttons
    def draw(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x + self.w > mouse[0] > self.x and self.y + self.h > mouse[1] > self.y:
            pygame.draw.rect(gameDisplay, self.ac, (self.x, self.y, self.w, self.h))
            if click[0] == 1 != None:
                card_game.player.update_suit(self.suit)
                card_game.update_display()
        else:
            pygame.draw.rect(gameDisplay, self.ic, (self.x, self.y, self.w, self.h)) 

        TextSurf, TextRect = text_objects(self.suit, font)
        TextRect.center = ((self.x + (self.w/2)), (self.y + (self.h/2)))
        gameDisplay.blit(TextSurf, TextRect)

# Class for Button That Displays All Cards
class NumberButton():
    def __init__(self, number, x, y, w, h, ic, ac):
        self.number = number
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.ic = ic
        self.ac = ac

    # Function to draw buttons
    def draw(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.x + self.w > mouse[0] > self.x and self.y + self.h > mouse[1] > self.y:
            pygame.draw.rect(gameDisplay, self.ac, (self.x, self.y, self.w, self.h))
            if click[0] == 1 != None:
                card_game.player.update_number(self.number)
                card_game.update_display()
        else:
            pygame.draw.rect(gameDisplay, self.ic, (self.x, self.y, self.w, self.h))

        TextSurf, TextRect = text_objects(self.number, font)
        TextRect.center = ((self.x + (self.w/2)), (self.y + (self.h/2)))
        gameDisplay.blit(TextSurf, TextRect)

# Class for Player
class Player:
    def __init__(self):
        self.suit = ''
        self.number = ''
        self.points = 0
        self.lives = 3
 
    # Updates the suit attribute of player to the chosen suit
    def update_suit(self, new_suit):
        self.suit = new_suit
 
    # Updates the number attribute of player to the chosen number
    def update_number(self, new_number):
        self.number = new_number
 
    # Renders the card chosen
    def render_card(self):
        player_card = pygame.image.load(f'img/{self.number}{self.suit}.png').convert()
        game_texts('Your Card', 400, 440)
        gameDisplay.blit(player_card, (350, 490))

# Class for Opponent
class Opponent():
    def __init__(self):
        pass

    # Chooses a random suit and number for opponent card from the remaining list of cards
    def choose_card(self):
        randSuit = random.choice(list(CARDS.keys()))
        randNumber = random.choice(CARDS[randSuit])
        
        self.suit = randSuit
        self.number = randNumber

    # Renders the random card chosen
    def render_card(self):
        player_card = pygame.image.load(f'img/{self.number}{self.suit}.png').convert()
        game_texts('Opponents Card', 730, 440)
        gameDisplay.blit(player_card, (680, 490))

# Class for game controller
class Play:
    def __init__(self):
        self.player = Player()
        self.opponent = Opponent()
        self.game_finished = False

    # Updates display with all text
    def update_display(self):
        gameDisplay.fill(background_color)
        pygame.draw.rect(gameDisplay, grey, pygame.Rect(0, 0, 250, 700))
        gameDisplay.blit(card_deck, (500, 250))

        if self.player.suit:
            game_texts(f'Suit: {self.player.suit}', 550, 160)

        if self.player.number:
            game_texts(f'Number: {self.player.number}', 550, 190)
    
        # Checks if player has chosen suit and number then renders card if they have and then checks the round
        if self.player.suit != '' and self.player.number != '':
            self.player.render_card()
            self.check_round()

        game_texts(f'Points: {card_game.player.points}', 100, 100)
        game_texts(f'Lives: {card_game.player.lives}', 85, 200)
        pygame.display.update()

    # Checks the round to see winner
    def check_round(self):
        time.sleep(1)
        self.opponent.choose_card()
        self.opponent.render_card()

 
        if self.opponent.suit == self.player.suit and self.opponent.number == self.player.number:
            self.player.lives -= 1
            game_texts('-1 Life', 560, 530, red)
        else:
            self.player.points += 10 
            game_texts('+10 Points', 560, 530)

        self.check_game()
        CARDS[self.player.suit].remove(self.player.number)

        if not CARDS[self.player.suit]:
            del CARDS[self.player.suit]

        self.player.suit = ''
        self.player.number = ''

        pygame.display.update()

    # Checks the game to see if there is a winner
    def check_game(self):
        if self.player.lives == 0:
            pygame.draw.rect(gameDisplay, background_color, pygame.Rect(250, 0, 650, 430))
            game_finish('YOU LOST', 550, 250, red)
            self.game_finished = True
        
        if self.player.points == 510:
            pygame.draw.rect(gameDisplay, background_color, pygame.Rect(250, 0, 650, 700))
            game_finish('YOU WON', 550, 250, dark_green)
            self.game_finished = True

    # Quits the game
    def quit(self):
        sys.exit()

# Function to render all of the suit buttons (Clubs, Spades, Hearts, Diamonds)
def render_suits_button():
    x = 360
    y = 50
 
    for key in CARDS:
        key = SuitButton(key, x, y, 85, 35, light_slat, dark_slat)
        key.draw()
        x += 120 

# Function to render all of the number buttons (A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K)
def render_numbers_button(suitArr):
    x = 330
    y = 100
 
    if card_game.player.suit != '':
        if not CARDS[card_game.player.suit]:
            pass
        else:
            for value in CARDS[suitArr]:
                value = NumberButton(value, x, y, 35, 35, light_slat, dark_slat)
                value.draw()
                x += 40

# Initiated game controller class
card_game = Play()
running = True

# Game Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
 
        
        

        # If statement to check if game has finished and load the Quit or Play Again Buttons
        if card_game.game_finished:
            quit_game = GenericButton('Quit!', 625, 350, 100, 50, red, dark_red)
            play_again = GenericButton('Play Again!', 375, 350, 100, 50, green, dark_green)
            if quit_game.draw():
                running = False
            elif play_again.draw():
                card_game.player.lives = 3
                card_game.player.points = 0
                card_game.game_finished = False
                CARDS = CARDSDICTIONARY
                gameDisplay.fill(background_color)
                pygame.draw.rect(gameDisplay, grey, pygame.Rect(0, 0, 250, 700))
                pygame.display.update()
        else:
            card_deck = pygame.image.load('img/back.png').convert()
            gameDisplay.blit(card_deck, (500, 250))
            render_suits_button()
            render_numbers_button(card_game.player.suit)
                
            


    pygame.display.flip()