import arcade
import PlayerClass 
import SpriteListClass
alto=960
ancho=720
EscalaSprite=0.5
class GameView(arcade.View):
    def __init__(self,player:PlayerClass.Player, window, background_color):
        super().__init__(window, background_color)
        self.player:PlayerClass.Player=player


    def setup(self):
        self.background_color=arcade.color.AMAZON
        self.lista_ladrillos=arcade.SpriteList()
        self.lista_dineros=arcade.SpriteList()
        for x in range(32,ancho,64):
            for y in (32, alto-32):
                wall=arcade.Sprite(":resources:images/tiles/brickBrown.png",scale=EscalaSprite)
                wall.center_x=x
                wall.center_y=y
                self.lista_ladrillos.append(wall)

        for y in range(96,alto,64):
            for x in (32,ancho-32):
                wall=arcade.Sprite(":resources:images/tiles/brickBrown.png",scale=EscalaSprite)
                wall.center_x=x
                wall.center_y=y
                self.lista_ladrillos.append(wall)
        
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
        self.player.sprite
    def on_update(self):
        pass
