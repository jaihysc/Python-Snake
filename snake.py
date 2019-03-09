import random
import sys
import pygame

WIDTH = 400
HEIGHT = 400
FPS = 30

GRID_SIZE = 10
#Check resolution
exit = False
if WIDTH % GRID_SIZE != 0:
    print("[FATAL] | Width does not support desired grid size (width must be divisible by grid size)")
if HEIGHT % GRID_SIZE != 0:
    print("[FATAL] | Height does not support desired grid size (height must be divisible by grid size)")
if exit:
    sys.exit(0)
#
# GAME_GRID = []
# for i in range(int(HEIGHT / GRID_SIZE)):
#     GAME_GRID.append([0] * int(WIDTH / GRID_SIZE))

SNAKE_X = [2, 1, 0] #TO get position: WIDTH / GRID_SIZE * [X]
SNAKE_Y = [0, 0, 0]

class Player(pygame.sprite.Sprite):
    """
    Everything about the player
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect() #Figures out size of rect by itself
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
    def update(self):
        """
        Logic and events for the player every cycle
        """
        # self.rect.x += 5
        # if self.rect.left > WIDTH:
        #     self.rect.right = 0
def MoveSnake(x, y):
    #some checks to make sure it does not exceed game screen
    #if (SNAKE_X[0] + x >= 0 and SNAKE_X[0] + x <= GRID_SIZE - 1) and SNAKE_Y[0] + y >= 0 and SNAKE_Y[0] + y <= GRID_SIZE - 1:
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
#Init
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
CLOCK = pygame.time.Clock()

GAME_SPRITES = pygame.sprite.Group()
PLAYER = Player()
GAME_SPRITES.add(PLAYER)
#Game
RUNGAME = True
while RUNGAME:
    #Keep loop running at right speed
    CLOCK.tick(FPS)
    #Process events
    for event in pygame.event.get():
        #Window close
        if event.type == pygame.QUIT:
            RUNGAME = False
        #Inputs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                MoveSnake(0, -1)
            elif event.key == pygame.K_s:
                MoveSnake(0, 1)
            elif event.key == pygame.K_a:
                MoveSnake(-1, 0)
            elif event.key == pygame.K_d:
                MoveSnake(1, 0)
            elif event.key == pygame.K_SPACE:
                SNAKE_X.append(SNAKE_X[len(SNAKE_X) - 1] - 1)
                SNAKE_Y.append(SNAKE_Y[len(SNAKE_Y) - 1])
    #Update
    #GAME_SPRITES.update()
    # Draw
    SCREEN.fill((255, 255, 255))
    #Calculate the position of the snake based on its position within the grid
    #Head
    pygame.draw.rect(SCREEN, (200, 255, 0), (WIDTH / GRID_SIZE * SNAKE_X[0], HEIGHT / GRID_SIZE * SNAKE_Y[0],
                                               WIDTH / GRID_SIZE - 1, HEIGHT / GRID_SIZE - 1))
    #Body
    for i in range(len(SNAKE_X) - 1):
        i += 1 #Don't draw the head
        pygame.draw.rect(SCREEN, (0, 255, 0), (WIDTH / GRID_SIZE * SNAKE_X[i], HEIGHT / GRID_SIZE * SNAKE_Y[i],
                                               WIDTH / GRID_SIZE - 1, HEIGHT / GRID_SIZE - 1))  #-1 so you can see the body segments
    #GAME_SPRITES.draw(SCREEN)
    pygame.display.flip() #Draw, do this last as we are FLIPPing the display
pygame.quit()
