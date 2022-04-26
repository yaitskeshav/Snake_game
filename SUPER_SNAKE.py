import pickle
from tkinter.tix import PopupMenu
import pygame
import random
import os


try:
    with open('score.dat', 'rb') as file:
        high_score = pickle.load(file)
except:
    high_score = 0



display_width = 900
display_height = 600
block_size = 30 
FPS = 10


os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
pygame.font.init()
pygame.mixer.init()
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('SUPER SNAKE')
clock = pygame.time.Clock() 


bialy = (255,255,255)
black = (0,0,0)
czerwony = (255,0,0)
LIGHT_RED = (155,0,0)

RED=(247, 2, 2)
GREEN=(67, 247, 2)
BLUE=(0, 0, 247)

PINK=(255, 0, 85)
YELLOW=(242, 255, 0)
SAFFRON=(247, 92, 2)


ciemnyZielony = (0,120,0)

HEAD = pygame.image.load('snakehead30x30.png')
TAIL = pygame.image.load('snaketail30x30.png')
BODY = pygame.image.load('snakebody30x30.png')
TURNLEFT = pygame.image.load('turnleft30x30.png')
TURNRIGHT = pygame.image.load('turnright30x30.png')

SUPERHEAD = pygame.image.load('supersnakehead30x30.png')
SUPERTAIL = pygame.image.load('supersnaketail30x30.png')
SUPERBODY = pygame.image.load('supersnakebody30x30.png')
SUPERTURNLEFT = pygame.image.load('superturnleft30x30.png')
SUPERTURNRIGHT = pygame.image.load('superturnright30x30.png')


# Background Images

background1 = pygame.image.load('bg1.jpg')
background2 = pygame.image.load('bg2.jpg')
background3 = pygame.image.load('bg3.png')
background4 = pygame.image.load('bg4.jpg')
background5 = pygame.image.load('bg5.jpg')
background6 = pygame.image.load('bg6.jpg')
background7 = pygame.image.load('bg7.jpg')
background8 = pygame.image.load('bg8.jpg')
background9 = pygame.image.load('bg9.jpg')
background10 = pygame.image.load('bg10.jpeg')




wall = pygame.image.load('wall2.gif')
APPLE = pygame.image.load('NEWAPPLE.png')
APPLE_BIG = pygame.image.load('NEWAPPLE_BIG.png')
STONE = pygame.image.load('stone.gif')
STONE_BIG = pygame.image.load('ROCK_BIG.png')
START = pygame.image.load('PRISMA1.jpg')
CONTROLS = pygame.image.load('PRISMA2.jpg')
GAMEOVER = pygame.image.load('GAMEOVER.png')
RED_DIAMOND = pygame.image.load('RED_DIAMOND.png')
WHITE_DIAMOND = pygame.image.load('WHITE_DIAMOND.png')
WHITE_DIAMOND_BIG = pygame.image.load('WHITE_DIAMOND_BIG.png')
BLACK_DIAMOND = pygame.image.load('BLACK_DIAMOND.png')
BLACK_DIAMOND_BIG = pygame.image.load('BLACK_DIAMOND_BIG.png')
TIMERBACKGROUND = pygame.image.load('TIMERBACKGROUND.png')

ACTIVE_B = pygame.image.load('ACTIVE.png')
INACTIVE_B = pygame.image.load('INACTIVE.png')

POINT = pygame.mixer.Sound("sfx_point.wav")
HIT = pygame.mixer.Sound("sfx_hit.wav")
EVOLUTION = pygame.mixer.Sound("Star_Wars_-_Imperial_march.wav")
STONEDESTROY = pygame.mixer.Sound("STONEDESTROY.wav")

pygame.mixer.music.load('music.mp3')
pygame.mixer.music.set_volume(0.2)

# SILNIK GRY

class stones:
    
    def __init__(self):
        self.list = []

    def add(self, other):
    
        newStoneX, newStoneY = randLocationGen(self.list, other.list)
        newStone = [newStoneX, newStoneY]
        self.list.append(newStone)
        
    def show(self):

        for i in range(len(self.list)):
            gameDisplay.blit(STONE, (self.list[i][0],self.list[i][1]))
            
    def destroy(self, stone):
         
        self.list.remove(stone)
            
