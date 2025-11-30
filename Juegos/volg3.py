import arcade
import random
import math
import os

# --- Constantes ---
ALTO, ANCHO = 800, 800
TITULO = "Juego con sistema de oleadas"

VELOCIDAD_JUGADOR = 4
VELOCIDAD_BALA = 15
RECORD_FILE = "record.txt"

# =====================================================
# ESTADÍSTICAS DE ENEMIGOS
# (AQUÍ CONTROLAS SPRITES Y VALORES)
# =====================================================
ESTADISTICAS_ENEMIGOS = {
    "malo": {
        "sprite": "enemigos/malo.png",
        "vida": 30,
        "velocidad": 1.2,
        "dano": 5,
        "xp": 3,
        "oro": 2
    },
    "medusa": {
        "sprite": "enemigos/medusa.png",
        "vida": 15,
        "velocidad": 2.0,
        "dano": 3,
        "xp": 1,
        "oro": 2
    }
}
# =====================================================
# MENÚ PRINCIPAL
# =====================================================
class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.fondo = arcade.load_texture("fondos/menu.jpeg")
        self.boton_jugar = (ANCHO//2, 350, 250, 60)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(ANCHO//2, ALTO//2, ANCHO, ALTO, self.fondo)
        arcade.draw_text("MI JUEGO", ANCHO//2 - 140, 580, arcade.color.WHITE, 50)

        x,y,w,h = self.boton_jugar
        arcade.draw_rectangle_filled(x,y,w,h, arcade.color.DARK_GREEN)
        arcade.draw_text("JUGAR", x-55, y-15, arcade.color.WHITE, 20)
        

    def on_mouse_press(self, x, y, button, modifiers):
        bx, by, bw, bh = self.boton_jugar
        if abs(x-bx) < bw/2 and abs(y-by) < bh/2:
            self.window.show_view(Juego())

# =====================================================
# WAVE MANAGER
# =====================================================
class WaveManager:
    def __init__(self):
        self.oleada_actual = 1
        self.enemigos_vivos = 0

        self.oleadas = {
            1: {"cantidad": 3, "tipos": ["malo"]},
            2: {"cantidad": 5, "tipos": ["malo", "medusa"]},
        }

    def obtener_oleada(self):
        return self.oleadas.get(self.oleada_actual, self.oleadas[max(self.oleadas)])

# =====================================================
# BALA
# =====================================================
class Bala(arcade.Sprite):
    def __init__(self, x, y, objetivo_x, objetivo_y, dano=25):
        super().__init__("proyectiles/bala1.png", 0.1)
        self.center_x = x
        self.center_y = y
        self.dano = dano

        dx = objetivo_x - x
        dy = objetivo_y - y
        ang = math.atan2(dy, dx)

        self.change_x = math.cos(ang) * VELOCIDAD_BALA
        self.change_y = math.sin(ang) * VELOCIDAD_BALA

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if not (0 < self.center_x < ANCHO and 0 < self.center_y < ALTO):
            self.kill()


# =====================================================
# JUGADOR
# =====================================================
class Jugador(arcade.Sprite):
    def __init__(self):
        super().__init__("sprites/abajo.png", 1)
        self.center_x = ANCHO//2
        self.center_y = ALTO//2

        self.vida = 100
        self.balas = 10
        self.dano = 25
        self.monedas = 0

        self.texturas = {
            "arriba": arcade.load_texture("sprites/arriba.png"),
            "abajo": arcade.load_texture("sprites/abajo.png"),
            "izquierda": arcade.load_texture("sprites/izquierda.png"),
            "derecha": arcade.load_texture("sprites/derecha.png"),
        }

    def mover(self, teclas):
        self.change_x = 0
        self.change_y = 0

        if teclas.get(arcade.key.W):
            self.change_y = VELOCIDAD_JUGADOR
            self.texture = self.texturas["arriba"]
        if teclas.get(arcade.key.S):
            self.change_y = -VELOCIDAD_JUGADOR
            self.texture = self.texturas["abajo"]

        if teclas.get(arcade.key.A):
            self.change_x = -VELOCIDAD_JUGADOR
            self.texture = self.texturas["izquierda"]
        if teclas.get(arcade.key.D):
            self.change_x = VELOCIDAD_JUGADOR
            self.texture = self.texturas["derecha"]

        self.center_x += self.change_x
        self.center_y += self.change_y

        self.center_x = max(20, min(ANCHO-20, self.center_x))
        self.center_y = max(20, min(ALTO-20, self.center_y))


# =====================================================
# GAME OVER
# =====================================================
class GameOverView(arcade.View):
    def __init__(self, juego):
        super().__init__()
        self.juego = juego

        self.record = self.cargar_record(juego.puntos)
        self.guardar_record()

    def cargar_record(self, puntos):
        if os.path.exists(RECORD_FILE):
            try:
                return max(int(open(RECORD_FILE).read()), puntos)
            except:
                return puntos
        return puntos

    def guardar_record(self):
        open(RECORD_FILE, "w").write(str(self.record))

    def on_draw(self):
        self.clear()
        arcade.draw_text("GAME OVER", 260, 600, arcade.color.RED, 50)
        arcade.draw_text(f"Puntos: {self.juego.puntos}", 260, 500, arcade.color.WHITE, 25)
        arcade.draw_text(f"Récord: {self.record}", 260, 460, arcade.color.YELLOW, 25)
        arcade.draw_text("ENTER para regresar al menú", 200, 350, arcade.color.WHITE, 20)
        
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ENTER:
            self.window.show_view(MenuView())


# =====================================================
# ENEMIGO
# =====================================================
class Enemigo(arcade.Sprite):
    def __init__(self, tipo, mult=1.0):
        stats = ESTADISTICAS_ENEMIGOS[tipo]
        super().__init__(stats["sprite"], 1)

        self.tipo = tipo
        self.vida = int(stats["vida"] * mult)
        self.velocidad = stats["velocidad"] * mult
        self.dano = stats["dano"]
        self.xp = stats["xp"]

        self.center_x = random.randint(40, ANCHO-40)
        self.center_y = random.randint(40, ALTO-40)

        self.change_x = random.choice([-1, 1]) * self.velocidad
        self.change_y = random.choice([-1, 1]) * self.velocidad

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if not (20 < self.center_x < ANCHO-20):
            self.change_x *= -1
        if not (20 < self.center_y < ALTO-20):
            self.change_y *= -1


# =====================================================
# JUEGO PRINCIPAL
# =====================================================
class Juego(arcade.View):
    def __init__(self):
        super().__init__()

        self.jugador = Jugador()
        self.enemigos = arcade.SpriteList()
        self.balas = arcade.SpriteList()
        self.teclas = {}
        self.fondo = arcade.load_texture("fondos/escenario.png")

        self.puntos = 0

        # Crear WaveManager
        self.wave_manager = WaveManager()

        # Primera oleada automática
        self.manejar_oleadas()

    def spawn_enemigo(self, tipo, mult):
        enemigo = Enemigo(tipo, mult)
        self.enemigos.append(enemigo)

    def manejar_oleadas(self):
        if self.wave_manager.enemigos_vivos == 0:
            datos = self.wave_manager.obtener_oleada()
            cantidad = datos["cantidad"]
            tipos = datos["tipos"]

            mult = 1 + (self.wave_manager.oleada_actual * 0.05)

            for _ in range(cantidad):
                tipo = random.choice(tipos)
                self.spawn_enemigo(tipo, mult)

            self.wave_manager.enemigos_vivos = cantidad
            self.wave_manager.oleada_actual += 1

    # =====================================================
    # EVENTOS
    # =====================================================
    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(ANCHO//2, ALTO//2, ANCHO, ALTO, self.fondo)
        self.jugador.draw()
        self.enemigos.draw()
        self.balas.draw()

        arcade.draw_text(f"Vida: {self.jugador.vida}", 10, ALTO-30, arcade.color.WHITE, 14)
        arcade.draw_text(f"Oro: {self.jugador.monedas}", 10, ALTO-60, arcade.color.YELLOW, 16)
        arcade.draw_text(f"XP: {self.puntos}", 10, ALTO-150, arcade.color.LIGHT_GREEN, 16)
        arcade.draw_text(f"Oleada: {self.wave_manager.oleada_actual-1}", 10, ALTO-90, arcade.color.GREEN, 14)
        arcade.draw_text(f"Balas: {self.jugador.balas}", 10, ALTO-120, arcade.color.LIGHT_BLUE, 14)


    def on_key_press(self, symbol, modifiers):
        self.teclas[symbol] = True

        # Abrir tienda
        if symbol == arcade.key.M:
            self.window.show_view(TiendaView(self))



    def on_key_release(self, symbol, modifiers):
        self.teclas[symbol] = False

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_RIGHT and self.jugador.balas > 0:
            bala = Bala(self.jugador.center_x, self.jugador.center_y, x, y, self.jugador.dano)
            self.balas.append(bala)
            self.jugador.balas -= 1

    # =====================================================
    # UPDATE
    # =====================================================
    def on_update(self, delta_time):
        self.jugador.mover(self.teclas)
        self.enemigos.update()
        self.balas.update()

        # Balas → enemigos
        for bala in self.balas:
            impactados = arcade.check_for_collision_with_list(bala, self.enemigos)
            if impactados:
                bala.kill()
                for enemigo in impactados:
                    enemigo.vida -= bala.dano
                    if enemigo.vida <= 0:
                        enemigo.kill()
                        # XP
                        self.puntos += enemigo.xp
                        # ORO
                        self.jugador.monedas += ESTADISTICAS_ENEMIGOS[enemigo.tipo]["oro"]

        # Enemigos → jugador
        for enemigo in arcade.check_for_collision_with_list(self.jugador, self.enemigos):
            self.jugador.vida -= enemigo.dano * 0.2

        # Oleadas
        self.wave_manager.enemigos_vivos = len(self.enemigos)
        self.manejar_oleadas()

        # Muerte
        if self.jugador.vida <= 0:
            self.window.show_view(GameOverView(self))

# =====================================================
# TIENDA
# =====================================================
class TiendaView(arcade.View):
    def __init__(self, juego):
        super().__init__()
        self.juego = juego
        self.jugador = juego.jugador

        self.opciones = [
            ("Recargar balas (+5)", 5),
            ("Curar (+20 vida)", 10),
            ("Aumentar daño (+5)", 20)
        ]

    def on_draw(self):
        self.clear()
        arcade.draw_text("TIENDA", 300, 600, arcade.color.YELLOW, 50)

        arcade.draw_text(f"oro: {self.jugador.monedas}",
                         260, 540, arcade.color.WHITE, 20)

        y = 450
        for i, (nombre, precio) in enumerate(self.opciones):
            arcade.draw_text(f"{i+1}. {nombre} — {precio} puntos", 150, y, arcade.color.WHITE, 20)
            y -= 60

        arcade.draw_text("Presiona 1, 2 o 3 para comprar", 200, 200, arcade.color.GRAY, 18)
        arcade.draw_text("Presiona ESC para volver", 230, 160, arcade.color.GRAY, 18)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.juego)

        # Compra con 1, 2 o 3
        if key == arcade.key.KEY_1:
            self.comprar(0)
        if key == arcade.key.KEY_2:
            self.comprar(1)
        if key == arcade.key.KEY_3:
            self.comprar(2)

    def comprar(self, index):
        nombre, precio = self.opciones[index]

        # Ahora las compras usan ORO
        if self.juego.jugador.monedas >= precio:
            self.juego.jugador.monedas -= precio

            if index == 0:     # balas
                self.juego.jugador.balas += 5
            elif index == 1:   # curar
                self.juego.jugador.vida = min(100, self.juego.jugador.vida + 20)
            elif index == 2:   # daño
                self.juego.jugador.dano += 5
        else:
            print("No tienes suficiente oro.")



# =====================================================
# EJECUTAR
# =====================================================
if __name__ == "__main__":
    ventana = arcade.Window(ANCHO, ALTO, TITULO)
    ventana.show_view(MenuView())
    arcade.run()
