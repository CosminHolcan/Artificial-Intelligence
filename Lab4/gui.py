# -*- coding: utf-8 -*-

from pygame.locals import *
import pygame, time
from utils import *
from controller import *

class GUI():

    def initPyGame(self, dimension):
        # init the pygame
        pygame.init()
        pygame.display.set_caption("drone exploration with AE")

        # create a surface on screen that has the size of 800 x 480
        screen = pygame.display.set_mode(dimension)
        screen.fill(WHITE)
        return screen


    def closePyGame(self):
        # closes the pygame
        running = True
        # loop for events
        while running:
         # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False
        pygame.quit()


    def movingDrone(self, currentMap : Map, path, speed=1, markSeen=True):
        # animation of a drone on a path
        n = currentMap.n
        m = currentMap.m
        screen = self.initPyGame((currentMap.n * n, currentMap.m * m))

        drona = pygame.image.load("drona.png")

        screen.blit(self.image(currentMap), (0, 0))
        for i in range(len(path)):


            if markSeen:
                brick = pygame.Surface((n, m))
                brick.fill(GREEN)
                x = path[i][0]
                y = path[i][1]
                if (currentMap.surface[x][y] != 2) :
                    screen.blit(brick, (y * 20, x * 20))

        pygame.display.flip()
        #time.sleep(0.5 * speed)
        self.closePyGame()


    def image(self, currentMap : Map, colour=BLUE, background=WHITE):
        # creates the image of a map
        n = currentMap.n
        m = currentMap.m
        imagine = pygame.Surface((currentMap.n * n, currentMap.m * m))
        brick = pygame.Surface((n, m))
        brick.fill(colour)
        brick2 = pygame.Surface((n,m))
        brick2.fill(RED)
        imagine.fill(background)
        for i in range(currentMap.n):
            for j in range(currentMap.m):
                if (currentMap.surface[i][j] == 1):
                    imagine.blit(brick, (j * m, i * n))
                elif (currentMap.surface[i][j] == 2) :
                    imagine.blit(brick2, (j * m, i * n))

        return imagine

    def mapImage(self, currentMap, drone : Drone):
        n = currentMap.n
        m = currentMap.m
        dr = pygame.image.load("drona.png")
        screen = self.initPyGame((currentMap.n * n, currentMap.m * m))
        screen.blit(self.image(currentMap),(0,0))
        screen.blit(dr, (drone.y * m, drone.x * n))
        pygame.display.flip()
        self.closePyGame()


