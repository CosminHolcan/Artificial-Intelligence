# -*- coding: utf-8 -*-

import pickle
from domain import *


class Repository():
    def __init__(self):
        self.__population = Population()
        self.__map = Map()
        self.__map.randomMap()
        self.__data = list()
        self.__initialX = None
        self.__initialY = None

    def createPopulation(self):
        self.__population = Population()


    def saveMap(self, numFile):
        with open(numFile, 'wb') as f:
            pickle.dump(self.map, f)
            f.close()

    def loadMap(self, numFile = MAP_FILE):
        with open(numFile, "rb") as f:
            dummy = pickle.load(f)
            self.__map.n = dummy.n
            self.__map.m = dummy.m
            self.__map.surface = dummy.surface
            f.close()

    '''
    def loadData(self, numFile = DATA_FILE):
        with open(numFile, "r") as file:
            lines = file.readlines()
            tokens = lines[0].split()
            self.__initialX = int(tokens[0])
            self.__initialY = int(tokens[1])
            for line in lines[1:]:
                tokens = line.split()
                self.__data.append((tokens[0], tokens[1]))

    def saveData(self, numFile = DATA_FILE):
        with open(numFile, "w") as file:
            file.write(f"{self.__initialX} {self.__initialY}\n")
            for (seed, fitness) in self.__data :
                file.write(f"{seed} {fitness}")
    '''

    def addExecution(self, seed, fitness):
        self.__data.append((seed, fitness))


    def setInitialPosition(self, x, y):
        self.__initialX = x
        self.__initialY = y

    def getInitialPosition(self):
        return self.__initialX, self.__initialY

    def getMap(self):
        return self.__map

    def getPopulation(self):
        return self.__population

    def setPopulation(self, newPopulation):
        self.__population = newPopulation

    def getFitnesses(self):
        result = list()
        for x in self.__data :
            result.append(x[1])
        return result

    def getData(self):
        return self.__data





