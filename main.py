import arcade
import PlayerClass
import ViewsClasses
Alto=960
Ancho=720
Titulo="Final Project"
def main():
    Jugador=PlayerClass()
    Window=arcade.Window()
    ViewsClasses.MenuView.setup()
    Window.show_view(ViewsClasses.MenuView())