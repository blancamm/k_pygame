import pygame
import sys
import random #podriamos poner fom random import randint y asi no tenemos que poner random.randint y solo randint

ROJO = (255, 0 ,0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
NEGRO = (0,0,0)
BLANCO = (255, 255, 255)
ANCHO = 900
ALTURA = 650

pygame.init()
pygame.font.init()

VIDAS = 3
NumeroVidas = str(VIDAS)

PUNTOS = 0
NumeroPuntos = str(PUNTOS)


class Bola():
    def __init__(self, x, y, vx=5, vy=5, color= (255, 255, 255), radio = 10): #ponemos algunos por defecto
        self.x = x
        self.y= y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.radio = radio
        self.anchura = radio *2
        self.altura = radio *2

    def actualizar(self):
        self.x += self.vx
        self.y += self.vy 

        if self.x <= 0 or self.x >= ANCHO:
            self.vx = -self.vx

        if self.y <= 75:
            self.vy = -self.vy

        if self.y >= ALTURA:

            self.x = ANCHO //2
            self. y = ALTURA//2
            
            self.vx = random.randint(5,8)* random.choice([-1, 1])
            self.vy = random.randint (5,8)*random.choice([-1, 1])
            
            return True #aqui estamos poniendo que si golpea el suelo te devuelva True -> pierdeBola = bola.actualizar = True
        return False

    def dibujar(self, lienzo):
        pygame.draw.circle(lienzo, self.color, (self.x, self.y), self.radio)

    def comprueba_colision(self, objeto):
        choqueX = self.x >= objeto.x and self.x <= objeto.x+objeto.ancho or \
            self.x + self.anchura >= objeto.x and self.x+ self.anchura <= objeto.ancho

        choqueY = self.y >= objeto.y and self.y <= objeto.y+objeto.alto or \
            self.y + self.altura >= objeto.y and self.y+ self.altura <= objeto.alto

        if choqueX and choqueY:
            self.vy *= -1
            global PUNTOS
            global NumeroPuntos
            PUNTOS += 5
            NumeroPuntos = str(PUNTOS)




class Raqueta():
    def __init__(self, ancho=150, alto= 25, x=0, y=0):
        self.ancho= ancho
        self.alto = alto
        self.x = (ANCHO -self.ancho)//2
        self.y  = (ALTURA - self.alto)
        self.color = BLANCO
        self.vx = 10
        self.vy = 10

    def dibujar(self, lienzo):
        rectangulo = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        pygame.draw.rect(lienzo, self.color, rectangulo)

    def actualizar (self):
        teclas_pulsadas =pygame.key.get_pressed()
        if teclas_pulsadas[pygame.K_LEFT] and self.x >0:
            self.x -= self.vx
        if teclas_pulsadas[pygame.K_RIGHT] and self.x < (ANCHO-self.ancho):   
            self.x += self.vx

class Marcador():
    def __init__(self):
        self.__color = (123, 125, 125 )
        self.__x = 0
        self.__y = 0
        self.__ancho = ANCHO
        self.__altura = 75
        self.__fuente = pygame.font.SysFont('Elephant',24)

    def dibujarMarcador(self, lienzo):
        rectangulo = pygame.Rect(self.__x, self.__y, self.__ancho, self.__altura)
        pygame.draw.rect(lienzo, self.__color, rectangulo)

    def puntosyvidas(self):
        text_vidas = self.__fuente.render('VIDAS', True, BLANCO)
        vidas = self.__fuente.render(NumeroVidas, True, BLANCO)
        text_puntos = self.__fuente.render('PUNTOS', True, BLANCO)
        puntos = self.__fuente.render(NumeroPuntos, True, BLANCO)
        return [text_vidas, vidas, text_puntos, puntos]

    def fin(self):
        pantalla.fill (NEGRO)
        fuente = pygame.font.SysFont('Elephant',36)
        texto_gameOver = fuente.render('GAME OVER', True, ROJO)
        fuentemini = pygame.font.SysFont('Elephant',24)
        texto_puntuacion = fuentemini.render('PUNTUACION:', True, BLANCO)
        texto_Puntos = fuentemini.render(NumeroPuntos, True, BLANCO)
        return [texto_gameOver, texto_puntuacion, texto_Puntos]
            


raqueta = Raqueta()
bola= Bola(random.randint(0, ANCHO), 
                random.randint(0, ALTURA),
                random.randint(5,8)*random.choice([-1, 1]), 
                random.randint(5,8)*random.choice([-1, 1]), 
                (random.randint(0,255), random.randint(0,255), random.randint(0,255)))
marcador = Marcador()

pygame.init()


pantalla = pygame.display.set_mode((ANCHO,ALTURA))

def refrescar_pantalla():
        pantalla.fill (NEGRO)
        bola.dibujar(pantalla)
        raqueta.dibujar(pantalla)
        marcador.dibujarMarcador(pantalla)
        escribir = marcador.puntosyvidas()
        pantalla.blit(escribir[0], (50,20))
        pantalla.blit(escribir[1], (200, 20))
        pantalla.blit(escribir[2], (600, 20))
        pantalla.blit(escribir[3], (800, 20))
        pygame.display.flip()


reloj = pygame.time.Clock()

gameOver= False

while not gameOver and VIDAS > 0:
    reloj.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            gameOver = True

        
    #modificacion de estados
    raqueta.actualizar()
    pierdebola = bola.actualizar()
    if pierdebola:
        
        VIDAS -= 1
        NumeroVidas = str(VIDAS)
        refrescar_pantalla()

        if VIDAS == 0:
            gameOver = True

        pygame.time.delay(1000)
            
    bola.comprueba_colision(raqueta)

    #gestion de pantalla
    refrescar_pantalla()

while gameOver:
    final = marcador.fin()
    pantalla.blit(final[0], (300, 275))
    pantalla.blit(final[1], (300, 350))
    pantalla.blit(final[2], (525, 350))
    pygame.display.flip()
    pygame.time.delay(3500)
    pygame.quit()
    sys.exit()

