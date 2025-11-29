import arcade
import PlayerClass

ANCHO = 1280
ALTO = 720
ESCALA_SPRITE = 0.5

class GameView(arcade.View):
    def __init__(self, player: PlayerClass.Player):
        super().__init__()
        self.player: PlayerClass.Player = player


    def setup(self):
        arcade.set_background_color(arcade.color.AMAZON)
        self.lista_ladrillos = arcade.SpriteList()
        self.lista_jugador = arcade.SpriteList()
        self.lista_jugador.append(self.player)
        
        for x in range(32,ANCHO,64):
                for y in (32, ALTO-32):
                    wall=arcade.Sprite(":resources:images/tiles/brickBrown.png",scale=ESCALA_SPRITE)
                    wall.center_x=x
                    wall.center_y=y
                    self.lista_ladrillos.append(wall)

        for y in range(96,ALTO,64):
                for x in (32,ANCHO-32):
                    wall=arcade.Sprite(":resources:images/tiles/brickBrown.png",scale=ESCALA_SPRITE)
                    wall.center_x=x
                    wall.center_y=y
                    self.lista_ladrillos.append(wall)

        
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.A:
            self.player.izquierda = True
        elif symbol == arcade.key.W:
            self.player.arriba = True
        elif symbol == arcade.key.S:
            self.player.abajo = True
        elif symbol == arcade.key.D:
            self.player.derecha = True
        elif symbol == arcade.key.ESCAPE:
            pause_view = PauseMenu(self)
            self.window.show_view(pause_view)

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.A:
            self.player.izquierda = False
        elif symbol == arcade.key.D:
            self.player.derecha = False
        elif symbol == arcade.key.W:
            self.player.arriba = False
        elif symbol == arcade.key.S:
            self.player.abajo = False

    def on_draw(self):
        self.clear()
        self.lista_ladrillos.draw()
        self.lista_jugador.draw()
        
    def on_update(self, delta_time):
        self.player.update()


class PauseMenu(arcade.View):
    def __init__(self, game_view: GameView):
        super().__init__()
        self.game_view = game_view
    
    def on_draw(self):
        # Dibuja el juego de fondo
        self.game_view.on_draw()
        
        # Overlay oscuro
        arcade.draw_rectangle_filled(ANCHO // 2, ALTO // 2, ANCHO, ALTO, (0, 0, 0, 150))
        arcade.draw_text("PAUSA", ANCHO // 2, ALTO // 2 + 50, arcade.color.WHITE, 40, anchor_x="center")
        arcade.draw_text("Presiona ESC para continuar", ANCHO // 2, ALTO // 2, arcade.color.WHITE, 20, anchor_x="center")
    
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)