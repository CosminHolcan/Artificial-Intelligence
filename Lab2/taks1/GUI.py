from Controller import *

class GUI:
    def __init__(self, controller):
        self.controller = controller

    def image_map(self):
        imagine = pygame.Surface((420, 420))
        brick = pygame.Surface((20, 20))
        brick.fill(BLUE)
        imagine.fill(WHITE)
        map = self.controller.map
        for i in range(20):
            for j in range(20):
                if (map.surface[i][j] == 1):
                    imagine.blit(brick, (j * 20, i * 20))
        return imagine

    def image_with_drone(self):
        imagine = pygame.Surface((420, 420))
        brick = pygame.Surface((20, 20))
        brick.fill(BLUE)
        imagine.fill(WHITE)
        map = self.controller.map
        for i in range(20):
            for j in range(20):
                if (map.surface[i][j] == 1):
                    imagine.blit(brick, (j * 20, i * 20))
        x = self.controller.drone.x
        y = self.controller.drone.y
        drona = pygame.image.load("drona.png")
        imagine.blit(drona, (y * 20, x * 20))
        return imagine

    def displayWithPath(self, image, path):
        mark = pygame.Surface((20, 20))
        mark.fill(GREEN)
        for move in path:
            image.blit(mark, (move[1] * 20, move[0] * 20))

        return image

    def run(self):
        pygame.init()
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Path in simple environment")

        screen = pygame.display.set_mode((1400, 400))
        screen.fill(BLACK)
        image = self.image_map()
        secondImage = self.image_map()
        thirdImage = self.image_map()

        greedyTimeFirst = time.time()
        greedyPath = self.controller.searchGreedy()
        greedyTimeSecond = time.time()

        print("Greedy time : ", greedyTimeSecond-greedyTimeFirst)
        print("Greedy length : ", str(len(greedyPath)))

        aStarTimeFirst = time.time()
        aStarPath = self.controller.searchAStar()
        aStarTimeSecond = time.time()

        print("A * time :", aStarTimeSecond-aStarTimeFirst)
        print("A * length : ", str(len(aStarPath)))



        dfsFirstTime = time.time()
        dfsPath = self.controller.searchDFS()
        dfsSecondTime = time.time()

        print("DFS  time : ", dfsSecondTime-dfsFirstTime)
        print("DFS length : ", str(len(dfsPath)))
        




        screen.blit(self.displayWithPath(image, greedyPath), (0, 0))
        screen.blit(self.displayWithPath(secondImage, aStarPath), (500, 0))
        screen.blit(self.displayWithPath(thirdImage, dfsPath), (1000, 0))
        pygame.display.flip()
        time.sleep(15)

    def run_greedy(self):
        greedyTimeFirst = time.time()
        pygame.init()
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Path in simple environment")

        screen = pygame.display.set_mode((900, 400))
        screen.fill(BLACK)
        greedyPath = self.controller.searchGreedy()

        for position in greedyPath :
            x = position[0]
            y = position[1]
            self.controller.drone.move(x, y)
            screen.blit(self.image_with_drone(), (0,0))
            pygame.display.flip()
            pygame.time.wait(100)

        greedyTimeSecond = time.time()

        print("Greedy time : ", greedyTimeSecond - greedyTimeFirst)

    def run_astar(self):
        aStarTimeFirst = time.time()
        pygame.init()
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Path in simple environment")

        screen = pygame.display.set_mode((900, 400))
        screen.fill(BLACK)
        aStarPath = self.controller.searchAStar()

        for position in aStarPath :
            x = position[0]
            y = position[1]
            self.controller.drone.move(x, y)
            screen.blit(self.image_with_drone(), (500, 0))
            pygame.display.flip()
            pygame.time.wait(100)

        aStarTimeSecond = time.time()

        print("A * time :", aStarTimeSecond - aStarTimeFirst)

    def run_second(self):
        self.run_greedy()
        self.run_astar()