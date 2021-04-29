# -*- coding: utf-8 -*-

from random import *
from utils import *
import numpy as np
from queue import PriorityQueue


# the class gene can be replaced with int or float, or other types
# depending on your problem's representation

class Map():
    def __init__(self, n=N, m=M):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))

    def randomMap(self, fill=FILL_PROPORTION, nrSensors=NO_SENSORS):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill:
                    self.surface[i][j] = 1
        sensors = set()
        while len(sensors) != nrSensors:
            i = randint(0, self.n - 1)
            j = randint(0, self.m - 1)
            if self.surface[i][j] != 1:
                if (i, j) not in sensors:
                    sensors.add((i, j))
                    self.surface[i][j] = 2

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string

    def getSensors(self):
        sensors = list()
        for i in range(self.m):
            for j in range(self.n):
                if self.surface[i][j] == 2:
                    sensors.append((i, j))
        return sensors

    def onMapPosition(self, x, y):
        return 0 <= x < self.m and 0 <= y < self.n

    def noWallPosition(self, x, y):
        return self.onMapPosition(x, y) and self.surface[x][y] != 1

    def getNeighboursInRange(self, x, y, r):
        neighbours = list()
        for direction in DIRECTIONS:
            currentX = x
            currentY = y
            for distance in range(r):
                currentX += direction[0]
                currentY += direction[1]
                if self.noWallPosition(currentX, currentY):
                    neighbours.append((currentX, currentY))
                else:
                    break
        return neighbours.copy()

    def getValidNeighbours(self, x, y):
        result = list()
        if y > 0:
            if self.surface[x][y - 1] != 1:
                result.append((x, y - 1))
        if x > 0:
            if self.surface[x - 1][y] != 1:
                result.append((x - 1, y))
        if x < 19:
            if self.surface[x + 1][y] != 1:
                result.append((x + 1, y))
        if y < 19:
            if self.surface[x][y + 1] != 1:
                result.append((x, y + 1))
        return result

def searchAStar(map:Map, initial, final):
    initialX = initial[0]
    initialY = initial[1]
    finalX = final[0]
    finalY = final[1]
    distanc = dict()
    prev = dict()
    visited = set()
    distanc[(initialX, initialY)] = 0
    visited.add((initialX, initialY))
    pq = PriorityQueue()
    pq.put((0, (initialX, initialY)))
    found = False
    while not pq.empty():
        elem = pq.get()
        position = elem[1]
        if position == (finalX, finalY):
            found = True
            break
        for neighbour in map.getValidNeighbours(position[0], position[1]):
            if neighbour in distanc:
                currentPriority = abs(finalX - neighbour[0]) + abs(finalY - neighbour[1]) + \
                                  distanc[neighbour]
                possiblePriority = abs(finalX - neighbour[0]) + abs(finalY - neighbour[1]) + \
                                   distanc[position] + 1
                if possiblePriority < currentPriority:
                    prev[neighbour] = position
                    distanc[neighbour] = distanc[position] + 1
                    priority = abs(finalX - neighbour[0]) + abs(finalY - neighbour[1]) + \
                               distanc[neighbour]
                    pq.put((priority, neighbour))
            else:
                prev[neighbour] = position
                distanc[neighbour] = distanc[position] + 1
                priority = abs(finalX - neighbour[0]) + abs(finalY - neighbour[1]) + \
                           distanc[neighbour]
                pq.put((priority, neighbour))
    if not found:
        return list()
    path = list()
    current = finalX, finalY
    while current != (initialX, initialY):
        path.append(current)
        current = prev[current]
    path.append(current)
    return list(reversed(path))

class Drone:
    def __init__(self, x, y, battery = BATTERY):
        self.x = x
        self.y = y
        self.battery = battery

    def move(self, newX, newY):
        self.x = newX
        self.y = newY

class Sensor():
    def __init__(self, x, y, energy):
        self.x = x
        self.y = y
        self.energy = energy

    def getPosition(self):
        return (self.x, self.y)

    def getRepresentation(self):
        return (self.x, self.y, self.energy)


