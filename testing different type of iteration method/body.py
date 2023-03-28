from vector import VectorCalculation, VectorForm

class Body():
    
    def __init__(self, name: str, mass: float, x: VectorForm, v: VectorForm, a: VectorForm): #radius, colour
        self.name = name
        self.mass = mass
        self.x = x
        self.v = v
        self.a = a
