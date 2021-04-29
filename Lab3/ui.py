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
    def __init__(self, controller):
        self.__controller = controller
        self.__gui= GUI()
        self.__averages = None
        self.__solutionFitness = None
        self.__solutionIndivid = None

    def createRandomMap(self):
        fill = input("Fill : ")
        map = self.__controller.getMap()
        if fill :
            fill = float(fill)
            map.randomMap(fill)
        else :
            map.randomMap()

    def loadMap(self):
        fileName = input("file : ")
        repo = self.__controller.getRepo()
        repo.loadMap(fileName)

    def saveMap(self):
        fileName = input("file : ")
        repo = self.__controller.getRepo()
        repo.saveMap(fileName)

    def visualizeMap(self):
        map = self.__controller.getMap()
        self.__gui.mapImage(map)

    def runSolver(self):
        self.__averages, self.__solutionFitness, self.__solutionIndivid = self.__controller.solver()

    def viewStatistics(self):
        repo = self.__controller.getRepo()
        data = repo.getData()
        print("All runs until now")
        for (seed, fitness) in data :
            print(f"seed {seed} fitness {fitness}")
        fitnesses = repo.getFitnesses()
        print("average solution fitness "+str(np.average(fitnesses))+" standard deviation : "+str(np.std(fitnesses)))
        plt.plot(self.__averages)
        plt.xlabel("Average fitness of population on generations, last run")
        plt.show()

    def viewPath(self):
        map = self.__controller.getMap()
        self.__gui.movingDrone(map, self.__solutionIndivid)

    def run30x(self):
        for step in range(30):
            print("step : ",step)
            self.runSolver()


    def menu(self):
        print("Commands are :")
        print("1. random map")
        print("2. load map")
        print("3. save map")
        print("4. view map")
        print("5. run solver")
        print("6. view statistics")
        print("7. view path")
        print("8. run 30x")

    def run(self):
        self.menu()
        commands = {
            "random map" : self.createRandomMap,
            "load map" : self.loadMap,
            "save map" : self.saveMap,
            "view map" : self.visualizeMap,
            "run solver" : self.runSolver,
            "view statistics" : self.viewStatistics,
            "view path" : self.viewPath,
            "run 30x" : self.run30x
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



