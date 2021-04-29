from GUI import *

def main() :
    m = Map()
    m.loadMap("test1.map")


    x = randint(0, 19)
    y = randint(0, 19)
    while m.surface[x][y] != 0 :
        x = randint(0, 19)
        y = randint(0, 19)

    initialX = x
    initialY = y

    d = Drone(initialX, initialY)

    x = randint(0, 19)
    y = randint(0, 19)
    while m.surface[x][y] != 0 or (x == initialY and y == initialY):
        x = randint(0, 19)
        y = randint(0, 19)

    finalX = x
    finalY = y

    controller = Controller(m, d, initialX, initialY, finalX, finalY)
    gui = GUI(controller)
    gui.run()

if __name__ == "__main__":
    main()