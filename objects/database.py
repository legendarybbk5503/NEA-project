from objects.vector import VectorForm as Vec
from objects.body import Body

class DatabaseFormat():
    
    def __init__(self, mass: float, color: str, x:Vec, v: Vec, a: Vec):
        self.mass = mass
        self.color = color
        self.t = [0]
        self.x = [x]
        self.v = [v]
        self.a = [a]
    
    def appendxva(self, t: float, x: Vec, v: Vec, a: Vec):
        self.t.append(t)
        self.x.append(x)
        self.v.append(v)
        self.a.append(a)
    
    def print(self):
        print(f"mass = {self.mass}")
        print(f"color = {self.color}")
        for i in range(len(self.t)):
            print(f"t = {self.t[i]}")
            print(f"x = {self.x[i].print()}")
            print(f"v = {self.v[i].print()}")
            print(f"a = {self.a[i].print()}")

class DatabaseDict():
    def __init__(self, bodies: list[Body]):
        self.db = {body.name: DatabaseFormat(
            body.mass,
            body.color,
            body.x,
            body.v,
            body.a
        ) for body in bodies}
    
    def appendxva(self, name, t, x, v, a):
        self.db.get(name).appendxva(t, x, v, a)

    def print(self):
        for key, value in self.db.items():
            print(key)
            value.print()
            print('-' * 40)