import pygame as pg
import sys
from random import randint, choice

ANCHO = 800
ALTO = 600
FPS = 60

class Marcador():
    def __init__(self, x, y ,fontsize = 25, color = (255,255,255)):
        self.fuente = pg.font.SysFont('Arial', fontsize)
        self.color = color
        self.x = x
        self.y = y 

    def dibuja(self, text, lienzo):
        image = self.fuente.render(str(text), True, self.color) #te devuelve una surface con forma de rectangulo
        lienzo.blit(image, (self.x, self.y))

class Bola(pg.sprite.Sprite): #va a heredar de la lcase sprite sus funcionalidades y atributos
    def __init__(self, x, y):
        #pg.sprite.Sprite.__init__(self) - ESTA SERIA UNA FORMA
        super().__init__() #ESTA ES LA OTRA FORMA
        self.image = pg.image.load('./imagenes/ball1.png').convert_alpha() #creo que es importante el nombre del atributo para que luego lo llame sprite
        self.rect = self.image.get_rect(center = (x,y))#aqui ya no me tengo que preocupar de las dimensiones, lo tiene el propio objeto
        #lo de arriba es una instancia de la clase rectangulo


        self.vx = randint(5,10)*choice([-1, 1])
        self.vy = randint(5,10)*choice([-1, 1])

    def update (self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.left <= 0 or self.rect.right >= ANCHO:
            self.vx *= -1

        if self.rect.top <= 0 or self.rect.bottom >= ALTO: #esto son las distintas posiciones del objeto rectangulo
            self.vy *= -1

class Game():
    def __init__(self):
        self.pantalla = pg.display.set_mode((ANCHO, ALTO)) 
        self.vidas = 3
        self.botes = 0
        self.cuentaGolpes = Marcador(10, 10)


        self.ballGroup = pg.sprite.Group ()
        for i in range(randint(1,20)):
           bola= Bola (randint(0, ANCHO), randint(0, ALTO))
           self.ballGroup.add(bola) 

      
    def bucle_principal(self):
        game_Over = False #es variable, no es atributo. No tiene sentido fuera de este metodo por eso solo es variable y no atributo
        reloj= pg.time.Clock()
        while not game_Over:
            reloj.tick(FPS)

            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    game_Over= True

            self.ballGroup.update()

            self.pantalla.fill((0,0,0))
            self.cuentaGolpes.dibuja('HOLA', self.pantalla)
            self.ballGroup.draw(self.pantalla)


            pg.display.flip()

if __name__ == '__main__':
    pg.init()
    pg.font.init()
    game = Game()
    game.bucle_principal()

