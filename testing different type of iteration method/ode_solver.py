from vector import VectorForm, VectorCalculation
from body import Body
from iteration import Iteration
import matplotlib.pyplot as plt

class ODE():
    
    def __init__(self, dt, bodies: list[Body]):
        self.__bodies = bodies
        #universal gravitational constant
        self.__G = 6.6743e-11
        self.__t = [0]
        self.__dt = dt
        
    def compare(self, mode): #compare different modes
        plt.plot(0, 0, 'o', color = "blue")
        plt.plot(384.4e6, 0, 'o', color = "yellow")
        for _ in range(500):
            
            #t_(n+1) = t_n + dt
            newt = self.__t[-1] + self.__dt
            self.__t.append(newt)
            
            oldBodies = self.__bodies.copy()
            for body in self.__bodies:
                init = Iteration(self.__dt, self.__G, oldBodies)
                match mode:
                    case "euler":    x, v, a = init.euler(newt, body)
                    case "leapfrogKDK": x, v, a = init.leapfrogKDK(newt, body)
                    case "leapfrogDKD": x, v, a = init.leapfrogDKD(newt, body)
                
                if body.name == "earth": x = VectorForm(0, 0)
                body.x = x
                body.v = v
                body.a = a
                
                pos = x.print()
                match body.name:
                    case "earth": plt.plot(pos[0], pos[1], 'o', color = "blue")
                    case "moon":
                        match mode:
                            case "euler": color = "yellow"
                            case "leapfrogKDK": color = "red"
                            case "leapfrogDKD": color = "pink"
                        plt.plot(pos[0], pos[1], 'o', color = color)
    
    def circle(self): #for checking accuracy
        circle = plt.Circle((0, 0), 384.4e6, color = "black", fill = False, linewidth = 7.0)
        plt.gca().add_patch(circle)
    
    def draw(self):  #genearte a static graph          
        plt.gca().set_aspect('equal')
        plt.show()

def main():
    pass

if __name__ == "__main__":
    main()