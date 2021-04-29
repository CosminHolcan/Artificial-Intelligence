import math
from queue import PriorityQueue
from Domain import *


class Controller :
    def __init__(self, map, drone, initialX, initialY, finalX, finalY):
        self.map = map
        self.drone = drone
        self.initialX = initialX
        self.initialY = initialY
        self.finalX = finalX
        self.finalY = finalY

    def initialisation(self):
        self.distances = dict()
        self.prev = dict()
        self.visited = set()
        self.distances[(self.initialX, self.initialY)] = 0
        self.visited.add((self.initialX, self.initialY))

    def getValidNeighbours(self, x, y):
        result = list()
        if y > 0:
            if self.map.surface[x][y - 1] == 0 :
                result.append((x, y - 1))
        if x > 0:
            if self.map.surface[x - 1][y] == 0 :
                result.append((x - 1, y))
        if x < 19:
            if self.map.surface[x + 1][y] == 0 :
                result.append((x + 1, y))
        if y < 19:
            if self.map.surface[x][y + 1] == 0 :
                result.append((x, y + 1))
        return result

    def searchGreedy(self):
        self.initialisation()
        pq = PriorityQueue()
        pq.put((0, (self.initialX, self.initialY)))
        found = False
        while not pq.empty():
            elem = pq.get()
            position = elem[1]
            self.visited.add(position)
            if position == (self.finalX, self.finalY):
                found = True
                break
            for neighbour in self.getValidNeighbours(position[0], position[1]):
                if neighbour not in self.visited:
                    self.prev[neighbour] = position
                    priority = abs(self.finalX-neighbour[0])+abs(self.finalY-neighbour[1])
                    pq.put((priority, neighbour))
        if not found:
            return list()
        path = list()
        current = self.finalX, self.finalY
        while current != (self.initialX, self.initialY):
            path.append(current)
            current = self.prev[current]
        path.append(current)
        return list(reversed(path))

    def searchAStar(self):
        self.initialisation()
        pq = PriorityQueue()
        pq.put((0, (self.initialX, self.initialY)))
        found = False
        while not pq.empty():
            elem = pq.get()
            position = elem[1]
            if position == (self.finalX, self.finalY):
                found = True
                break
            for neighbour in self.getValidNeighbours(position[0], position[1]):
                if neighbour in self.distances:
                    currentPriority = abs(self.finalX - neighbour[0]) + abs(self.finalY - neighbour[1]) + \
                                      self.distances[neighbour]
                    possiblePriority = abs(self.finalX - neighbour[0]) + abs(self.finalY - neighbour[1]) + \
                                       self.distances[position] + 1
                    if possiblePriority < currentPriority:
                        self.prev[neighbour] = position
                        self.distances[neighbour] = self.distances[position] + 1
                        priority = abs(self.finalX - neighbour[0]) + abs(self.finalY - neighbour[1]) + \
                                   self.distances[neighbour]
                        pq.put((priority, neighbour))
                else:
                    self.prev[neighbour] = position
                    self.distances[neighbour] = self.distances[position] + 1
                    priority = abs(self.finalX - neighbour[0]) + abs(self.finalY - neighbour[1]) + \
                               self.distances[neighbour]
                    pq.put((priority, neighbour))
        if not found:
            return list()
        path = list()
        current = self.finalX, self.finalY
        while current != (self.initialX, self.initialY):
            path.append(current)
            current = self.prev[current]
        path.append(current)
        return list(reversed(path))

    def searchDFS(self):
        self.initialisation()
        stack = list()
        stack.append((self.initialX, self.initialY))
        found = False
        while not found and len(stack) != 0 :
            current = stack.pop()
            if current == (self.finalX, self.finalY) :
                found = True
                break
            self.visited.add(current)
            for neighbour in self.getValidNeighbours(current[0], current[1]) :
                if neighbour not in self.visited :
                    stack.append(neighbour)
                    self.prev[neighbour] = current
        if not found :
            return list()
        path = list()
        current = self.finalX, self.finalY
        while current != (self.initialX, self.initialY):
            path.append(current)
            current = self.prev[current]
        path.append(current)
        return list(reversed(path))


