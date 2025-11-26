import arcade
import PlayerClass 
import SpriteListClass
class GameView(arcade.View):
    def __init__(self,player:PlayerClass.Player,objeto1:SpriteListClass.Objetos, window, background_color):
        super().__init__(window, background_color)
        self.player:PlayerClass.Player=player
        self.objeto1:SpriteListClass.Objetos=objeto1

    def setup(self):
        arcade.set_background_color(arcade.color.BLUE)
        
    def on_key_press(self, symbol, modifiers):
        if symbol==arcade.key.A:
            self.player.izquierda=True
        elif symbol==arcade.key.W:
            self.player.arriba=True
        elif symbol==arcade.key.S:
            self.player.abajo=True
        elif symbol==arcade.key.D:
            self.player.derecha=True

    def on_key_release(self, symbol, modifiers):
        if symbol==arcade.key.A:
            self.player.izquierda=False
        elif symbol==arcade.key.D:
            self.player.derecha=False
        elif symbol==arcade.key.W:
            self.player.arriba=False
        elif symbol==arcade.key.S:
            self.player.abajo=False

    def on_draw(self):
        self.clear()

    def on_update(self):
        pass
