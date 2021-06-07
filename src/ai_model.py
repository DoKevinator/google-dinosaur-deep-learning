
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

import pickle

import os
os.environ["PATH"] += os.pathsep + 'C:\Program Files (x86)\graphviz-0.16\graphviz-0.16\graphviz'

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

    # Series of lists to contain the genomes and neural networks for each dino in
    # the population.
    neuralnetList = []
    dinos = []
    genomeList = []

    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        # initialize the fitness to 0
        genome.fitness = 0

        # store the genome/neuralnetwork
        neuralnetList.append(net)
        dinos.append(Dinosaur(44,47))
        genomeList.append(genome)


    ai_gamer = Game(dinos)
    ai_gamer.run()
    while not dinosAreDead( dinos ):

        for i, d in enumerate(dinos):
            inputs = [ai_gamer.getGamespeed(), d.rect.bottom, ai_gamer.getDistToNextObstacle(), ai_gamer.getHeightOfNextObstacle()]
            output = neuralnetList[i].activate(inputs) 

            index = findLargestIndex(output)
            if index == 0:
                d.jump()
            elif index == 1:
                d.duck()
            elif index == 2:
                d.unduck()
            else:
                d.unduck() # do nothing 
            
            #subtract by the numbers of times jumped to unincentivize constant jumping
            genomeList[i].fitness = d.score - d.timesJumped 

        pygame.time.wait(16)  # sleep for 16 milliseconds (1 frame, 60FPS)
        ai_gamer.updateGame()


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

    # Run for up to 50 generations.
    winner = p.run(ai_plays, 50)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    pickle.dump( winner, open( "chad.p", "wb" ) )

    node_names = {-1:"gameSpeed", -2:"yPosition", -3:"distToNextObstable", -4:"heightOfNextObstacle", 0:'Jump', 1: 'Duck', 2:'Unduck', 3:"Nothing"}
    visualize.draw_net(config, winner, True, node_names=node_names)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    # p.run(ai_plays, 1)

def main():
    run("./config-feedforward-2.txt")

main()

