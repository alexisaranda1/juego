import pygame
from constantes import *
from clase_auxiliar import Auxiliar

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho, alto, tipo=0):
        super().__init__()
        self.imagen_plataforma = Auxiliar.obtenerSuperficieDesdeSpriteSheet(f"{IMAGENES}/tiles/block2.png", 8, 8)[tipo]
        self.imagen_plataforma = pygame.transform.scale(self.imagen_plataforma, (ancho, alto))
        self.image = self.imagen_plataforma
        self.rect = self.image.get_rect()
        self.posicion_inicial_x = x
        self.rect.x = x
        self.rect.y = y
        self.name = "plataforma"
        self.rectangulo_colision_suelo = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, ALTURA_RECTANGULO_SUELO)
        self.rectangulo_colision_inferior = pygame.Rect(self.rect.x, self.rect.y + self.rect.height - ALTURA_RECTANGULO_INFERIOR, self.rect.width, ALTURA_RECTANGULO_INFERIOR)

    def update(self, pantalla, desplazamiento):
        self.mover(desplazamiento)
        self.draw(pantalla)
    def mover(self, desplazamiento):
        if desplazamiento > 0:  
            self.rect.x -= desplazamiento
            self.rectangulo_colision_suelo.x -= desplazamiento
    def draw(self,pantalla):
          pygame.draw.rect(pantalla,ROJO,self.rect)
          pantalla.blit(self.image, self.rect)
          


