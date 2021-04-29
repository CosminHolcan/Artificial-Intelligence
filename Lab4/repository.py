# -*- coding: utf-8 -*-

import pickle
from domain import *


class Repository():
    def __init__(self):
        self.__map = Map()
        self.loadMap("mymap.txt")
        '''
        x = randint(0, M-1)
        y = randint(0, N-1)
        while self.__map.surface[x][y] != 0 :
            x = randint(0, M - 1)
            y = randint(0, N - 1)
        self.__drone = Drone(x,y)
        '''
        self.__drone = Drone(14, 8)

    def randomMap(self, fill = FILL_PROPORTION):
        map = Map()
        map.randomMap(fill)
        self.__map = map
        x = randint(0, M - 1)
        y = randint(0, N - 1)
        while self.__map.surface[x][y] != 0:
            x = randint(0, M - 1)
            y = randint(0, N - 1)
        self.__drone = Drone(x, y)


    def saveMap(self, numFile):
        with open(numFile, 'wb') as f:
            pickle.dump(self.__map, f)
            f.close()

    def loadMap(self, numFile = MAP_FILE):
        with open(numFile, "rb") as f:
            dummy = pickle.load(f)
            self.__map.n = dummy.n
            self.__map.m = dummy.m
            self.__map.surface = dummy.surface
            f.close()
        x = randint(0, M - 1)
        y = randint(0, N - 1)
        while self.__map.surface[x][y] != 0:
            x = randint(0, M - 1)
            y = randint(0, N - 1)
        self.__drone = Drone(x, y)


    def setInitialPosition(self, x, y):
        self.__initialX = x
        self.__initialY = y

    def getInitialPosition(self):
        return self.__initialX, self.__initialY

    def getMap(self):
        return self.__map

    def getDrone(self):
        return self.__drone





