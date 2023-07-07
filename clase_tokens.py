import pygame
from constantes import *
from clase_auxiliar import Auxiliar


class Token(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho, alto, tiempo_frame_ms = 80, tiempo_movimiento_ms = 10):

        super().__init__()
        self.imagenes = Auxiliar.obtenerSuperficieDesdeSpriteSheet("imagenes/tiles/key.png", 14, 1, False,1,1)
        self.image = self.imagenes[0]
        self.rect = self.image.get_rect()
        self.posicion_inicial_x = x
        self.rect.x = x
        self.rect.y = y
        self.frame = 0
        self.visible = True
        self.animacion = self.imagenes
        self.imagen = self.animacion[self.frame]
        self.tiempo_transcurrido_animacion = 0
        self.tiempo_frame_ms = tiempo_frame_ms
        self.tiempo_transcurrido_movimiento = 0
        self.tiempo_movimiento_ms = tiempo_movimiento_ms

    def realizar_animacion(self, delta_ms):
        self.tiempo_transcurrido_animacion += delta_ms
        if self.tiempo_transcurrido_animacion >= self.tiempo_frame_ms:
            self.tiempo_transcurrido_animacion = 0
            if self.frame < len(self.animacion) - 1:
                self.frame += 1 
            else: 
                self.frame = 0
            self.imagen = self.animacion[self.frame]  # Actualizar self.imagen con el nuevo frame


    def update(self, pantalla, desplazamiento, delta_ms):
        self.mover(desplazamiento)
        self.realizar_animacion(delta_ms)
        if self.visible:  
            pygame.draw.rect(pantalla,AZUL,self.rect)
            pantalla.blit(self.imagen, self.rect)

   
    def mover(self, desplazamiento):
        if desplazamiento > 0:  
            self.rect.x -= desplazamiento
  
