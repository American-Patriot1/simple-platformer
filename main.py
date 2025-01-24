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
    def __init__(self,x,y,width,height):
        super(Player, self).__init__()
        self.size = [width,height]
        self.image = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)
        self.color1=0
        self.color2=0
        self.color3=0
        self.color4=255
        pygame.draw.circle(self.image, (self.color1,self.color2,self.color3,self.color4), (self.size[0]/2, self.size[1]/2), self.size[0])
        self.rect=self.image.get_rect(center = (self.size[0]*2, self.size[1]*2))
        self.rect.centerx=x
        self.rect.centery=y
        self.gravity=1
        self.jump_timer=0
    def move(self):
        if event.key==pygame.K_a:
            player.rect.centerx+=-10
        if event.key==pygame.K_d:
            player.rect.centerx+=10
        if event.key==pygame.K_s:
            player.rect.centery+=10
        if event.key==pygame.K_w:
            player.rect.centery+=-10
    def grav(self):
        player.rect.centery+=self.gravity
        player.gravity+=.1

class Platform(pygame.sprite.Sprite):
    def __init__(self, id_num, x, y, width, height):
        super(Platform, self).__init__()
        self.id=id_num
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
plat=Platform(1,600,350,500,50)
player=Player(600,0,25,50)
running = True
count=0
while running:
    count+=1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            player.move()
    screen.fill(WHITE)

    player.grav()
    screen.blit(player.image,player.rect)
    screen.blit(plat.image,plat.rect)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()