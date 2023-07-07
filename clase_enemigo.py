
from constantes import *
from clase_auxiliar import Auxiliar
import pygame
pygame.init()


class Enemigo(pygame.sprite.Sprite):
    
    def __init__(self, x, y, velocidad_caminar, velocidad_correr, gravedad, fuerza_salto, tiempo_frame_ms, tiempo_movimiento_ms, altura_salto, escala=1, intervalo_tiempo_salto=100) -> None:
        super().__init__()
        self.caminar_derecha = Auxiliar.obtenerSuperficieDesdeSpriteSheet("imagenes/baddies/totem_walk.png", 7, 1,False ,escala=escala)
        self.caminar_izquierda = Auxiliar.obtenerSuperficieDesdeSpriteSheet("imagenes/baddies/totem_walk.png", 7, 1,True, escala=escala)
        self.quieto_derecha = Auxiliar.obtenerSuperficieDesdeSpriteSheet("imagenes/baddies/totem_walk.png", 7, 1, False,escala=escala)
        self.quieto_izquierda = Auxiliar.obtenerSuperficieDesdeSpriteSheet("imagenes/baddies/totem_walk.png", 7, 1, True, escala=escala)

        self.contador = 0
        self.frame = 0
        self.vidas = 5
        self.puntaje = 0
        self.movimiento_x = 0
        self.movimiento_y = 0
        self.velocidad_caminar = velocidad_caminar
        self.velocidad_correr = velocidad_correr
        self.gravedad = gravedad
        self.fuerza_salto = fuerza_salto
        self.animacion = self.quieto_derecha
        self.direccion = DIRECCION_D
        self.image = self.animacion[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rectangulo_colisiones = pygame.Rect(x, y, self.rect.width, self.rect.height)
        self.rectangulo_colision_suelo = pygame.Rect(self.rectangulo_colisiones)
        self.rectangulo_colision_suelo.height = ALTURA_RECTANGULO_SUELO
        self.rectangulo_colision_suelo.y = y + self.rect.height - ALTURA_RECTANGULO_SUELO

        self.está_saltando = False
        self.está_cayendo = False
        self.está_disparando = False
        self.está_apuñalando = False

        self.tiempo_transcurrido_animacion = 0
        self.tiempo_frame_ms = tiempo_frame_ms
        self.tiempo_transcurrido_movimiento = 0
        self.tiempo_movimiento_ms = tiempo_movimiento_ms
        self.y_inicio_salto = 0
        self.altura_salto = altura_salto

        self.tiempo_transcurrido = 0
        self.tiempo_último_salto = 0  # en base al tiempo transcurrido general
        self.intervalo_tiempo_salto = intervalo_tiempo_salto
   
    def cambiar_x(self, delta_x):
        self.rect.x += delta_x
        self.rectangulo_colisiones.x += delta_x
        self.rectangulo_colision_suelo.x += delta_x

    def cambiar_y(self, delta_y):
        self.rect.y += delta_y
        self.rectangulo_colisiones.y += delta_y
        self.rectangulo_colision_suelo.y += delta_y

    def realizar_movimiento(self, delta_ms, lista_plataformas):
        self.tiempo_transcurrido_movimiento += delta_ms
        if self.tiempo_transcurrido_movimiento >= self.tiempo_movimiento_ms:
            self.tiempo_transcurrido_movimiento = 0

            if not self.está_en_plataforma(lista_plataformas):
                if self.movimiento_y == 0:
                    self.está_cayendo = True
                    self.cambiar_y(self.gravedad)
            else:
                self.está_cayendo = False
                self.cambiar_x(self.movimiento_x)
                if self.contador <= 50:
                    self.movimiento_x = -self.velocidad_caminar
                    self.animacion = self.caminar_izquierda
                    self.contador += 1 
                elif self.contador <= 100:
                    self.movimiento_x = self.velocidad_caminar
                    self.animacion = self.caminar_derecha
                    self.contador += 1
                else:
                    self.contador = 0
    
    def está_en_plataforma(self, lista_plataformas):
        retorno = False
        
        if self.rectangulo_colision_suelo.bottom >= ALTURA_RECTANGULO_SUELO:
            retorno = True     
        else:
            for plataforma in lista_plataformas:
                if self.rectangulo_colision_suelo.colliderect(plataforma.rectangulo_colision_suelo):
                    retorno = True
                    break       
        return retorno    

    def realizar_animación(self, delta_ms):
        self.tiempo_transcurrido_animacion += delta_ms
        if self.tiempo_transcurrido_animacion >= self.tiempo_frame_ms:
            self.tiempo_transcurrido_animacion = 0
            if self.frame < len(self.animacion) - 1:
                self.frame += 1 
            else: 
                self.frame = 0
    
    def update(self, delta_ms, lista_plataformas, desplazamiento, pantalla):
        self.realizar_movimiento(delta_ms, lista_plataformas)
        self.realizar_animación(delta_ms)
        if desplazamiento > 0:  
            self.rect.x -= desplazamiento
        self.dibujar(pantalla)
        self.image = self.animacion[self.frame]
        pantalla.blit(self.image, self.rect)

    def dibujar(self, pantalla):
        if DEBUG:
            pygame.draw.rect(pantalla, color=(255, 0, 0), rect=self.rectangulo_colision)
            pygame.draw.rect(pantalla, color=(255, 255, 0), rect=self.rectangulo_colision_suelo)

    def recibir_disparo(self):
        self.vidas -= 1
