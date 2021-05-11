from arkanoid import ANCHO, ALTO, FPS, levels
import pygame as pg
from random import randint, choice
from enum import Enum


class Marcador(pg.sprite.Sprite):

    plantilla = '{}'
    
    def __init__(self, x, y , justificado = 'topleft', fontsize = 25, color = (255,255,255)):
        super().__init__() #porque viene del nombre super clase
        self.fuente = pg.font.SysFont('Arial', fontsize)
        self.text = 0
        self.color = color
        self.x = x
        self.y = y
        self.justificado = justificado
        self.image = None
        
       
       
    def update(self, dt):
        self.image = self.fuente.render(self.plantilla.format(self.text), True, self.color) #se llama imagen para que el draw lo entienda del render
        #así cambio las posicion de distintas esquinas, segun lo que me interese topleft, o top rigth
        d = {self.justificado: (self.x, self.y)}
        self.rect = self.image.get_rect(**d)

class CuentaVidas(Marcador):
    plantilla = 'Vidas: {}'
    
class Ladrillo(pg.sprite.Sprite):
    disfraces = ['greenTile.png', 'redTile.png', 'redTileBreak.png']

    def __init__(self, x, y, esDuro = False):
        super().__init__()
        self.imagenes = self.cargaImagenes()
        self.esDuro = esDuro
        self.imagen_actual = 1 if self.esDuro else 0 #si es true la iamgen es 1 si es false que sea duro es la imagen 0, es decir, el ladrillo verde
        self.image = self.imagenes[self.imagen_actual]
        self.rect = self.image.get_rect(topleft= (x,y))
        self.numGolpes = 0

    def cargaImagenes(self):
        imagenes = []
        for fichero in self.disfraces:
            imagenes.append(pg.image.load('./imagenes/{}'.format(fichero)))
        return imagenes

    def update(self,dt):
        if self.esDuro and self.numGolpes == 1:
            self.imagen_actual = 2
            self.image = self.imagenes[self.imagen_actual]

    def desaparece(self):
        self.numGolpes +=1
        return self.numGolpes > 0 and not self.esDuro or self.numGolpes >1 and self.esDuro

        '''
        ES DECIR:

        if (self.numGolpes > 0 and not self.esDuro) or (self.numGolpes >1 and self.esDuro)
            return True
        else:
            return False
        '''

class Bola(pg.sprite.Sprite): #va a heredar de la lcase sprite sus funcionalidades y atributos
    
    disfraces = ['ball1.png','ball2.png', 'ball3.png', 'ball4.png', 'ball5.png']

    class Estado (Enum):
        viva = 0
        agoniazando = 1
        muerta = 2

    def __init__(self, x, y):
        #pg.sprite.Sprite.__init__(self) - ESTA SERIA UNA FORMA
        super().__init__()                #ESTA ES LA OTRA FORMA

        self.imagenes = self.cargaImagenes()
        self.imagen_actual = 0
        self.image = self.imagenes[self.imagen_actual]

        self.milisegundos_acumulados = 0
        self.milisegundos_para_cambiar = 1000// FPS *10

        self.rect = self.image.get_rect(center = (x,y))                     #aqui ya no me tengo que preocupar de las dimensiones, lo tiene el propio objeto
                                                                            #lo de arriba es una instancia de la clase rectangulo

        self.estado = Bola.Estado.viva #es un valor

        self.vx = randint(5,8)*choice([-1, 1])
        self.vy = randint(5,8)*choice([-1, 1])

    def cargaImagenes(self):
        imagenes = []
        for fichero in self.disfraces:
            imagenes.append(pg.image.load('./imagenes/{}'.format(fichero)))
        return imagenes

    def prueba_colision(self, grupo):
        candidatos = pg.sprite.spritecollide(self, grupo, False) #false para no borrar la raqueta aunque la toque
        if len(candidatos)>0 :
            self.vy *=-1
        return candidatos

    def update (self,dt):
        if self.estado == Bola.Estado.viva:

            self.rect.x += self.vx
            self.rect.y += self.vy

            if self.rect.left <= 0 or self.rect.right >= ANCHO:
                self.vx *= -1

            if self.rect.top <= 0 or self.rect.bottom >= ALTO: #esto son las distintas posiciones del objeto rectangulo
                self.vy *= -1

            if self.rect.bottom >= ALTO:
                self.estado = Bola.Estado.agoniazando #porque queremos que salga la animacion
                self.rect.bottom = ALTO #PARA QUE REBOTE

        elif self.estado == Bola.Estado.agoniazando:
            self.milisegundos_acumulados += dt
            if self.milisegundos_acumulados >= self.milisegundos_para_cambiar:
                self.imagen_actual += 1
                self.milisegundos_acumulados = 0
                if self.imagen_actual >= len(self.disfraces):
                    self.estado = Bola.Estado.muerta
                    self.imagen_actual = 0
                self.image = self.imagenes[self.imagen_actual]

        else:
            self.rect.center = (ANCHO//2, ALTO//2)
            self.vx = randint(5,10)*choice([-1, 1])
            self.vy = randint(5,10)*choice([-1, 1])
            self.estado = Bola.Estado.viva

class Raqueta(pg.sprite.Sprite):
    fotos = ['electric00.png', 'electric01.png', 'electric02.png']

    def __init__(self, x, y, w=100, h = 30):
        super().__init__()
        self.imagenes = self.cargaImagenes()
        self.imagen_actual = 0 #actual como indice
        self.milisegundos_para_cambiar = 1000// FPS *5
        self.milisegundos_acumulados = 0
        self.image = self.imagenes[self.imagen_actual]
        self.rect = self.image.get_rect(centerx = x, bottom = y)
        self.vx = 10

    def cargaImagenes(self):
        imagenes = []
        for fichero in self.fotos:
            imagenes.append(pg.image.load('./imagenes/{}'.format(fichero)))
        return imagenes

    def update(self, dt):
        teclas_Pulsadas = pg.key.get_pressed()
        if teclas_Pulsadas[pg.K_LEFT]:
            self.rect.x -= self.vx
        
        if teclas_Pulsadas[pg.K_RIGHT]:
            self.rect.x += self.vx

        #los topes segun sus geometrias:
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= ANCHO:
            self.rect.right = ANCHO

        self.milisegundos_acumulados += dt
        if self.milisegundos_acumulados >= self.milisegundos_para_cambiar:
            self.imagen_actual += 1
            if self.imagen_actual >= len(self.fotos):
                self.imagen_actual = 0
            self.milisegundos_acumulados = 0
        self.image = self.imagenes[self.imagen_actual]