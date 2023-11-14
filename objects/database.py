from objects.vector import VectorForm as Vec
from objects.body import Body
from pygame import Color

class DatabaseFormat():
    
    def __init__(self, mass: float, color: Color, x:Vec, v: Vec, a: Vec):
        """Create a database

        Args:
            mass (float): mass of the object
            color (Color): color of the object
            x (Vec): displacement at t = 0
            v (Vec): velocity at t = 0
            a (Vec): acceleration at t = 0
        """

        self.mass = mass
        self.color = color
        self.t = [0]
        self.x = [x]
        self.v = [v]
        self.a = [a]
    
    def appendxva(self, t: float, x: Vec, v: Vec, a: Vec):
        """Append datas

        Args:
            t (float): time
            x (Vec): displacement
            v (Vec): velocity
            a (Vec): acceleration
        """

        self.t.append(t)
        self.x.append(x)
        self.v.append(v)
        self.a.append(a)
    
    def print(self):
        """Print the database in console in a more readable form
        """
        print(f"mass = {self.mass}")
        print(f"color = {self.color}")
        for i in range(len(self.t)):
            print(f"t = {self.t[i]}")
            print(f"x = {self.x[i].print()}")
            print(f"v = {self.v[i].print()}")
            print(f"a = {self.a[i].print()}")

class DatabaseDict():
    def __init__(self, bodies: list[Body]):
        """Create a dictionary object

        Args:
            bodies (list[Body]): list of bodies
        """

        self.db = {body.name: DatabaseFormat(
            body.mass,
            body.color,
            body.x,
            body.v,
            body.a
        ) for body in bodies}
    
    def appendxva(self, name, t: int, x: Vec, v: Vec, a: Vec):
        """Append datas under the object

        Args:
            name (_type_): name of the body
            t (int): time
            x (Vec): displacement
            v (Vec): velocity
            a (Vec): acceleration
        """

        self.db.get(name).appendxva(t, x, v, a)

    def print(self):
        """Print the database in console in a more readable form
        """

        for key, value in self.db.items():
            print(key)
            value.print()
            print('-' * 40)