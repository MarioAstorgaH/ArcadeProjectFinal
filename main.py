import arcade
import PlayerClass
import ViewsClasses

ANCHO = 1280
ALTO = 720
TITLE = "Final Project"

def main():
    jugador = PlayerClass.Player("assets/sprites/player/thelost.png", 0.5)
    window = arcade.Window(ANCHO, ALTO, TITLE)
    gameView = ViewsClasses.GameView(jugador)
    gameView.setup()
    window.show_view(gameView)
    arcade.run()

if __name__ == "__main__":
    main()