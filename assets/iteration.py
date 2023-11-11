from objects.body import Body
from objects.vector import VectorCalculation, VectorForm as Vec

class Iteration():
    
    def __init__(self, bodies:list[Body], **kwargs):
        self.__bodies = bodies
        self.__dt = kwargs.get("dt", 86400) #default: a day
        self.__G = kwargs.get('G', 6.67e-11)
    
    def __acc(self, body: Body, bodyx: Vec = None) -> Vec:
        """get acceleration

        Args:
            body (Body): body to be calculated the acceleration
            bodyx (Vec, optional): position vector of body. Defaults to the latest position.

        Returns:
            Vec: new acceleration 
        """
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
    def leapfrogDKD(self, body: Body) -> tuple:
        """leapfrog drift-kick-drift method

        Args:
            body (Body): the body that will be moved

        Returns:
            tuple: new x, v, a (position vector, velocity and acceleration)
        """
        oldX = body.x
        oldV = body.v
        oldA = body.a
        dt   = self.__dt
        
        #print("\nleapfrogDKD", currentT//dt, currentT, body.name)
        #print(body.x.print())
        
        vt = VectorCalculation().scalarProduct(oldV, dt/2)
        halfX = VectorCalculation().sum(oldX, vt)
        
        halfA = self.__acc(body, halfX)
        
        at = VectorCalculation().scalarProduct(halfA, dt)
        newV  = VectorCalculation().sum(oldV, at)
        
        vt2 = VectorCalculation().scalarProduct(newV, dt/2)
        newX  = VectorCalculation().sum(halfX, vt2)
        
        return newX, newV, halfA
