import arcade
import Player
import Views
Alto=960
Ancho=720
Titulo="Final Project"
def main():
    Jugador=Player()
    Window=arcade.Window()
    Views.MenuView.setup()
    Window.show_view(Views.MenuView())