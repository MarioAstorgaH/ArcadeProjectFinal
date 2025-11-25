import arcade
import PlayerClass
class MenuView(arcade.View):
    def __init__(self, window = None, background_color = None):
        super().__init__(window, background_color)
        
    def setup(self):
        arcade.set_background_color(arcade.color.BLUE)
        
    def on_key_press(self, symbol, modifiers):
        if symbol==arcade.key.A:
            PlayerClass.izquierda=True
        elif symbol==arcade.key.D:
            PlayerClass.derecha=True
    def on_key_release(self, symbol, modifiers):
        if symbol==arcade.key.A:
            PlayerClass.izquierda=False
        elif symbol==arcade.key.D:
            PlayerClass.derecha=False
    def on_draw(self):
        self.clear()
    def on_update(self):
        pass
