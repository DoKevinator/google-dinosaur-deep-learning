
# import os
import neat 
import visualize

import pygame
from pygame import *

from common_tools import *
from scoreboard import *
from dinosaur import * 
from ground import * 
from cloud import * 
from ptera import *
from cactus import * 
from game import * 

import os
os.environ["PATH"] += os.pathsep + 'C:\Program Files (x86)\graphviz-0.16\graphviz-0.16\graphviz'

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

# dino_inputs = [ "gameSpeed", "yPosition", "distToNextObstable", "typeOfNextObstacle", "heightOfNextObstacle"]
# dino_outputs = [ "jump", "duck", "unduck", "nothing" ]

gamespeed = 4

def dinosAreDead( dinos ):
    for d in dinos:
        if not d.isDead:
            return False
    return True

def findLargestIndex(output):
    largestIndex = -1
    largest = -999
    for i, out in enumerate(output):
        if out > largest:
            largestIndex = i
            largest = out
    
    return largestIndex


def ai_plays(genomes, config):
    # dinos = [Dinosaur(44,47)]*30    # create an array of 30 dinos
    dino = Dinosaur(44,47)
    i = 0
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        ai_gamer = Game(dino)
        ai_gamer.run()
        while not dino.isDead:
            inputs = [ai_gamer.getGamespeed(), dino.rect.bottom, ai_gamer.getDistToNextObstacle(), ai_gamer.getHeightOfNextObstacle()]
            output = net.activate(inputs)
            index = findLargestIndex(output)
            # print("index is = " + str(index), flush=True)
            if index == 0:
                dino.jump()
            elif index == 1:
                dino.duck()
            elif index == 2:
                dino.unduck()
            else:
                dino.unduck() # do nothing 

            pygame.time.wait(16)  # sleep for 16 milliseconds (1 frame)
            ai_gamer.updateGame()

        genome.fitness = dino.score
        # i += 1


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
    winner = p.run(ai_plays, 2)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    # winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    # for xi, xo in zip(xor_inputs, xor_outputs):
    #     output = winner_net.activate(xi)
    #     print("input {!r}, expected output {!r}, got {!r}".format(xi, xo, output))

    node_names = {-1:'Jump', -2: 'Duck', -3:'Unduck', -4:"Nothing", 0:"Dino"}
    visualize.draw_net(config, winner, True, node_names=node_names)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    p.run(ai_plays, 1)

def main():
    run("./config-feedforward-2.txt")

main()

