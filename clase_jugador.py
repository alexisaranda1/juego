
import pygame
from constantes import *
from clase_auxiliar import Auxiliar

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, ancho, alto):
        """
        Inicializa un objeto jugador.

        Argumentos:
        - x: Posición horizontal inicial del jugador.
        - y: Posición vertical inicial del jugador.
        - ancho: Ancho del jugador.
        - alto: Alto del jugador.
        """
        super().__init__()

        self.rect = pygame.Rect(x, y, ancho, alto)
        self.vel_x = 0
        self.vel_y = 0
        self.velocidad = 4
        self.mask = None
        self.gravedad = GRAVEDAD
        self.direccion = DIRECCION_I
        self.contador_animacion = 0
        self.contador_caida = 0
        self.contador_salto = 0
        self.golpeado = False
        self.contador_golpe = 0
        self.esta_cayendo = False
        self.contador_doble_salto = 0
        self.vidas = 5
        self.puntaje = 0

        self.quieto_der= Auxiliar.obtenerSuperficieDesdeSpriteSheet(f"{IMAGENES}hero/idle.png", 1, 1,False)
        self.quieto_izq = Auxiliar.obtenerSuperficieDesdeSpriteSheet(f"{IMAGENES}hero/idle.png", 1, 1,True) 
        self.caminar_der = Auxiliar.obtenerSuperficieDesdeSpriteSheet(f"{IMAGENES}hero/walk.png", 6, 1)
        self.caminar_izq = Auxiliar.obtenerSuperficieDesdeSpriteSheet(f"{IMAGENES}hero/walk.png", 6, 1, True)
        self.salto_der = Auxiliar.obtenerSuperficieDesdeSpriteSheet(f"{IMAGENES}hero/jump.png", 3, 1,False ,2)
        self.salto_izq = Auxiliar.obtenerSuperficieDesdeSpriteSheet(f"{IMAGENES}hero/jump.png", 3, 1, True,2)
        self.caida_der = Auxiliar.obtenerSuperficieDesdeSpriteSheet(f"{IMAGENES}hero/fall.png", 3, 1,False)
        self.caida_izq = Auxiliar.obtenerSuperficieDesdeSpriteSheet(f"{IMAGENES}hero/fall.png", 3, 1, True)
        self.animacion = self.quieto_der
        self.image = self.animacion[0]
        self.rect = self.image.get_rect()
        
    def saltar(self):
        if self.vel_y == 0:
            self.vel_y = - self.gravedad * 8
            self.contador_animacion = 0
            self.contador_salto += 1
            if self.contador_salto == 1:
                self.contador_caida = 0  
    def mover(self, dx, dy):

        self.rect.x += dx
        self.rect.y += dy

    def recibir_golpe(self):
        self.golpeado = True

    def mover_izquierda(self, vel):
        self.vel_x = -vel
        if self.direccion != DIRECCION_I:
            self.direccion = DIRECCION_I
            self.contador_animacion = 0

    def mover_derecha(self, vel):
        nueva_posicion_x = self.rect.x + vel
        limite_derecho = ANCHO_VENTANA * 3/4

        if nueva_posicion_x >= 0:
            # Si el jugador está antes del límite derecho
            if nueva_posicion_x + self.rect.w <= limite_derecho:
                self.rect.x = nueva_posicion_x
            else:
                # Si el jugador está en o después del límite derecho
                self.rect.x = limite_derecho - self.rect.w

        self.vel_x = vel

        if self.direccion != DIRECCION_D:
            self.direccion = DIRECCION_D
            self.contador_animacion = 0
    def update(self, fps):
        self.vel_y += min(1, (self.contador_caida / fps) * self.gravedad)
        self.mover(self.vel_x, self.vel_y)

        if self.golpeado:
            self.contador_golpe += 1
        if self.contador_golpe > fps * 2:
            self.golpeado = False
            self.contador_golpe = 0

        self.contador_caida += 1
        self.update_sprite()

        self.contador_animacion += 1
        if self.contador_animacion >= len(self.animacion):
            self.contador_animacion = 0

        self.image = self.animacion[self.contador_animacion]

    def aterrizar(self):
        self.contador_caida = 0
        self.vel_y = 0
        self.contador_salto = 0
    def chocar_cabeza(self):
        self.contador_salto = 0
        self.vel_y *= -1
    def update_sprite(self):
        if self.golpeado:
            if self.direccion == DIRECCION_D:
                self.animacion = self.quieto_der
            else:
                self.animacion = self.quieto_izq
        elif self.vel_y < 0:
            if self.contador_salto == 1:
                if self.direccion == DIRECCION_D:
                    self.animacion = self.salto_der
                else:
                    self.animacion = self.salto_izq
            elif self.contador_salto == 2:
                if self.direccion == DIRECCION_D:
                    self.animacion = self.salto_der
                else:
                    self.animacion = self.salto_izq
        elif self.vel_y > self.gravedad * 2:
            if self.direccion == DIRECCION_D:
                self.animacion = self.caida_der
            else:
                self.animacion = self.caida_izq
        elif self.vel_x != 0:
            if self.direccion == DIRECCION_D:
                self.animacion = self.caminar_der
            else:
                self.animacion = self.caminar_izq
        else:
            if self.direccion == DIRECCION_D:
                self.animacion = self.quieto_der
            else:
                self.animacion = self.quieto_izq

    def draw(self, ventana):
        pygame.draw.rect(ventana,VERDE,self.rect)
        ventana.blit(self.image, (self.rect.x , self.rect.y))
       
       
        # Manejar la colisión vertical del jugador con las plataformas
    def handle_vertical_collision(self, platforms, dy):
        collided_platforms = []
        for platform in platforms:
            if pygame.sprite.collide_rect(self, platform):
                if dy > 0:
                    self.rect.bottom = platform.rect.top
                    self.aterrizar()
                elif dy < 0:
                    self.rect.top = platform.rect.bottom
                    self.chocar_cabeza()

                collided_platforms.append(platform)

        return collided_platforms

    # Verificar la colisión del jugador con una plataforma
    def collide(self, platforms, dx):
        self.mover(dx, 0)
        self.update_sprite()
        collided_platform = None
        for platform in platforms:
            if pygame.sprite.collide_rect(self, platform):
                collided_platform = platform
                break

        self.mover(-dx, 0)
        self.update_sprite()
        return collided_platform

    # Manejar el movimiento del jugador

    def handle_move(self, platforms):
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        collide_left = self.collide(platforms, -self.velocidad * 2)
        collide_right = self.collide(platforms, self.velocidad * 2)

        if keys[pygame.K_LEFT] and not collide_left:
            self.mover_izquierda(self.velocidad)
        if keys[pygame.K_RIGHT] and not collide_right:
            self.mover_derecha(self.velocidad)
            
        # Llamada al método saltar cuando se presiona la tecla de espacio
        if keys[pygame.K_SPACE]:
            self.saltar()
        # Manejo de la colisión vertical con las plataformas
        vertical_collide = self.handle_vertical_collision(platforms, self.vel_y)

        # Actualización del estado del jugador y detección de colisión con plataformas
        to_check = [collide_left, collide_right, *vertical_collide]
        for platform in to_check:
            if platform and platform.name == "plataforma":
                self.aterrizar()
                break  # Salir del bucle después de la primera colisión con una plataforma
