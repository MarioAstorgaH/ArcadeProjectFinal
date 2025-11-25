import arcade
class Player(arcade.sprite):
    def __init__(self):
        self.sprite=None 
        self.vida=1
        self.velocidad=10 #Velocidad Constante
        self.sprite.center_x=20

        #Movimiento
        self.izquierda=False
        self.derecha=False

