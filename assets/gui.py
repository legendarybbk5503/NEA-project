import pygame
import sys
from objects.button import Button_init, Textbox_init
from objects.database import DatabaseFormat, DatabaseDict
from assets.simulation import Builtin_Simulation
from assets.statistics import Statistics
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib


class GUI():
    def __init__(self):
        """Create a GUI object for pygame
        """

        pygame.init()
        self.__width, self.__height = 1000, 1000
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        pygame.display.set_caption("hello world")
        
        self.__clear() #black background
        pygame.display.flip()

        self.__buttons = Button_init(self.__width, self.__height)
        self.__textboxes = Textbox_init(self.__width, self.__height)

        self.__circle_radius = 7
        
        self.__previous_vars = {}
        self.__previous_vars["displacement_mode"] = None

        self.__paused = False
        self.__speed = 1

        clock = pygame.time.Clock()
        clock.tick(60)

    def __scaling(self, db: DatabaseDict) -> tuple[float, float, float]:
        """Get the scale factor for the simulation 
        when converting real life coordinate into pygame pixels coordinate

        Args:
            db (DatabaseDict): database

        Returns:
            tuple[float, float, float]: scale_factor, min_x, min_y (for scaling each coordinate)
        """

        temp = [data.x for data in db.db.values()]
        coordinates = []
        [coordinates.extend(lst) for lst in temp]
        
        x, y = [], []
        for coor in coordinates:
            x.append(coor.printx())
            y.append(coor.printy())
        
        max_x, min_x = max(x), min(x)
        max_y, min_y = max(y), min(y)

        sf_x = (self.__width - 150) / (max_x - min_x)
        sf_y = (self.__height - 150) / (max_y - min_y)

        scale_factor = min(sf_x, sf_y)
        return scale_factor, min_x, min_y

    def __scaled_coor(self, x: float, y: float, min_x: float, min_y: float, scale_factor: float) -> tuple[int, int]:
        """Convert original coordinate into pygame coordinate

        Args:
            x (float): original x coordinate
            y (float): original y coordinate
            min_x (float): minimum x in all data
            min_y (float): minimum y in all data
            scale_factor (float): scale factor for scaling

        Returns:
            tuple[int, int]: x, y in pygame coordinate
        """

        scaled_x = int(((x - min_x) * scale_factor)) + 75
        scaled_y = int(((y - min_y) * scale_factor)) + 75
        return scaled_x, scaled_y

    def __format_time(self, seconds: float) -> str:
        """Convert time in seconds into human readable approximate form

        Args:
            seconds (float): time in seconds

        Returns:
            str: human readable approximate form of time
        """

        years = seconds // (365 * 24 * 3600)
        days = (seconds // (24 * 3600)) % 365
        hours = (seconds // 3600) % 24
        minutes = (seconds // 60) % 60
        remaining_seconds = seconds % 60

        if years > 0:
            if years == 1: return f"1 yr, {days} days"
            else: return f"{years} yrs"
        elif days > 0:
            if days == 1: return f"1 day, {hours} hrs"
            else: return f"{days} days"
        elif hours > 0:
            if hours == 1: return f"1 hr, {minutes} mins"
            else: return f"{hours}hrs"
        elif minutes > 0:
            if minutes == 1: return f"1 min, {seconds} s"
            else: return f"{minutes} mins"
        else: return f"{remaining_seconds} s"

    def __draw_circle(self, data: DatabaseFormat, i: int, min_x: float, min_y: float, scale_factor: float) -> tuple[int, int]:
        """Draw the circles of the object

        Args:
            data (DatabaseFormat): database of the object
            i (int): index
            min_x (float): minimum x for scaling
            min_y (float): minimum y for scaling
            scale_factor (float): scale factor for scaling into pygame coordinate

        Returns:
            tuple[int, int]: center(x, y)
        """

        color = data.color
        x, y = data.x[i].printx(), data.x[i].printy()
        center = self.__scaled_coor(x, y, min_x, min_y, scale_factor)
        pygame.draw.circle(self.__screen, color, center, self.__circle_radius)
        return center

    def __draw_check_buttons(self, db: DatabaseDict, iterationNo: float):
        """Check all buttons in draw

        Args:
            db (DatabaseDict): database
            iterationNo (float): number of iterations
        """

        for event in pygame.event.get():
            if self.__isExit(event):
                self.__exit()
            elif self.__isHome(event):
                self.__home()
            elif self.__isBack(event):
                simulation_choice = self.__previous_vars["simulation_choice"]
                self.__simulation_run(simulation_choice)
            elif self.__isPlay_again(event):
                self.__draw(db, iterationNo)
            elif self.__isStatistics(event):
                self.__statistics(db)
            elif self.__isPause(event):
                self.__draw_pause(db, iterationNo)
            elif self.__isSpeedUp(event):
                self.__draw_speedup()
            elif self.__isSlowDown(event):
                self.__draw_slowdown()
    
    def __draw_pause(self, db, iterationNo):
        self.__paused = not self.__paused
        button = self.__buttons.pause
        button._text = "Pause" if self.__paused is False else "Resume"
        button.draw(self.__screen)
        pygame.display.update(button._rect)

        while self.__paused is True: #pause
            self.__draw_check_buttons(db, iterationNo)
    
    def __draw_speedup(self):
        l = [0.1, 0.2, 0.5, 1, 2, 5]
        if self.__speed != 5:
            self.__speed = l[(l.index(self.__speed) + 1) % len(l)]
        button = self.__buttons.speed
        button._text = f"Speed: {str(self.__speed)}x"
        button.draw(self.__screen)
        pygame.display.update(button._rect)

    def __draw_slowdown(self):
        l = [0.1, 0.2, 0.5, 1, 2, 5]
        if self.__speed != 0.1:
            self.__speed = l[(l.index(self.__speed) - 1) % len(l)]
        button = self.__buttons.speed
        button._text = f"Speed: {str(self.__speed)}x"
        button.draw(self.__screen)
        pygame.display.update(button._rect)
        
    def __draw(self, db: DatabaseDict, iterationNo: float):
        """Create the drawing screen and draw the simulation on the screen
        with the choice of play again and statistics

        Args:
            db (DatabaseDict): database
            iterationNo (int): number of iterations
        """

        self.__previous_vars["db"] = db
        self.__previous_vars["iterationNo"] = iterationNo

        self.__screen.fill((0, 0, 0)) #black
        pygame.display.flip()

        #extract name, x only from d
        scale_factor, min_x, min_y = self.__scaling(db)
        scaled_centers = {name: [] for name in db.db.keys()}

        for i in range(iterationNo):
            self.__clear()
            self.__buttons.home_button.draw(self.__screen)
            self.__buttons.back_button.draw(self.__screen)
            self.__buttons.play_again.draw(self.__screen)
            self.__buttons.statistics.draw(self.__screen)
            self.__buttons.speed.draw(self.__screen)
            self.__buttons.pause.draw(self.__screen)
            self.__buttons.speedup.draw(self.__screen)
            self.__buttons.slowdown.draw(self.__screen)

            #show time
            time = next(iter(db.db.values())).t[i]
            self.__buttons.simulation_time._text = f"Time: {self.__format_time(time)}"
            self.__buttons.simulation_time.draw(self.__screen)

            #draw each objects
            for name, data in db.db.items():
                center = self.__draw_circle(data, i, min_x, min_y, scale_factor)
                scaled_centers[name].append(center)

            #draw trajectory
            if i > 0:
                for name, centers in scaled_centers.items():
                    for j in range(len(centers)):
                        if j > 0:
                            color = db.db[name].color
                            previous = centers[j-1]
                            now = centers[j]
                            pygame.draw.line(self.__screen, color, previous, now, 2)

            pygame.display.flip()           

            self.__draw_check_buttons(db, iterationNo)

            pygame.time.wait(int(10/self.__speed))

        while True:
            self.__draw_check_buttons(db, iterationNo)
        
    def __statistics(self, db: DatabaseDict):
        """Create the statistics screen and let user pick between different statistics

        Args:
            db (DatabaseDict): database
        """

        self.__clear()

        self.__buttons.home_button.draw(self.__screen)
        self.__buttons.back_button.draw(self.__screen)
        l = len(db.db)
        if l == 2:
            [button.draw(self.__screen) for button in self.__buttons.statistics_earthmoon]
        else:
            [button.draw(self.__screen) for button in self.__buttons.statistics_solar[:l]]

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if self.__isExit(event):
                    self.__exit()
                elif self.__isHome(event):
                    self.__home()
                elif self.__isBack(event):
                    iterationNo = self.__previous_vars["iterationNo"]
                    self.__draw(db, iterationNo)
                else:
                    if l == 2:
                        choice = self.__isStatistics_earthmoon(event) #choose body
                    else:
                        choice = self.__isStatistics_solar(event, l)

                    if choice is not False: #False then nothing will happen
                        if l == 2:
                            name = ["earth", "moon"][choice]
                        else:
                            lst = ["sun", "mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto"]
                            name = lst[choice]
                        self.__statistics_setting(name)

    def __statistics_setting(self, name: str):
        """Let the user pick between displacement, velocity, acceleration, force and energy
        
        Args:
            name (str): name of the object
        """

        self.__previous_vars["name"] = name

        self.__clear()
        self.__buttons.home_button.draw(self.__screen)
        self.__buttons.back_button.draw(self.__screen)
        [button.draw(self.__screen) for button in self.__buttons.statistics_mode]

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if self.__isExit(event):
                    self.__exit()
                elif self.__isHome(event):
                    self.__home()
                elif self.__isBack(event):
                    db = self.__previous_vars["db"]
                    self.__statistics(db)
                else:
                    choice = self.__isMode(event)
                    if choice is not False: #False then nothing will happen
                        if choice == 4: #energy
                            self.__statistics_energy(name)
                        else: 
                            if choice == 0: #displacement
                                displacement_mode = self.__statistics_displacement()
                            else:
                                displacement_mode = None
                            #0: displacement, 1: velocity, 2: acceleration, 3: force
                            self.__statistics_general(name, choice, displacement_mode)

    def __statistics_energy(self, name: str):
        """Let the user pick bewteen energies

        Args:
            name (str): name of the object
        """

        self.__previous_vars["data_choice"] = 4

        self.__clear()
        self.__buttons.home_button.draw(self.__screen)
        self.__buttons.back_button.draw(self.__screen)
        [button.draw(self.__screen) for button in self.__buttons.statistics_energy]

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if self.__isExit(event):
                    self.__exit()
                elif self.__isHome(event):
                    self.__home()
                elif self.__isBack(event):
                    self.__statistics_setting(name)
                else:
                    choice = self.__isEnergy(event)
                    if choice is not False: #False then nothing will happen
                        fig, ax, = self.__stats.energy(name, choice, self.__G)
                        self.__embed_graph(fig, ax)

    def __statistics_displacement(self) -> int:
        """Let the user pick between displacement mode

        Returns:
            int: index of the modes
        """

        self.__clear()
        self.__buttons.home_button.draw(self.__screen)
        self.__buttons.back_button.draw(self.__screen)
        [button.draw(self.__screen) for button in self.__buttons.statistics_displacement]

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if self.__isExit(event):
                    self.__exit()
                elif self.__isHome(event):
                    self.__home()
                elif self.__isBack(event):
                    name = self.__previous_vars["name"]
                    self.__statistics_setting(name)
                else:
                    choice = self.__isDisplacement(event)
                    if choice is not False:
                        self.__previous_vars["displacement_mode"] = choice
                        return choice #displacement mode

    def __statistics_general(self, name: str, data_choice: int, displacement_mode: int):
        """Let the user choose between x, y and magnitude

        Args:
            name (str): name of the objects
            data_choice (int): which type of data
            displacement_mode (int): if its displacement, which type of displacement
        """
        
        self.__previous_vars["data_choice"] = data_choice
        self.__clear()
        self.__buttons.home_button.draw(self.__screen)
        self.__buttons.back_button.draw(self.__screen)
        [button.draw(self.__screen) for button in self.__buttons.statistics_general]

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if self.__isExit(event):
                    self.__exit()
                elif self.__isHome(event):
                    self.__home()
                elif self.__isBack(event):
                    if displacement_mode is not None:
                        displacement_mode = self.__statistics_displacement()
                        self.__statistics_general(name, data_choice, displacement_mode)
                    else:
                        self.__statistics_setting(name)
                else:
                    choice = self.__isGeneral(event)
                    if choice is not False:
                        fig, ax = self.__stats.general(name, data_choice, choice, displacement_mode)
                        self.__embed_graph(fig, ax)

    def __embed_graph(self, fig: matplotlib.figure , ax: matplotlib.axes.Axes):
        """Plot the graph add it to pygame screen

        Args:
            fig (matplotlib.figure): matplotlib figure
            ax (matplotlib.axes.Axes): matplotlib axes
        """

        self.__clear()
        self.__buttons.home_button.draw(self.__screen)
        self.__buttons.back_button.draw(self.__screen)

        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        image_surface = pygame.image.fromstring(raw_data, size, "RGB")
        image_surface = pygame.transform.scale(image_surface, (750, 750))
        self.__screen.blit(image_surface, (125, 125))

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if self.__isExit(event):
                    self.__exit()
                elif self.__isHome(event):
                    self.__home()
                elif self.__isBack(event):
                    name = self.__previous_vars["name"]
                    data_choice = self.__previous_vars["data_choice"]
                    if data_choice == 4:
                        self.__statistics_energy(name)
                    else:
                        displacement_mode = self.__previous_vars["displacement_mode"]
                        self.__statistics_general(name, data_choice, displacement_mode)
                    


    def __clear(self):
        """Clear pygame screen
        """

        self.__screen.fill((0, 0, 0)) #black

    def __isExit(self, event: pygame.event) -> bool:
        """Check if the exit button is clicked

        Args:
            event (_type_): pygame event

        Returns:
            bool: True if the exit button is clicked else False
        """
        
        return event.type == pygame.QUIT

    def __isStart(self, event: pygame.event) -> bool:
        """Check if the start button is clicked

        Args:
            event (pygame.event): pygame event

        Returns:
            bool: True if the start button is clicked else False
        """

        button = self.__buttons.start_button
        button.isHover(self.__screen)
        return button.isCollide(event)

    def __isSimulation_select(self, event: pygame.event) -> int | bool:
        """Check if the simulation selection buttons are clicked

        Args:
            event (pygame.event): pygame event

        Returns:
            int | bool: index of the buttons if they are clicked else False
        """

        for i, button in enumerate(self.__buttons.simulation_selection_buttons):
            button.isHover(self.__screen)
            if button.isCollide(event):
                return i
        return False

    def __isHome(self, event: pygame.event) -> bool:
        """Check if the home button is clicked

        Args:
            event (pygame.event): pygame event

        Returns:
            bool: True if the home button is clicked else False
        """

        button = self.__buttons.home_button
        button.isHover(self.__screen)
        return button.isCollide(event)

    def __isBack(self, event: pygame.event) -> bool:
        """Check if the back button is clicked

        Args:
            event (pygame.event): pygame event

        Returns:
            bool: True if the back button is clicked else False
        """

        button = self.__buttons.back_button
        button.isHover(self.__screen)
        return button.isCollide(event)

    def __isEnter(self, event: pygame.event) -> bool:
        """Check if the enter button is clicked

        Args:
            event (pygame.event): pygame event

        Returns:
            bool: True if the enter button is clicked else False
        """

        button = self.__buttons.simulation_setting_enter
        button.isHover(self.__screen)
        return button.isCollide(event)

    def __isPlay_again(self, event: pygame.event) -> bool:
        """Check if the back button is clicked

        Args:
            event (pygame.event): pygame event

        Returns:
            bool: True if the back button is clicked
        """

        button = self.__buttons.play_again
        button.isHover(self.__screen)
        return button.isCollide(event)
    
    def __isPause(self, event: pygame.event) -> bool:
        """Check if the pause button is clicked

        Args:
            event (pygame.event): pygame event

        Returns:
            bool: True if the back button is clicked
        """

        button = self.__buttons.pause
        button.isHover(self.__screen)
        return button.isCollide(event)
    
    def __isSpeedUp(self, event: pygame.event) -> bool:
        button = self.__buttons.speedup
        button.isHover(self.__screen)
        return button.isCollide(event)

    def __isSlowDown(self, event: pygame.event) -> bool:
        button = self.__buttons.slowdown
        button.isHover(self.__screen)
        return button.isCollide(event)

    def __isStatistics(self, event: pygame.event) -> bool:
        """Check if the statistics button is clicked

        Args:
            event (pygame.event): pygame event

        Returns:
            bool: True if the statistics button is clicked else False
        """

        button = self.__buttons.statistics
        button.isHover(self.__screen)
        return button.isCollide(event)

    def __isStatistics_earthmoon(self, event: pygame.event) -> int | bool:
        """Check if the earth or moon buttons are clicked

        Args:
            event (pygame.event): pygame event

        Returns:
            int | bool: index of the object if it is clicked else False
        """

        for i, button in enumerate(self.__buttons.statistics_earthmoon):
            button.isHover(self.__screen)
            if button.isCollide(event):
                return i #0-1
        return False

    def __isStatistics_solar(self, event: pygame.event, l: int) -> int | bool:
        """Check if the objects buttons are clicked

        Args:
            event (pygame.event): pygame event
            l (int): number of objects from the sun

        Returns:
            int | bool: index of the object if it is clicked else False
        """

        for i, button in enumerate(self.__buttons.statistics_solar[:l]):
            button.isHover(self.__screen)
            if button.isCollide(event):
                return i #0-10
        return False
    
    def __isMode(self, event: pygame.event) -> int | bool:
        """Check if the statistics mode buttons are clicked

        Args:
            event (pygame.event): pygame event

        Returns:
            int | bool: index of the mode if it is clicked else False
        """

        for i, button in enumerate(self.__buttons.statistics_mode):
            button.isHover(self.__screen)
            if button.isCollide(event):
                return i #0-5
        return False
    
    def __isEnergy(self, event: pygame.event) -> int | bool:
        """Check if the differnet types of energies buttons are clicked

        Args:
            event (pygame.event): pygame event

        Returns:
            int | bool: index of the energy if it is clicked else False
        """

        for i, button in enumerate(self.__buttons.statistics_energy):
            button.isHover(self.__screen)
            if button.isCollide(event):
                return i #0-2
        return False

    def __isDisplacement(self, event: pygame.event) -> int | bool:
        """Check if the different types of displacements buttons are clicked

        Args:
            event (pygame.event): pygame event

        Returns:
            int | bool: index of the displacement if it is clicked else False
        """

        for i, button in enumerate(self.__buttons.statistics_displacement):
            button.isHover(self.__screen)
            if button.isCollide(event):
                return i #0-2
        return False
    
    def __isGeneral(self, event: pygame.event) -> int | bool:
        """Check if the drection buttons are clicked

        Args:
            event (pygame.event): pygame event

        Returns:
            int | bool: index of the direction if it is clicked else False
        """

        for i, button in enumerate(self.__buttons.statistics_general):
            button.isHover(self.__screen)
            if button.isCollide(event):
                return i #0-2
        return False

    def __exit(self):
        """Exit pygame
        """

        pygame.quit()
        sys.exit()

    def __enter(self, choice: int) -> list[float, float, int]:
        """Return the textbox values, if they are blank then default values

        Args:
            choice (int): choice of the simulation

        Returns:
            list[float, float, int]: setting values [G, dt, iterationNo]
        """

        values = []
        default = [
            [6.67e-11, 3600, 720],
            [6.67e-11, 43200, 1500],
            [6.67e-11, 432000, 2200],
            [6.67e-11, 1728000, 4600]
        ]
        for i, textbox in enumerate(self.__textboxes.simulation_setting_textboxes):
            value = textbox.value
            if value == "":
                values.append(default[choice][i])
            else:
                if i in [0, 1]:
                    values.append(float(value))
                elif i == 2:
                    values.append(int(value))
        return values

    def __draw_setting(self, simulation_choice: int) -> list[float, float, int]:
        """Create the screen of drawing setting and return the values

        Args:
            simulation_choice (int): choice of the simulation

        Returns:
            list[float, float, int]: setting values [G, dt, iterationNo]
        """

        self.__clear()
        
        for textbox in self.__textboxes.simulation_setting_textboxes:
            textbox.draw(self.__screen)
        
        match simulation_choice:
            case 0:
                for button in self.__buttons.simulation_setting_earthmoon_default_buttons:
                    button.draw(self.__screen)
            case 1:
                for button in self.__buttons.simulation_setting_inner_solar_default_buttons:
                    button.draw(self.__screen)
            case 2:
                for button in self.__buttons.simulation_setting_middle_solar_default_buttons:
                    button.draw(self.__screen)
            case 3:
                for button in self.__buttons.simulation_setting_outer_solar_default_buttons:
                    button.draw(self.__screen)

        self.__buttons.simulation_setting_guide1.draw(self.__screen)
        self.__buttons.simulation_setting_guide2.draw(self.__screen)
        self.__buttons.simulation_setting_enter.draw(self.__screen)
        self.__buttons.home_button.draw(self.__screen)
        self.__buttons.back_button.draw(self.__screen)
        pygame.display.flip()

        typing = [False] * 3
        while True:
            for event in pygame.event.get():
                #check buttons
                if self.__isExit(event):
                    self.__exit()
                elif self.__isHome(event):
                    self.__home()
                elif self.__isBack(event):
                    self.__start()
                elif self.__isEnter(event):
                    try:
                        value = self.__enter(simulation_choice)
                    except:
                        button = self.__buttons.simulation_setting_enter_error
                        button.draw(self.__screen)
                        pygame.display.flip()
                    else:
                        return value


                #check textboxes
                for i, textbox in enumerate(self.__textboxes.simulation_setting_textboxes):
                    if typing[i] is False:
                        textbox.isHover(self.__screen)
                    if textbox.isCollide(event):
                        typing[i] = True
                        textbox._color = "gray"
                        textbox.draw(self.__screen)
                        pygame.display.update(textbox._rect)
                    if typing[i] is True:
                        textbox.typing(event, self.__screen)
                        if textbox.isExit_textbox(event):
                            typing[i] = False
                            textbox._color = textbox._orginal_color
                            textbox.draw(self.__screen)
                            pygame.display.update(textbox._rect)
            pygame.time.delay(10)

    def __simulation_run(self, simulation_choice: int):
        """Load and calculate the simulation with given values

        Args:
            simulation_choice (int): choice of the simulation
        """

        self.__previous_vars["simulation_choice"] = simulation_choice

        self.__clear()
        values = self.__draw_setting(simulation_choice)
        match simulation_choice:
            case 0: model = Builtin_Simulation().earth_moon(*values)
            case 1: model = Builtin_Simulation().inner_solar_system(*values)
            case 2: model = Builtin_Simulation().middle_solar_system(*values)
            case 3: model = Builtin_Simulation().outer_solar_system(*values)
        self.__G = values[0]
        db = model.load()
        
        self.__stats = Statistics(db.db)
        self.__draw(db, values[2])

    def __home(self):
        """Back to home screen
        """

        self.__clear()
        self.run()

    def __start(self):
        """Create the screen for user to select with simulation
        """

        self.__clear()
        for button in self.__buttons.simulation_selection_buttons:
            button.draw(self.__screen)
        self.__buttons.home_button.draw(self.__screen)
        self.__buttons.back_button.draw(self.__screen)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if self.__isExit(event):
                    self.__exit()
                elif self.__isHome(event):
                    self.__home()
                elif self.__isBack(event):
                    self.run()
                simulation_choice = self.__isSimulation_select(event)
                if simulation_choice is not False:
                    self.__simulation_run(simulation_choice)

            pygame.time.delay(10)        

    def run(self):
        """Start the whole programme
        And a start button
        """
        
        self.__clear()
        self.__buttons.start_button.draw(self.__screen)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if self.__isExit(event):
                    self.__exit()

                elif self.__isStart(event):
                    self.__start()
            pygame.time.delay(10)