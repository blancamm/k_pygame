import pygame
import sys
import random #podriamos poner fom random import randint y asi no tenemos que poner random.randint y solo randint

ROJO = (255, 0 ,0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
NEGRO = (0,0,0)
ANCHO = 800
ALTURA = 600

pygame.init()

pantalla = pygame.display.set_mode((ANCHO,ALTURA))

gameOver= False

class Bola():
    def __init__(self, x, y, vx=5, vy=5, color= (255, 255, 255), radio = 10): #ponemos algunos por defecto
        self.x = x
        self.y= y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.radio = radio

    def actualizar(self):
        self.x += self.vx
        self.y += self.vy 

        if self.x <= 0 or self.x >= 800:
            self.vx = -self.vx

        if self.y <= 0 or self.y >= 600:
            self.vy = -self.vy

    def dibujar(self, lienzo):
        pygame.draw.circle(lienzo, self.color, (self.x, self.y), self.radio)

bolas = []
for _ in range (10):
    bola = Bola(random.randint(0, ANCHO), 
                random.randint(0, ALTURA),
                random.randint(5,10), 
                random.randint(5,10), 
                (random.randint(0,255), random.randint(0,255), random.randint(0,255)))
    bolas.append(bola)


reloj = pygame.time.Clock()

while not gameOver:
    reloj.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            gameOver = True

    #modificacion de estados

    for bola in bolas:
        bola.actualizar()

    #gestion de pantalla
    pantalla.fill (NEGRO)
    for bola in bolas:
        bola.dibujar(pantalla)
        


    pygame.display.flip()
    
pygame.quit()
sys.exit()
