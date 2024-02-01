from objects.vector import VectorForm as Vec
from pygame import Color
class Body():
    
    def __init__(self, name: str, mass: float, color: Color):
        """init a body

        Args:
            name (str): name of the object
            mass (float): mass of the object
            color (Color): color of the object
        """
        self.name = name
        self.mass = mass
        self.color = color
        
        #current data
        self.x = None
        self.v = None
        self.a = None
        self.t = None
        
        #previous data
        self.oldx = None
        self.oldv = None
        self.olda = None
        self.oldt = None

    def xva(self, x: Vec, v: Vec, a: Vec = Vec(0, 0)):
        """update xva data

        Args:
            x (Vec): _description_
            v (Vec): _description_
            a (Vec, optional): _description_. Defaults to 0.
        """
        #old = new
        self.oldx = self.x
        self.oldv = self.v
        self.olda = self.a
        
        #udpate new
        self.x = x
        self.v = v
        self.a = a
