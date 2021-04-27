import pygame
import sys
import random

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
        return -1  #hay que poner en ambos un menos, porque pasamos de uno a otro(del anterior valor que se ha dado a la variable)   
    return 1

pygame.init()

pantalla = pygame.display.set_mode((800,600))

gameOver= False

#bola 1
x = 400 #esto es la mitad (se podria poner con variables)
y = 300

vx = -7
vy = -7

#bola 2(la vamos a hacer de forma aleatoria)
x2 = random.randint(0, 800)
y2 = random.randint(0, 600)
vx2 = random.randint(5,15)
vy2 = random.randint (5,15)

reloj = pygame.time.Clock()

while not gameOver:
    reloj.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            gameOver = True

    x += vx
    y += vy
    x2 += vx2
    y2 += vy2

    vx *=rebotax(x)
    vy *=rebotay(y)
    vx2 *=rebotax(x2)
    vy2 *=rebotay(y2)




    

    pantalla.fill (NEGRO)
    pygame.draw.circle(pantalla, ROJO, (x, y), 10)
    pygame.draw.circle(pantalla, VERDE, (x2, y2), 10)


    pygame.display.flip()
    
pygame.quit()
sys.exit()
