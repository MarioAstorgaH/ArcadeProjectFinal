import arcade
class Player(arcade.Sprite):
    def __init__(self, sprite, scale):
        super().__init__(sprite, scale)
        
        # Posición inicial
        self.center_x = 360
        self.center_y = 480

        # Estadisticas
        self.vida: int = 6  # Corazones por default
        self.velocidad: float = 5  # Velocidad Constante (píxeles por frame)
        self.damage: float = 3.5  # Cantidad de daño que inflige el personaje
        self.velocidadLagrima: float = 1
        self.rango: float = 6
        self.fireRate: float = 3.5

        # Movimiento
        self.izquierda: bool = False
        self.derecha: bool = False
        self.arriba: bool = False
        self.abajo: bool = False

        # Disparo
        self.disparo: bool = False
        self.disparoArriba: bool = False
        self.disparoAbajo: bool = False
        self.disparoDerecha: bool = False
        self.disparoIzquierda: bool = False
    
    def update(self):
        """Actualiza la posición según las teclas presionadas"""
        if self.izquierda:
            self.center_x -= self.velocidad
        if self.derecha:
            self.center_x += self.velocidad
        if self.arriba:
            self.center_y += self.velocidad
        if self.abajo:
            self.center_y -= self.velocidad
        
# Clase padre para otros tipos de enemigos
class EnemigoTipo1(arcade.Sprite):
    def __init__(self, sprite, scale, vida=10, damage=1):
        super().__init__(sprite, scale)
        self.vida: float = vida
        self.damage: float = damage