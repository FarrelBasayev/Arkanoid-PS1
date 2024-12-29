import pygame
from time import *
from random import *
pygame.init()
running = True

screen = pygame.display.set_mode((500,500))
background = (83,0,0)
screen.fill(background)
clock = pygame.time.Clock()
plat_x = 200
plat_y = 400

class Area():
    def __init__(self,x,y,width,height,color):
        self.rect = pygame.Rect(x,y,width,height)
        self.fill_color = background

    def color(self,new_color):
        self.fill_color = new_color

    def fill(self):
        pygame.draw.rect(screen,self.fill_color,self.rect)

    def collide_point(self,x,y):
        return self.rect.collidepoint(x,y)

    def collide_rect(self,rect):
        return self.rect.colliderect(rect)

class Label(Area):
    def set_text(self,text,fsize=12,color=(0,0,0)):
        self.image = pygame.font.SysFont('verdana',fsize).render(text,True,color)

    def draw(self,shift_x=0,shift_y=0):
        self.fill()
        screen.blit(self.image,(self.rect.x + shift_x,self.rect.y + shift_y))


class Picture(Area):
    def __init__(self,filename,x=0,y=0,width=10,height=10):
        Area.__init__(self,x=x,y=y,width=width,height=height,color=None)
        self.image = pygame.image.load(filename)

    def draw(self):
        screen.blit(self.image,(self.rect.x,self.rect.y))


ball = Picture('ball.png',160,200,50,50)
ball_x = 6
ball_y = 6
platform = Picture('platform.png',plat_x,plat_y,100,30)
move_right = False
move_left = False

start_x = 5
start_y = 5
count = 9
monsters = []


for j in range(3):
    y = start_y + 55*j
    x = start_x + 27.5*j
    for  i in range(count):
        monster = Picture('enemy2.png',x,y,50,50)
        monsters.append(monster)
        x = x + 55
    count -= 1



while running:
    
    ball.fill()
    platform.fill()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move_right = True
            elif event.key == pygame.K_LEFT:
                move_left = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right = False
            elif event.key == pygame.K_LEFT:
                move_left = False
    if move_right == True:
        platform.rect.x += 7
    elif move_left == True:
        platform.rect.x -= 7
    if platform.rect.x > 400:
        move_right = False
    elif platform.rect.x < 0:
        move_left = False
    ball.rect.x += ball_x
    ball.rect.y += ball_y
    if ball.collide_rect(platform.rect):
        ball_y *= -1
    if ball.rect.x > 450:
        ball_x *= -1
    elif ball.rect.x < 0:
        ball_x *= -1
    elif ball.rect.y < 0:
        ball_y *= -1
    
    if ball.rect.y > (platform.rect.y)+20:
        status = Label(140,250,50,50,color=background)
        status.set_text('LOL U LOSE',55,(255,0,0))
        status.draw(10,10)
        running = False
    if len(monsters) == 24:
        title = Label(140,250,50,50,color=background)
        title.set_text('DESTROY THE BASAYEV',30,(255,0,0))
        title.draw(10,10)
    if len(monsters) == 0:
        status = Label(140,250,50,50,color=background)
        status.set_text('OMG U WIN',55,(0,255,0))
        status.draw(10,10)
        running = False
    for monster in monsters:
        monster.draw()
        if ball.collide_rect(monster.rect):
            monsters.remove(monster)
            monster.fill()
            ball_y *= -1

    platform.draw()
    ball.draw()

    pygame.display.update()
    clock.tick(40)