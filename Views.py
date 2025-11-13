import arcade
class MenuView(arcade.View):
    def __init__(self, window = None, background_color = None):
        super().__init__(window, background_color)
        
    def setup(self):
        arcade.set_background_color(arcade.color.BLUE)
        

    def on_draw(self):
        pass
    def on_update(self):
        pass
