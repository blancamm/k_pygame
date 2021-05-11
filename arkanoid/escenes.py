
from arkanoid import ANCHO, ALTO, levels, FPS
from arkanoid.entities import Marcador, Bola, Raqueta, Ladrillo, CuentaVidas
from random import randint, choice

import sys

import pygame as pg
from enum import Enum

class Escene():
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.TodoGroup= pg.sprite.Group()
        self.reloj = pg.time.Clock()


    def rest(self):
        pass

    def bucle_principal(self):
        pass

    def manejo_eventos(self):
        for evento in pg.event.get():
            if evento.type == pg.QUIT or \
                evento.type ==pg.KEYDOWN and evento.key == pg.K_q:
                pg.quit()
                sys.exit()


class Game(Escene):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        #self.pantalla = pantalla 
        self.fondo = pg.image.load('./imagenes/background.png')

        #SE CREA ESTOS GRoupS PARA PODER HACER LA COLISION ENTRE ELLOS
        self.grupoJugador = pg.sprite.Group()
        self.grupoLadrillos = pg.sprite.Group()
        #self.TodoGroup = pg.sprite.Group ()

        self.TodoGroup.add(self.grupoLadrillos)
        self.cuentaPuntos = Marcador(10, 10, fontsize=50)
        self.cuentaVidas = CuentaVidas(790, 10, 'topright', 50)
        self.TodoGroup.add(self.cuentaPuntos, self.cuentaVidas) #se puede añadir con comas

        self.bola= Bola (randint(0, ANCHO), randint(0, ALTO))
        self.TodoGroup.add(self.bola) 

        self.raqueta = Raqueta(x = ANCHO//2, y=ALTO-30)
        self.grupoJugador.add(self.raqueta)
        self.TodoGroup.add(self.grupoJugador)

        self.reset()

    def reset(self): # es como resetear las cosas
        self.vidas = 3
        self.puntuacion = 0
        self.level = 0
        self.TodoGroup.remove(self.grupoLadrillos)
        self.grupoLadrillos.empty()
        self.disponer_ladrillos(levels[self.level])
        self.TodoGroup.add(self.grupoLadrillos)
        self.TodoGroup.remove(self.cuentaPuntos, self.cuentaVidas)
        self.TodoGroup.add(self.cuentaPuntos, self.cuentaVidas)

    

    def disponer_ladrillos(self, level):

        for fila, cadena in enumerate(level):
            contador = 0
            for contador, caracter in enumerate(cadena):
                x = 5 + (100 * contador)
                y = 5 + (40 * fila)
                if caracter in'XD':
                    ladrillo = Ladrillo(x,y, caracter == 'D') #si el carcater es igual  D, te saldran D==D que es true, entonces te saldran un ladrillo duro
                    self.grupoLadrillos.add(ladrillo)
                    
                contador += 1

 
    def bucle_principal(self):
        game_Over = False #es variable, no es atributo. No tiene sentido fuera de este metodo por eso solo es variable y no atributo
        

        while not game_Over and self.vidas > 0:
            dt = self.reloj.tick(FPS)

            self.manejo_eventos()

            #self.disponer_ladrillos()
            self.cuentaPuntos.text = self.puntuacion #o se podria hacer con format
            self.cuentaVidas.text =self.vidas
            self.bola.prueba_colision(self.grupoJugador)
            tocados = self.bola.prueba_colision(self.grupoLadrillos)

            for ladrillo in tocados:
                self.puntuacion +=5
                if ladrillo.desaparece():
                    self.grupoLadrillos.remove(ladrillo)
                    self.TodoGroup.remove(ladrillo)
                    if len(self.grupoLadrillos) == 0:
                        self.level += 1
                        self.disponer_ladrillos(levels[self.level])
                        self.TodoGroup.add(self.grupoLadrillos)

            self.TodoGroup.update(dt)

            if self.bola.estado == Bola.Estado.muerta:
                self.vidas -= 1

            self.pantalla.blit(self.fondo, (0,0))
            
            self.TodoGroup.draw(self.pantalla)


            pg.display.flip()

#la pantalla de inicio
class Portada(Escene):
    def __init__(self, pantalla):
        super().__init__(pantalla)

        self.instrucciones = Marcador(ANCHO//2, ALTO//2, 'center', 50, (255, 255,0))
        self.instrucciones.text = 'Pulsa espacio para jugar'
        self.TodoGroup.add(self.instrucciones)


    def reset(self):
        pass


    def bucle_principal(self):
        game_Over = False

        while not game_Over:
            dt = self.reloj.tick (FPS)

            self.manejo_eventos()

            teclas_pulsadas = pg.key.get_pressed()
            if teclas_pulsadas[pg.K_SPACE]:
                game_Over = True

            self.TodoGroup.update(dt)
            self.pantalla.fill((0,0,0))
            self.TodoGroup.draw(self.pantalla)

            pg.display.flip()







