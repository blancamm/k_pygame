import pygame 
import sys

pygame.init()
pantalla = pygame.display.set_mode((600,400))
pygame.display.set_caption('hola mundo')

gameOver = False

while not gameOver:
    #Gestion de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            gameOver= True
    #Gestion del estado(actualizar las funciones)
    print('hola mundo')

    #Refrescar la pantalla
    pantalla.fill((0, 255, 0)) 
    pygame.display.flip()#e lo mueve a la memoria de la tarjeta grafica. ESENCIAL

pigame.quit()
sys.exit() #o se puede meter ests dos lineas en una funcion y esta linea se llama a la funcion


