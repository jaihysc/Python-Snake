import sys, termios, tty, os, time
print("Welcome to snake...inside...Python")

#Game grid
gameGrid = []
#Populate game grid
width = 100
height = 30

#Snake
snakeX = [1, 0]
snakeY = [0, 0]

#Main
def drawGameGrid():
    #Reset the grid
    gameGrid = []
    for i in range(height):
        gameGrid.append([0] * width)

    #Set the snake to certain points on game grid
    for i in range(len(snakeX)):
        x = snakeX[i]
        y = snakeY[i]
        gameGrid[y][x] = 1

    #Draw
    os.system('clear')
    for i in range(height):
        line = ""
        for ii in range(width):
            if gameGrid[i][ii] == 0:
                line += "#"
            else:
                line += "~"
        print(line)

#Keypress
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
 
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def MoveSnake(x, y):
    for i in range(len(snakeX) - 1): #Subtract 1 as there is nothing ahead of the head
        #Index backward
        index = len(snakeX) - i - 1 # subtract 1 as len is 1 based
        #print(index, i)
        #Move the previous body segment to the segment ahead of it
        snakeX[index] = snakeX[index - 1]
        snakeY[index] = snakeY[index - 1]
    #Set the head, some checks to make sure it does not exceed game screen
    if snakeX[0] + x >= 0 and snakeX[0] + x < width:
        snakeX[0] = snakeX[0] + x
    if snakeY[0] + y >= 0 and snakeY[0] + y < height:
        snakeY[0] = snakeY[0] + y
while True:
    drawGameGrid()
    
    #Movement
    char = getch()

    if (char == "a"):
        MoveSnake(-1, 0)
    elif (char == "d"):
        MoveSnake(1, 0)
    elif (char == "w"):
        MoveSnake(0, -1)
    elif (char == "s"):
        MoveSnake(0, 1)
    elif (char == 't'):
        snakeX.append(snakeX[len(snakeX) - 1] - 1)
        snakeY.append(snakeY[len(snakeY) - 1] - 1)