class Graph():
    def __init__(self, map : Map, drone : Drone):
        self.map = map
        droneX = drone.x
        droneY = drone.y
        sensorsPositions = map.getSensors().copy()
        self.sensors = list()
        for pos in sensorsPositions :
            for energy in range(6):
                sensor = Sensor(pos[0], pos[1], energy)
                self.sensors.append(sensor)
        self.sensors.append(Sensor(droneX, droneY, 0))
        self.distances = dict()
        self.paths = dict()
        for sensor1 in self.sensors :
            initial = sensor1.getPosition()
            self.distances[initial] = dict()
            self.paths[initial] = dict()
            for sensor2 in self.sensors :
                final = sensor2.getPosition()
                path = searchAStar(map, initial, final)
                self.distances[initial][final] = len(path)-1
                self.paths[initial][final] = path.copy()

class Ant():
    def __init__(self, map : Map, drone:Drone, graph : Graph):
        self.map = map
        self.drone = drone
        self.path = [(drone.x, drone.y, 0)]
        self.graph = graph
        self.battery = BATTERY
        self.used_energy = 0

    def nextMoves(self):
        nextMoves = list()
        sensors = self.graph.sensors
        distances = self.graph.distances
        lastPositionInPath = (self.path[-1][0], self.path[-1][1])
        for sensor in sensors :
            positionSensor = sensor.getPosition()
            found = False
            for pos in self.path :
                if pos[0] == positionSensor[0] and pos[1] == positionSensor[1] :
                    found = True
                    break
            if not found:
                if distances[lastPositionInPath][positionSensor] + sensor.energy <= self.battery - self.used_energy:
                    nextMoves.append(sensor)
        return nextMoves.copy()

    def visibility(self, sensor):
        sensorPosition = sensor.getPosition()
        energy = sensor.energy
        sensorX = sensorPosition[0]
        sensorY = sensorPosition[1]
        neighbours = self.map.getNeighboursInRange(sensorX, sensorY, energy)
        total_squares = len(neighbours)
        lastPositionInPath = (self.path[-1][0], self.path[-1][1])
        return total_squares/ (self.graph.distances[lastPositionInPath][sensorPosition] + energy)

    def addMove(self, trace, alpha = ALPHA, beta= BETA, q0 = Q0):
        visibilities = list()
        nextSteps = self.nextMoves()
        lastPositionInPath = (self.path[-1][0], self.path[-1][1])
        if (len(nextSteps)) == 0 :
            return
        for step in nextSteps :
            v = self.visibility(step)
            visibilities.append((step, v))
        probabilities = list()
        for i in range(len(visibilities)) :
            sensor = visibilities[i][0]
            sensorRepresentation = sensor.getRepresentation()
            visibility = visibilities[i][1]
            tau = trace[self.path[-1]][sensorRepresentation]
            value = (tau**alpha)*(visibility**beta)
            probabilities.append((sensor, value))
        if (random() < q0) :
            probabilities = max(probabilities, key=lambda a : a[1])
            sensor = probabilities[0]
            self.used_energy += self.graph.distances[lastPositionInPath][sensor.getPosition()] + sensor.energy
            self.path.append(sensor.getRepresentation())
        else :
            sum_prob = sum([probabilities[i][1] for i in range(len(probabilities))])
            if sum_prob == 0 :
                return
            nextMove = np.random.choice([i for i in range(len(probabilities))], 1, False, [y[1]/sum_prob for y in probabilities])[0]
            nextMove = probabilities[nextMove]
            sensor = nextMove[0]
            self.used_energy += self.graph.distances[lastPositionInPath][sensor.getPosition()] + sensor.energy
            self.path.append(sensor.getRepresentation())

    def fitness(self):
        squares = set()
        for p in self.path :
            positionX = p[0]
            positionY = p[1]
            energy = p[2]
            current_squares = self.map.getNeighboursInRange(positionX,positionY, energy)
            for square in current_squares :
                squares.add(square)
        return len(squares)

    def sensors_activated(self):
        squares = set()
        for p in self.path :
            positionX = p[0]
            positionY = p[1]
            energy = p[2]
            current_squares = self.map.getNeighboursInRange(positionX, positionY, energy)
            for square in current_squares :
                squares.add(square)
        result = list()
        for square in squares :
            result.append(square)
        return result

    def getWholePath(self):
        result = []
        for i in range(len(self.path) - 1):
            x = (self.path[i][0], self.path[i][1])
            y = (self.path[i+1][0], self.path[i+1][1])
            result += self.graph.paths[x][y]
        print(self.path)
        return result






