import pygame as pg

pg.init()
pantalla = pg.display.set_mode((600,400))
pg.display.set_caption('hola mundo')

gameOver = False

while not gameOver:
    #Gestion de eventos
    for evento in pg.event.get():
        pass
   
    #Gestion del estado(actualizar las funciones)
    print('hola mundo')

    #Refrescar la pantalla
    pantalla.fill((0, 255, 0)) 
    pg.display.flip()#e lo mueve a la memoria de la tarjeta grafica. ESENCIAL


