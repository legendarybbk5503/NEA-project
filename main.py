from assets.vector import VectorCalculation, VectorForm
from assets.body import Body
from assets.simulation import Simulation

def earthMoon(dt):
    #Body(name, mass, position vector, velocity, acceleration)
    earth = Body("earth", 5.972e24, 6378.1e3, "blue")
    moon  = Body("moon", 7.348e22, 1737.4e3, "yellow")
    
    earth.xva(VectorForm(0, 0), VectorForm(0, 0), VectorForm(0, 0))
    moon.xva(VectorForm(384.4e6, 0), VectorForm(0, 1022), VectorForm(0, 0))
    
    model = Simulation(dt, [earth, moon])
    model.run(1, 5)

def sunEarthMoon(dt):
    sun   = Body("sun", 1.989e30, 696340e3, "red")
    earth = Body("earth", 5.972e24, 6378.1e3, "blue")
    moon  = Body("moon", 7.348e22, 1737.4e3, "yellow")
    
    sun.xva(VectorForm(0, 0), VectorForm(0, 0), VectorForm(0, 0))
    earth.xva(VectorForm(149.1e9, 0), VectorForm(0, 30000), VectorForm(0, 0))
    moon.xva(VectorForm(149.1e9, 0), VectorForm(0, 30000), VectorForm(0, 0))
    
    model = Simulation(dt, [sun, earth, moon])
    model.run(1, 5)
    
def _3dbody(dt):
    a = Body("a", 1, 0.05, "red")
    b = Body("b", 1, 0.05, "green")
    c = Body("c", 1, 0.05, "blue")
    a.xva(VectorForm(-0.97000436, 0.24308753), VectorForm(0.466203685, 0.43236573), VectorForm(0, 0))
    b.xva(VectorForm(0.97000436, -0.24308753), VectorForm(0.466203685, 0.43236573), VectorForm(0, 0))
    c.xva(VectorForm(0, 0), VectorForm(-0.93240737, -0.86473146), VectorForm(0, 0))
    model = Simulation(dt, [a, b, c], 1)
    model.run(1, 5)
    

def main():
    dt = 86400
    earthMoon(dt)
    #sunEarthMoon(dt)
    #_3dbody(0.05)

if __name__ == "__main__":
    main()