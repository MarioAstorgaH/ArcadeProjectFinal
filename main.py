import arcade
import PlayerClass
import ViewsClasses
alto=960
ancho=720
title = "Final Project"
def main():
    jugador=PlayerClass.Player()
    window=arcade.Window(alto,ancho,title)
    gameView = ViewsClasses.GameView(jugador)
    gameView.setup()
    window.show_view(gameView)
