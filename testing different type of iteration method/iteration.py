from body import Body
from vector import VectorCalculation, VectorForm

class Iteration():
    
    def __init__(self, dt: int, G: int, bodies:list[Body]):
        self.__dt = dt
        self.__G = G #universal gravitational constant
        self.__bodies = bodies
    
    #acceleration
    def __acc(self, body: Body):        
        acc = []
        for otherBody in self.__bodies:
            if otherBody.name != body.name:
                diff = VectorCalculation().difference(otherBody.x, body.x)
                norm = VectorCalculation().norm(diff)
                a = VectorCalculation().scalarProduct(diff, self.__G * otherBody.mass / (norm ** 3))
                acc.append(a)
        return VectorCalculation().sum(*acc)
    
    def euler(self, currentT, body: Body):
        oldX = body.x
        oldV = body.v
        oldA = body.a
        dt = self.__dt
        
        print("\nt euler", currentT, body.name)
        
        #x_(n+1) = x_n + v_n * dt
        vt = VectorCalculation().scalarProduct(oldV, dt)
        newX = VectorCalculation().sum(oldX, vt)
        
        #v_(n+1) = v_n + a_n * dt
        at = VectorCalculation().scalarProduct(oldA, dt)
        newV = VectorCalculation().sum(oldV, at)
        
        #a_(n+1) = f(x_n+1) (a function of x_n+1)
        body.x = newX
        newA = self.__acc(body)
        
        #print('x', newX.print())
        #print('v', newV.print())
        #print('a', newA.print())
        return newX, newV, newA
    
    def leapfrogKDK(self, currentT, body: Body):
        oldX = body.x
        oldV = body.v
        oldA = body.a
        dt   = self.__dt
        
        print("\nt leapfrogKDK", currentT, body.name)
        
        #v_(n+1/2) = v_n + a_n * dt/2
        at = VectorCalculation().scalarProduct(oldA, dt/2)
        halfV = VectorCalculation().sum(oldV, at)
        
        #x_(n+1) = x_n + v_(n+1/2) * dt
        vt = VectorCalculation().scalarProduct(halfV, dt)
        newX  = VectorCalculation().sum(oldX, vt)
        
        #v_(n+1) = v_(n+1/2) + a_(n+1) * dt/2
        body.x = newX
        newA  = self.__acc(body)
        at2 = VectorCalculation().scalarProduct(newA, dt/2)
        newV  = VectorCalculation().sum(halfV, at2)
        
        #print('x', newX.print())
        #print('v', newV.print())
        #print('a', newA.print())
        return newX, newV, newA

    def leapfrogDKD(self, currentT, body: Body):
        oldX = body.x
        oldV = body.v
        oldA = body.a
        dt   = self.__dt
        
        print("\nt leapfrogDKD", currentT, body.name)
        
        vt = VectorCalculation().scalarProduct(oldV, dt/2)
        halfX = VectorCalculation().sum(oldX, vt)
        
        body.x = halfX
        halfA = self.__acc(body)
        
        at = VectorCalculation().scalarProduct(halfA, dt)
        newV  = VectorCalculation().sum(oldV, at)
        
        vt2 = VectorCalculation().scalarProduct(newV, dt/2)
        newX  = VectorCalculation().sum(halfX, vt2)
        
        #print('x', newX.print())
        #print('v', newV.print())
        #print('a', halfA.print())
        return newX, newV, halfA
    
    def rk2(self, currentT, body: Body):
        oldX = body.x
        oldV = body.v
        oldA = body.a
        dt = self.__dt
        
        print("\nt rk2", currentT, body.name)
        
        