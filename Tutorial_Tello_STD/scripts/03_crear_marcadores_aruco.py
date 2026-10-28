"""Crea marcas de referencia para la cámara frontal del DJI Tello estándar.
No conecta con el dron. OpenCV contrib requerido.
"""
from pathlib import Path
import cv2

OUT = Path('marcadores')
OUT.mkdir(exist_ok=True)
dic = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

for id_marca in [1, 2, 3]:
    marcador = cv2.aruco.generateImageMarker(dic, id_marca, 500)
    # Margen blanco indispensable para buena detección.
    imagen = cv2.copyMakeBorder(marcador, 65, 65, 65, 65,
                               cv2.BORDER_CONSTANT, value=255)
    ruta = OUT / f'marca_{id_marca}.png'
    cv2.imwrite(str(ruta), imagen)
    print('Marca lista para imprimir:', ruta.resolve())

print('Imprime sin deformar, con fondo mate, alto contraste y tamaño medido.')
