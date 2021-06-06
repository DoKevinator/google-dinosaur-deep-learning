
import pygame 
from pygame import *

from cloud import * 
from ptera import *
from cactus import *
from scoreboard import *
from dinosaur import * 
from ground import * 

pygame.init()

background_color = (235, 235, 235)
width = 600
height = 150
win = pygame.display.set_mode( (width, height) )
clock = pygame.time.Clock()
pygame.display.set_caption( "Google Chrome Dino Game" )

high_score = 0

FPS = 60
gravity = 0.6

class Game():
    def __init__(self, dinosaur):
        self.gamespeed = 4
        self.dino = dinosaur

        self.cacti = pygame.sprite.Group()
        self.pteras = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        self.last_obstacle = pygame.sprite.Group()

        Cactus.containers = self.cacti
        Ptera.containers = self.pteras
        Cloud.containers = self.clouds

        # basic setup for the pygame window
        self.temp_images,self.temp_rect = load_sprite_sheet('numbers.png',12,1,11,int(11*6/5),-1)
        self.HI_image = pygame.Surface((22,int(11*6/5)))
        self.HI_rect = self.HI_image.get_rect()
        self.HI_image.fill(background_color)
        self.HI_image.blit(self.temp_images[10],self.temp_rect)
        self.temp_rect.left += self.temp_rect.width
        self.HI_image.blit(self.temp_images[11],self.temp_rect)
        self.HI_rect.top = height*0.1
        self.HI_rect.left = width*0.73

        win.fill( background_color )
        # self.dino = self.dinosaur(44,47)  # 44, 47 is the size of the self.dino
        # self.dino = self.dinosaur
        self.ground = Ground(-1 * self.gamespeed) 
        self.curScore = Scoreboard()
        self.highScore = Scoreboard(width*0.78)
        self.counter = 0
    
    def getGamespeed(self):
        return self.gamespeed
    
    def getDistToNextObstacle(self):
        if len(self.last_obstacle) > 0:
            return self.last_obstacle.sprites()[0].rect.left - self.dino.rect.right
        else :
            return 999

    def getTypeOfNextObstacle(self):
        return 1

    def getHeightOfNextObstacle(self):
        if len(self.last_obstacle) > 0:
            return self.last_obstacle.sprites()[0].rect.top
        else :
            return 0

    def run(self):
        if pygame.display.get_surface() == None:
            print("Couldn't load display surface")
            return True
        else:
            win.fill( background_color )

            for event in pygame.event.get():
                # check if X button is pressed
                if event.type == pygame.QUIT:
                    self.running = False
                    # save high score before exit
                    f = open("highscore", "w")
                    f.write(str(high_score))
                    f.close()
                    exit()  # close the program
    
    def updateGame(self):
        # check if the self.dino collided with an obstacle
        pygame.event.pump()
        for c in self.cacti:
            c.movement[0] = -1*self.gamespeed
            if pygame.sprite.collide_mask(self.dino,c):
                self.dino.isDead = True
        
        for p in self.pteras:
            p.movement[0] = -1*self.gamespeed
            if pygame.sprite.collide_mask(self.dino,p):
                self.dino.isDead = True
        
        # create new obstacles 
        if len(self.cacti) < 2:
            if len(self.cacti) == 0:
                #self.last_obstacle.empty()
                self.last_obstacle.add(Cactus(self.gamespeed,40,40))
            else:
                # this check is to help space out some obtacles to avoid impossible-to-dodge death traps
                if len(self.last_obstacle) > 0 and (600-self.last_obstacle.sprites()[len(self.last_obstacle)-1].rect.right) > 37.5*self.gamespeed:
                    for l in self.last_obstacle:
                        if l.rect.right < width*0.7 and random.randrange(0,50) == 10:
                            #self.last_obstacle.empty()
                            self.last_obstacle.add(Cactus(self.gamespeed, 40, 40))

        if len(self.pteras) == 0 and random.randrange(0,200) == 10 and self.counter > 500:
            # this check is to help space out some obtacles to avoid impossible-to-dodge death traps
            if len(self.last_obstacle) > 0 and (600-self.last_obstacle.sprites()[len(self.last_obstacle)-1].rect.right) > 37.5*self.gamespeed:
                for l in self.last_obstacle:
                    if l.rect.right < width*0.8:
                        #self.last_obstacle.empty()
                        self.last_obstacle.add(Ptera(self.gamespeed, 46, 40))
        
        if len(self.clouds) < 5 and random.randrange(0,300) == 10:
                Cloud(width,random.randrange(height/5,height/2))
        
        self.dino.update()
        self.cacti.update()
        self.pteras.update()
        self.clouds.update()
        self.ground.update()
        self.curScore.update(self.dino.score, background_color)
        self.highScore.update(high_score, background_color)
		
        if len(self.last_obstacle) > 0:
            if self.last_obstacle.sprites()[0].rect.left - self.dino.rect.right < 0:
                self.last_obstacle.remove(self.last_obstacle.sprites()[0])

        if pygame.display.get_surface() != None:
            win.fill(background_color)
            self.ground.draw(win)
            self.clouds.draw(win)
            self.curScore.draw(win)
            if high_score != 0:
                self.highScore.draw()
                win.blit(self.HI_image,self.HI_rect)
            self.cacti.draw(win)
            self.pteras.draw(win)
            self.dino.draw(win)

            pygame.display.update()
        clock.tick()

        if self.counter%700 == 699:
            self.ground.speed -= 1
            self.gamespeed += 1
        self.counter = self.counter + 1
    
        pygame.display.update()

