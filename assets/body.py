from assets.vector import VectorCalculation, VectorForm

class Body():
    
    def __init__(self, name: str, mass: float, radius: float, color: str):
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

    #update the value of x(position vector), v(velocoty), a(acceleration)
    def xva(self, x: VectorForm, v: VectorForm, a: VectorForm, t: float = 0):
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