import pygame
import sys

ROJO = (255, 0 ,0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
NEGRO = (0,0,0)

pygame.init()

pantalla = pygame.display.set_mode((800,600))

gameOver= False

x = 400 #esto es la mitad (se podria poner con variables)
y = 300

velocidadx = -7
velocidady = -7
reloj = pygame.time.Clock()

while not gameOver:
    reloj.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            gameOver = True

    x += velocidadx
    y += velocidady

    if y <= 0 or y >=600: #porque puede que no llegue al 0 como tal como la velocidad -7
        velocidady = -velocidady


    if x <= 0 or x >= 800:
        velocidadx = -velocidadx  #hay que poner en ambos un menos, porque pasamos de uno a otro(del anterior valor que se ha dado a la variable)

    pantalla.fill (NEGRO)
    pygame.draw.circle(pantalla, ROJO, (x, y), 10)


    pygame.display.flip()
    
pygame.quit()
sys.exit()
