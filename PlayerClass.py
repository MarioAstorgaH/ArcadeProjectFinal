import arcade
class Player(arcade.Sprite):
    def __init__(self):
        #Diseño
        self.sprite=None

        #Estadisticas
        self.vida:int=6 #Corazones por default
        self.velocidad:float=1 #Velocidad Constante
        self.damage:float=3.5 #Cantidad de daño que inflige el personaje
        self.velocidadLagrima:float=1
        self.rango:float=6
        self.fireRate:float=3.5

        #Movimiento
        self.izquierda:bool=False
        self.derecha:bool=False
        self.arriba:bool=False
        self.abajo:bool=False

        #Disparo
        self.disparo:bool=False
        self.disparoArriba:bool=False
        self.disparoAbajo:bool=False
        self.disparoDerecha:bool=False
        self.disparoIzquierda:bool=False
        
#Clase padre para otros tipos de enemigos
class EnemigoTipo1(arcade.Sprite):
    def __init__(self):
        self.vida:float
        self.damage:float