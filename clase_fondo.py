import pygame
from constantes import *

class Fondo:
    def __init__(self, imagen_fondo):
        self.imagen = pygame.image.load(imagen_fondo).convert_alpha()
        self.imagen = pygame.transform.scale(self.imagen, (ANCHO_VENTANA, ALTO_VENTANA))
        self.posicion_fondo = 0

    def dibujar(self, jugador):
        self.mover(jugador.vel_x)
        ventana = pygame.display.get_surface()  # Obtener la superficie de la ventana
        posicion_fondo_relativa = self.posicion_fondo % self.imagen.get_rect().width
        ventana.blit(self.imagen, (posicion_fondo_relativa - self.imagen.get_rect().width, 0))
        if posicion_fondo_relativa < ANCHO_VENTANA:
            ventana.blit(self.imagen, (posicion_fondo_relativa, 0))
        self.score(jugador)

    def score (self,jugador):
        ventana = pygame.display.get_surface()
        puntaje = pygame.font.Font(None,36)
        mensaje_puntaje = puntaje.render( "LLAVES: " + str(jugador.puntaje),True, AMARILLO)
        vida = pygame.font.Font(None,36)
        mensaje_vida = vida.render( "VIDAS: " + str(jugador.vidas),True, AMARILLO)
        ventana.blit(mensaje_puntaje,(0,20))
        ventana.blit(mensaje_vida,(300,20))



    def mover(self, desplazamiento):
        if desplazamiento > 0:  
            self.posicion_fondo -= desplazamiento

