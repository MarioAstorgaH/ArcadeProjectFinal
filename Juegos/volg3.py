import arcade
import random
import math

# --- Constantes ---
ALTO, ANCHO = 800, 800
TITULO = "Juego con Enemigos, Disparo, Loot y Tienda"

VELOCIDAD_JUGADOR = 4
VELOCIDAD_ENEMIGO = 2
VELOCIDAD_BALA = 15
FONDO_PATH = "fondos/escenario.png"


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.fondo = arcade.load_texture("fondos/menu.jpeg")

        # BOTONES (x, y, ancho, alto) → se guardan como TUPLAS
        self.boton_jugar = (ANCHO // 2, 350, 250, 60)
        self.boton_salir = (ANCHO // 2, 250, 250, 60)


    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(ANCHO // 2, ALTO // 2, ANCHO, ALTO, self.fondo)

        arcade.draw_text("MI JUEGO", ANCHO // 2 - 130, 600, arcade.color.WHITE, 40)

        # ------------ BOTÓN JUGAR ------------
        x, y, w, h = self.boton_jugar
        arcade.draw_rectangle_filled(x, y, w, h, arcade.color.DARK_GREEN)
        arcade.draw_text("JUGAR", x - 60, y - 15, arcade.color.WHITE, 20)

        # ------------ BOTÓN SALIR ------------
        x, y, w, h = self.boton_salir
        arcade.draw_rectangle_filled(x, y, w, h, arcade.color.DARK_RED)
        arcade.draw_text("SALIR", x - 50, y - 15, arcade.color.WHITE, 20)


    def on_mouse_press(self, x, y, button, modifiers):

        # ------ Click en botón JUGAR ------
        bx, by, bw, bh = self.boton_jugar
        if abs(x - bx) < bw / 2 and abs(y - by) < bh / 2:
            juego = Juego()
            self.window.show_view(juego)
            return

        # ------ Click en botón SALIR ------
        bx, by, bw, bh = self.boton_salir
        if abs(x - bx) < bw / 2 and abs(y - by) < bh / 2:
            arcade.close_window()


# --- Clase Bala ---
class Bala(arcade.Sprite):
    def __init__(self, x, y, objetivo_x, objetivo_y, dano=25):
        super().__init__("proyectiles/bala1.png", 0.1)
        self.center_x = x
        self.center_y = y
        self.dano = dano

        # Dirección hacia el objetivo
        dx = objetivo_x - x
        dy = objetivo_y - y
        angulo = math.atan2(dy, dx)
        self.change_x = math.cos(angulo) * VELOCIDAD_BALA
        self.change_y = math.sin(angulo) * VELOCIDAD_BALA

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Si sale de pantalla, eliminar
        if not (0 < self.center_x < ANCHO and 0 < self.center_y < ALTO):
            self.kill()

# --- Clase Jugador ---
class Jugador(arcade.Sprite):
    def __init__(self):
        super().__init__("sprites/abajo.png", 1)
        self.center_x = ANCHO // 2
        self.center_y = ALTO // 2
        self.vida = 100
        self.balas = 10
        self.direccion = "abajo"
        self.monedas = 0
        self.dano = 25

    def mover(self, teclas):
        self.change_x = 0
        self.change_y = 0

        if teclas.get(arcade.key.W, False):
            self.change_y = VELOCIDAD_JUGADOR
            self.texture = arcade.load_texture("sprites/arriba.png")
        elif teclas.get(arcade.key.S, False):
            self.change_y = -VELOCIDAD_JUGADOR
            self.texture = arcade.load_texture("sprites/abajo.png")

        if teclas.get(arcade.key.A, False):
            self.change_x = -VELOCIDAD_JUGADOR
            self.texture = arcade.load_texture("sprites/izquierda.png")
        elif teclas.get(arcade.key.D, False):
            self.change_x = VELOCIDAD_JUGADOR
            self.texture = arcade.load_texture("sprites/derecha.png")

        self.center_x += self.change_x
        self.center_y += self.change_y

        # Limitar dentro de la pantalla
        self.center_x = max(20, min(ANCHO - 20, self.center_x))
        self.center_y = max(20, min(ALTO - 20, self.center_y))


# --- Clase Enemigo ---
class Enemigo(arcade.Sprite):
    def __init__(self, imagen="enemigos/enemigo.png", x=None, y=None, vida=50, velocidad=2, loot=None):
        super().__init__(imagen, 1)
        self.vida = vida
        self.velocidad = velocidad
        self.loot = loot or [("moneda", 1)]

        self.center_x = x if x else random.randint(50, ANCHO - 50)
        self.center_y = y if y else random.randint(50, ALTO - 50)
        self.change_x = random.choice([-1, 1]) * velocidad
        self.change_y = random.choice([-1, 1]) * velocidad

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Rebote en bordes
        if self.center_x < 20 or self.center_x > ANCHO - 20:
            self.change_x *= -1
        if self.center_y < 20 or self.center_y > ALTO - 20:
            self.change_y *= -1

    def morir(self):
        print("💀 Enemigo muerto")
        return self.loot
# --- Clase Principal ---
class Juego(arcade.View):
    def __init__(self):
        super().__init__()
        self.jugador = Jugador()
        self.enemigos = arcade.SpriteList()
        self.balas = arcade.SpriteList()
        self.teclas = {}
        self.juego_pausado = False
        self.fondo = arcade.load_texture("fondos/escenario.png")

        # enemigos iniciales
        for _ in range(5):
            self.spawn_enemigo("basico", (50, 300, 100, 400))

        for _ in range(3):
            self.spawn_enemigo("rapido", (400, 700, 200, 600))

    def controlar_spawn(self):
        """Mantiene cierta cantidad de enemigos en el mapa"""
        max_enemigos = 10  # <<-- AQUÍ CONTROLAS EL MÁXIMO DE ENEMIGOS
        if len(self.enemigos) < max_enemigos:
            # Crea enemigos aleatorios para rellenar
            if random.random() < 0.5:
                self.spawn_enemigo("basico", (50, 300, 100, 400))
            else:
                self.spawn_enemigo("rapido", (400, 700, 200, 600))

    # ---------------------- SISTEMA DE SPAWN ----------------------
    def spawn_enemigo(self, tipo, area):
        """Crea enemigos de distintos tipos según el parámetro"""
        x = random.randint(area[0], area[1])
        y = random.randint(area[2], area[3])

        if tipo == "basico":
            enemigo = Enemigo(
                imagen="enemigos/enemigo.png",
                x=x, y=y,
                vida=60,
                velocidad=2,
                loot=[("moneda", random.randint(10, 15))]
            )
        elif tipo == "rapido":
            enemigo = Enemigo(
                imagen="enemigos/Medusa.png",
                x=x, y=y,
                vida=40,
                velocidad=4,
                loot=[("moneda", random.randint(12, 20))]
            )
        else:
            return

        self.enemigos.append(enemigo)
    # ---------------------- menu visual ----------------------
    def on_draw(self):
        self.clear()
        arcade.start_render()
        arcade.draw_texture_rectangle(ANCHO // 2, ALTO // 2, ANCHO, ALTO, self.fondo)
        self.jugador.draw()
        self.enemigos.draw()
        self.balas.draw()

        # HUD
        arcade.draw_text(f"Vida: {self.jugador.vida}", 10, ALTO - 30, arcade.color.WHITE, 14)
        arcade.draw_text(f"Balas: {self.jugador.balas}", 10, ALTO - 60, arcade.color.YELLOW, 14)
        arcade.draw_text(f"Monedas: {self.jugador.monedas}", 10, ALTO - 90, arcade.color.LIGHT_GREEN, 14)

        if self.juego_pausado:
            arcade.draw_rectangle_filled(ANCHO // 2 ,ALTO // 2, 700, 500, (0, 0, 0, 200))
            arcade.draw_text("MENÚ DE TIENDA", ANCHO // 2 - 100, ALTO // 2 + 80, arcade.color.WHITE, 20)
            arcade.draw_text("Presiona [X] para comprar 10 balas por 10 monedas", ANCHO // 2 - 130, ALTO // 2, arcade.color.YELLOW, 14)
            arcade.draw_text("Presiona [U] para aumentar tu daño por 50 monedas", ANCHO // 2 - 130, ALTO // 2 + 30, arcade.color.YELLOW, 14)
            arcade.draw_text("Presiona [Z] para comprar 20 balas por 18 monedas", ANCHO // 2 - 130, ALTO // 2 + 15, arcade.color.YELLOW, 14)
            arcade.draw_text("Presiona [M] para cerrar", ANCHO // 2 - 80, ALTO // 2 - 60, arcade.color.WHITE, 14)
        
    def on_key_press(self, symbol, modifiers):
        self.teclas[symbol] = True
    # ---------------------- tienda interna ----------------------
        if symbol == arcade.key.M:
            self.juego_pausado = not self.juego_pausado

        if self.juego_pausado and symbol == arcade.key.E:
            costo = 50
            if self.jugador.vida >= 100:
                print("⚠️ Vida ya está al máximo.")
                return
            if self.jugador.monedas >= costo:
                self.jugador.monedas -= costo
                self.jugador.vida += 100 -self.jugador.vida

                print(f"💥 Compraste vida por {costo} monedas.")

        if self.juego_pausado and symbol == arcade.key.X:
            costo = 10
            if self.jugador.monedas >= costo:
                self.jugador.monedas -= costo
                self.jugador.balas += 10
                print(f"💥 Compraste 10 balas por {costo} monedas.")
            else:
                print("⚠️ No tienes suficiente dinero.")

        if self.juego_pausado and symbol == arcade.key.U:
            costo = 50
            if self.jugador.monedas >= costo:
                self.jugador.dano += 10
                self.jugador.monedas -= costo
                print("🔺 Daño aumentado a", self.jugador.dano)


        if self.juego_pausado and symbol == arcade.key.Z:
            costo = 18
            if self.jugador.monedas >= costo:
                self.jugador.monedas -= costo
                self.jugador.balas += 20
                print("💥 Compraste 20 balas. Total:", self.jugador.balas)
            else:
                print("⚠️ No tienes suficiente dinero.")

    def on_key_release(self, symbol, modifiers):
        self.teclas[symbol] = False

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.juego_pausado and button == arcade.MOUSE_BUTTON_RIGHT:
            if self.jugador.balas > 0:
                bala = Bala(self.jugador.center_x, self.jugador.center_y, x, y, dano=self.jugador.dano )
                self.balas.append(bala)
                self.jugador.balas -= 1
            else:
                print("⚠️ No tienes balas. Abre el menú con [M] para comprar.")
        bala = Bala(self.jugador.center_x, self.jugador.center_y, x, y, dano=self.jugador.dano)

    def on_update(self, delta_time):
        if self.juego_pausado:
            return

        self.jugador.mover(self.teclas)
        self.enemigos.update()
        self.balas.update()

        # --- Colisiones bala - enemigo ---
        for bala in self.balas:
            enemigos_golpeados = arcade.check_for_collision_with_list(bala, self.enemigos)
            if enemigos_golpeados:
                bala.kill()
                for enemigo in enemigos_golpeados:
                    enemigo.vida -= bala.dano
                    if enemigo.vida <= 0:
                        loot = enemigo.morir()
                        for item, cantidad in loot:
                            if item == "moneda":
                                self.jugador.monedas += cantidad
                        enemigo.kill()

        # --- Colisión jugador - enemigo ---
        for enemigo in arcade.check_for_collision_with_list(self.jugador, self.enemigos):
            self.jugador.vida -= 0.5

        self.controlar_spawn()

# --- Ejecutar ---
if __name__ == "__main__":
    ventana = arcade.Window(ANCHO, ALTO, TITULO)

    # Mostrar menú de inicio
    menu = MenuView()
    ventana.show_view(menu)

    arcade.run()