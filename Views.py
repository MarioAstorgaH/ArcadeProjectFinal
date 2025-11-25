import arcade
import Player
class MenuView(arcade.View):
    def __init__(self, window = None, background_color = None):
        super().__init__(window, background_color)
        
    def setup(self):
        arcade.set_background_color(arcade.color.BLUE)
        
    def on_key_press(self, symbol, modifiers):
        if symbol==arcade.key.A:
            Player.izquierda=True
        elif symbol==arcade.key.D:
            Player.derecha=True
    def on_key_release(self, symbol, modifiers):
        if symbol==arcade.key.A:
            Player.izquierda=False
        elif symbol==arcade.key.D:
            Player.derecha=False
    def on_draw(self):
        self.clear()
    def on_update(self):
        pass
