from vector import VectorCalculation, VectorForm
from body import Body
from ode_solver import ODE

def earthmoon(dt, mode):
    #Body(name, mass, position vector, velocity, acceleration)
    earth = Body("earth", 5.972e24, VectorForm(0, 0), VectorForm(0, 0), VectorForm(0, 0))
    moon  = Body("moon", 7.348e22, VectorForm(384.4e6, 0), VectorForm(0, 1022), VectorForm(0, 0))
    
    model = ODE(dt, [earth, moon])
    model.compare(mode)
    return model

def main():
    dt = 86400
    model = earthmoon(dt, "euler")
    model = earthmoon(dt, "leapfrogKDK")
    model = earthmoon(dt, "leapfrogDKD")
    model.circle()
    model.draw()

if __name__ == "__main__":
    main()