import arcade
import PlayerClass
import ViewsClasses
alto=960
ancho=720
title = "Final Project"
def main():
    jugador=PlayerClass.Player()
    window=arcade.Window(alto,ancho,title)
    gameView = ViewsClasses.GameView(jugador,window,arcade.color.BLACK)
    gameView.setup()
    window.show_view(gameView)
    arcade.run()

if __name__=="__main__":
    main()