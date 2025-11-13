import arcade
import Views
Alto=960
Ancho=720
Titulo=Hola
def main():
    Window=arcade.Window()
    Views.MenuView.setup()
    Window.show_view(Views.MenuView())