from repository import *

class Controller():
    def __init__(self, repo : Repository):
        self.__repo = repo
        self.trace = dict()
        map = self.__repo.getMap()
        drone = self.__repo.getDrone()
        self.graph = Graph(map, drone)
        self.trace = dict()
        sensors = self.graph.sensors
        for sensor1 in sensors :
            sensor1Repr = sensor1.getRepresentation()
            self.trace[sensor1Repr] = dict()
            for sensor2 in sensors :
                sensor2Repr = sensor2.getRepresentation()
                self.trace[sensor1Repr][sensor2Repr] = 1.0


    def getRepo(self):
        return self.__repo

    def getMap(self):
        return self.__repo.getMap()

    def getDrone(self):
        return self.__repo.getDrone()


    def epoch(self):
        ants = [Ant(self.getMap(), self.getDrone(), self.graph) for _ in range(POPULATION)]
        for i in range(len(self.getMap().getSensors())):
            for x in ants:
                x.addMove(self.trace)
        dTrace = [1.0 / ants[i].used_energy for i in range(len(ants))]
        sensors = self.graph.sensors
        for sensor1 in sensors :
            sensor1Repr = sensor1.getRepresentation()
            for sensor2 in sensors :
                sensor2Repr = sensor2.getRepresentation()
                self.trace[sensor1Repr][sensor2Repr] = (1-RHO)*self.trace[sensor1Repr][sensor2Repr]
        for i in range(len(ants)):
            for j in range(len(ants[i].path) - 1):
                x = ants[i].path[j]
                y = ants[i].path[j + 1]
                self.trace[x][y] += dTrace[i]
        f = [[ants[i].fitness(), i] for i in range(len(ants))]
        f = max(f)
        return ants[f[1]]




