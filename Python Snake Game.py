# Program created by Eric Michalski

import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

#   Imports for ASCII art
import sys
from colorama import init
init(strip=not sys.stdout.isatty())
from termcolor import cprint
from pyfiglet import figlet_format

#   Cube class for snacks and snake objects

class cube(object):
    rows = 20
    w = 500

    #   Initializes cube object variables

    def __init__(self, start, color=(255,0,0), dirx=1,diry=0):
        self.pos = start
        self.dirx = dirx
        self.diry = diry
        self.color = color

    #   Sets the position of the cube object and/or moves the object

    def move(self, dirx, diry):
        self.dirx = dirx
        self.diry = diry
        self.pos = (self.pos[0] + self.dirx, self.pos[1] + self.diry)   # Increments position by direction (0,1,-1)

    #   Draws the cube object onto the board and draws eyes onto the head of snake

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows   # Distance between white lines
        i = self.pos[0] # Variable for x position
        j = self.pos[1] # Variable for y position
        
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))    # Draws cube inside the white lined grid (This is why (dis - 2) is included) with a color
        if eyes:
            center = dis // 2  # Gets center of cube by dividing distance by 2
            radius = 3
            circleMiddle = (i*dis + center - radius, j*dis + 8) # Gets middle of a circle with radius of 3 to be used for eyes
            circleMiddle2 = (i*dis + dis - radius*2, j*dis + 8) # Gets middle of a circle with radius of 3 to be used for eyes
            pygame.draw.circle(surface, (255,255,255), circleMiddle, radius)  # Draws first white eye
            pygame.draw.circle(surface, (255,255,255), circleMiddle2, radius) # Draws second white eye
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius-1)  # Draws first black eye
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius-1) # Draws second black eye

#   Snake class for the snake object

class snake(object):
    global walls
    body = []   # Body of snake
    turns = {}  # Number of turns

    #   Initializes snake object variables

    def __init__(self, color, pos):
        self.color = color          # Defines color of snake
        self.head = cube(pos,self.color)       # Defines head of snake
        self.body.append(self.head) # Appends to body of snake
        self.dirx = 0               # Initial x direction movement (No direction)
        self.diry = 1               # Initial y direction movement (Up direction)

    #   Moves snake

    def move(self):
        global walls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # Quits the game
                pygame.quit()

            keys = pygame.key.get_pressed() # Returns a list of keys pressed

            for key in keys:
                if keys[pygame.K_LEFT]: # User pushes left arrow
                    self.dirx = -1
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry] # Adds the current position of the head of snake and where it turned

                elif keys[pygame.K_RIGHT]: # User pushes right arrow
                    self.dirx = 1
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry] # Adds the current position of the head of snake and where it turned

                elif keys[pygame.K_UP]: # User pushes up arrow
                    self.dirx = 0
                    self.diry = -1
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry] # Adds the current position of the head of snake and where it turned

                elif keys[pygame.K_DOWN]: # User pushes down arrow
                    self.dirx = 0
                    self.diry = 1
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry] # Adds the current position of the head of snake and where it turned
        
        for i, c in enumerate(self.body):   # Index and cube object of body
            p = c.pos[:]    # Current position of body
            if p in self.turns:  # If current position is where head turned
                turn = self.turns[p]    # Then grab the turn index of where head turned
                c.move(turn[0], turn[1])    # Sets dirx and diry for cube object of body
                if i == len(self.body) - 1:     # If the cube is the last one
                    self.turns.pop(p)                # Then remove that turn from the list
            else:
                if c.dirx == -1 and c.pos[0] <= 0:  # If snake reaches left side of window
                    if (walls == "open"):    # If the walls are open
                        c.pos = (c.rows - 1, c.pos[1])  # Snake appears at right side
                    elif (walls == "closed"):    # If user changed settings to closed walls
                        printmessage("You ran into a wall and lost", "Play Again")
                        s.reset((10,10),)
                elif c.dirx == 1 and c.pos[0] >= c.rows - 1:    # If snake reaches right side of window
                    if (walls == "open"):    # If the walls are open
                        c.pos = (0, c.pos[1])           # Snake appears at left side
                    elif (walls == "closed"):    # If user changed settings to closed walls
                        printmessage("You ran into a wall and lost", "Play Again")
                        s.reset((10,10),)
                elif c.diry == -1 and c.pos[1] <= 0:    # If snake reaches top of window
                    if (walls == "open"):    # If the walls are open
                        c.pos = (c.pos[0], c.rows - 1)  # Snake appears at bottom
                    elif (walls == "closed"):    # If user changed settings to closed walls
                        printmessage("You ran into a wall and lost", "Play Again")
                        s.reset((10,10),)
                elif c.diry == 1 and c.pos[1] >= c.rows - 1:    # If snake reaches bottom of window
                    if (walls == "open"):    # If the walls are open
                        c.pos = (c.pos[0], 0)           # Snake appears at top
                    elif (walls == "closed"):    # If user changed settings to closed walls
                        printmessage("You ran into a wall and lost", "Play Again")
                        s.reset((10,10),)
                else:
                    c.move(c.dirx, c.diry)  # Else, perform a regular move

    #   Resets snake after losing the game

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirx = 0
        self.diry = 1

    #   Add a cube to the snake

    def addCube(self):
        tail = self.body[-1]    # Tail of snake
        tdx = tail.dirx     # X direction of tail
        tdy = tail.diry     # Y direction of tail

        if tdx == 1 and tdy == 0:       # If tail position direction is right
            self.body.append(cube((tail.pos[0] - 1,tail.pos[1]),self.color))     # Add a cube one less in the x direction (left side) than the current position of the tail
        elif tdx == -1 and tdy == 0:    # If tail position direction is left
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1]),self.color))     # Add a cube one more in the x direction (right side) than the current position of the tail
        elif tdx == 0 and tdy == 1:     # If tail position direction is up
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1),self.color))     # Add a cube one less in the y direction (bottom side) than the current position of the tail
        elif tdx == 0 and tdy == -1:    # If tail positoin direction is down
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1),self.color))     # Add a cube one more in the y direction (top side) than the current position of the tail

        self.body[-1].dirx = tdx    # Assigns new cubes x direction to current x direction
        self.body[-1].diry = tdy    # Assigns new cubes y direction to current y direction

    #   Draws snake

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:  # If we draw the first snake, draw eyes to set head apart from body
                c.draw(surface, True)
            else:       # Else, draw the body
                c.draw(surface)
        
