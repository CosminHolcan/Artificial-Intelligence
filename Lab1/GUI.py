from Controller import *

class GUI :
    def __init__(self, controller, choice):
        self.controller = controller
        self.choice = choice

    def image_detected_map(self, x, y):
        imagine = pygame.Surface((420, 420))
        brick = pygame.Surface((20, 20))
        empty = pygame.Surface((20, 20))
        empty.fill(WHITE)
        brick.fill(BLACK)
        imagine.fill(GRAYBLUE)
        detectedMap = self.controller.detectedMap
        for i in range(N):
            for j in range(M):
                if (detectedMap.surface[i][j] == 1):
                    imagine.blit(brick, (j * 20, i * 20))
                elif (detectedMap.surface[i][j] == 0):
                    imagine.blit(empty, (j * 20, i * 20))

        drona = pygame.image.load("drona.png")
        imagine.blit(drona, (y * 20, x * 20))
        return imagine

    def image_environment(self):
        imagine = pygame.Surface((420, 420))
        brick = pygame.Surface((20, 20))
        brick.fill(BLUE)
        imagine.fill(WHITE)
        environment = self.controller.environment
        for i in range(N):
            for j in range(M):
                if (environment.getSurface()[i][j] == 1):
                    imagine.blit(brick, (j * 20, i * 20))
        return imagine

    def run(self):
        if self.choice == "by hand" :
            self.run_byHand()
        elif self.choice == "dsf" :
            self.run_dsf()

    def run_byHand(self):
        pygame.init()
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("drone exploration")

        screen = pygame.display.set_mode((800, 400))
        screen.fill(WHITE)
        screen.blit(self.image_environment(), (0, 0))
        running = True
        self.controller.intialiseByHand()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == KEYDOWN:
                    pressed_keys = pygame.key.get_pressed()
                    self.controller.moveByHand(pressed_keys)
            drone_x = self.controller.drone.x
            drone_y = self.controller.drone.y
            self.image_detected_map(drone_x, drone_y)
            screen.blit(self.image_detected_map(drone_x, drone_y), (400, 0))
            pygame.display.flip()

        pygame.quit()

    def run_dsf(self):
        pygame.init()
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("drone exploration")

        screen = pygame.display.set_mode((800, 400))
        screen.fill(WHITE)
        screen.blit(self.image_environment(), (0, 0))
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            else :
                self.controller.moveDSF()
                pygame.time.wait(100)
                if (self.controller.complete == True):
                    running = False
                else:
                    drone_x = self.controller.drone.x
                    drone_y = self.controller.drone.y
                    screen.blit(self.image_detected_map(drone_x, drone_y), (400, 0))
                    pygame.display.flip()
        pygame.quit()
