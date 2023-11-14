from matplotlib import pyplot as plt
from objects.vector import VectorCalculation as calc
from objects.database import DatabaseDict
import matplotlib

class Statistics:
    def __init__(self, db: DatabaseDict):
        """Initialsing a statistics object for future use

        Args:
            db (DatabaseDict): database
        """

        self.__db = db

        self.__t = []

        self.__displacement_from_itself_x = {}
        self.__displacement_from_itself_y = {}
        self.__displacement_from_itself_mag = {}

        self.__displacement_from_center_x = {}
        self.__displacement_from_center_y = {}
        self.__displacement_from_center_mag = {}

        self.__displacement_from_center_object_x = {}
        self.__displacement_from_center_object_y = {}
        self.__displacement_from_center_object_mag = {}

        self.__v_x = {}
        self.__v_y = {}
        self.__v_mag = {}
        
        self.__a_x = {}
        self.__a_y = {}
        self.__a_mag = {}

        self.__force_x = {}
        self.__force_y = {}
        self.__force_mag = {}

        self.__fig, self.__ax = plt.subplots(figsize = (7, 7))

    def __get_t(self, name: str) -> list[float]:
        """Get the list of time

        Args:
            name (str): name of the object

        Returns:
            list[float]: a list of time
        """

        if len(self.__t) == 0:
            self.__t = self.__db[name].t
        return self.__t

    def __get_v_x(self, name: str) -> list[float]:
        """Get the list of velocity in x direction

        Args:
            name (str): name of the object

        Returns:
            list[float]: a list of velocity in x direction
        """

        if name not in self.__v_x:
            self.__v_x[name] = [vec.printx() for vec in self.__db[name].v]
        return self.__v_x[name]
    
    def __get_v_y(self, name: str) -> list[float]:
        """Get the list of velocithy in y direction

        Args:
            name (str): name of the object

        Returns:
            list[float]: a list of velocity in y direction
        """

        if name not in self.__v_y:
            self.__v_y[name] = [-vec.printy() for vec in self.__db[name].v]
        return self.__v_y[name]

    def __get_v_mag(self, name: str) -> list[float]:
        """Get the list of speed

        Args:
            name (str): name of the object

        Returns:
            list[float]: a list of speed
        """

        if name not in self.__v_mag:
            self.__v_mag[name] = [calc().norm(vec) for vec in self.__db[name].v]
        return self.__v_mag[name]

    def __get_a_x(self, name: str) -> list[float]:
        """Get the list of acceleration in x direction

        Args:
            name (str): name of the object

        Returns:
            list[float]: a list of acceleration in x direction
        """

        if name not in self.__a_x:
            self.__a_x[name] = [vec.printx() for vec in self.__db[name].a]
            self.__a_x[name][0] = self.__a_x[name][1]
        return self.__a_x[name]
    
    def __get_a_y(self, name: str) -> list[float]:
        """Get the list of acceleration in y direction

        Args:
            name (str): name of the object

        Returns:
            list[float]: a list of acceleration in y direction
        """

        if name not in self.__a_y:
            self.__a_y[name] = [-vec.printy() for vec in self.__db[name].a]
            self.__a_y[name][0] = self.__a_y[name][1]
        return self.__a_y[name]

    def __get_a_mag(self, name: str) -> list[float]:
        """Get the list of acceleration in magnitude

        Args:
            name (str): name of the object

        Returns:
            list[float]: a list of acceleration in magnitude
        """

        if name not in self.__a_mag:
            self.__a_mag[name] = [calc().norm(vec) for vec in self.__db[name].a]
            #remove [0] in order to show a nicer sine wave in graph, as [0] = (0, 0)
            self.__a_mag[name][0] = self.__a_mag[name][1]
        return self.__a_mag[name]

    def __get_force_x(self, name: str) -> list[float]:
        """Get the list of force in x direction

        Args:
            name (str): name of the object

        Returns:
            list[float]: a list of force in x direction
        """

        if name not in self.__force_x:
            mass = self.__db[name].mass
            a_x = self.__get_a_x(name)
            self.__force_x[name] = [mass * a for a in a_x]
        return self.__force_x[name]

    def __get_force_y(self, name: str) -> list[float]:
        """Get the list of force in y direction

        Args:
            name (str): name of the object

        Returns:
            list[float]: a list of force in y direction
        """

        if name not in self.__force_y:
            mass = self.__db[name].mass
            a_y = self.__get_a_y(name)
            self.__force_y[name] = [-mass * a for a in a_y]
        return self.__force_y[name]
    
    def __get_force_mag(self, name: str) -> list[float]:
        """Get the list of force in magnitude

        Args:
            name (str): name of the object

        Returns:
            list[float]: a list of force in magnitude
        """

        if name not in self.__force_mag:
            mass = self.__db[name].mass
            a_mag = self.__get_a_mag(name)
            self.__force_mag[name] = [mass * a for a in a_mag]
        return self.__force_mag[name]

    def __get_displacement_from_itself_x(self, name: str) -> list[float]:
        """Get the list of displacement in x direction from itself

        Args:
            name (str): name of the object

        Returns:
            list[float]: a list of displacement in x direction from itself 
        """

        if name not in self.__displacement_from_itself_x:
            initial_x = self.__db[name].x[0].printx()
            delta_x = [vec.printx() - initial_x for vec in self.__db[name].x]
            self.__displacement_from_itself_x[name] = delta_x
        return self.__displacement_from_itself_x[name]

    def __get_displacement_from_itself_y(self, name: str) -> list[float]:
        """Get the list of displacement in y direction from itself

        Args:
            name (str): name of the object

        Returns:
            list[float]: a list of displacement in y direction from itself 
        """
        
        if name not in self.__displacement_from_itself_y:
            initial_y = self.__db[name].x[1].printy()
            delta_y = [-(vec.printy() - initial_y) for vec in self.__db[name].x]
            self.__displacement_from_itself_y[name] = delta_y
        return self.__displacement_from_itself_y[name]

    def __get_displacement_from_itself_mag(self, name: str) -> list[float]:
        """Get the list of displacement in magnitude from itself

        Args:
            name (str): name of the object

        Returns:
            list[float]: a list of displacement in magnitude from itself 
        """
        
        if name not in self.__displacement_from_itself_mag:
            initial_x = self.__db[name].x[0].printx()
            initial_y = self.__db[name].x[1].printy()
            distance = [
                ((vec.printx() - initial_x) ** 2 + (vec.printy() - initial_y) ** 2) ** 0.5
                for vec in self.__db[name].x
            ]
            self.__displacement_from_itself_x[name] = distance
        return self.__displacement_from_itself_x[name]

    def __get_displacement_from_center_x(self, name: str) -> list[float]:
        """Get the list of displacement in x direction from center

        Args:
            name (str): name of the object

        Returns:
            list[float]: a list of displacement in x direction from center 
        """
        
        if name not in self.__displacement_from_center_x:
            delta_x = [vec.printx() for vec in self.__db[name].x] #vec - 0
            self.__displacement_from_itself_x[name] = delta_x
        return self.__displacement_from_itself_x[name]
    
    def __get_displacement_from_center_y(self, name: str) -> list[float]:
        """Get the list of displacement in y direction from center

        Args:
            name (str): name of the object

        Returns:
            list[float]: a list of displacement in y direction from center 
        """

        if name not in self.__displacement_from_center_y:
            delta_y = [-vec.printy() for vec in self.__db[name].x] #vec - 0
            self.__displacement_from_itself_y[name] = delta_y
        return self.__displacement_from_itself_y[name]
    
    def __get_displacement_from_center_mag(self, name: str) -> list[float]:
        """Get the list of distance from center

        Args:
            name (str): name of the object

        Returns:
            list[float]: a list of distance from center 
        """

        if name not in self.__displacement_from_center_mag:
            delta_y = [
                ((vec.printx()) ** 2 + (vec.printy()) ** 2) ** 0.5
                for vec in self.__db[name].x
            ] #vec - 0
            self.__displacement_from_itself_y[name] = delta_y
        return self.__displacement_from_itself_y[name]

    def __get_displacement_from_center_object_x(self, name: str) -> list[float]:
        """Get the list of displacement in x direction from center object

        Args:
            name (str): name of the object

        Returns:
            list[float]: a list of displacement in x direction from center object
        """

        if name not in self.__displacement_from_center_object_x:
            if len(self.__db) == 2:
                center_object_x = self.__db["earth"].x[0].printx()
            else:
                center_object_x = self.__db["sun"].x[0].printx()
            delta_x = [vec.printx() - center_object_x for vec in self.__db[name].x]
            self.__displacement_from_itself_x[name] = delta_x
        return self.__displacement_from_itself_x[name]
    
    def __get_displacement_from_center_object_y(self, name: str) -> list[float]:
        """Get the list of displacement in y direction from center object

        Args:
            name (str): name of the object

        Returns:
            list[float]: a list of displacement in y direction from center object
        """

        if name not in self.__displacement_from_center_object_y:
            if len(self.__db) == 2:
                center_object_y = self.__db["earth"].x[0].printy()
            else:
                center_object_y = self.__db["sun"].x[0].printy()
            delta_y = [-(vec.printy() - center_object_y) for vec in self.__db[name].x]
            self.__displacement_from_itself_y[name] = delta_y
        return self.__displacement_from_itself_y[name]
    
    def __get_displacement_from_center_object_mag(self, name: str) -> list[float]:
        """Get the list of distance from center object

        Args:
            name (str): name of the object

        Returns:
            list[float]: a list of distance from center object
        """

        if name not in self.__displacement_from_center_object_mag:
            if len(self.__db) == 2:
                center_object_x = self.__db["earth"].x[0].printx()
                center_object_y = self.__db["earth"].x[0].printy()
            else:
                center_object_x = self.__db["sun"].x[0].printx()
                center_object_y = self.__db["sun"].x[0].printy()
            delta_y = [
                ((vec.printx() - center_object_x) ** 2 + (vec.printy() - center_object_y) ** 2) ** 0.5
                for vec in self.__db[name].x
            ]
            self.__displacement_from_itself_y[name] = delta_y
        return self.__displacement_from_itself_y[name]

    def __energy_ke(self, name: str, mass: float) -> list[float]:
        """Get the list of kinetic energy

        Args:
            name (str): name of the object
            mass (float): mass of the object

        Returns:
            list[float]: a list of kinetic energy
        """

        v_mag = self.__get_v_mag(name)
        ke = list(map(lambda v: 0.5 * mass * (v**2), v_mag))
        return ke

    def __energy_pe(self, name: str, mass: float, G: float) -> list[float]:
        """Get the list of gravitational potential energy

        Args:
            name (str): name of the object
            mass (float): mass of the object
            G (float): gravitational constant

        Returns:
            list[float]: a list of gravitional potential energy
        """

        pe = []
        for i in range(len(self.__t)):
            temp = 0
            x = self.__db[name].x[i]
            for other_name, other_data in self.__db.items():
                if name != other_name:
                    other_mass = other_data.mass
                    delta_r = calc().difference(x, other_data.x[i])
                    delta_r = calc().norm(delta_r)
                    temp += - G * other_mass * mass / delta_r
            pe.append(temp)
        return pe
    
    def __velocity(self, name: str, direction: int) -> list[float]:
        """Get the required velocity list

        Args:
            name (str): name of the object
            direction (int): direction of velocity

        Returns:
            list[float]: a list of the required velocity
        """

        match direction:
            case 0:
                y_axis = self.__get_v_x(name)
                plt.ylabel("Velocity (x-dir) / ms^-1")
                self.__ax.set_title("Velocity in x-direction against Time")
            case 1:
                y_axis = self.__get_v_y(name)
                plt.ylabel("Velocity (y-dir) / ms^-1")
                self.__ax.set_title("Velocity in y-direction against Time")
            case 2:
                y_axis = self.__get_v_mag(name)
                plt.ylabel("Speed / ms^-1")
                self.__ax.set_title("Speed against Time")
        return y_axis

    def __acceleration(self, name: str, direction: int) -> list[float]:
        """Get the required acceleration list

        Args:
            name (str): name of the object
            direction (int): direction of acceleration

        Returns:
            list[float]: a list of the required acceleration
        """

        match direction:
            case 0:
                y_axis = self.__get_a_x(name)
                plt.ylabel("Acceleration (x-dir) / ms^-2")
                self.__ax.set_title("Acceleration in x-direction against Time")
            case 1:
                y_axis = self.__get_a_y(name)
                plt.ylabel("Acceleration (y-dir) / ms^-2")
                self.__ax.set_title("Acceleration in y-direction against Time")
            case 2:
                y_axis = self.__get_a_mag(name)
                plt.ylabel("Acceleration (magnitude) / ms^-2")
                self.__ax.set_title("Acceleration (magnitude) against Time")
        return y_axis
    
    def __force(self, name: str, direction: int) -> list[float]:
        """Get the required force list

        Args:
            name (str): name of the object
            direction (int): direction of force

        Returns:
            list[float]: a list of the required force
        """

        match direction:
            case 0:
                y_axis = self.__get_force_x(name)
                plt.ylabel("Force (x-dir) / N")
                self.__ax.set_title("Force in x-direction against Time")
            case 1:
                y_axis = self.__get_force_y(name)
                plt.ylabel("Force (y-dir) / N")
                self.__ax.set_title("Force in y-direction against Time")
            case 2:
                y_axis = self.__get_force_mag(name)
                plt.ylabel("Force (magnitude) / N")
                self.__ax.set_title("Force (magnitude) against Time")
        return y_axis

    def __displacement_from_itself(self, name: str, direction: int) -> list[float]:
        """Get the required displacement list

        Args:
            name (str): name of the object
            direction (int): direction of displacement

        Returns:
            list[float]: a list of the required displacement
        """

        match direction:
            case 0:
                y_axis = self.__get_displacement_from_itself_x(name)
                plt.ylabel("Displacement (x-dir) / m")
                self.__ax.set_title("Displacement in x-direction from Itself at t = 0")
            case 1:
                y_axis = self.__get_displacement_from_itself_y(name)
                plt.ylabel("Displacement (y-dir) / m")
                self.__ax.set_title("Displacement in y-direction from Itself at t = 0")
            case 2:
                y_axis = self.__get_displacement_from_itself_mag(name)
                plt.ylabel("Distance / m")
                self.__ax.set_title("Distance from Itself at t = 0")
        return y_axis
    
    def __displacement_from_center(self, name: str, direction: int) -> list[float]:
        """Get the required displacement list

        Args:
            name (str): name of the object
            direction (int): direction of displacement

        Returns:
            list[float]: a list of the required displacement
        """
        
        match direction:
            case 0:
                y_axis = self.__get_displacement_from_center_x(name)
                plt.ylabel("Displacement (x-dir) / m")
                self.__ax.set_title("Displacement in x-direction from Center at t = 0")
            case 1:
                y_axis = self.__get_displacement_from_center_y(name)
                plt.ylabel("Displacement (y-dir) / m")
                self.__ax.set_title("Displacement in y-direction from Center at t = 0")
            case 2:
                y_axis = self.__get_displacement_from_center_mag(name)
                plt.ylabel("Distance / m")
                self.__ax.set_title("Distance from Center at t = 0")
        return y_axis

    def __displacement_from_center_object(self, name: str, direction: int) -> list[float]:
        """Get the required displacement list

        Args:
            name (str): name of the object
            direction (int): direction of displacement

        Returns:
            list[float]: a list of the required displacement
        """
        
        match direction:
            case 0:
                y_axis = self.__get_displacement_from_center_object_x(name)
                plt.ylabel("Displacement (x-dir) / m")
                self.__ax.set_title("Displacement in x-direction from Center Object at t = 0")
            case 1:
                y_axis = self.__get_displacement_from_center_object_y(name)
                plt.ylabel("Displacement (y-dir) / m")
                self.__ax.set_title("Displacement in y-direction from Center Object at t = 0")
            case 2:
                y_axis = self.__get_displacement_from_center_object_mag(name)
                plt.ylabel("Distance / m")
                self.__ax.set_title("Distance from Center Object at t = 0")
        return y_axis

    def general(self, name: str, data_choice: int, direction: int, displacement_mode: int) -> tuple[matplotlib.figure, matplotlib.axes]:
        """Use the data to create fig, ax

        Args:
            name (str): name of the object
            data_choice (int): index of the data choice
            direction (int): index of the direction
            displacement_mode (int): index of the displacement mode

        Returns:
            tuple[matplotlib.figure, matplotlib.axes]: matplotlib fig and ax for plotting graph
        """

        t = self.__get_t(name)
        self.__ax.clear()

        match data_choice:
            case 0: #displacement
                match displacement_mode:
                    case 0: y_axis = self.__displacement_from_itself(name, direction)
                    case 1: y_axis = self.__displacement_from_center(name, direction)
                    case 2: y_axis = self.__displacement_from_center_object(name, direction)
            case 1: y_axis = self.__velocity(name, direction)
            case 2: y_axis = self.__acceleration(name, direction)
            case 3: y_axis = self.__force(name, direction)
        
        plt.xlabel("Time / s")
        self.__ax.plot(t, y_axis)

        return self.__fig, self.__ax

    def energy(self, name: str, energy_choice: int, G: float) -> tuple[matplotlib.figure, matplotlib.axes]:
        """Use the data to create fig, ax

        Args:
            name (str): name of the object
            energy_choice (int): index of the energy choice
            G (float): gravitational constant

        Returns:
            tuple[matplotlib.figure, matplotlib.axes]: matplotlib fig and ax for plotting graph
        """

        mass = self.__db[name].mass
        t = self.__get_t(name)
        self.__ax.clear()

        match energy_choice:
            case 0:
                ke = self.__energy_ke(name, mass)
                self.__ax.plot(t, ke, label = "Kinetic Energy")
                plt.xlabel("Time / s")
                plt.ylabel("Kinetic Energy / J")
                self.__ax.set_title("Kinetic Energy against Time")

            case 1:
                pe = self.__energy_pe(name, mass, G)
                self.__ax.plot(t, pe, label = "Gravitational Energy")
                plt.xlabel("Time / s")
                plt.ylabel("Gravitational Potential Energy / J")
                self.__ax.set_title("Gravitational Potential Energy against Time")

            case 2:
                ke = self.__energy_ke(name, mass)
                pe = self.__energy_pe(name, mass, G)
                total = [i + j for i, j in zip(ke, pe)]
                self.__ax.plot(t, ke, label = "Kinetic Energy")
                self.__ax.plot(t, pe, label = "Gravitational Potential Energy")
                self.__ax.plot(t, total, label = "Total Energy")
                self.__ax.set_title("Total Energy against Time")
                plt.xlabel("Time / s")
                plt.ylabel("Energies / J")
                plt.legend()

        return self.__fig, self.__ax
