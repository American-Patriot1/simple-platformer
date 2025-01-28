import pygame
import sys
import random
import math
pygame.init()
screen_width = 1200
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Tutorial")
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,id):
        super(Player, self).__init__()
        self.size = [width,height]
        self.id=id
        self.image = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)
        if id==0:
            self.color1=255
            self.color2=0
            self.color3=0
            self.color4=255
        elif id==1:
            self.color1=0
            self.color2=0
            self.color3=255
            self.color4=255
        pygame.draw.circle(self.image, (self.color1,self.color2,self.color3,self.color4), (self.size[0]/2, self.size[1]/2), self.size[0])
        self.rect=self.image.get_rect(center = (self.size[0]*2, self.size[1]*2))
        self.rect.centerx=x
        self.rect.centery=y
        self.gravity=5
        # self.grav_inc=.25
        self.jump_timer=20
        self.in_jump=0
        self.on_surface=False
    def move(self,keys):
        if ((keys[pygame.K_a]) and (self.id==0)) or ((keys[pygame.K_LEFT]) and (self.id==1)):
            self.rect.centerx+=-10
        if ((keys[pygame.K_d]) and (self.id==0)) or ((keys[pygame.K_RIGHT]) and (self.id==1)):
            self.rect.centerx+=10
        if ((keys[pygame.K_SPACE]) and (self.id==0)) or ((keys[pygame.K_UP]) and (self.id==1)):
            if (self.on_surface==True) or (self.in_jump==True):
                self.rect.centery-=self.jump_timer
                self.jump_timer-=1
                self.in_jump=True
                if (self.jump_timer<=0):
                    # self.gravity=10
                    self.in_jump=False
                    self.jump_timer=20
        elif self.in_jump==True:
            self.rect.centery-=self.jump_timer
            self.jump_timer-=2
            if (self.jump_timer<=0):
                # self.gravity=10
                self.in_jump=False
                self.jump_timer=20
    def grav(self):
        if (self.in_jump==False) and (self.on_surface==False):
            self.rect.centery+=self.gravity
            # self.gravity+=self.grav_inc
    def collide(self):
        if pygame.sprite.spritecollide(self,plats,False):
            self.on_surface=True
        else:
            self.on_surface=False
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height,amt_move):
        super(Platform, self).__init__()
        self.size = [width,height]
        self.image = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)
        self.color1=0
        self.color2=0
        self.color3=0
        self.color4=255
        self.image.fill((self.color1,self.color2,self.color3,self.color4))
        self.rect=self.image.get_rect(center = (self.size[0]*2, self.size[1]*2))
        self.rect.centerx=x
        self.rect.centery=y
        self.amt_move=amt_move/2
        self.movement=[random.choice(["left","right"]),amt_move]
    def move(self):
        if self.movement[1]==0:
            pass
        elif self.movement[0]=="left":
            self.rect.centerx-=1
            self.amt_move-=1
            if self.amt_move==0:
                self.movement[0]="right"
                self.amt_move=self.movement[1]
        elif self.movement[0]=="right":
            self.rect.centerx+=1
            self.amt_move-=1
            if self.amt_move==0:
                self.movement[0]="left"
                self.amt_move=self.movement[1]
plats=pygame.sprite.Group()
plats.add(Platform(600,200,500,25,0))
plats.add(Platform(600,600,500,25,0))
plats.add(Platform(300,400,100,25,200))
plats.add(Platform(900,400,100,25,200))
plats.add(Platform(600,400,100,25,200))
player=Player(600,0,25,50,0)
player1=Player(600,0,25,50,1)
running = True
count=0
while running:
    count+=1
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(WHITE)
    player.collide()
    player.move(keys)
    player.grav()
    player1.collide()
    player1.move(keys)
    player1.grav()

    for p in plats:
        p.move()

    screen.blit(player.image,player.rect)
    screen.blit(player1.image,player1.rect)
    plats.draw(screen)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()