import pygame
import sys
from objects.button import Button_init, Textbox_init
from assets.simulation import Builtin_Simulation

class GUI():
    def __init__(self):
        pygame.init()
        self.__width, self.__height = 1000, 1000
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        pygame.display.set_caption("hello world")
        
        self.__clear() #black background
        pygame.display.flip()

        self.__buttons = Button_init(self.__width, self.__height)
        self.__textboxes = Textbox_init(self.__width, self.__height)

        self.__circle_radius = 7

        clock = pygame.time.Clock()
        clock.tick(60)

    def __scaling(self, db):
        temp = [data.x for data in db.db.values()]
        coordinates = []
        [coordinates.extend(lst) for lst in temp]
        
        x, y = [], []
        for coor in coordinates:
            x.append(coor.printx())
            y.append(coor.printy())
        
        max_x, min_x = max(x), min(x)
        max_y, min_y = max(y), min(y)

        sf_x = (self.__width - 100) / (max_x - min_x)
        sf_y = (self.__height - 100) / (max_y - min_y)

        scale_factor = min(sf_x, sf_y)
        return scale_factor, min_x, min_y

    def __scaled_coor(self, x, y, min_x, min_y, scale_factor):
        scaled_x = int(((x - min_x) * scale_factor)) + 50
        scaled_y = int(((y - min_y) * scale_factor)) + 50
        return scaled_x, scaled_y

    def __format_time(self, seconds):
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

    def __draw_circle(self, data, i, min_x, min_y, scale_factor):
        color = data.color
        x, y = data.x[i].printx(), data.x[i].printy()
        center = self.__scaled_coor(x, y, min_x, min_y, scale_factor)
        pygame.draw.circle(self.__screen, color, center, self.__circle_radius)
        return center

    def __draw(self, db, iterationNo):
        self.__screen.fill((0, 0, 0)) #black
        pygame.display.flip()

        #extract name, x only from d
        scale_factor, min_x, min_y = self.__scaling(db)
        scaled_centers = {name: [] for name in db.db.keys()}

        for i in range(iterationNo):
            self.__clear()
            self.__buttons.home_button.draw(self.__screen)
            self.__buttons.play_again.draw(self.__screen)
            self.__buttons.statistics.draw(self.__screen)

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
            pygame.time.wait(5)            

            for event in pygame.event.get():
                if self.__isExit(event):
                    self.__exit()
                elif self.__isHome(event):
                    self.__home()
                elif self.__isPlay_again(event):
                    self.__draw(db, iterationNo)
                elif self.__isStatistics(event):
                    self.__statistics(db, iterationNo)
        
        while True:
            for event in pygame.event.get():
                if self.__isExit(event):
                    self.__exit()
                elif self.__isHome(event):
                    self.__home()
                elif self.__isPlay_again(event):
                    self.__draw(db, iterationNo)
                elif self.__isStatistics(event):
                    self.__statistics(db, iterationNo)
        
    def __statistics(self, db, iterationNo):
        self.__clear()

        self.__buttons.home_button.draw(self.__screen)
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
                else:
                    if l == 2:
                        choice = self.__isStatistics_earthmoon(event) #choose object
                    else:
                        choice = self.__isStatistics_solar(event, l)
                    if choice is not False: #False then nothing will happen
                        self.__statistics_setting(choice, db, iterationNo, l)

    def __statistics_setting(self, object, db, iterationNo, l):
        self.__clear()
        self.__buttons.home_button.draw(self.__screen)
        [button.draw(self.__screen) for button in self.__buttons.statistics_mode]

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if self.__isExit(event):
                    self.__exit()
                elif self.__isHome(event):
                    self.__home()
                else:
                    choice = self.__isMode(event)
                    if choice is not False: #False then nothing will happen
                        if choice == 4: #energy
                            self.__statistics_energy()
                        else: 
                            if choice == 0: #displacement
                                displacement_mode = self.__statistics_displacemet()
                            #0: displacement, 1: velocity, 2: acceleration, 3: force
                            self.__statistics_general(choice, displacement_mode)

    def __statistics_energy(self):
        self.__clear()
        self.__buttons.home_button.draw(self.__screen)
        [button.draw(self.__screen) for button in self.__buttons.statistics_energy]

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if self.__isExit(event):
                    self.__exit()
                elif self.__isHome(event):
                    self.__home()
                else:
                    choice = self.__isEnergy(event)
                    if choice is not False: #False then nothing will happen
                        pass #StatsEnergy(data_choice, KE/PE/total)
#------------------------------------tbc-----------------------------------------

    def __statistics_displacemet(self):
        self.__clear()
        self.__buttons.home_button.draw(self.__screen)
        [button.draw(self.__screen) for button in self.__buttons.statistics_displacement]

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if self.__isExit(event):
                    self.__exit()
                elif self.__isHome(event):
                    self.__home()
                else:
                    choice = self.__isDisplacement(event)
                    if choice is not False:
                        return choice #displacement mode

    def __statistics_general(self, data_choice, displacement_mode = -1):
        self.__clear()
        self.__buttons.home_button.draw(self.__screen)
        [button.draw(self.__screen) for button in self.__buttons.statistics_general]

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if self.__isExit(event):
                    self.__exit()
                elif self.__isHome(event):
                    self.__home()
                else:
                    choice = self.__isGeneral(event)
                    if choice is not False:
                        pass #Stats(data_choice, x/y/magnitude, displacement_mode)
