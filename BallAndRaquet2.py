import pygame as pg
import sys
import random

ANCHO = 800
ALTO = 400



#los atributos deben ser en ingles porque luego al llamarlas en las librerias si no es en ingles se lia 

class Bola(pg.sprite.Sprite): #hereda de la clase sprite
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self) #otra manera es super().__init__()
        self.image = pg.image.load('./imagenes/ball1.png').convert_alpha() #eso ultimo es para aplicar transparencia
                                                                            #te devuleve un surface una calcamonia
        self.rect = self.image.get_rect(center = (x, y)) #nos da un rectangulo de 30x30, porque es la dimencion de la self.image

        self.vx = random.randint(5,10) * random.choica ([-1,1])
        self.vy = random.randint(5,10) * random.choica ([-1,1])

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.left <= 0 or self.rect.rigth >= ANCHO:
            self.vx *= -1
        if self.rect.top <= 0 or self.rect.bottonm>= ALTO:
            self.vt *= -1

        
class Game():
    def __init__ (self):
        self.pantalla = pg.display.set_mode((ANCHO,ALTO))
        self.vidas = 3
        self.puntacion = 0

        self.bola = Bola (ANCHO//2, ALTO//2)




        
