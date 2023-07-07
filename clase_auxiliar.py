
import pygame
import json

class Auxiliar:
    
    @staticmethod
    def obtenerSuperficieDesdeSpriteSheet(ruta, columnas, filas, voltear=False, paso=1, escala=2):
        """
        Carga una imagen de un spritesheet y devuelve una lista de superficies 
        correspondientes a cada fotograma.

        :param ruta: La ruta del archivo de imagen del spritesheet.
        :param columnas: El número de columnas en el spritesheet.
        :param filas: El número de filas en el spritesheet.
        :param voltear: Un valor booleano opcional para indicar si se deben voltear horizontalmente las superficies.
        :param paso: Un valor opcional para especificar el salto entre columnas al extraer los fotogramas.
        :param escala: Un valor opcional para especificar el factor de escala de las superficies.

        :return: Una lista de superficies correspondientes a cada fotograma extraído del spritesheet.
        """
        lista = []
        superficie_imagen = pygame.image.load(ruta).convert_alpha()
        ancho_fotograma = int(superficie_imagen.get_width() / columnas)
        alto_fotograma = int(superficie_imagen.get_height() / filas)
        x = 0
        
        for fila in range(filas):
            for columna in range(0, columnas, paso):
                x = columna * ancho_fotograma
                y = fila * alto_fotograma
                superficie_fotograma = superficie_imagen.subsurface(x, y, ancho_fotograma, alto_fotograma)
                if voltear:
                    superficie_fotograma = pygame.transform.flip(superficie_fotograma, True, False)
                
                # Escalar la superficie del fotograma
                nuevo_ancho = int(ancho_fotograma * escala)
                nuevo_alto = int(alto_fotograma * escala)
                superficie_fotograma = pygame.transform.scale(superficie_fotograma, (nuevo_ancho, nuevo_alto))
                
                lista.append(superficie_fotograma)
        return lista
    
    @staticmethod
    def leer_json(ruta_archivo):
        """
        La función `leer_json` lee y devuelve el contenido de un archivo JSON.
        
        :param ruta_archivo: El parámetro "ruta_archivo" es una cadena que representa la ruta al archivo
        JSON que deseas leer
        :return: los datos leídos del archivo JSON.
        """
        with open(ruta_archivo, 'r') as archivo_json:
            datos = json.load(archivo_json)
        return datos
    
