from assets.body import Body
from assets.vector import VectorCalculation, VectorForm

class Iteration():
    
    def __init__(self, dt: int, G: int, bodies:list[Body]):
        self.__dt = dt
        self.__G = G #universal gravitational constant
        self.__bodies = bodies
    
    #get acceleration
    def __acc(self, body: Body, bodyx: VectorForm = None) -> VectorForm:
        if bodyx is None:
            bodyx = body.x
        acc = []
        for otherBody in self.__bodies:
            if otherBody.name != body.name:
                diff = VectorCalculation().difference(otherBody.x, bodyx)
                norm = VectorCalculation().norm(diff)
                a = VectorCalculation().scalarProduct(diff, self.__G * otherBody.mass / (norm ** 3))
                acc.append(a)
        return VectorCalculation().sum(*acc)

    #leapfrogDKD method
    def leapfrogDKD(self, currentT, body: Body) -> tuple:
        oldX = body.x
        oldV = body.v
        oldA = body.a
        dt   = self.__dt
        
        print("\nleapfrogDKD", currentT//dt, currentT, body.name)
        print(body.x.print())
        
        vt = VectorCalculation().scalarProduct(oldV, dt/2)
        halfX = VectorCalculation().sum(oldX, vt)
        
        halfA = self.__acc(body, halfX)
        
        at = VectorCalculation().scalarProduct(halfA, dt)
        newV  = VectorCalculation().sum(oldV, at)
        
        vt2 = VectorCalculation().scalarProduct(newV, dt/2)
        newX  = VectorCalculation().sum(halfX, vt2)
        
        return newX, newV, halfA
