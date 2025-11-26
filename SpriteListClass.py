import arcade
class Objetos(arcade.SpriteList):
    def __init__(self,sprite:arcade.Sprite):
        super().__init__()
        self.sprite=sprite
        