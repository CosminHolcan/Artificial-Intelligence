# -*- coding: utf-8 -*-

from random import *
from utils import *
import numpy as np


# the class gene can be replaced with int or float, or other types
# depending on your problem's representation

class Drone:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, newX, newY):
        self.x = newX
        self.y = newY

class Gene:
    def __init__(self):
        self.value = choice(DIRECTIONS)


class Individual:
    def __init__(self,size=INDIVIDUAL_SIZE):
        self.__size = size
        self.__x = [Gene() for _ in range(self.__size)]
        self.__f = None

    def copyRepresentation(self):
        l = list()
        for i in range(self.__size) :
            g = Gene()
            g.value = self.__x[i].value
            l.append(g)
        return l

    def setRepresentation(self, newRepresentation):
        self.__x = newRepresentation

    def fitness(self, initialX, initialY, map):
        greenArea = set()
        currentX = initialX
        currentY = initialY
        currentGeneGreenArea = map.getGreenArea(currentX, currentY)
        for position in currentGeneGreenArea :
            greenArea.add(position)
        for gene in self.__x :
            direction = gene.value
            currentX = currentX+direction[0]
            currentY = currentY + direction[1]
            if not map.validPosition(currentX, currentY) :
                self.__f = len(greenArea)
                return
            currentGeneGreenArea = map.getGreenArea(currentX, currentY)
            for position in currentGeneGreenArea:
                greenArea.add(position)
        self.__f = len(greenArea)

    def getFitness(self):
        return self.__f

    def createPath(self, initialX, initialY, map):
        currentX = initialX
        currentY = initialY
        path = list()
        path.append((initialX, initialY))
        for gene in self.__x:
            direction = gene.value
            currentX = currentX + direction[0]
            currentY = currentY + direction[1]
            if not map.validPosition(currentX, currentY):
                return path
            path.append((currentX, currentY))
        return path




    def mutate(self, mutateProbability=MUTATE_PROBABILITY):
        if random() < mutateProbability:
            firstGene = randint(0, self.__size-1)
            secondGene = randint(0, self.__size-1)
            while secondGene == firstGene :
                secondGene = randint(0, self.__size-1)
            aux = self.__x[firstGene].value
            self.__x[firstGene].value = self.__x[secondGene].value
            self.__x[secondGene].value = aux


    def crossover(self, otherParent, crossoverProbability=CROSSOVER_PROBABILITY):
        offspring1, offspring2 = Individual(self.__size), Individual(self.__size)
        if random() < crossoverProbability:
            cuttingPoint = randint(1, self.__size-1)
            offspring1.__x = self.copyRepresentation()[:cuttingPoint]+otherParent.copyRepresentation()[cuttingPoint:]
            offspring2.__x = otherParent.copyRepresentation()[:cuttingPoint]+self.copyRepresentation()[cuttingPoint:]
        return offspring1, offspring2


class Population():
    def __init__(self, populationSize=POPULATION_SIZE, individualSize=INDIVIDUAL_SIZE):
        self.__populationSize = populationSize
        self.__v = [Individual(individualSize) for _ in range(populationSize)]

    def getPopulation(self):
        return self.__v

    def evaluate(self, initialX, initialY, map):
        # evaluates the population
        for x in self.__v:
            x.fitness(initialX, initialY, map)

    def selection(self, k=0):
        fitnessSum = 0
        for x in self.__v :
            fitnessSum += x.getFitness()
        result = set()
        while len(result) != k :
            individ = np.random.choice(self.__v,1, False, [y.getFitness()/fitnessSum for y in self.__v])
            result.add(individ[0])
        return result

    def setPopulation(self, newPopulation):
        self.__v = newPopulation

    def getPopulationSize(self):
        return self.__populationSize

    def best(self, initialX, initialY, map):
        bestFitness = -1
        best = None
        for individ in self.__v :
            if individ.getFitness() > bestFitness :
                bestFitness = individ.getFitness()
                best = individ
        return best.createPath(initialX, initialY, map), bestFitness

    def averageFitness(self):
        fitnessSum = 0
        for x in self.__v:
            fitnessSum += x.getFitness()
        return fitnessSum / self.__populationSize



class Map():
    def __init__(self, n=20, m=20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))

    def randomMap(self, fill=FILL_PROPORTION):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill:
                    self.surface[i][j] = 1

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string

    def validPosition(self, x, y):
        return 0 <=x < self.m and 0<=y<self.n and self.surface[x][y] == 0

    def getMargins(self, x, y):
        readings = [0, 0, 0, 0]
        # UP
        xf = x - 1
        while ((xf >= 0) and (self.surface[xf][y] == 0)):
            xf = xf - 1
            readings[UP] = readings[UP] + 1
        # DOWN
        xf = x + 1
        while ((xf < self.n) and (self.surface[xf][y] == 0)):
            xf = xf + 1
            readings[DOWN] = readings[DOWN] + 1
        # LEFT
        yf = y + 1
        while ((yf < self.m) and (self.surface[x][yf] == 0)):
            yf = yf + 1
            readings[LEFT] = readings[LEFT] + 1
        # RIGHT
        yf = y - 1
        while ((yf >= 0) and (self.surface[x][yf] == 0)):
            yf = yf - 1
            readings[RIGHT] = readings[RIGHT] + 1
        return readings

    def getGreenArea(self, x, y):
        result = list()
        result.append((x,y))
        # UP
        xf = x - 1
        while ((xf >= 0) and (self.surface[xf][y] == 0)):
            result.append((xf, y))
            xf = xf - 1
        # DOWN
        xf = x + 1
        while ((xf < self.n) and (self.surface[xf][y] == 0)):
            result.append((xf, y))
            xf = xf + 1
        # LEFT
        yf = y + 1
        while ((yf < self.m) and (self.surface[x][yf] == 0)):
            result.append((x, yf))
            yf = yf + 1
        # RIGHT
        yf = y - 1
        while ((yf >= 0) and (self.surface[x][yf] == 0)):
            result.append((x, yf))
            yf = yf - 1
        return result



