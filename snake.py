import random
import sys
import pygame

WIDTH = 400
HEIGHT = 400
FPS = 8

GRID_SIZE = 10
# GAME_GRID = []
# for i in range(int(HEIGHT / GRID_SIZE)):
#     GAME_GRID.append([0] * int(WIDTH / GRID_SIZE))

SNAKE_X = [0] #TO get position: WIDTH / GRID_SIZE * [X]
SNAKE_Y = [0]
SNAKE_MOVE_DIR = 'D'

FOOD_X = [0]
FOOD_Y = [0]

SCORE = 0
def MoveSnake(x, y):
    #Check if head is colliding with body
    for i in range(len(SNAKE_X) -1):
        i += 1 #Don't count the head obviously
        if SNAKE_X[i] == SNAKE_X[0] and SNAKE_Y[i] == SNAKE_Y[0]:
            return True
    #some checks to make sure it does not exceed game screen
    if (SNAKE_X[0] + x >= 0 and SNAKE_X[0] + x <= GRID_SIZE - 1) and SNAKE_Y[0] + y >= 0 and SNAKE_Y[0] + y <= GRID_SIZE - 1:
        for i in range(len(SNAKE_X) - 1): #Subtract 1 as there is nothing ahead of the head
            #Index backward
            index = len(SNAKE_X) - i - 1 # subtract 1 as len is 1 based
            #Move the previous body segment to the segment ahead of it
            #print(SNAKE_X[index], "->", SNAKE_X[index - 1])
            SNAKE_X[index] = SNAKE_X[index - 1]
            SNAKE_Y[index] = SNAKE_Y[index - 1]
            #print(SNAKE_X, SNAKE_Y)
        #Set the head,
        SNAKE_X[0] = SNAKE_X[0] + x
        SNAKE_Y[0] = SNAKE_Y[0] + y
    else:
        return True
random.seed()
def SpawnFood():
    FOOD_X[0] = random.randrange(GRID_SIZE)
    FOOD_Y[0] = random.randrange(GRID_SIZE)
SpawnFood()
def FoodCollision():
    if SNAKE_X[0] == FOOD_X[0] and SNAKE_Y[0] == FOOD_Y[0]:
        SpawnFood()
        if SNAKE_MOVE_DIR == 'U':
            SNAKE_X.append(SNAKE_X[len(SNAKE_X) - 1])
            SNAKE_Y.append(SNAKE_Y[len(SNAKE_Y) - 1] + 1)
        elif SNAKE_MOVE_DIR == 'D':
            SNAKE_X.append(SNAKE_X[len(SNAKE_X) - 1])
            SNAKE_Y.append(SNAKE_Y[len(SNAKE_Y) - 1] - 1)
        elif SNAKE_MOVE_DIR == 'L':
            SNAKE_X.append(SNAKE_X[len(SNAKE_X) - 1] + 1)
            SNAKE_Y.append(SNAKE_Y[len(SNAKE_Y) - 1])
        elif SNAKE_MOVE_DIR == 'R':
            SNAKE_X.append(SNAKE_X[len(SNAKE_X) - 1] - 1)
            SNAKE_Y.append(SNAKE_Y[len(SNAKE_Y) - 1])
        global SCORE
        SCORE += 1
        return True
    else:
        return False
#Init
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
CLOCK = pygame.time.Clock()

#Game
GAME_OVER = False
RUNGAME = True
def MainGame():
    global GAME_OVER
    global RUNGAME
    global SNAKE_MOVE_DIR
    global FOOD_X
    global FOOD_Y
    global SNAKE_X
    global SNAKE_Y
    global SCORE
    global GRID_SIZE
    while GAME_OVER == False and RUNGAME:
        #Keep loop running at right speed
        CLOCK.tick(FPS)
        #Process events
        for event in pygame.event.get():
            #Window close
            if event.type == pygame.QUIT:
                RUNGAME = False
            #Inputs
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and SNAKE_MOVE_DIR != 'D':
                    SNAKE_MOVE_DIR = 'U'
                elif event.key == pygame.K_s and SNAKE_MOVE_DIR != 'U':
                    SNAKE_MOVE_DIR = 'D'
                elif event.key == pygame.K_a and SNAKE_MOVE_DIR != 'R':
                    SNAKE_MOVE_DIR = 'L'
                elif event.key == pygame.K_d and SNAKE_MOVE_DIR != 'L':
                    SNAKE_MOVE_DIR = 'R'
        #Update
        #GAME_SPRITES.update()
        #Enlarge the screen if score is greater than area / 5
        if SCORE > GRID_SIZE * GRID_SIZE / 10:
            GRID_SIZE += 1
        #Move the snake
        if SNAKE_MOVE_DIR == 'U':
            GAME_OVER = MoveSnake(0, -1)
        elif SNAKE_MOVE_DIR == 'D':
            GAME_OVER = MoveSnake(0, 1)
        elif SNAKE_MOVE_DIR == 'L':
            GAME_OVER = MoveSnake(-1, 0)
        elif SNAKE_MOVE_DIR == 'R':
            GAME_OVER = MoveSnake(1, 0)
        #Bypass game over at startup
        if GAME_OVER == None:
            GAME_OVER = False
        #Have we nommed any food?
        FoodCollision()

        # Draw
        SCREEN.fill((255, 255, 255))
        #Score text
        basicfont = pygame.font.SysFont(None, 24)
        text = basicfont.render(str(SCORE) + " | " + str(GRID_SIZE), True, (0, 0, 0), (255, 255, 255))
        textrect = text.get_rect()
        textrect.centerx = SCREEN.get_rect().centerx
        textrect.centery = SCREEN.get_rect().centery
        SCREEN.blit(text, textrect)
        #Calculate the position of the snake based on its position within the grid
        #Head
        pygame.draw.rect(SCREEN, (200, 255, 0), (WIDTH / GRID_SIZE * SNAKE_X[0], HEIGHT / GRID_SIZE * SNAKE_Y[0],
                                                WIDTH / GRID_SIZE - 1, HEIGHT / GRID_SIZE - 1))
        #Body
        for i in range(len(SNAKE_X) - 1):
            i += 1 #Don't draw the head
            pygame.draw.rect(SCREEN, (0, 255, 0), (WIDTH / GRID_SIZE * SNAKE_X[i], HEIGHT / GRID_SIZE * SNAKE_Y[i],
                                                WIDTH / GRID_SIZE - 1, HEIGHT / GRID_SIZE - 1))  #-1 so you can see the body segments
        #Draw food
        for i in range(len(FOOD_X)):
            pygame.draw.rect(SCREEN, (255, 0, 0), (WIDTH / GRID_SIZE * FOOD_X[0], HEIGHT / GRID_SIZE * FOOD_Y[0],
                                                WIDTH / GRID_SIZE - 5, HEIGHT / GRID_SIZE - 5))
        pygame.display.flip() #Draw, do this last as we are FLIPPing the display
    if GAME_OVER:
        print("Snake Died :(")
        #Reset the game
        GAME_OVER = False
        SNAKE_MOVE_DIR = 'D'
        SNAKE_X = [0] #TO get position: WIDTH / GRID_SIZE * [X]
        SNAKE_Y = [0]

        FOOD_X = [0]
        FOOD_Y = [0]
        SCORE = 0
        GRID_SIZE = 10
        SpawnFood()
#Keep running the game
while RUNGAME:
    MainGame()
pygame.quit()
