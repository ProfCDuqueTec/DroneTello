"""Captura imagen estando el Tello en tierra: no despega."""
import time
from pathlib import Path
import cv2
from djitellopy import Tello

dron = Tello()
stream_activo = False
try:
    dron.connect()
    dron.streamon()
    stream_activo = True
    lectura = dron.get_frame_read()
    imagen = None
    for _ in range(25):
        time.sleep(0.2)
        frame = lectura.frame
        if frame is not None and frame.size > 0:
            imagen = frame.copy()
            break
    if imagen is None:
        raise RuntimeError('No llegaron fotogramas; revisar firmware, Wi-Fi y video')
    destino = Path('foto_tello.png')
    if not cv2.imwrite(str(destino), imagen):
        raise RuntimeError('No se pudo escribir la imagen')
    print('Guardada:', destino.resolve())
finally:
    if stream_activo:
        try:
            dron.streamoff()
        except Exception as exc:
            print('Aviso al cerrar video:', exc)
    dron.end()
