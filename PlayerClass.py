import arcade
class Player(arcade.Sprite):
    def __init__(self):
        self.sprite=None 
        self.vida=1
        self.velocidad=10 #Velocidad Constante
        self.sprite.center_x=20

        #Movimiento
        self.izquierda=False
        self.derecha=False
        self.arriba=False
        self.abajo=False

        #Disparo
        self.disparo=False
        self.disparoArriba=False
        self.disparoAbajo=False
        self.disparoDerecha=False
        self.disparoIzquierda=False

