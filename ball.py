import pygame
import sys
import random #podriamos poner fom random import randint y asi no tenemos que poner random.randint y solo randint

ROJO = (255, 0 ,0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
NEGRO = (0,0,0)
ANCHO = 800
ALTURA = 600

def rebotax(x):
    if x <= 0 or x >= ANCHO:
        return -1  #hay que poner en ambos un menos, porque pasamos de uno a otro(del anterior valor que se ha dado a la variable)
    return 1

def rebotay(y):
    if y <= 0 or y >= ALTURA:
        return -1   
    return 1

pygame.init()

pantalla = pygame.display.set_mode((800,600))

gameOver= False

class Bola():
    def __init__(self, x, y, vx, vy, color):
        self.x = x
        self.y= y
        self.vx = vx
        self.vy = vy
        self.color = color

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
        bola.x += bola.vx
        bola.y += bola.vy

        bola.vy *= rebotay(bola.y)
        bola.vx *= rebotay(bola.x)

    #gestion de pantalla
    pantalla.fill (NEGRO)
    for bola in bolas:
        pygame.draw.circle(pantalla, bola.color, (bola.x, bola.y), 10)


    pygame.display.flip()
    
pygame.quit()
sys.exit()
