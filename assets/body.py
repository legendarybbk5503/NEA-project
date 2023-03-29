from assets.vector import VectorCalculation, VectorForm

class Body():
    
    def __init__(self, name: str, mass: float, radius: float, color: str):
        """init a body

        Args:
            name (str): name of the object
            mass (float): mass of the object
            radius (float): radius of the object
            color (str): color of the object
        """
        self.name = name
        self.mass = mass
        self.radius = radius
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

    def xva(self, x: VectorForm, v: VectorForm, a: VectorForm, t: float = 0):
        """update datas

        Args:
            x (VectorForm): update x (position vector)
            v (VectorForm): update v (velocity)
            a (VectorForm): update a (acceleration)
            t (float, optional): update t (time). Defaults to 0.
        """
        #old = new
        self.oldx = self.x
        self.oldv = self.v
        self.olda = self.a
        self.oldt = self.t
        
        #udpate new
        self.x = x
        self.v = v
        self.a = a
        self.t = t