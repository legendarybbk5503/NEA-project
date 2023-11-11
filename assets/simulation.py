from objects.vector import VectorForm as Vec
from objects.body import Body
from assets.iteration import Iteration
from objects.database import DatabaseDict
from pygame import Color

class Simulation():
    
    def __init__(self, bodies: list[Body], **kwargs):
        #list of bodies
        self.__bodies = bodies
        #universal gravitational constant
        self.__G = kwargs.get('G', 6.67e-11)
        #delta t (time interval)
        self.__dt = kwargs.get("dt", 86400)
        #number of iterations
        self.iterationNo = kwargs.get("iterationNo", 1000)
    
    def load(self):
        db = DatabaseDict(self.__bodies)
        for i in range(self.iterationNo):
            init = Iteration(self.__bodies, dt = self.__dt, G = self.__G)
            for body in self.__bodies:
                t = self.__dt * (i + 1) #as i starts from 0
                x, v, a = init.leapfrogDKD(body)
                db.appendxva(body.name, t, x, v, a)
                body.xva(x, v, a)
        return db

class Builtin_Simulation():
    def __init__(self):
        self.__sun_red = Color("#FF0000")
        self.__mercury_gray = Color("#B7B8B9")
        self.__venus_orange = Color("#FFC649")
        self.__earth_blue = Color("#287AB8")
        self.__moon_yellow = Color("#F6F1D5")
        self.__mars_red = Color("#BC2732")
        self.__jupiter_brown = Color("#d8ca9d")
        self.__saturn_brown = Color("#eddbad")
        self.__uranus_blue = Color("#ACE5EE")
        self.__neptune_blue = Color("#478be7")
        self.__pluto_brown = Color("#ccba99")

        self.__mercury = Body("mercury", 0.33e24, self.__mercury_gray)
        self.__sun   = Body("sun", 1.989e30, self.__sun_red)
        self.__venus = Body("venus", 4.87e24, self.__venus_orange)
        self.__earth = Body("earth", 5.97e24, self.__earth_blue)
        self.__mars = Body("mars", 0.642e24, self.__mars_red)
        self.__jupiter = Body("jupitar", 1898e24, self.__jupiter_brown)
        self.__saturn = Body("saturn", 568e24, self.__saturn_brown)
        self.__uranus = Body("uranus", 86.8e24, self.__uranus_blue)
        self.__neptune = Body("neptune", 102e24, self.__neptune_blue)
        self.__pluto = Body("pluto", 0.013e24, self.__pluto_brown)
        
        self.__sun.xva(Vec(0, 0), Vec(0, 0))
        self.__mercury.xva(Vec(57.9e9, 0), Vec(0, -47.4e3))
        self.__venus.xva(Vec(108.2e9, 0), Vec(0, -35.0e3))
        self.__earth.xva(Vec(149.6e9, 0), Vec(0, -29.8e3))
        self.__mars.xva(Vec(228e9, 0), Vec(0, -24.1e3))
        self.__jupiter.xva(Vec(778.5e9, 0), Vec(0, -13.1e3))
        self.__saturn.xva(Vec(1432e9, 0), Vec(0, -9.7e3))
        self.__uranus.xva(Vec(2867e9, 0), Vec(0, -6.8e3))
        self.__neptune.xva(Vec(4515e9, 0), Vec(0, -5.4e3))
        self.__pluto.xva(Vec(5906.4e9, 0), Vec(0, -4.7e3))

    def earth_moon(self, G, dt, iterationNo):
        earth = Body("earth", 5.97e24, self.__earth_blue)
        moon  = Body("moon", 7.35e22, self.__moon_yellow)

        earth.xva(Vec(0, 0), Vec(0, 0))
        moon.xva(Vec(384.4e6, 0), Vec(0, -1022), Vec(0, 0))

        planets = [
            earth,
            moon
        ]
        model = Simulation(planets, G = G,dt = dt, iterationNo = iterationNo)
        return model

    def inner_solar_system(self, G, dt, iterationNo):
        planets = [
            self.__sun,
            self.__mercury,
            self.__venus,
            self.__earth,
            self.__mars
        ]
        model = Simulation(planets, G = G, dt = dt, iterationNo = iterationNo)
        return model
    
    def middle_solar_system(self, G, dt, iterationNo):
        planets = [
            self.__sun,
            self.__mercury,
            self.__venus,
            self.__earth,
            self.__mars,
            self.__jupiter,
            self.__saturn
        ]
        model = Simulation(planets, G = G, dt = dt, iterationNo = iterationNo)
        return model


    def outer_solar_system(self, G, dt, iterationNo):
        planets = [
            self.__sun,
            self.__mercury,
            self.__venus,
            self.__earth,
            self.__mars,
            self.__jupiter,
            self.__saturn,
            self.__uranus,
            self.__neptune,
            self.__pluto
        ]
        model = Simulation(planets, G = G, dt = dt, iterationNo = iterationNo)
        return model


def main():
    pass

if __name__ == "__main__":
    main()