class apple:
    
    def __init__(self, stones, snake):
        self.renew(stones, snake)
    
    def renew(self, stones, snake):
        self.x, self.y = randLocationGen(stones.list, snake.list)
        
    def show(self):
        gameDisplay.blit(APPLE, (self.x, self.y))
        
class diamond:
    
    def __init__(self):
        self.timer = 0
        self.x = None
        self.y = None
        
    def renew(self, stones, snake, FPS):
        self.timer = 10*FPS
        self.x, self.y = randLocationGen(stones.list, snake.list)
    
    def kill(self):
        self.timer = 0
        self.x = None
        self.y = None
        
    def show(self, color):
        if self.timer > 0:
            self.timer -= 1
            if color == 'red':
                gameDisplay.blit(RED_DIAMOND, (self.x, self.y))
            elif color =='white':
                gameDisplay.blit(WHITE_DIAMOND, (self.x, self.y))
            elif color =='black':
                gameDisplay.blit(BLACK_DIAMOND, (self.x, self.y))
        else:
            self.kill()
            
          
class snake:
    
    def __init__(self, lead_x, lead_y):
        self.direction = "right"
        
        self.list = [["right", lead_x-2*block_size, lead_y],
                     ["right", lead_x-block_size, lead_y],
                     ["right", lead_x, lead_y]]
                          
        self.head = ["right", lead_x, lead_y]
        self.length = 3
        self.superTimer = 0
        
    def superSnake(self, FPS):
        self.superTimer = 10*FPS
        
    def update(self, lead_x, lead_y):
        self.head = []
        self.head.append(self.direction)
            
        self.head.append(lead_x)
        self.head.append(lead_y)
        
        self.list.append(self.head)
        
        if len(self.list) > self.length:
            del self.list[0]

        if self.superTimer > 0:
            self.superTimer -= 1

    def show(self, FPS):
        
        if self.superTimer > 0:
            self.view(SUPERHEAD, SUPERTAIL, SUPERBODY, SUPERTURNLEFT, SUPERTURNRIGHT)
            
            gameDisplay.blit(TIMERBACKGROUND, (800, 529))
            font = pygame.font.Font('flup.ttf', 25)
            text = font.render(str(self.superTimer/FPS), True, black)
            gameDisplay.blit(text, [830,537])
            
        else:
            self.view(HEAD, TAIL, BODY, TURNLEFT, TURNRIGHT)
        

                
    def view(self, head, tail, body, turnleft, turnright):
        
        gameDisplay.blit(rotate(self.list[-1],head), (self.list[-1][1],self.list[-1][2]))       
        gameDisplay.blit(rotate(self.list[1],tail), (self.list[0][1],self.list[0][2]))
            
        for i in range(1, self.length-1):
            
            if self.list[i][0] == self.list[i+1][0]:
                gameDisplay.blit(rotate(self.list[i],body), (self.list[i][1],self.list[i][2]))
            
            elif (self.list[i][0] == "down" and self.list[i+1][0] == "right") or (self.list[i][0] == "right" and self.list[i+1][0] == "up") or (self.list[i][0] == "up" and self.list[i+1][0] == "left") or (self.list[i][0] == "left" and self.list[i+1][0] == "down"):       
                gameDisplay.blit(rotate(self.list[i+1],turnleft), (self.list[i][1],self.list[i][2]))
            
            elif (self.list[i][0] == "right" and self.list[i+1][0] == "down") or (self.list[i][0] == "down" and self.list[i+1][0] == "left") or (self.list[i][0] == "left" and self.list[i+1][0] == "up") or (self.list[i][0] == "up" and self.list[i+1][0] == "right"):        
                gameDisplay.blit(rotate(self.list[i+1],turnright), (self.list[i][1],self.list[i][2]))
        
    def isDead(self, other):
        
        for eachSegment in self.list[:-1]:
            if eachSegment[1] == self.head[1] and eachSegment[2] == self.head[2]:
                HIT.play()
                pygame.mixer.music.set_volume(0.2)
                return True
                
        if self.superTimer <= 0:
            
            for eachStone in other.list:
                if eachStone[0] == self.head[1] and eachStone[1] == self.head[2]:
                    HIT.play()
                    return  True
                    
            if self.head[1] >= display_width-block_size or self.head[1] < block_size or self.head[2] >= display_height-block_size or self.head[2] < block_size:
                HIT.play()
                return True
                
        return False
        
    def trim(self):
        if len(self.list) > 13:
            self.list = self.list[10:]
            self.length -= 10