#------------------------------------tbc-----------------------------------------



    def __clear(self):
        self.__screen.fill((0, 0, 0)) #black

    def __isExit(self, event):
        return event.type == pygame.QUIT

    def __isStart(self, event):
        button = self.__buttons.start_button
        button.isHover(self.__screen)
        return button.isCollide(event)

    def __isSimulation_select(self, event):
        for i, button in enumerate(self.__buttons.simulation_selection_buttons):
            button.isHover(self.__screen)
            if button.isCollide(event):
                return i
        return False

    def __isHome(self, event):
        button = self.__buttons.home_button
        button.isHover(self.__screen)
        return button.isCollide(event)

    def __isEnter(self, event):
        button = self.__buttons.simulation_setting_enter
        button.isHover(self.__screen)
        return button.isCollide(event)

    def __isPlay_again(self, event):
        button = self.__buttons.play_again
        button.isHover(self.__screen)
        return button.isCollide(event)

    def __isStatistics(self, event):
        button = self.__buttons.statistics
        button.isHover(self.__screen)
        return button.isCollide(event)

    def __isStatistics_earthmoon(self, event):
        for i, button in enumerate(self.__buttons.statistics_earthmoon):
            button.isHover(self.__screen)
            if button.isCollide(event):
                return i #0-1
        return False

    def __isStatistics_solar(self, event, l):
        for i, button in enumerate(self.__buttons.statistics_solar[:l]):
            button.isHover(self.__screen)
            if button.isCollide(event):
                return i #0-10
        return False
    
    def __isMode(self, event):
        for i, button in enumerate(self.__buttons.statistics_mode):
            button.isHover(self.__screen)
            if button.isCollide(event):
                return i #0-5
        return False
    
    def __isEnergy(self, event):
        for i, button in enumerate(self.__buttons.statistics_energy):
            button.isHover(self.__screen)
            if button.isCollide(event):
                return i #0-2
        return False

    def __isDisplacement(self, event):
        for i, button in enumerate(self.__buttons.statistics_displacement):
            button.isHover(self.__screen)
            if button.isCollide(event):
                return i #0-2
        return False
    
    def __isGeneral(self, event):
        for i, button in enumerate(self.__buttons.statistics_general):
            button.isHover(self.__screen)
            if button.isCollide(event):
                return i #0-2
        return False

    def __exit(self):
        pygame.quit()
        sys.exit()

    def __enter(self, choice):
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
                #choice 0: earth moon
                #choice 1: inner solar system
                #choice 2: outer solar system
                values.append(default[choice][i])
            else:
                if i in [0, 1]:
                    values.append(float(value))
                elif i == 2:
                    values.append(int(value))
        return values

    def __draw_setting(self, choice):
        self.__clear()
        
        for textbox in self.__textboxes.simulation_setting_textboxes:
            textbox.draw(self.__screen)
        
        if choice == 0:
            for button in self.__buttons.simulation_setting_earthmoon_default_buttons:
                button.draw(self.__screen)
        elif choice == 1:
            for button in self.__buttons.simulation_setting_inner_solar_default_buttons:
                button.draw(self.__screen)
        elif choice == 2:
            for button in self.__buttons.simulation_setting_middle_solar_default_buttons:
                button.draw(self.__screen)
        elif choice == 3:
            for button in self.__buttons.simulation_setting_outer_solar_default_buttons:
                button.draw(self.__screen)

        self.__buttons.simulation_setting_guide1.draw(self.__screen)
        self.__buttons.simulation_setting_guide2.draw(self.__screen)
        self.__buttons.simulation_setting_enter.draw(self.__screen)
        self.__buttons.home_button.draw(self.__screen)
        pygame.display.flip()

        typing = [False] * 3
        while True:
            for event in pygame.event.get():
                #check buttons
                if self.__isExit(event):
                    self.__exit()
                elif self.__isEnter(event):
                    try:
                        value = self.__enter(choice)
                    except:
                        button = self.__buttons.simulation_setting_enter_error
                        button.draw(self.__screen)
                        pygame.display.flip()
                    else:
                        return value
                elif self.__isHome(event):
                    self.__home()

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

    def __simulation_run(self, choice):
        self.__clear()
        values = self.__draw_setting(choice)
        match choice:
            case 0: model = Builtin_Simulation().earth_moon(*values)
            case 1: model = Builtin_Simulation().inner_solar_system(*values)
            case 2: model = Builtin_Simulation().middle_solar_system(*values)
            case 3: model = Builtin_Simulation().outer_solar_system(*values)
        db = model.load()
        
        self.__draw(db, values[2])

        while True:
            for event in pygame.event.get():
                if self.__isExit(event):
                    self.__exit()
                elif self.__isHome(event):
                    self.__home()

    def __home(self):
        self.__clear()
        self.run()

    def __start(self):
        self.__clear()
        for button in self.__buttons.simulation_selection_buttons:
            button.draw(self.__screen)
        self.__buttons.home_button.draw(self.__screen)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if self.__isExit(event):
                    self.__exit()
                choice = self.__isSimulation_select(event)
                if choice is not False:
                    self.__simulation_run(choice)
                elif self.__isHome(event):
                    self.__home()
            pygame.time.delay(10)        

    def run(self):
        self.__buttons.start_button.draw(self.__screen)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if self.__isExit(event):
                    self.__exit()

                elif self.__isStart(event):
                    self.__start()
            pygame.time.delay(10)