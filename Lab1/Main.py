from GUI import *

def main() :
    e = Environment()
    e.loadEnvironment("test2.map")

    m = DMap()

    x = randint(0, 19)
    y = randint(0, 19)
    d = Drone(x, y)

    controller = Controller(e, d, m)
    gui = GUI(controller, "dsf")
    gui.run()

if __name__ == "__main__":
    main()