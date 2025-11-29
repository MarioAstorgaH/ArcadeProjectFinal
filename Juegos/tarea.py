import arcade

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Mover Sprite con el Mouse")
        self.sprite = arcade.Sprite("imagen.png", scale=0.5)
        self.sprite.center_x = 400
        self.sprite.center_y = 300

    def on_draw(self):
        arcade.start_render()
        self.sprite.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        self.sprite.center_x = x
        self.sprite.center_y = y

arcade.run()
