from vector import VectorForm

class databse():
    
    def __init__(self, name: str, mass: float, radius: float, color: str):
        self.name = name
        self.mass = mass
        self.radius = radius
        self.color = color
        self.t = []
        self.x = []
        self.v = []
        self.a = []
    
    def appendxva(self, t: float, x: VectorForm, v: VectorForm, a: VectorForm):
        self.t.append()
        self.x.append()
        self.v.append()
        self.a.append()
        