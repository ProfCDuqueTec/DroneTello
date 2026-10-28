"""Lee marcas ArUco en una foto. Sin dron ni vuelo.
Uso: python 04_reconocer_marca_en_foto.py marcadores/marca_1.png
"""
import argparse
import cv2

parser = argparse.ArgumentParser(description='Detección ArUco en imagen')
parser.add_argument('foto', help='Ruta del archivo JPG/PNG')
args = parser.parse_args()

imagen = cv2.imread(args.foto)
if imagen is None:
    raise SystemExit('No se pudo leer la imagen. Revisa la ruta.')

dic = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
detector = cv2.aruco.ArucoDetector(dic, cv2.aruco.DetectorParameters())
corners, ids, _ = detector.detectMarkers(imagen)

if ids is None:
    print('Ninguna marca reconocida')
else:
    print('IDs reconocidos:', ids.flatten().tolist())
    cv2.aruco.drawDetectedMarkers(imagen, corners, ids)
    cv2.imwrite('resultado_deteccion.png', imagen)
    print('Evidencia: resultado_deteccion.png')
