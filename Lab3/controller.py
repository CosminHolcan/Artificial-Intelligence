from repository import *
import numpy as np


class Controller():
    def __init__(self, repo):
        self.__repo = repo
        self.__repo.loadMap()
        self.randomInitialisation()
        self.__numberIterations = NUMBER_ITERATIONS

    def randomInitialisation(self):
        map = self.__repo.getMap()
        x = randint(0, 19)
        y = randint(0, 19)
        while not map.validPosition(x, y) :
            x = randint(0, 19)
            y = randint(0, 19)
        self.__repo.setInitialPosition(x, y)


    def iteration(self):
        # args - list of parameters needed to run one iteration
        # a iteration:
        # selection of the parrents
        # create offsprings by crossover of the parents
        # apply some mutations
        # selection of the survivors
        initialX, initialY = self.__repo.getInitialPosition()
        map = self.__repo.getMap()
        currentPopulation = self.__repo.getPopulation()
        futurePopulation = list()
        while len(futurePopulation) != currentPopulation.getPopulationSize() :
            firstParent, secondParent = currentPopulation.selection(2)
            offspring1, offspring2 = firstParent.crossover(secondParent)
            offspring1.mutate()
            offspring1.fitness(initialX, initialY, map)
            futurePopulation.append(offspring1)
        for individ in currentPopulation.getPopulation() :
            futurePopulation.append(individ)
        futurePopulation.sort(key= lambda x:x.getFitness(), reverse=True)
        futurePopulation = futurePopulation[:currentPopulation.getPopulationSize()]
        currentPopulation.setPopulation(futurePopulation)

    def run(self):
        # args - list of parameters needed in order to run the algorithm

        # until stop condition
        #    perform an iteration
        #    save the information need it for the satistics

        # return the results and the info for statistics
        population = self.__repo.getPopulation()
        initialX, initialY = self.__repo.getInitialPosition()
        map = self.__repo.getMap()
        population.evaluate(initialX, initialY, map)
        bestIndivid, bestFitness = self.__repo.getPopulation().best(initialX, initialY, map)
        solutionIndivid = bestIndivid
        solutionFitness = bestFitness
        averages = list()
        averages.append(population.averageFitness())
        for _ in range(self.__numberIterations) :
            self.iteration()
            population.evaluate(initialX, initialY, map)
            bestIndivid, bestFitness = self.__repo.getPopulation().best(initialX, initialY, map)
            if bestFitness > solutionFitness :
                solutionFitness = bestFitness
                solutionIndivid = bestIndivid
            averages.append(population.averageFitness())
        return averages,solutionFitness, solutionIndivid


    def solver(self):
        # args - list of parameters needed in order to run the solver

        # create the population,
        # run the algorithm
        # return the results and the statistics
        currentSeed = randint(1,1000)
        seed(currentSeed)
        self.__repo.createPopulation()
        averages, solutionFitness, solutionIndivid = self.run()
        self.__repo.addExecution(currentSeed, solutionFitness)
        return averages, solutionFitness, solutionIndivid

    def getRepo(self):
        return self.__repo

    def getMap(self):
        return self.__repo.getMap()

    def getInitialPosition(self):
        return self.__repo.getInitialPosition()

