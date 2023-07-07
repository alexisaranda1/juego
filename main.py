import pygame

from constantes import *
from clase_jugador import Player
from clase_plataforma import Platform
from clase_fondo import Fondo
from clase_tokens import Token
from clase_enemigo import Enemigo
from clase_auxiliar import Auxiliar

pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.init()

pygame.mixer.init()
pygame.mixer.music.load("sonidos/sound/main_theme_sped_up.ogg")
pygame.mixer.music.set_volume(0.0) 
pygame.mixer.music.play(-1)  # Reproduce la música en bucle infinito (-1)

clock = pygame.time.Clock()

# Grupo de sprites, instanciación de los objetos
     
sprites_jugador = pygame.sprite.Group()

# jugador = Jugador(x=0, y=ALTO_VENTANA - 198, velocidad_caminar=4,
#                    velocidad_correr=8,poder_salto=25, tiempo_frame_ms=80, tiempo_movimiento_ms=10, altura_salto=150)

jugador = Player(x=0 , y=ALTO_VENTANA -198 , ancho=50 , alto=50 )
sprites_jugador.add(jugador)
sprites_enemigo = pygame.sprite.Group()

enemigo = Enemigo(x=400, y=ALTO_VENTANA - 105, velocidad_caminar=4,   
                  velocidad_correr=8, gravedad=8, fuerza_salto=25,
                  tiempo_frame_ms=80, tiempo_movimiento_ms=10, altura_salto=150,
                  escala=1, intervalo_tiempo_salto=100)

sprites_enemigo.add(enemigo)

ruta_json = 'confi.json' 
datos = Auxiliar.leer_json(ruta_json)  
imagen_fondo = Fondo(datos["nivel_1"]["fondo"])

sprites_plataformas = pygame.sprite.Group()
for coordenada in datos["nivel_1"]["plataformas"]:
            x, y, ancho, alto, tipo = coordenada
            plataforma = Platform(x, y, ancho, alto, tipo)
            sprites_plataformas.add(plataforma)
            
sprites_tokens =  pygame.sprite.Group()
for coordenada in datos["nivel_1"]["tokens"]:
            x, y, ancho, alto = coordenada
            token_obtenido = Token(x, y, ancho, alto)
            sprites_tokens.add(token_obtenido)

run = True
while run:

    movimiento = jugador.vel_x

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    delta_ms = clock.tick(FPS)
    
    imagen_fondo.dibujar(jugador)

    jugador.handle_move(sprites_plataformas)
    sprites_jugador.update(FPS)
     
    for plataforma in sprites_plataformas:
        plataforma.update(pantalla, movimiento)

    for token in sprites_tokens:
        token.update(pantalla, movimiento, delta_ms)
    sprites_enemigo.update(delta_ms,sprites_plataformas,movimiento, pantalla)
    jugador.draw(pantalla)
    

    pygame.display.flip()

pygame.quit()