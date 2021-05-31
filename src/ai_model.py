
import os
import neat 
# import visualize
import random

import pygame
from pygame import *

from common_tools import *
from scoreboard import *
from dinosaur import * 
from ground import * 
from cloud import * 
from ptera import *
from cactus import * 

pygame.init()

background_color = (235, 235, 235)
width = 600
height = 150
win = pygame.display.set_mode( (width, height) )
clock = pygame.time.Clock()
pygame.display.set_caption( "Google Dino Game" )

high_score = 0

FPS = 60
gravity = 0.6


# # 2-input XOR inputs and expected outputs.
# xor_inputs = [(0.0, 0.0), (0.0, 1.0), (1.0, 0.0), (1.0, 1.0)]
# xor_outputs = [   (0.0,),     (1.0,),     (1.0,),     (0.0,)]


# def eval_genomes(genomes, config):
#     for genome_id, genome in genomes:
#         genome.fitness = 4.0
#         net = neat.nn.FeedForwardNetwork.create(genome, config)
#         for xi, xo in zip(xor_inputs, xor_outputs):
#             output = net.activate(xi)
#             genome.fitness -= (output[0] - xo[0]) ** 2


# def run(config_file):
#     # Load configuration.
#     config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
#                          neat.DefaultSpeciesSet, neat.DefaultStagnation,
#                          config_file)

#     # Create the population, which is the top-level object for a NEAT run.
#     p = neat.Population(config)

#     # Add a stdout reporter to show progress in the terminal.
#     p.add_reporter(neat.StdOutReporter(True))
#     stats = neat.StatisticsReporter()
#     p.add_reporter(stats)
#     p.add_reporter(neat.Checkpointer(5))

#     # Run for up to 300 generations.
#     winner = p.run(eval_genomes, 300)

#     # Display the winning genome.
#     print('\nBest genome:\n{!s}'.format(winner))

#     # Show output of the most fit genome against training data.
#     print('\nOutput:')
#     winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
#     for xi, xo in zip(xor_inputs, xor_outputs):
#         output = winner_net.activate(xi)
#         print("input {!r}, expected output {!r}, got {!r}".format(xi, xo, output))

#     node_names = {-1:'A', -2: 'B', 0:'A XOR B'}
#     visualize.draw_net(config, winner, True, node_names=node_names)
#     visualize.plot_stats(stats, ylog=False, view=True)
#     visualize.plot_species(stats, view=True)

#     p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
#     p.run(eval_genomes, 10)

dino_inputs = [ "gameSpeed", "yPosition", "distToNextObstable", "typeOfNextObstacle", "heightOfNextObstacle"]
dino_outputs = [ "jump", "duck", "unduck" ]

gamespeed = 4

def load_ai_game(dinos):
    global high_score
    if high_score == 0:
        f = open("highscore")
        high_score = int(f.read())
        f.close()
    
    gamespeed = 4   # how fast the ground/cacti are moving

    cacti = pygame.sprite.Group()
    pteras = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()

    Cactus.containers = cacti
    Ptera.containers = pteras
    Cloud.containers = clouds

    temp_images,temp_rect = load_sprite_sheet('numbers.png',12,1,11,int(11*6/5),-1)
    HI_image = pygame.Surface((22,int(11*6/5)))
    HI_rect = HI_image.get_rect()
    HI_image.fill(background_color)
    HI_image.blit(temp_images[10],temp_rect)
    temp_rect.left += temp_rect.width
    HI_image.blit(temp_images[11],temp_rect)
    HI_rect.top = height*0.1
    HI_rect.left = width*0.73

    win.fill( background_color )
    # dino = Dinosaur(44,47)  # 44, 47 is the size of the dino
    # dino = dinosaur
    ground = Ground(-1 * gamespeed) 
    curScore = Scoreboard()
    highScore = Scoreboard(width*0.78)
    counter = 0

    Cloud.container = clouds
    running = True
    
    while running:
        if pygame.display.get_surface() == None:
            print("Couldn't load display surface")
            return True
        else:
            win.fill( background_color )

            for event in pygame.event.get():
                # check if X button is pressed
                if event.type == pygame.QUIT:
                    running = False
                    # save high score before exit
                    f = open("highscore", "w")
                    f.write(str(high_score))
                    f.close()
                    exit()  # close the program

                # # check if space or down arrow is pressed
                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_SPACE:
                #         dino.jump()
                #     elif event.key == pygame.K_DOWN:
                #         dino.duck()

                # # check for when down arrow is unpressed
                # if event.type == pygame.KEYUP:
                #     if event.key == pygame.K_DOWN:
                #         dino.unduck()

        for c in cacti:
                c.movement[0] = -1*gamespeed
                for d in dinos:
                    if pygame.sprite.collide_mask(d,c):
                        d.isDead = True
        
        for p in pteras:
                p.movement[0] = -1*gamespeed
                for d in dinos:
                    if pygame.sprite.collide_mask(d,p):
                        d.isDead = True
        
        if len(cacti) < 2:
                if len(cacti) == 0:
                    last_obstacle.empty()
                    last_obstacle.add(Cactus(gamespeed,40,40))
                else:
                    for l in last_obstacle:
                        if l.rect.right < width*0.7 and random.randrange(0,50) == 10:
                            last_obstacle.empty()
                            last_obstacle.add(Cactus(gamespeed, 40, 40))

        if len(pteras) == 0 and random.randrange(0,200) == 10 and counter > 500:
            for l in last_obstacle:
                if l.rect.right < width*0.8:
                    last_obstacle.empty()
                    last_obstacle.add(Ptera(gamespeed, 46, 40))
        
        if len(clouds) < 5 and random.randrange(0,300) == 10:
                Cloud(width,random.randrange(height/5,height/2))
        
        for d in dinos:
            d.update()
        cacti.update()
        pteras.update()
        clouds.update()
        ground.update()
        # curScore.update(dino.score)
        highScore.update(high_score)

        if pygame.display.get_surface() != None:
            win.fill(background_color)
            ground.draw()
            clouds.draw(win)
            curScore.draw()
            if high_score != 0:
                highScore.draw()
                win.blit(HI_image,HI_rect)
            cacti.draw(win)
            pteras.draw(win)
            for d in dinos:
                d.draw()

            pygame.display.update()
        clock.tick(FPS)
    
        # if dino.isDead:
        #     gameOver = True
        #     if dino.score > high_score:
        #         high_score = dino.score

        if counter%700 == 699:
            ground.speed -= 1
            gamespeed += 1
        counter = counter + 1

        # if gameOver:
        #     load_game()

        pygame.display.update()

def dinosAreDead( dinos ):
    for d in dinos:
        if not d.isDead:
            return False
    return True

def ai_plays(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 4.0
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        dinos = [Dinosaur(44,47)]*30    # create an array of 30 dinos
        load_ai_game(dinos)
        # while not dinosAreDead(dinos):


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(ai_plays, 300)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # # Show output of the most fit genome against training data.
    # print('\nOutput:')
    # winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    # for xi, xo in zip(xor_inputs, xor_outputs):
    #     output = winner_net.activate(xi)
    #     print("input {!r}, expected output {!r}, got {!r}".format(xi, xo, output))

    # node_names = {-1:'A', -2: 'B', 0:'A XOR B'}
    # visualize.draw_net(config, winner, True, node_names=node_names)
    # visualize.plot_stats(stats, ylog=False, view=True)
    # visualize.plot_species(stats, view=True)

    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    p.run(ai_plays, 10)

def main():
    run("./config-feedforward.txt")

main()

