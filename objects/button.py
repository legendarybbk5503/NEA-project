import pygame

class Button():
    def __init__(self, x, y, width, height, color, text, text_color):
        self._rect = pygame.Rect(x, y, width, height)
        self._orginal_color = color
        self._color = color
        self._text = text
        self.__text_color = text_color
    
    def __draw_text(self, surface):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self._text, True, self.__text_color)
        text_rect = text_surface.get_rect(center = self._rect.center)
        surface.blit(text_surface, text_rect)

    def draw(self, surface):
        pygame.draw.rect(surface, self._color, self._rect)
        self.__draw_text(surface)
    
    def isHover(self, surface):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self._rect.collidepoint(mouse_x, mouse_y):
            self._color = "gray"
            self.draw(surface)
            pygame.display.update(self._rect)
        elif self._color != self._orginal_color:
            self._color = self._orginal_color
            self.draw(surface)
            pygame.display.update(self._rect)

    def isCollide(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self._rect.collidepoint(event.pos)
        return False

class Button_init():
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__center_x = self.__width // 2
        self.__center_y = self.__height // 2

        self.__button_init()

    def __start_button(self):
        button_width = 500
        button_height = 100
        return Button(
            self.__center_x - button_width // 2,
            self.__center_y - button_height // 2,
            button_width,
            button_height,
            "white",
            "Start",
            "red"
        )
    
    def __home_button(self):
        button_width = 100
        button_height = 50
        return Button(
            self.__width - button_width,
            0,
            button_width,
            button_height,
            "white",
            "Home",
            "red"
        )
    
    def __back_button(self):
        button_width = 100
        button_height = 50
        return Button(
            0,
            0,
            button_width,
            button_height,
            "white",
            "Back",
            "red"
        )

    def __simulation__selection_buttons(self):
        button_width = 230
        button_height = 75
        width_space = (self.__width - (button_width * 4)) // 5
        x_list = [button_width * i + width_space * (i + 1) for i in range(4)]
        y = self.__center_y - button_height // 2
        texts = [
            "earth moon",
            "inner solar system",
            "middle solar system",
            "outer solar system"
        ]
        return [
            Button(
                x,
                y,
                button_width,
                button_height,
                "white",
                text,
                "red"
            )
        for x, text in zip(x_list, texts)
        ]

    def __simulation_setting_earthmoon_default_buttons(self):
        button_width = 350
        button_height = 100
        height_space = 200
        texts = ["Default: 6.67e-11", "Default: 3600 (an hour)", "Default: 720 (about a month)"]
        y_list = [self.__center_y - 100 + height_space * i for i in [-1, 0, 1]]
        return [
            Button(
                self.__center_x + 100,
                y,
                button_width,
                button_height,
                "white",
                text,
                "red"
            )
            for text, y in zip(texts, y_list)
        ]

    def __simulation_setting_inner_solar_default_buttons(self):
        button_width = 350
        button_height = 100
        height_space = 200
        texts = ["Default: 6.67e-11", "Default: 43200 (half a day)", "Default: 1500 (about 2 yrs)"]
        y_list = [self.__center_y - 100 + height_space * i for i in [-1, 0, 1]]
        return [
            Button(
                self.__center_x + 100,
                y,
                button_width,
                button_height,
                "white",
                text,
                "red"
            )
            for text, y in zip(texts, y_list)
        ]

    def __simulation_setting_middle_solar_default_buttons(self):
        button_width = 350
        button_height = 100
        height_space = 200
        texts = ["Default: 6.67e-11", "Default: 432000 (5 days)", "Default: 2200 (about 30 yrs)"]
        y_list = [self.__center_y - 100 + height_space * i for i in [-1, 0, 1]]
        return [
            Button(
                self.__center_x + 100,
                y,
                button_width,
                button_height,
                "white",
                text,
                "red"
            )
            for text, y in zip(texts, y_list)
        ]

    def __simulation_setting_outer_solar_default_buttons(self):
        button_width = 350
        button_height = 100
        height_space = 200
        texts = ["Default: 6.67e-11", "Default: 1728000 (20 days)", "Default: 4600 (about 250 yrs)"]
        y_list = [self.__center_y - 100 + height_space * i for i in [-1, 0, 1]]
        return [
            Button(
                self.__center_x + 100,
                y,
                button_width,
                button_height,
                "white",
                text,
                "red"
            )
            for text, y in zip(texts, y_list)
        ]

    def __simulation_setting_guide1(self):
        button_width = 500
        button_height = 50
        return Button(
            self.__center_x - button_width // 2,
            0,
            button_width,
            button_height,
            "white",
            "Click and type to change the value",
            "red"
        )
    def __simulation_setting_guide2(self):
        button_width = 500
        button_height = 50
        return Button(
            self.__center_x - button_width // 2,
            button_height,
            button_width,
            button_height,
            "white",
            "Leave them blank for default values",
            "red"
        )

    def __simulation_setting_enter(self):
        button_width = 300
        button_height = 100
        return Button(
            self.__center_x - button_width // 2,
            self.__height - button_height * 1.5,
            button_width,
            button_height,
            "white",
            "Enter",
            "red"
        )

    def __simulation_setting_enter_error(self):
        button_width = 500
        button_height = 100
        return Button(
            self.__center_x - button_width // 2,
            self.__height - 275,
            button_width,
            button_height,
            "white",
            "Invalid values, please check the inputs",
            "red"
        )

    def __simulation_time(self):
        button_width = 300
        button_height = 50
        return Button(
            self.__center_x - button_width // 2,
            0,
            button_width,
            button_height,
            "white",
            "Time: 0 seconds",
            "red"
        )

    def __play_again(self):
        button_width = 300
        button_height = 50
        return Button(
            self.__center_x - button_width - 50,
            self.__height - button_height,
            button_width,
            button_height,
            "white",
            "Play Again",
            "red"
        )

    def __statistics(self):
        button_width = 300
        button_height = 50
        return Button(
            self.__center_x + 50,
            self.__height - button_height,
            button_width,
            button_height,
            "white",
            "Statistics",
            "red"
        )

    def __statistics_earthmoon(self):
        button_width = 150
        button_height = 50
        width_space = 699 // 3
        texts = ["earth", "moon"]
        return [
            Button(
                width_space * (i+1) + button_width * (i),
                self.__center_y - button_height // 2,
                button_width,
                button_height,
                "white",
                text,
                "red"
            )
        for i, text in enumerate(texts)
        ]

    def __statistics_solar(self):
        button_width = 150
        button_height = 50
        width_space = 252 // 6
        height_space = 252 // 6
        texts = ["Sun", "Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]
        buttons1 = [
            Button(
                width_space * (i+1) + button_width * i,
                self.__center_y - height_space - button_height,
                button_width,
                button_height,
                "white",
                texts[i],
                "red"
            )
        for i in range(5)
        ]
        buttons2 = [
            Button(
                width_space * (i+1) + button_width * i,
                self.__center_y + height_space,
                button_width,
                button_height,
                "white",
                texts[i+5],
                "red"
            )
        for i in range(5)
        ]
        return [*buttons1, *buttons2]

    def __statistics_mode(self):
        button_width = 175
        button_height = 50
        width_space = 126 // 6
        texts = ["Displacement", "Velocity", "Acceleration", "Force", "Energy"]
        return [
            Button(
                width_space * (i+1) + button_width * i,
                self.__center_y - button_height // 2,
                button_width,
                button_height,
                "white",
                text,
                "red"
            )
        for i, text in enumerate(texts)
        ]

    def __statistics_energy(self):
        button_width = 200
        button_height = 50
        width_space = 100
        texts = ["Kinetic Energy", "Potential Energy", "Total Energy"]
        return [
            Button(
                width_space * (i+1) + button_width * i,
                self.__center_y - button_height // 2,
                button_width,
                button_height,
                "white",
                text,
                "red"
            )
        for i, text in enumerate(texts)
        ]

    def __statistics_displacement(self):
        button_width = 600
        button_height = 50
        height_space = 852 // 4
        texts = [
            "Displacement from the object itself at t = 0",
            "Displacement from the centre object at t = 0",
            "Displacement from the centre object at that moment"
        ]
        return [
            Button(
                self.__center_x - button_width // 2,
                height_space * (i+1) + button_height * (i),
                button_width,
                button_height,
                "white",
                text,
                "red"
            )
        for i, text in enumerate(texts)
        ]

    def __statistics_general(self):
        button_width = 200
        button_height = 50
        width_space = 100
        texts = ["x-direction", "y-direction", "Magnitude"]
        return [
            Button(
                width_space * (i+1) + button_width * i,
                self.__center_y - button_height // 2,
                button_width,
                button_height,
                "white",
                text,
                "red"
            )
        for i, text in enumerate(texts)
        ]

    def __button_init(self):
        self.start_button = self.__start_button()
        self.simulation_selection_buttons = self.__simulation__selection_buttons()
        self.home_button = self.__home_button()
        self.back_button = self.__back_button()
        self.simulation_setting_earthmoon_default_buttons = self.__simulation_setting_earthmoon_default_buttons()
        self.simulation_setting_inner_solar_default_buttons = self.__simulation_setting_inner_solar_default_buttons()
        self.simulation_setting_middle_solar_default_buttons = self.__simulation_setting_middle_solar_default_buttons()
        self.simulation_setting_outer_solar_default_buttons = self.__simulation_setting_outer_solar_default_buttons()
        self.simulation_setting_guide1 = self.__simulation_setting_guide1()
        self.simulation_setting_guide2 = self.__simulation_setting_guide2()
        self.simulation_setting_enter = self.__simulation_setting_enter()
        self.simulation_setting_enter_error = self.__simulation_setting_enter_error()
        self.simulation_time = self.__simulation_time()
        self.play_again = self.__play_again()
        self.statistics = self.__statistics()
        self.statistics_earthmoon = self.__statistics_earthmoon()
        self.statistics_solar = self.__statistics_solar()
        self.statistics_mode = self.__statistics_mode()
        self.statistics_energy = self.__statistics_energy()
        self.statistics_displacement = self.__statistics_displacement()
        self.statistics_general = self.__statistics_general()

class Textbox(Button):
    def __init__(self, x, y, width, height, color, text, text_color):
        self.__orignal_text = text
        self.value = ""
        super().__init__(x, y, width, height, color, text, text_color)
    
    def isExit_textbox(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return not self._rect.collidepoint(event.pos)

    def typing(self, event, screen):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if len(self.value) > 0:
                    self.value = self.value[:-1]
            else:
                self.value += event.unicode
            self._text = self.__orignal_text + self.value
            super().draw(screen)
            pygame.display.update(self._rect)

class Textbox_init():
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__center_x = self.__width // 2
        self.__center_y = self.__height // 2

        self.__textbox_init()
    
    def __simulation_setting_textboxes(self):
        textbox_width = 500
        textbox_height = 100
        height_space = 200
        texts = ["Gravitional Constant: ", "Time Step (s): ", "Number of Iterations: "]
        y_list = [self.__center_y - 100 + height_space * i for i in [-1, 0, 1]]
        return [
            Textbox(
            50,
            y,
            textbox_width,
            textbox_height,
            "white",
            text,
            "red"
            )
        for text, y in zip(texts, y_list)
        ]
    
    def __textbox_init(self):
        self.simulation_setting_textboxes = self.__simulation_setting_textboxes()