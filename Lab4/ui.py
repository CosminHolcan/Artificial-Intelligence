# -*- coding: utf-8 -*-


# imports
from gui import *
from controller import *
from repository import *
from domain import *
import matplotlib.pyplot as plt


# create a menu
#   1. map options:
#         a. create random map
#         b. load a map
#         c. save a map
#         d visualise map
#   2. EA options:
#         a. parameters setup
#         b. run the solver
#         c. visualise the statistics
#         d. view the drone moving on a path
#              function gui.movingDrone(currentMap, path, speed, markseen)
#              ATENTION! the function doesn't check if the path passes trough walls

class UserInterface():
    def __init__(self, controller : Controller):
        self.__controller = controller
        self.__gui= GUI()
        self.__ant = None

    def createRandomMap(self):
        fill = input("Fill : ")
        repo = self.__controller.getRepo()
        if fill :
            fill = float(fill)
            repo.randomMap(fill)
        else :
            repo.randomMap()
        self.__controller = Controller(repo)

    def loadMap(self):
        fileName = input("file : ")
        repo = self.__controller.getRepo()
        repo.loadMap(fileName)
        self.__controller = Controller(repo)

    def saveMap(self):
        fileName = input("file : ")
        repo = self.__controller.getRepo()
        repo.saveMap(fileName)

    def visualizeMap(self):
        map = self.__controller.getMap()
        drone = self.__controller.getDrone()
        self.__gui.mapImage(map, drone)

    def oneEpoch(self):
        ant = self.__controller.epoch()
        self.__ant = ant

    def solver(self):
        best_ant = None
        for _ in range(ITERATIONS) :
            self.oneEpoch()
            if best_ant == None :
                best_ant = self.__ant
            elif (self.__ant.fitness() > best_ant.fitness()) :
                best_ant = self.__ant
        self.__ant = best_ant

    def viewPath(self):
        map = self.__controller.getMap()
        path = self.__ant.path
        print(self.__ant.fitness())
        for p in path :
            print("position : "+str(p[0])+" "+str(p[1])+" energy : "+str(p[2]))
        wholePath = self.__ant.getWholePath()
        self.__gui.movingDrone(map, wholePath)

    def viewSensors(self):
        map = self.__controller.getMap()
        print(self.__ant.fitness())
        path = self.__ant.sensors_activated()
        self.__gui.movingDrone(map, path)



    def menu(self):
        print("Commands are :")
        print("1. random map")
        print("2. load map")
        print("3. save map")
        print("4. map")
        print("5. one epoch")
        print("6. path")
        print("7. solver")
        print("8. sensors")

    def run(self):
        self.menu()
        commands = {
            "random map" : self.createRandomMap,
            "load map" : self.loadMap,
            "save map" : self.saveMap,
            "map" : self.visualizeMap,
            "one epoch": self.oneEpoch,
            "path" : self.viewPath,
            "solver" : self.solver,
            "sensors" : self.viewSensors
        }
        while True :
            cmd = input("Your command is : ")
            if cmd == "exit" :
                return
            elif cmd in commands :
                commands[cmd]()
            else :
                print("Invalid command !")

if __name__ == "__main__" :
    repo = Repository()
    controller = Controller(repo)
    ui = UserInterface(controller)
    ui.run()



