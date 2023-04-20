from assets.vector import VectorForm

class DatabaseFormat():
    
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
        self.t.append(t)
        self.x.append(x)
        self.v.append(v)
        self.a.append(a)
    
    def print(self):
        print(f"{self.name = }")
        print(f"{self.radius = }")
        print(f"{self.color = }")
        for i in range(len(self.t)):
            print(self.t[i])
            print(self.x[i].print())
            print(self.v[i].print())
            print(self.a[i].print())

class DatabaseDict():
    def __init__(self):
        self.db = {}
    
    def print(self):
        for key, value in self.db.items():
            print(key)
            value.print()