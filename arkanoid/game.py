from arkanoid import ALTO, ANCHO, levels, FPS
from arkanoid.escenes import Portada, Game
import pygame as pg

pg.init()
pg.font.init()

class Arkanoid():
    def __init__(self):
        pantalla = pg.display.set_mode ((ANCHO, ALTO))
        self.escenas = [Portada(pantalla), Game(pantalla)]
        self.escena_activa = 0

    def start (self):
        while True:
            la_escena = self.escenas[self.escena_activa]
            la_escena.reset()
            la_escena.bucle_principal()
            self.escena_activa += 1
            if self.escena_activa >= len(self.escenas):
                self.escena_activa = 0

                #self.escena_activa = (self.escena_activa +1) % len(self.escena) TE DA EL RESTO. ES LO MISMO QUE LAS 3 LINEAS ANTERIORES. VARIA ENTRE 0 Y 1 EL VALOR

