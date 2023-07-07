import pygame
from clase_jugador import Player
from constantes import *

import math

class Bala():

    def __init__(self, propietario, x_inicial, y_inicial, x_final, y_final, velocidad, ruta_imagen, tiempo_animacion_ms, tiempo_movimiento_ms, ancho=5, alto=5) -> None:
        self.tiempo_transcurrido_movimiento = 0
        self.tiempo_transcurrido_animacion = 0
        self.imagen = pygame.image.load(ruta_imagen).convert()
        self.imagen = pygame.transform.scale(self.imagen, (ancho, alto))
        self.rectangulo = self.imagen.get_rect()
        self.x = x_inicial
        self.y = y_inicial
        self.propietario = propietario
        self.rectangulo.x = x_inicial
        self.rectangulo.y = y_inicial
        self.tiempo_animacion_ms = tiempo_animacion_ms
        self.tiempo_movimiento_ms = tiempo_movimiento_ms
        angulo = math.atan2(y_final - y_inicial, x_final - x_inicial)  # Obtengo el ángulo en radianes
        print('El ángulo en grados es:', int(angulo * 180 / math.pi))

        self.movimiento_x = math.cos(angulo) * velocidad
        self.movimiento_y = math.sin(angulo) * velocidad

        self.activo = True

    def cambiar_x(self, delta_x):
        self.x = self.x + delta_x
        self.rectangulo.x = int(self.x)

    def cambiar_y(self, delta_y):
        self.y = self.y + delta_y
        self.rectangulo.y = int(self.y)

    def hacer_movimiento(self, delta_ms, lista_plataformas, lista_enemigos, jugador):
        self.tiempo_transcurrido_movimiento += delta_ms
        if self.tiempo_transcurrido_movimiento >= self.tiempo_movimiento_ms:
            self.tiempo_transcurrido_movimiento = 0
            self.cambiar_x(self.movimiento_x)
            self.cambiar_y(self.movimiento_y)
            self.verificar_impacto(lista_plataformas, lista_enemigos, jugador)

    def hacer_animacion(self, delta_ms):
        self.tiempo_transcurrido_animacion += delta_ms
        if self.tiempo_transcurrido_animacion >= self.tiempo_animacion_ms:
            self.tiempo_transcurrido_animacion = 0
            pass

    def verificar_impacto(self, lista_plataformas, lista_enemigos, jugador):
        if self.activo and self.propietario != jugador and self.rectangulo.colliderect(jugador.rectangulo):
            print("IMPACTO EN EL JUGADOR")
            jugador.recibir_disparo()
            self.activo = False
        for enemigo_auxiliar in lista_enemigos:
            if self.activo and self.propietario != enemigo_auxiliar and self.rectangulo.colliderect(enemigo_auxiliar.rectangulo):
                print("IMPACTO EN EL ENEMIGO")
                self.activo = False

    def actualizar(self, delta_ms, lista_plataformas, lista_enemigos, jugador):
        self.hacer_movimiento(delta_ms, lista_plataformas, lista_enemigos, jugador)

        self.hacer_animacion(delta_ms)

    def dibujar(self, pantalla):
        if self.activo:
            if DEBUG:
                pygame.draw.rect(pantalla, color=(255, 0, 0), rect=self.rectangulo_colision)
            pantalla.blit(self.imagen, self.rectangulo)
