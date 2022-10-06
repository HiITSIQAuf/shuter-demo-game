from ursina import *

mouse.locked = True

class MainMenu(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
        )
        
        self.main_menu = Entity(parent = self, enabled = True)
        self.levels_menu = Entity(parent = self, enabled = False)
        self.player = None

        def start():
            self.player.enable()
            mouse.locked = True
            self.main_menu.disable()
            self.player.time_running = True
        title = Entity(model = "quad", scale = (0.8, 0.2, 0.2), texture = "assets/wen_dreg.jpg", parent = self.main_menu, y = 0.3)

        start_button = Button(text = "S t a r t - G a m e", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.02, parent = self.main_menu)
        quit_button = Button(text = "Q u i t", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.1, parent = self.main_menu)
        quit_button.on_click = application.quit
        start_button.on_click = Func(start)
