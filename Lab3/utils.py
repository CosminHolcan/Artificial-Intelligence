# -*- coding: utf-8 -*-

#Creating some colors
BLUE  = (0, 0, 255)
GRAYBLUE = (50,120,120)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

#define indexes variations
DIRECTIONS = [[-1, 0], [1, 0], [0, 1], [0, -1]]

#define mapsize
mapLengh = 20

#total number of genes from an individual
INDIVIDUAL_SIZE = 20

#total number of individuals in a population
POPULATION_SIZE = 100

#define other constants
MUTATE_PROBABILITY = 0.04
CROSSOVER_PROBABILITY = 0.8

NUMBER_ITERATIONS = 100


MAP_FILE = "test1.map"
DATA_FILE = "data.txt"
FILL_PROPORTION = 0.15

