import pygame
import random
from pygame.locals import *
import sys
from utilities import *
from settings import *

# Initialize all Pygame modules 
pygame.init()

# Create the game screen 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((0,0,0))
pygame.display.update()

# ---- [LOAD IMAGES]-------
# load turtle image
turtle = pygame.image.load("turtle.png")
turtle = pygame.transform.scale(turtle, turtleSize)
turtle_loc = turtle.get_rect()
turtle_loc.center = (turtleStartingLoc)

# load balloons image
balloons = pygame.image.load("balloons.png")
balloons = pygame.transform.scale(balloons, (balloonsSize))
balloons_loc = balloons.get_rect()
balloons_loc.center = (balloonsStartingLoc)

# load fist image
fist = pygame.image.load("fist.png")
fist = pygame.transform.scale(fist, fistSize)
fist_loc = fist.get_rect()
fist_loc.center = (fistStartingLoc)

# global Variables
class Game:
    def __init__(self):
        self.keyPresses = 0
        self.maxKeyPresses = 600
        self.running = True
game = Game()

# draw elevation marks
def elevationMarkings(speed):
    for i in range(300):
        pygame.draw.rect(screen, colorBLACK,(WIDTH*0.97, HEIGHT * 0.9 - i * 50 + speed, 10, 3))
        if i % 5 == 0:
            draw_text(screen, str(i*10) + " m", x=WIDTH*0.9, y=HEIGHT * 0.9 - i * 50 + speed, size = 35)

def startingScreen():
    counter = 0
    clock = pygame.time.Clock()  

    while game.running:
        
        counter += 1
        clock.tick(FPS)

        # If the player clicks the red 'x', it is considered a quit event
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                game.running = False
                
        
        # fill the screen
        screen.fill(colorWHITE)
        
        # draw main text
        draw_text(screen, "RAGE AGAINST TURTLE STEVE", x=WIDTH/2,y= HEIGHT*0.3,size = 50)
        draw_text(screen, "the angrier you are,", x=WIDTH/2,y= HEIGHT*0.35,size = 30)
        draw_text(screen, "the higher Steve will fly", x=WIDTH/2,y= HEIGHT*0.4,size = 30)
              
        # make text blink
        if counter < 50:
            draw_text(screen, "- - - Press any key to continue - - -", x=WIDTH/2,y =HEIGHT * 0.6 ,size = 40)
        if counter >= 100:
            counter = 0

        # update screen
        pygame.display.update()

def chargeRageBar():
    counter = 0
    seconds = 10
    blinkCounter = 0
    clock = pygame.time.Clock()

    while True:
        
        counter += 1
        clock.tick(FPS)

        for event in pygame.event.get():

            # If the player clicks the red 'x', it is considered a quit event
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            # charge rage bar
            if event.type == KEYDOWN:
                if game.keyPresses < game.maxKeyPresses:
                    game.keyPresses += 1

        # countdown   
        if counter % 60 == 0:
            seconds -= 1

        # exit loop
        if seconds < 0:
            break
        
        # fill the screen
        screen.fill(colorWHITE)

        # ----[text labels]----
        # make text blink
        blinkCounter += 1
        if blinkCounter < 25:
            draw_text(screen, "Press any key to charge the Rage Bar", x=WIDTH/2,y=50,size = 40)
        if blinkCounter >= 35:
            blinkCounter = 0

        draw_text(screen, "Timer: " + str(seconds),x=80,y=20)
        draw_text(screen, "RAGE BAR", x=WIDTH * 0.15 ,y=HEIGHT*0.85, size = 20)

        # draw rage Bar
        pygame.draw.rect(screen,colorGRAY, (WIDTH * 0.05,HEIGHT*0.9,200,30))
        pygame.draw.rect(screen,colorRED, (WIDTH * 0.05,HEIGHT*0.9,game.keyPresses/game.maxKeyPresses * 200,30))
       
       # blit images to screen
        screen.blit(fist,fist_loc) 
        screen.blit(balloons,balloons_loc)
        screen.blit(turtle,turtle_loc)

        # update screen
        pygame.display.update()

def main():

    # starting screen
    startingScreen()

    # charge rage bar by pressing keys
    chargeRageBar()

    # loop utilities
    clock = pygame.time.Clock()
    marks_loc = 0   
    counter = 0
    
    # Turtle Launch Animation Triggers
    punchTurtle = True
    launchTurtle = False
    moveTurtle = True
    moveScreen = False
    
    # variables for motion
    velocity = 200 * game.keyPresses/ game.maxKeyPresses
    secondsElapsed = 0
    gravity = -3

    while True:
        
        counter +=1
        clock.tick(FPS)

        #----- [Turtle Launch Animation]------
        # 1. Punch Turtle
        if punchTurtle == True:
            fist_loc[1] -= 25
        if fist_loc[1] <= HEIGHT * 0.7:
            punchTurtle = False
            launchTurtle = True

        # 2. Launch Turtle 
        if launchTurtle == True:

            # decrease velocity by accounting for the force of gravity 
            if counter % 60 == 0:
                secondsElapsed += 1

            velocity += int(secondsElapsed * gravity)
            
            if velocity < 0:
                velocity = 0
                moveScreen = False

            # 3. move the turtle and the ballons 
            if moveTurtle == True:
                turtle_loc[1] -= velocity
                balloons_loc[1] -= velocity

            # make the screen move instead of the turtle when the turtle reaches a certain height
            if turtle_loc[1] <= HEIGHT * 0.5:
                moveTurtle = False
                moveScreen = True

                # 4. move screen 
                if moveScreen == True:
                    marks_loc += velocity
                    fist_loc[1] += velocity

        # ------- [CHECK FOR EVENTS] ------
        # Get feedback from the player in the form of events
        for event in pygame.event.get():
            # If the player clicks the red 'x', it is considered a quit event
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        #------ [DRAW SCREEN]--------
        screen.fill(colorWHITE)
        screen.blit(fist,fist_loc) 
        screen.blit(balloons,balloons_loc)
        screen.blit(turtle,turtle_loc)
        elevationMarkings(marks_loc)
        pygame.display.update()       

main()