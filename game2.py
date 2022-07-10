import pygame
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
        self.maxKeyPresses = 750
        self.running = True

game = Game()

clock = pygame.time.Clock()

# draw elevation marks
def elevationMarkings(speed):
    for i in range(500):
        pygame.draw.rect(screen, colorBLACK,(WIDTH*0.97, HEIGHT * 0.9 - i * 50 + speed, 10, 3))
        if i % 5 == 0:
            draw_text(screen, str(i*10) + " m", x=WIDTH*0.9, y=HEIGHT * 0.9 - i * 50 + speed, size = 35)

def startingScreen():
    counter = 0
    running = True

    while running:
        
        counter += 1
        clock.tick(FPS)

        # If the player clicks the red 'x', it is considered a quit event
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                running = False
                
        # fill the screen
        screen.fill(colorWHITE)
        
        # draw main text
        draw_text(screen, "RAGE AGAINST TURTLE STEVE", x=WIDTH/2,y= HEIGHT*0.25,size = 65)
        draw_text(screen, "Smash your keyboard to charge the Rage Bar.", x=WIDTH/2,y= HEIGHT*0.35,size = 30)
        draw_text(screen, "The angrier you are,", x=WIDTH/2,y= HEIGHT*0.4,size = 30)
        draw_text(screen, "the higher Steve will fly.", x=WIDTH/2,y= HEIGHT*0.45,size = 30)
              
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
    flickerCounter = 0

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
        # make text flicker
        flickerCounter += 1
        if flickerCounter < 25:
            draw_text(screen, "Press any key to charge the Rage Bar", x=WIDTH/2, y=HEIGHT * 0.2,size = 52)
        if flickerCounter >= 35:
            flickerCounter = 0

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


def restartGame(marks_loc):
    counter = 0
    running = True

    while running:
        
        counter += 1
        clock.tick(FPS)

        # If the player clicks the red 'x', it is considered a quit event
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                running = False
                game.running = False
                
        # fill the screen
        screen.fill(colorWHITE)
        screen.fill(colorWHITE)
        screen.blit(fist,fist_loc) 
        screen.blit(balloons,balloons_loc)
        screen.blit(turtle,turtle_loc)
        elevationMarkings(marks_loc)
        
        # draw main text
        draw_text(screen, "You can get much angrier that that!", x=WIDTH/2,y= HEIGHT*0.68,size = 45)
              
        # make text flicker
        if counter < 20:
            draw_text(screen, "make steve fly higher", x=WIDTH/2,y= HEIGHT*0.75,size = 20)
            draw_text(screen, "try to beat your won record", x=WIDTH/2,y= HEIGHT*0.79,size = 20)
            draw_text(screen, "- - - Press any key to continue - - -", x=WIDTH/2,y =HEIGHT * 0.85 ,size = 30)
        if counter >= 40:
            counter = 0

        # update screen
        pygame.display.update()

def main():

    while True:
        
        #set initial locaiton of images 
        turtle_loc.center = (turtleStartingLoc)
        balloons_loc.center = (balloonsStartingLoc)
        fist_loc.center = (fistStartingLoc)

        # starting screen
        startingScreen()

        # charge rage bar by pressing keys
        game.keyPresses = 0
        chargeRageBar()

        # loop utilities
        game.running = True
        marks_loc = 0   
        counter = 0
        
        # Turtle Launch Animation Triggers
        moveFist = True
        launchTurtle = False
        moveTurtle = True
        moveScreen = False
        
        # variables for motion
        velocity = 130 * game.keyPresses/ game.maxKeyPresses
        secondsElapsed = 0
        gravity = -9.8

        while game.running:
            
            counter +=1
            clock.tick(FPS)

            #----- [Turtle Launch Animation]------
            # 1. move fist updward to punch turtle
            if moveFist == True:
                fist_loc[1] -= 25
            # 1.1 stop moving the fist when a certain hight is reached
            if fist_loc[1] <= HEIGHT * 0.7:
                moveFist = False
                launchTurtle = True

            # 2. Launch Turtle 
            if launchTurtle == True:

                # 2.1 move the turtle and the ballons upward
                if moveTurtle == True:
                    turtle_loc[1] -= velocity
                    balloons_loc[1] -= velocity

                # 2.2 stop moving the turtle when a certain hight is reached 
                if turtle_loc[1] <= HEIGHT * 0.5:
                    moveTurtle = False
                    moveScreen = True

                    # 3. make the illusion that the turtle is moving by making all objects on the screen move downward 
                    if moveScreen == True:
                        marks_loc += velocity
                        fist_loc[1] += velocity

                #----[DECREASE VELOCITY]------
                # decrease velocity by accounting for the force of gravity acting upon the turtle
                if counter % 60 == 0:
                    secondsElapsed += 1

                velocity += int(secondsElapsed * gravity)
                
                if velocity < 0:
                    velocity = 0
                    moveScreen = False
                    restartGame(marks_loc)

            # ------- [CHECK FOR EVENTS in PYGAME] ------
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

            #update the screen
            pygame.display.update()       

main()
