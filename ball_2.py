import pygame as pg
import sys
from random import randint, choice

ANCHO = 800
ALTO = 600
FPS = 60

class Marcador(pg.sprite.Sprite):
    def __init__(self, x, y ,fontsize = 25, color = (255,255,255)):
        super().__init__() #porque viene del nombre super clase
        self.fuente = pg.font.SysFont('Arial', fontsize)
        self.text = 0
        self.color = color
        self.image = self.fuente.render(str(self.text), True, self.color) #se llama imagen para que el draw lo entienda del render
        self.rect = self.image.get_rect(topleft = (x, y)) #lo referencio segun donde quiero poner la esquina superior izquierda del rectangulo


    def update(self,dt): #necesario en los sprite para que se actualiza lo que te da el grupo
        self.image = self.fuente.render(str(self.text), True, self.color)

class Bola(pg.sprite.Sprite): #va a heredar de la lcase sprite sus funcionalidades y atributos
    def __init__(self, x, y):
        #pg.sprite.Sprite.__init__(self) - ESTA SERIA UNA FORMA
        super().__init__()                  #ESTA ES LA OTRA FORMA
        self.image = pg.image.load('./imagenes/ball1.png').convert_alpha()  #creo que es importante el nombre del atributo para que luego lo llame sprite
        self.rect = self.image.get_rect(center = (x,y))                     #aqui ya no me tengo que preocupar de las dimensiones, lo tiene el propio objeto
                                                                            #lo de arriba es una instancia de la clase rectangulo


        self.estoyViva = True


        self.vx = randint(5,10)*choice([-1, 1])
        self.vy = randint(5,10)*choice([-1, 1])

    def prueba_colision(self, grupo):
        candidatos = pg.sprite.spritecollide(self, grupo, False) #false para no borrar la raqueta aunque la toque
        if len(candidatos)>0 :
            self.vy *=-1

    def update (self,dt):
        if self.estoyViva:
            self.rect.x += self.vx
            self.rect.y += self.vy

            if self.rect.left <= 0 or self.rect.right >= ANCHO:
                self.vx *= -1

            if self.rect.top <= 0 or self.rect.bottom >= ALTO: #esto son las distintas posiciones del objeto rectangulo
                self.vy *= -1

            if self.rect.bottom >= ALTO:
                self.estoyViva = False
        else:
            self.rect.center = (ANCHO//2, ALTO//2)
            self.vx = randint(5,10)*choice([-1, 1])
            self.vy = randint(5,10)*choice([-1, 1])
            self.estoyViva = True

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
        self.TodoGroup.add(self.cuentaSegundos)

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
            self.bola.prueba_colision(self.grupoJugador)

            self.TodoGroup.update(dt)

            if not self.bola.estoyViva:
                self.vidas -= 1
                print(self.vidas)

            self.pantalla.fill((0,0,0))
            
            self.TodoGroup.draw(self.pantalla)


            pg.display.flip()

if __name__ == '__main__':
    pg.init()
    pg.font.init()
    game = Game()
    game.bucle_principal()

