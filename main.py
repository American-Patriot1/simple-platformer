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
        self.height=height
        self.width=width
        self.gravity=1
        self.grav_inc=.25
        self.jump_timer=20
        self.in_jump=0
        self.in_jump_move_direction=[1,1] #0 --> left | 1 --> right | [1,1] --> normal/have not moved
        self.on_surface=False
        self.slow_jump_movement=.4
    def move(self,keys):
        if ((keys[pygame.K_a]) and (self.id==0)) or ((keys[pygame.K_LEFT]) and (self.id==1)):
            if self.on_surface==False:
                if self.in_jump_move_direction==[1,1]:
                    self.in_jump_move_direction[1]=self.slow_jump_movement
            self.rect.centerx-=(10*self.in_jump_move_direction[0])
        if ((keys[pygame.K_d]) and (self.id==0)) or ((keys[pygame.K_RIGHT]) and (self.id==1)):
            if self.on_surface==False:
                if self.in_jump_move_direction==[1,1]:
                    self.in_jump_move_direction[0]=self.slow_jump_movement
            self.rect.centerx+=(10*self.in_jump_move_direction[1])
        if ((keys[pygame.K_SPACE]) and (self.id==0)) or ((keys[pygame.K_UP]) and (self.id==1)):
            if (self.on_surface==True) or (self.in_jump==True):
                self.rect.centery-=self.jump_timer
                self.jump_timer-=1
                self.in_jump=True
                if (self.jump_timer<=0):
                    self.gravity=1
                    self.in_jump=False
                    self.in_jump_move_direction=[1,1]
                    self.jump_timer=20
        elif self.in_jump==True:
            self.rect.centery-=self.jump_timer
            self.jump_timer-=2
            if (self.jump_timer<=0):
                self.gravity=1
                self.in_jump=False
                self.in_jump_move_direction=[1,1]
                self.jump_timer=20
    def grav(self):
        if (self.in_jump==False) and (self.on_surface==False):
            self.rect.centery+=self.gravity
            self.gravity+=self.grav_inc
    def collide(self):
        if pygame.sprite.spritecollide(self,plats,False):
                self.on_surface=True
                self.in_jump_move_direction=[1,1]
        else:
            self.on_surface=False
        for plat in plats:
            if self.rect.colliderect(plat.rect):
                if self not in plat.players_on_platform:
                    plat.players_on_platform.append(self)
            else:
                try:
                    plat.players_on_platform.remove(self)
                except:
                    pass
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
        self.height=height
        self.width=width
        self.rect.centerx=x
        self.rect.centery=y
        self.amt_move=amt_move/2
        self.movement=[random.choice(["left","right"]),amt_move]
        self.players_on_platform=[]
    def move(self):
        if self.movement[1]==0:
            pass
        elif self.movement[0]=="left":
            self.rect.centerx-=1
            for player in self.players_on_platform:
                player.rect.centerx-=1
            self.amt_move-=1
            if self.amt_move==0:
                self.movement[0]="right"
                self.amt_move=self.movement[1]
        elif self.movement[0]=="right":
            self.rect.centerx+=1
            for player in self.players_on_platform:
                player.rect.centerx+=1
            self.amt_move-=1
            if self.amt_move==0:
                self.movement[0]="left"
                self.amt_move=self.movement[1]
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, radius,reverse):
        super(Enemy, self).__init__()
        self.radius = radius
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        self.color1=0
        self.color2=0
        self.color3=0
        self.color4=255
        pygame.draw.circle(self.image, (self.color1,self.color2,self.color3,self.color4), (self.radius, self.radius), self.radius)
        self.rect=self.image.get_rect(center = (radius,radius))
        self.rect.centerx=x
        self.rect.centery=y
        self.gravity=1
        self.grav_inc=.25
        self.which_player=random.choice([x for x in players])
        self.reverse=reverse
        if self.reverse==-1:
            self.rect.centery=800
    def grav(self):
        self.rect.centery+=self.gravity*self.reverse
        self.gravity+=self.grav_inc
        if self.rect.centerx>self.which_player.rect.centerx:
            self.rect.centerx-=random.randint(0,2)
        else:
            self.rect.centerx+=random.randint(0,2)
        if self.rect.centery>800:
            self.reverse=random.choice([1,-1])
            self.rect.centerx=random.randint(100,1100)
            self.which_player=random.choice([x for x in players])
            if self.reverse==-1:
                self.rect.centery=800
            elif self.reverse==1:
                self.rect.centery=-100
        elif self.rect.centery>750:
            self.gravity=1
        elif self.rect.centery<-150:
            self.reverse=random.choice([1,-1])
            self.rect.centerx=random.randint(100,1100)
            self.which_player=random.choice([x for x in players])
            if self.reverse==-1:
                self.rect.centery=800
            elif self.reverse==1:
                self.rect.centery=-100
        elif self.rect.centery<-100:
            self.gravity=1
    def player_kill(self):
        pygame.sprite.spritecollide(self,players,True)
