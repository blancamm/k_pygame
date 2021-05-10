import pygame as pg
import sys
from random import randint, choice
from enum import Enum

ANCHO = 800
ALTO = 600
FPS = 60

'''

UN TIPO DE MARCADOR

class Marcador(pg.sprite.Sprite):

    class Justificado(Enum):
        izquierda = 'I'
        derecha = 'D'
        centrado = 'C'
    
    def __init__(self, x, y , justificado = None, fontsize = 25, color = (255,255,255)):
        super().__init__() #porque viene del nombre super clase
        self.fuente = pg.font.SysFont('Arial', fontsize)
        self.text = 0
        self.color = color
        self.x = x
        self.y = y

        if not justificado:
            self.justificado= Marcador.Justificado.izquierda
        else:
            self.justificado = justificado

        self.image = self.fuente.render(str(self.text), True, self.color) #se llama imagen para que el draw lo entienda del render
        
        if self.justificado == Marcador.Justificado.izquierda:
            self.rect = self.image.get_rect(topleft = (x, y)) #lo referencio segun donde quiero poner la esquina superior izquierda del rectangulo
        elif self.justificado == Marcador.Justificado.derecha:
            self.rect = self.image.get_rect(topright =(x,y))
        else:
            self.rect = self.image.get_rect(midtop = (x,y))

    def update(self,dt): #necesario en los sprite para que se actualiza lo que te da el grupo
        self.image = self.fuente.render(str(self.text), True, self.color)
        if self.justificado == Marcador.Justificado.izquierda:
            self.rect = self.image.get_rect(topleft = (self.x, self.y)) #lo referencio segun donde quiero poner la esquina superior izquierda del rectangulo
        elif self.justificado == Marcador.Justificado.derecha:
            self.rect = self.image.get_rect(topright =(self.x, self.y))
        else:
            self.rect = self.image.get_rect(midtop = (self.x, self.y))

'''
class Marcador(pg.sprite.Sprite):
    
    def __init__(self, x, y , justificado = 'topleft', fontsize = 25, color = (255,255,255)):
        super().__init__() #porque viene del nombre super clase
        self.fuente = pg.font.SysFont('Arial', fontsize)
        self.text = 0
        self.color = color
        self.x = x
        self.y = y
        self.justificado = justificado
        self.image = self.fuente.render(str(self.text), True, self.color) #se llama imagen para que el draw lo entienda del render
        
       
       
    def update(self, dt):
        self.image = self.fuente.render(str(self.text), True, self.color) #se llama imagen para que el draw lo entienda del render
        #así cambio las posicion de distintas esquinas, segun lo que me interese topleft, o top rigth
        d = {self.justificado: (self.x, self.y)}
        self.rect = self.image.get_rect(**d)
        


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

        self.vx = randint(5,10)*choice([-1, 1])
        self.vy = randint(5,10)*choice([-1, 1])

    def cargaImagenes(self):
        imagenes = []
        for fichero in self.disfraces:
            imagenes.append(pg.image.load('./imagenes/{}'.format(fichero)))
        return imagenes

    def prueba_colision(self, grupo):
        candidatos = pg.sprite.spritecollide(self, grupo, False) #false para no borrar la raqueta aunque la toque
        if len(candidatos)>0 :
            self.vy *=-1

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


class Game():
    def __init__(self):
        self.pantalla = pg.display.set_mode((ANCHO, ALTO)) 
        self.vidas = 3
    

        #SE CREA ESTOS GRUPOS PARA PODER HACER LA COLISION ENTRE ELLOS

        self.grupoJugador = pg.sprite.Group()
        #self.grupoPelota = pg.sprite.Group() DE MOMENTO NO ES NECESARIO
        self.grupoLadrillos = pg.sprite.Group()
        
        self.TodoGroup = pg.sprite.Group ()

        self.cuentaSegundos = Marcador(10, 10)
        self.cuentaVidas = Marcador(790, 10, 'topright')
        self.TodoGroup.add(self.cuentaSegundos, self.cuentaVidas) #se puede añadir con comas

        self.bola= Bola (randint(0, ANCHO), randint(0, ALTO))
        self.TodoGroup.add(self.bola) 

        self.raqueta = Raqueta(x = ANCHO//2, y=ALTO-30)
        self.grupoJugador.add(self.raqueta)
        self.TodoGroup.add(self.raqueta)


      
    def bucle_principal(self):
        game_Over = False #es variable, no es atributo. No tiene sentido fuera de este metodo por eso solo es variable y no atributo
        reloj= pg.time.Clock()
        contandor_milisegundos = 0
        segundero = 0
        while not game_Over and self.vidas > 0:
            dt = reloj.tick(FPS)
            contandor_milisegundos += dt

            if contandor_milisegundos >= 1000: # es decir, un segundo
                segundero += 1
                contandor_milisegundos = 0 #vuelvo a inicializarlo a 0 para poder volver a contar otro segundo

            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    game_Over= True

            self.cuentaSegundos.text = segundero
            self.cuentaVidas.text = self.vidas
            self.bola.prueba_colision(self.grupoJugador)

            self.TodoGroup.update(dt)

            if self.bola.estado == Bola.Estado.muerta:
                self.vidas -= 1

            self.pantalla.fill((0,0,0))
            
            self.TodoGroup.draw(self.pantalla)


            pg.display.flip()

if __name__ == '__main__':
    pg.init()
    pg.font.init()
    game = Game()
    game.bucle_principal()