def rotate(segment, image):
    if segment[0] == "right":
        rotatedImage = pygame.transform.rotate(image, 0)
    elif segment[0] == "left":
        rotatedImage = pygame.transform.rotate(image, 180)
    elif segment[0] == "up":
        rotatedImage = pygame.transform.rotate(image, 90)    
    elif segment[0] == "down":
        rotatedImage = pygame.transform.rotate(image, 270)       
    return rotatedImage        
        
def draw_text(text, color, size, x, y):
    font = pygame.font.Font('flup.ttf', size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    gameDisplay.blit(text_surface, text_rect)
    
def button(text, x, y, width, height, inactive, active, text_color = black, action = None):
    cursor = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if (x + width > cursor[0] > x and y + height > cursor[1] > y):
        gameDisplay.blit(ACTIVE_B, (x,y))
        
        if click[0] == 1 and action != None:
            if action == 'play' or action == 'again':
                gameLoop()


            elif action=="reset-game":
                with open('score.dat', 'wb') as file:
                    pickle.dump(0, file)
                gameLoop()

            elif action == 'controls' or action == 'previous':
                show_controls()

            elif action == 'levels':
                show_all_levels()

            elif action == 'quit':
                pygame.quit()
                pygame.font.quit()
                quit()

            elif action == 'menu':
                show_game_intro()

            elif action == 'next':
                show_controls_next()
            
            elif action=='level-1':
                gameLoop("1")
            
            elif action=='level-2':
                gameLoop("2")

            elif action=='level-3':
                gameLoop("3")

            elif action=='level-4':
                gameLoop("4")

            elif action=='level-5':
                gameLoop("5")

            elif action=='level-6':
                gameLoop("6")

            elif action=='level-7':
                gameLoop("7")

            elif action=='level-8':
                gameLoop("8")

            elif action=='level-9':
                gameLoop("9")
                
            elif action=='level-10':
                gameLoop("10")
        
    else:
        gameDisplay.blit(INACTIVE_B, (x,y))
        
    draw_text(text, text_color, int(round(height/2)), x + width/2, y + height/4)
     
def score(score,level,highscore):
    font = pygame.font.Font('flup.ttf', 25)
    text = font.render("SCORE: "+str(score), True, black,YELLOW)
    level_num=font.render("LEVEL: "+str(level), True,black,SAFFRON)
    h_score=font.render("HIGH SCORE:"+str(highscore), True, RED ,YELLOW)
    gameDisplay.blit(text, [105,5])
    gameDisplay.blit(level_num, [405,5])
    gameDisplay.blit(h_score, [700,5])
    
def randLocationGen (stonesList, snakeList):
    randX = round((random.randrange(block_size, display_width - 2*block_size))/block_size)*block_size
    randY = round((random.randrange(block_size, display_height - 2*block_size))/block_size)*block_size
    

    for stone in stonesList:
        for element in snakeList:
            if(randX == stone[0] and randY == stone[1]) or (randX == element[1] and randY == element[2]):
                print("!TEXT!" + str(randX)+str(element[1]) + str(randY)+str(element[2]))
                return randLocationGen(stonesList, snakeList)
    
    return randX, randY


def pause ():
    
    draw_text("PAUSE", black, 60, display_width/2, display_height/2 -130)
    draw_text("Press P to continue", black, 30, display_width/2, display_height/2)
    pygame.display.update()
    
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return
                    
def show_game_intro():
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.font.quit()
                quit()                
                    
        gameDisplay.blit(START, (0,0))

        button("PLAY", 350, 225, 200, 70, czerwony, LIGHT_RED, action = 'play')
        button("CONTROLS", 350, 325, 200, 70, czerwony, LIGHT_RED, action = 'controls')
        button("LEVELS", 350, 425, 200, 70, czerwony, LIGHT_RED, action = 'levels')
        button("QUIT", 350, 525, 200, 70, czerwony, LIGHT_RED, action = 'quit')


        
        pygame.display.update()
        
        clock.tick(15)

         
def show_all_levels():
    try:
        with open('score.dat', 'rb') as file:
            high_score = pickle.load(file)
    except:
        high_score = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.font.quit()
                quit()
                
        gameDisplay.blit(CONTROLS, (0,0))
        
        draw_text("LEVELS", black, 50, display_width/2, display_height/2 -220)

        if high_score <=100:
            button("LEVEL 1", 50, 140, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-1')
            button("LEVEL 2", 350, 140, 200, 70, czerwony, LIGHT_RED,RED, )
            button("LEVEL 3", 650, 140, 200, 70, czerwony, LIGHT_RED, RED, )

            button("LEVEL 4", 50, 220, 200, 70, czerwony, LIGHT_RED, RED, )
            button("LEVEL 5", 350, 220, 200, 70, czerwony, LIGHT_RED, RED,)
            button("LEVEL 6", 650, 220, 200, 70, czerwony, LIGHT_RED, RED, )

            
            button("LEVEL 7", 50, 300, 200, 70, czerwony, LIGHT_RED, RED, )
            button("LEVEL 8", 350, 300, 200, 70, czerwony, LIGHT_RED, RED, )
            button("LEVEL 9", 650, 300, 200, 70, czerwony, LIGHT_RED, RED, )

            
            button("LEVEL 10", 350, 380, 200, 70, czerwony, LIGHT_RED, RED, )

        elif high_score>100 and high_score <=200:

            button("LEVEL 1", 50, 140, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-1')
            button("LEVEL 2", 350, 140, 200, 70, czerwony, LIGHT_RED,BLUE, action = 'level-2')
            button("LEVEL 3", 650, 140, 200, 70, czerwony, LIGHT_RED, RED,)

            button("LEVEL 4", 50, 220, 200, 70, czerwony, LIGHT_RED, RED, )
            button("LEVEL 5", 350, 220, 200, 70, czerwony, LIGHT_RED, RED, )
            button("LEVEL 6", 650, 220, 200, 70, czerwony, LIGHT_RED, RED, )

            
            button("LEVEL 7", 50, 300, 200, 70, czerwony, LIGHT_RED, RED, )
            button("LEVEL 8", 350, 300, 200, 70, czerwony, LIGHT_RED, RED, )
            button("LEVEL 9", 650, 300, 200, 70, czerwony, LIGHT_RED, RED, )

            
            button("LEVEL 10", 350, 380, 200, 70, czerwony, LIGHT_RED, RED, )


        
        
        elif high_score>200 and high_score <=300:

            button("LEVEL 1", 50, 140, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-1')
            button("LEVEL 2", 350, 140, 200, 70, czerwony, LIGHT_RED,BLUE, action = 'level-2')
            button("LEVEL 3", 650, 140, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-3')

            button("LEVEL 4", 50, 220, 200, 70, czerwony, LIGHT_RED, RED, )
            button("LEVEL 5", 350, 220, 200, 70, czerwony, LIGHT_RED, RED, )
            button("LEVEL 6", 650, 220, 200, 70, czerwony, LIGHT_RED, RED, )

            
            button("LEVEL 7", 50, 300, 200, 70, czerwony, LIGHT_RED, RED, )
            button("LEVEL 8", 350, 300, 200, 70, czerwony, LIGHT_RED, RED, )
            button("LEVEL 9", 650, 300, 200, 70, czerwony, LIGHT_RED, RED, )

            
            button("LEVEL 10", 350, 380, 200, 70, czerwony, LIGHT_RED, RED, )
            


        
        elif high_score>300 and high_score <=400:

            button("LEVEL 1", 50, 140, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-1')
            button("LEVEL 2", 350, 140, 200, 70, czerwony, LIGHT_RED,BLUE, action = 'level-2')
            button("LEVEL 3", 650, 140, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-3')

            button("LEVEL 4", 50, 220, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-4')
            button("LEVEL 5", 350, 220, 200, 70, czerwony, LIGHT_RED, RED, )
            button("LEVEL 6", 650, 220, 200, 70, czerwony, LIGHT_RED, RED, )

            
            button("LEVEL 7", 50, 300, 200, 70, czerwony, LIGHT_RED, RED, )
            button("LEVEL 8", 350, 300, 200, 70, czerwony, LIGHT_RED, RED, )
            button("LEVEL 9", 650, 300, 200, 70, czerwony, LIGHT_RED, RED, )

            
            button("LEVEL 10", 350, 380, 200, 70, czerwony, LIGHT_RED, RED, )


        
        
        elif high_score>400 and high_score <=500:

            button("LEVEL 1", 50, 140, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-1')
            button("LEVEL 2", 350, 140, 200, 70, czerwony, LIGHT_RED,BLUE, action = 'level-2')
            button("LEVEL 3", 650, 140, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-3')

            button("LEVEL 4", 50, 220, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-4')
            button("LEVEL 5", 350, 220, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-5')
            button("LEVEL 6", 650, 220, 200, 70, czerwony, LIGHT_RED, RED, )

            
            button("LEVEL 7", 50, 300, 200, 70, czerwony, LIGHT_RED, RED, )
            button("LEVEL 8", 350, 300, 200, 70, czerwony, LIGHT_RED, RED, )
            button("LEVEL 9", 650, 300, 200, 70, czerwony, LIGHT_RED, RED, )

            
            button("LEVEL 10", 350, 380, 200, 70, czerwony, LIGHT_RED, RED, )

        elif high_score>500 and high_score <=600:

            button("LEVEL 1", 50, 140, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-1')
            button("LEVEL 2", 350, 140, 200, 70, czerwony, LIGHT_RED,BLUE, action = 'level-2')
            button("LEVEL 3", 650, 140, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-3')

            button("LEVEL 4", 50, 220, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-4')
            button("LEVEL 5", 350, 220, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-5')
            button("LEVEL 6", 650, 220, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-6')

            
            button("LEVEL 7", 50, 300, 200, 70, czerwony, LIGHT_RED, RED, )
            button("LEVEL 8", 350, 300, 200, 70, czerwony, LIGHT_RED, RED, )
            button("LEVEL 9", 650, 300, 200, 70, czerwony, LIGHT_RED, RED, )

            
            button("LEVEL 10", 350, 380, 200, 70, czerwony, LIGHT_RED, RED, action = 'level-10')

        elif high_score>600 and high_score <=700:

            button("LEVEL 1", 50, 140, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-1')
            button("LEVEL 2", 350, 140, 200, 70, czerwony, LIGHT_RED,BLUE, action = 'level-2')
            button("LEVEL 3", 650, 140, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-3')

            button("LEVEL 4", 50, 220, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-4')
            button("LEVEL 5", 350, 220, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-5')
            button("LEVEL 6", 650, 220, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-6')

            
            button("LEVEL 7", 50, 300, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-7')
            button("LEVEL 8", 350, 300, 200, 70, czerwony, LIGHT_RED, RED,)
            button("LEVEL 9", 650, 300, 200, 70, czerwony, LIGHT_RED, RED, )

            
            button("LEVEL 10", 350, 380, 200, 70, czerwony, LIGHT_RED, RED, )

        elif high_score>700 and high_score <=800:

            button("LEVEL 1", 50, 140, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-1')
            button("LEVEL 2", 350, 140, 200, 70, czerwony, LIGHT_RED,BLUE, action = 'level-2')
            button("LEVEL 3", 650, 140, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-3')

            button("LEVEL 4", 50, 220, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-4')
            button("LEVEL 5", 350, 220, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-5')
            button("LEVEL 6", 650, 220, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-6')

            
            button("LEVEL 7", 50, 300, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-7')
            button("LEVEL 8", 350, 300, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-8')
            button("LEVEL 9", 650, 300, 200, 70, czerwony, LIGHT_RED, RED,)

            
            button("LEVEL 10", 350, 380, 200, 70, czerwony, LIGHT_RED, RED, )

        elif high_score>800 and high_score <=900:

            button("LEVEL 1", 50, 140, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-1')
            button("LEVEL 2", 350, 140, 200, 70, czerwony, LIGHT_RED,BLUE, action = 'level-2')
            button("LEVEL 3", 650, 140, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-3')

            button("LEVEL 4", 50, 220, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-4')
            button("LEVEL 5", 350, 220, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-5')
            button("LEVEL 6", 650, 220, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-6')

            
            button("LEVEL 7", 50, 300, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-7')
            button("LEVEL 8", 350, 300, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-8')
            button("LEVEL 9", 650, 300, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-9')

            
            button("LEVEL 10", 350, 380, 200, 70, czerwony, LIGHT_RED, RED,)   

        elif high_score>900:

            button("LEVEL 1", 50, 140, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-1')
            button("LEVEL 2", 350, 140, 200, 70, czerwony, LIGHT_RED,BLUE, action = 'level-2')
            button("LEVEL 3", 650, 140, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-3')

            button("LEVEL 4", 50, 220, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-4')
            button("LEVEL 5", 350, 220, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-5')
            button("LEVEL 6", 650, 220, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-6')

            
            button("LEVEL 7", 50, 300, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-7')
            button("LEVEL 8", 350, 300, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-8')
            button("LEVEL 9", 650, 300, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-9')

            
            button("LEVEL 10", 350, 380, 200, 70, czerwony, LIGHT_RED, BLUE, action = 'level-10')   





        button("MENU", 50, 500, 200, 70, czerwony, LIGHT_RED, action = 'menu')
  
        button("QUIT", 650, 500, 200, 70, czerwony, LIGHT_RED, action = 'quit')
    
        
        pygame.display.update()
        
        clock.tick(15)

def show_controls():
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.font.quit()
                quit()
                
        gameDisplay.blit(CONTROLS, (0,0))
        
        draw_text("GREETINGS", black, 38, display_width/2, display_height/2 -220)
        draw_text("Use arrows to navigate your little friend on the bord.", black, 28, display_width/2, display_height/2 -150)
        draw_text("Collect apples    , to increase your score and grow.", black, 28, display_width/2, display_height/2 -100)
        draw_text("Be careful not to hit walls and sudenlly appearing", black, 28, display_width/2, display_height/2 -50)
        draw_text("rocks     and most importantly don't bite yourself!", black, 28, display_width/2, display_height/2 -0)
        draw_text("Use diamonds to unlock special powers.", black, 28, display_width/2, display_height/2 +50)
        
        gameDisplay.blit(APPLE_BIG, (278, display_height/2 -110))
        gameDisplay.blit(STONE, (173, display_height/2 -0))
        
        button("MENU", 50, 500, 200, 70, czerwony, LIGHT_RED, action = 'menu')
        button("NEXT", 350, 500, 200, 70, czerwony, LIGHT_RED, action = 'next')
        button("QUIT", 650, 500, 200, 70, czerwony, LIGHT_RED, action = 'quit')
        
        pygame.display.update()
        
        clock.tick(15)
        
def show_controls_next():
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.font.quit()
                quit()
              
        gameDisplay.blit(CONTROLS, (0,0))
        
        draw_text("     will allow you to go through the walls", black, 28, display_width/2, display_height/2 -220)
        draw_text("and crash those sneaky stones.", black, 28, display_width/2, display_height/2 -170)
        draw_text("This effect will remain for 10 seconds.", black, 28, display_width/2, display_height/2 -120)
        draw_text("     will make snake shorter and easier to maneuver.", black, 28, display_width/2, display_height/2 -70)
        draw_text("Whenever you want,", black, 28, display_width/2, display_height/2 -20)
        draw_text("you can press P to pause the game."  , black, 28, display_width/2, display_height/2 +30)
        draw_text("GOOD LUCK!", black, 35, display_width/2, display_height/2 +100)
        
        gameDisplay.blit(BLACK_DIAMOND_BIG, (150, display_height/2 -225))
        gameDisplay.blit(WHITE_DIAMOND_BIG, (75, display_height/2 -75))        
        
        button("MENU", 50, 500, 200, 70, czerwony, LIGHT_RED, action = 'menu')
        button("PREVIOUS", 350, 500, 200, 70, czerwony, LIGHT_RED, action = 'previous')
        button("QUIT", 650, 500, 200, 70, czerwony, LIGHT_RED, action = 'quit')
        
        pygame.display.update()
        
        clock.tick(15)
                    
def gameLoop(*argv): 

    gameExit = False
    gameOver = False
    
    points = 0
    
    level=0

    for k in argv:

        try:
            if k=="1":
                gameDisplay.blit(background1, (0,0))
                level=1
                

            elif k=="2":
                gameDisplay.blit(background2, (0,0))
                points=100
                level=2
            elif k=="3":
                gameDisplay.blit(background3, (0,0))
                points=200
                level=3

            elif k=="4":
                gameDisplay.blit(background4, (0,0))
                points=300
                level=4

            elif k=="5":
                gameDisplay.blit(background5, (0,0))
                points=400
                level=5

            elif k=="6":
                gameDisplay.blit(background6, (0,0))
                points=500
                level=6

            elif k=="7":
                gameDisplay.blit(background7, (0,0))
                points=600
                level=7

            elif k=="8":
                gameDisplay.blit(background8, (0,0))
                points=700
                level=8

            elif k=="9":
                gameDisplay.blit(background9, (0,0))
                points=800
                level=9


            elif k=="10":
                gameDisplay.blit(background10, (0,0))
                points=900
                level=10

        except:
            gameDisplay.blit(background1, (0,0))

    speed = FPS

    lead_x = display_width/2 
    lead_y = display_height/2 
    lead_x_change = block_size 
    lead_y_change = 0 
    
    Snake = snake(lead_x, lead_y)
    Stones = stones()
    Apple = apple(Stones, Snake)
    Diamond = diamond()
    Trimer = diamond()

    while not gameExit:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                gameExit = True
            
            
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT) and Snake.direction != "right":
                    Snake.direction = "left"
                elif (event.key == pygame.K_RIGHT) and Snake.direction != "left":
                    Snake.direction = "right"
                elif (event.key == pygame.K_UP) and Snake.direction != "down":
                    Snake.direction = "up"    
                elif (event.key == pygame.K_DOWN) and Snake.direction != "up":
                    Snake.direction = "down"

                if event.key == pygame.K_p:
                    pause()
                    
        if Snake.direction == "left":
            lead_x_change = -block_size
            lead_y_change = 0
        elif Snake.direction == "right":
            lead_x_change = block_size
            lead_y_change = 0
        elif Snake.direction == "up":
            lead_y_change = -block_size
            lead_x_change = 0
        elif Snake.direction == "down":
            lead_y_change = block_size
            lead_x_change = 0
            
        lead_x += lead_x_change
        lead_y += lead_y_change
                    
        if (lead_x == Apple.x and lead_y == Apple.y):
            
            Apple.renew(Stones, Snake)
            Snake.length += 1
            points += 10
            POINT.play()
            
            if (points)%40 == 0:
                Stones.add(Snake)
                
            if (points)%70 == 0:
                speed += 1
                print(speed)
                
            if (points)%150 == 0:
                Diamond.renew(Stones, Snake, speed)
                
            if (points)%280 == 0:
                Trimer.renew(Stones, Snake, speed)
                
        if (lead_x == Diamond.x and lead_y == Diamond.y):
            
            points += 50
            Diamond.kill()
            Snake.superSnake(speed)
            EVOLUTION.play()
            
            if (points)%280 == 0:
                Trimer.renew(Stones, Snake, speed)
            
        if (lead_x == Trimer.x and lead_y == Trimer.y):
            points += 50
            Trimer.kill()
            Snake.trim()
            
            if (points)%150 == 0:
                Diamond.renew(Stones, Snake, speed)
            
        if Snake.superTimer > 0:
            if 15 <= Snake.superTimer:
                pygame.mixer.music.set_volume(0.05)
            if (15 > Snake.superTimer >= 10):
                pygame.mixer.music.set_volume(0.10)
            elif 10 > Snake.superTimer >= 5:
                pygame.mixer.music.set_volume(0.15)
            elif 5 > Snake.superTimer:
                pygame.mixer.music.set_volume(0.2)
            for stone in Stones.list:
                if stone[0] == Snake.head[1] and stone[1] == Snake.head[2]:
                    points += 20
                    Stones.destroy(stone)
                    STONEDESTROY.play()
        
                
            if lead_x >= display_width-block_size:
                lead_x = block_size
            elif lead_x < block_size:
                lead_x = display_width-2*block_size
            elif lead_y >= display_height-block_size:
                lead_y = block_size
            elif lead_y < block_size:
                lead_y = display_height-2*block_size

        Snake.update(lead_x, lead_y)
        gameOver = Snake.isDead(Stones)

        # CHANGING BG HERE

        if points<100:
            gameDisplay.blit(background1, (0,0))  
            level=1
    
        if points>=100 and points<200:        
            gameDisplay.blit(background2, (0,0))  
            level=2

        if points>=200 and points<300: 
            gameDisplay.blit(background3, (0,0))  
            level=3
            
        if points>=300 and points<400: 
            gameDisplay.blit(background4, (0,0))  
            level=4

        if points>=400 and points<500: 
            gameDisplay.blit(background5, (0,0))  
            level=5

        if points>=500 and points<600: 
            gameDisplay.blit(background6, (0,0))  
            level=6

        if points>=600 and points<700:
            gameDisplay.blit(background7, (0,0))  
            level=7
        if points>=700 and points<800: 
            gameDisplay.blit(background8, (0,0))  
            level=8

        if points>=800 and points<900: 
            gameDisplay.blit(background9, (0,0))  
            level=9

        if points>=900: 
            gameDisplay.blit(background10, (0,0))  
            level=10


            
        Apple.show()
        Stones.show()
        Diamond.show('black')
        Trimer.show('white')
        Snake.show(FPS)
        gameDisplay.blit(wall, (0,0))



        # Reading/Updating High Score
        with open('score.dat', 'rb') as file:
            hs=pickle.load(file)
           
            high_score=hs
            if hs<points:
                with open('score.dat', 'wb') as file:
            
                    pickle.dump(points, file)



            


        score(points,level,high_score) 
           
        pygame.display.update()   
        clock.tick(speed)
        
        while gameOver == True:

            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False 
                    if event.key == pygame.K_c:
                        gameLoop()
                        
            gameDisplay.blit(GAMEOVER, (0,0))
            draw_text("SCORE: " + str(points), black, 50, display_width/2, display_height/2-25)
            draw_text("HIGH SCORE: " + str(high_score), GREEN, 50, display_width/2, display_height/2-95)


            
                        
            button("MENU", 100, 370, 200, 70, czerwony, LIGHT_RED, action = 'menu')
            button("RESET GAME", 350, 370, 200, 60, czerwony,RED, LIGHT_RED, action = 'reset-game')
            button("QUIT", 600, 370, 200, 70, czerwony, LIGHT_RED, action = 'quit')

        
            pygame.display.update()
        
            clock.tick(15)





    pygame.quit()
    pygame.font.quit()

    quit()



pygame.mixer.music.play(loops=-1)
show_game_intro()