class Gold(pygame.sprite.Sprite):
    def __init__(self, x, y, radius,reverse):
        Gold(Enemy, self).__init__()
        self.radius = radius
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255,215,0,255), (self.radius, self.radius), self.radius)
        self.rect=self.image.get_rect(center = (radius,radius))
        self.rect.centerx=x
        self.rect.centery=y
        self.gravity=1
        self.grav_inc=.25
        self.left_or_right=random.choice(random.choice([-100,1500]))
        self.reverse=reverse
        if self.reverse==-1:
            self.rect.centery=800
    def grav(self):
        self.rect.centery+=self.gravity*self.reverse
        self.gravity+=self.grav_inc
        if self.rect.centerx>self.left_or_right:
            self.rect.centerx-=random.randint(0,2)
        else:
            self.rect.centerx+=random.randint(0,2)
        if self.rect.centery>800:
            self.reverse=random.choice([1,-1])
            self.rect.centerx=random.randint(100,1100)
            self.left_or_right=random.choice(random.choice([[-100,350],[1500,350]]))
            if self.reverse==-1:
                self.rect.centery=800
            elif self.reverse==1:
                self.rect.centery=-100
        elif self.rect.centery>750:
            self.gravity=1
        elif self.rect.centery<-150:
            self.reverse=random.choice([1,-1])
            self.rect.centerx=random.randint(100,1100)
            self.left_or_right=random.choice(random.choice([[-100,350],[1500,350]]))
            if self.reverse==-1:
                self.rect.centery=800
            elif self.reverse==1:
                self.rect.centery=-100
        elif self.rect.centery<-100:
            self.gravity=1
    def player_kill(self):
        pygame.sprite.spritecollide(self,players,False)

players=pygame.sprite.Group()
players.add(Player(600,0,25,50,0))
players.add(Player(600,0,25,50,1))

plats=pygame.sprite.Group()
plats.add(Platform(600,250,500,25,100))
plats.add(Platform(600,550,500,25,100))
plats.add(Platform(300,400,250,25,200))
plats.add(Platform(900,400,250,25,200))
plats.add(Platform(100,650,400,25,0))
plats.add(Platform(1100,650,400,25,0))
plats.add(Platform(100,100,400,25,0))
plats.add(Platform(1100,100,400,25,0))

# enemies=pygame.sprite.Group()
# for i in range(5):
#     enemies.add(Enemy(random.randint(100,1100),-100,12,random.choice([1,-1])))

golds=pygame.sprite.Group()
for i in range(1):
    golds.add(Gold(random.randint(100,1100),-100,12,random.choice([1,-1])))

running = True
count=0
while running:
    count+=1
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(WHITE)

    for player in players:
        player.collide()
        player.move(keys)
        player.grav()

    for p in plats:
        p.move()

    # for e in enemies:
    #     e.grav()
    #     e.player_kill()

    for gold in golds:
        gold.grav()
        gold.player_kill()

    players.draw(screen)

    plats.draw(screen)

    # enemies.draw(screen)

    golds.draw(screen)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()