from assets.vector import VectorForm, VectorCalculation
from assets.body import Body
from assets.iteration import Iteration
from assets.database import DatabaseFormat, DatabaseDict
import matplotlib.pyplot as plt
from time import perf_counter

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
        
        self.__bodyNo = len(bodies)
        self.__bodyCurrentNo = 0
        
        self.__databaseDict = DatabaseDict()
        
    def __update(self):
        #loop all body in bodies
        init = Iteration(self.__dt, self.__G, self.__bodies)
        for body in self.__bodies:
            #get data from database
            bodydb = self.__databaseDict.db.get(body.name, None)
            #create if not exist
            if bodydb is None:
                self.__databaseDict.db[body.name] = DatabaseFormat(
                    body.name,
                    body.mass,
                    body.radius,
                    body.color
                )
            #append new data into database
            self.__databaseDict.db[body.name].appendxva(self.__t, body.x, body.v, body.a)
            #update xva of each body
            x, v, a = init.leapfrogDKD(self.__t, body)
            body.xva(x, v, a, self.__t)
            
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
        #increase bodyNo by 1
        self.__bodyCurrentNo += 1
    
    def __remove(self, maxBodyNo):
        if maxBodyNo >= 0 and self.__bodyCurrentNo > maxBodyNo:
            lines = self.__ax.get_lines()[:self.__bodyNo]
            for line in lines:
                line.remove()
            circles = self.__ax.patches[:self.__bodyNo]
            for circle in circles:
                circle.remove()
            self.__bodyCurrentNo -= 1
                
    def run(self, noIterationPerFrame = 1, maxBodyNo = -1):
        start = perf_counter()
        #mode = "leapfrogDKD"
        
        for i in range(100):  
            #update t
            self.__t += self.__dt
            
            #plot new points            
            self.__plotNew()
            
            #remove when its longer than maxBodyNo
            self.__remove(maxBodyNo)
            
            #save the previous data into database
            #and update new t, x, v, a
            self.__update()
            
            #show the graph every n frames
            if i % noIterationPerFrame == 0:
                #auto scale size
                self.__ax.autoscale()
                #pause for each frame
                plt.pause(0.1)
                
        end = perf_counter()
        print(f"time: {end-start}")
        
        self.__databaseDict.print()
        
        plt.show()


def main():
    pass

if __name__ == "__main__":
    main()