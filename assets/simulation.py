from assets.vector import VectorForm, VectorCalculation
from assets.body import Body
from assets.iteration import Iteration
import matplotlib.pyplot as plt

class Simulation():
    
    def __init__(self, dt, bodies: list[Body], Gvalue: float = None):
        #list of bodies
        self.__bodies = bodies
        #universal gravitational constant
        self.__G = 6.6743e-11 if Gvalue is None else Gvalue
        #list of time
        self.__t = 0
        #delta t (time interval)
        self.__dt = dt
        
        self.__fig = plt.figure()
        self.__ax = self.__fig.add_subplot(111)
        self.__ax.set_facecolor('black')
        self.__ax.set_aspect("equal", "box")
        
        self.__bodyNo = 0

    def __update(self):
        #loop all body in bodies
        init = Iteration(self.__dt, self.__G, self.__bodies)
        for body in self.__bodies:
            
            #update xva of each body
            x, v, a = init.leapfrogDKD(self.__t, body)
            body.xva(x, v, a, self.__t)
            
            #pause for each frame
            plt.pause(0.01)

    #plot a new circle and line
    def __plotNew(self):
        circle = []
        for body in self.__bodies:
            #add circle
            circle.append(
                plt.Circle(
                    (body.x.printx(), body.x.printy()),
                    body.radius,
                    color = body.color
                )
            )
            #plot line
            if body.oldx is not None:
                plt.plot(
                    (body.oldx.printx(), body.x.printx()),
                    (body.oldx.printy(), body.x.printy()),
                    color = body.color
                )
        #plot circle
        for c in circle:
            self.__ax.add_patch(c)
        #auto scale size
        self.__ax.autoscale()

    def run(self):
        #mode = "leapfrogDKD"
        noIterationPerFrame = 5
        for i in range(400):  
            #update t
            self.__t += self.__dt
            
            #print the bodies every n iterations
            if i % noIterationPerFrame == 0:
                self.__plotNew()
                self.__bodyNo += 1
            
            #update new t, x, v, a
            self.__update()
                
        plt.show()


def main():
    pass

if __name__ == "__main__":
    main()