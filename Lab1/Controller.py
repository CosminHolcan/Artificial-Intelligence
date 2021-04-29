from Domain import *

class Controller():
    def __init__(self, environment, drone, detectedMap):
        self.environment = environment
        self.drone = drone
        self.detectedMap = detectedMap
        self.stack = list()
        self.stack.append([drone.x, drone.y])
        self.visited = np.zeros((20, 20))
        self.stack_back = list()
        self.go_back = False
        self.complete = False

    def getValidNeighbours(self, x, y):
        result = list()
        if y > 0:
            if self.detectedMap.surface[x][y - 1] == 0 and self.visited[x][y - 1] == 0:
                result.append((x, y - 1))
        if x > 0:
            if self.detectedMap.surface[x - 1][y] == 0 and self.visited[x - 1][y] == 0:
                result.append((x - 1, y))
        if x < 19:
            if self.detectedMap.surface[x + 1][y] == 0 and self.visited[x + 1][y] == 0:
                result.append((x + 1, y))
        if y < 19:
            if self.detectedMap.surface[x][y + 1] == 0 and self.visited[x][y + 1] == 0:
                result.append((x, y + 1))
        return result

    def intialiseByHand(self):
        drone_x = self.drone.x
        drone_y = self.drone.y
        walls = self.environment.readUDMSensors(drone_x, drone_y)
        self.detectedMap.markDetectedWalls(walls, drone_x, drone_y)
        self.detectedMap.surface[drone_x][drone_y] = 0


    def moveByHand(self, pressed_keys):
        drone_x = self.drone.x
        drone_y = self.drone.y
        if drone_x > 0:
            if pressed_keys[K_UP] and self.detectedMap.surface[drone_x - 1][drone_y] == 0:
                drone_x = drone_x - 1
        if drone_x < 19:
            if pressed_keys[K_DOWN] and self.detectedMap.surface[drone_x + 1][drone_y] == 0:
                drone_x = drone_x + 1

        if drone_y > 0:
            if pressed_keys[K_LEFT] and self.detectedMap.surface[drone_x][drone_y - 1] == 0:
                drone_y = drone_y - 1
        if drone_y < 19:
            if pressed_keys[K_RIGHT] and self.detectedMap.surface[drone_x][drone_y + 1] == 0:
                drone_y = drone_y + 1
        self.drone.move(drone_x, drone_y)
        walls = self.environment.readUDMSensors(drone_x, drone_y)
        self.detectedMap.markDetectedWalls(walls, drone_x, drone_y)

    def moveDSF(self):
        if len(self.stack) == 0:
            self.drone.move(None, None)
            self.complete =True
            return
        if not self.go_back :
            top = self.stack.pop()
            self.drone.move(top[0], top[1])
            drone_x = self.drone.x
            drone_y = self.drone.y
            walls = self.environment.readUDMSensors(drone_x, drone_y)
            self.detectedMap.markDetectedWalls(walls, drone_x, drone_y)
            self.visited[drone_x][drone_y] = 1
            valid_neighbour = False
            for neighbour in self.getValidNeighbours(drone_x, drone_y):
                self.stack.append((neighbour[0], neighbour[1]))
                valid_neighbour = True
            if not valid_neighbour :
                self.go_back = True
            else :
                self.stack_back.append((drone_x, drone_y))
        else :
            if len(self.stack_back) == 0 :
                self.drone.move(None, None)
                self.complete = True
                return
            top = self.stack_back.pop()
            self.drone.move(top[0], top[1])
            drone_x = top[0]
            drone_y = top[1]
            valid_neighbour = False
            for neighbour in self.getValidNeighbours(drone_x, drone_y):
                self.stack.append(neighbour)
                valid_neighbour = True
            if valid_neighbour :
                self.go_back = False
                self.stack_back.append((drone_x, drone_y))