#   Draws the Grid for the window

def drawGrid(w, rows, surface):
    sizeBtwn = w / rows # Ensures that the boxes will be even (No decimals)
    x = 0
    y = 0
    for i in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        pygame.draw.line(surface, (255,255,255), (x,0),(x,w)) # Draws white lines in window on x axis and parallel to x axis
        pygame.draw.line(surface, (255,255,255), (0,y),(w,y)) # Draws white lines in window on y axis and parallel to y axis

#   Updates and redraws the window

def redrawWindow(surface):
    global rows, width, s, snack, backcolor
    surface.fill(backcolor)   # Fills rest of window with black color
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)   # Draws grid onto window
    pygame.display.update() # Updates current window

#   Generates a randomly placed new snack with a random color thats not the snake color

def randomSnack(rows):
    global s
    positions = s.body
    while True:
        x = random.randrange(rows)  # Random x value
        y = random.randrange(rows)  # Random y value

        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:    # If the position of the snake is the same as the snake, don't place a snack there
            continue
        else:
            break
    return (x,y)    # Returns location of random positioned snack
     
#   Displays error message when snake runs into itself

def printmessage(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

#   Allows user to change settings of the game

def settings():
    global s, backcolor, walls, speed

    print("\n\tThe current settings are:\t")
    print("  -  Snake head color:", '(255,0,0)')
    print("  -  Snake body color:", '(255,0,0)')
    print("  -  Background color:", '(0,0,0)')
    print("  -  Walls (If the snake passes through one side and appears on the other side: ", 'open')
    print("  -  Frames per second:", speed, '\n')

    headColor = input("Would you like to change the snake's head color? (y/n) ")
    if headColor == 'y':
        print("\nHard Mode: Change the color (for both head and body) to black (0,0,0) (or color of background) \n")
        sred = int(input("Enter the integer number for the amount of red coloring between 0 and 255: "))
        sblue = int(input("Enter the integer number for the amount of blue coloring between 0 and 255: "))
        sgreen = int(input("Enter the integer number for the amount of green coloring between 0 and 255: "))
        while (sred > 255 or sblue > 255 or sgreen > 255 or sred < 0 or sblue < 0 or sgreen < 0):
            print("\nYou entered an invalid input. Please enter between 0 and 255\n")
            sred = int(input("Enter the integer number for the amount of red coloring between 0 and 255: "))
            sblue = int(input("Enter the integer number for the amount of blue coloring between 0 and 255: "))
            sgreen = int(input("Enter the integer number for the amount of green coloring between 0 and 255: "))
        s.head.color = (sred,sgreen,sblue)
    bodyColor = input("\nWould you like to change the snake's body color? (y/n) ")
    if bodyColor == 'y':
        print("\nHard Mode: Change the color (for both head and body) to black (0,0,0) (or color of background) \n")
        sred = int(input("Enter the integer number for the amount of red coloring between 0 and 255: "))
        sblue = int(input("Enter the integer number for the amount of blue coloring between 0 and 255: "))
        sgreen = int(input("Enter the integer number for the amount of green coloring between 0 and 255: "))
        while (sred > 255 or sblue > 255 or sgreen > 255 or sred < 0 or sblue < 0 or sgreen < 0):
            print("\nYou entered an invalid input. Please enter between 0 and 255\n")
            sred = int(input("Enter the integer number for the amount of red coloring between 0 and 255: "))
            sblue = int(input("Enter the integer number for the amount of blue coloring between 0 and 255: "))
            sgreen = int(input("Enter the integer number for the amount of green coloring between 0 and 255: "))
        s.color = (sred,sgreen,sblue)
    background = input("\nWould you like to change the background color? (y/n) ")
    if background == 'y':
        print("\nRecommended colors: (0,0,0) or (255,255,255)")
        print("Other colors may result in invisible snack and may make game harder\n")
        backred = int(input("Enter the amount of red coloring for the background between 0 and 255: "))
        backgreen = int(input("Enter the amount of green coloring for the background between 0 and 255: "))
        backblue = int(input("Enter the amount of blue coloring for the background between 0 and 255: "))
        while (backred > 255 or backblue > 255 or backgreen > 255 or backred < 0 or backblue < 0 or backgreen < 0):
            print("\nYou entered an invalid input. Please enter between 0 and 255\n")
            backred = int(input("Enter the integer number for the amount of red coloring between 0 and 255: "))
            backblue = int(input("Enter the integer number for the amount of blue coloring between 0 and 255: "))
            backgreen = int(input("Enter the integer number for the amount of green coloring between 0 and 255: "))
        backcolor = (backred,backgreen,backblue)
    wallChange = input("\nWould you like to change if the snake can pass through walls? (y/n) ")
    if wallChange == 'y':
        tempwall = input("Enter 'open' to allow the snake to pass through, or enter 'closed' to deny the snake: ")
        while (tempwall != "open" and tempwall != "closed"):
            print("\nYou entered an invalid input. Please enter 'open' or 'closed' without the apostrophes\n")
            tempwall = input("Enter 'open' to allow the snake to pass through, or enter 'closed' to deny the snake: ")
        walls = tempwall
    speedChange = input("\nWould you like to change the speed of the game? (y/n) ")
    if speedChange == 'y':
        print("\nRecommended frames per second: 10")
        print("Entering less than 8 may result in a slow game, and entering greater than 10 may result in a fast game\n")
        speed = int(input("Enter the frames per second you would like to play at: "))
        while (speed <= 0):
            print("\nYou entered an invalid input. Please enter an integer greater than 0\n")
            speed = int(input("Enter the frames per second you would like to play at: "))
    

#   Main function which calls other functions and connects game

def main():
    global width, rows, height, s, snack, backcolor, walls, speed
    width = 500 # Width of window in pixels
    rows = 20   # Number of rows in window
    flag = True
    red = random.randrange(0,255)   # Random red color
    green = random.randrange(0,255) # Random green color
    blue = random.randrange(0,255)  # Random blue color
    backcolor = (0,0,0) # Base background color
    walls = "open"  # Walls can be passed through
    speed = 10  # How many frames per second the game runs at

    while (red == 0 and green == 0 and blue == 0):  # While the random snack color is black (same as background)
        red = random.randrange(0,255)
        green = random.randrange(0,255)
        blue = random.randrange(0,255)

    s = snake((255,0,0), (10,10))   # Creates a snake object with color and initial position

    print("\n")

    cprint(figlet_format('SNAKE', font='big'),'white')

    print("|_____________ Welcome to Snake! _____________|")
    print(" - The objective is to collective as many multicolored snacks and grow the snake.")
    print(" - The longer the snake, the higher the score.")
    print(" - Passing through the sides of the screen will cause the snake to appear on the opposite side.")
    print(" - Running into yourself will result in a game over.")
    print(" - Use the arrows keys to move the snake across the grid.")

    change = input("\nWould you like to change the setting? (y/n) ")
    
    if change == 'y':
        settings()

    start = input("To start the game, please press enter")

    while (start != ""):
        print("\nInvalid input, please press enter\n")
        start = input("To start the game, please press enter")
    
    cube.rows = rows
    cube.width = width
    snack = cube(randomSnack(rows), color=(red,green,blue))    # Creates a snake cube object with color and inital random position

    win = pygame.display.set_mode((width, width))  # Window object
    clock = pygame.time.Clock() # Clock object to help track time

    while flag:
        pygame.time.delay(50) # Delays program by 50 ms so it does not run too fast
        clock.tick(speed)  # Makes sure game doesn't run past 10 frames per second (unless changed in settings)
        s.move()    # Calls snake object move function

        if (s.body[0].pos == snack.pos):    # If x position is equal to snack position
            s.addCube()   # Add new cube to snake
            red = random.randrange(0,255)
            green = random.randrange(0,255)
            blue = random.randrange(0,255)
            while (red == 0 and green == 0 and blue == 0):  # While the random snack color is black (same as background)
                red = random.randrange(0,255)
                green = random.randrange(0,255)
                blue = random.randrange(0,255)
            snack = cube(randomSnack(rows), color=(red,green,blue))    # Create new cube

        for x in range(len(s.body)):        # Returns the score and displays game over message if player runs into themselves
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
                print("Score: ", len(s.body))
                printmessage("You ran into yourself and lost", "Play Again?")
                s.reset((10,10),)
                break

        if (len(s.body) == 400):    # If the snake reaches the size of the board (20x20), then the player wins
            print("Score: ", len(s.body))
            printmessage("You won the game!", "Play Again?")
            s.reset((10,10),)

        redrawWindow(win)   # Redraws window

    pass

main()
