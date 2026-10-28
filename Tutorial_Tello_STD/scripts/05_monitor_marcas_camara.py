"""Detecta marcas con la cámara FRONTAL del Tello, estacionado en tierra.
No despega ni mueve motores. Detener con tecla Q sobre ventana de video.
"""
import time
import cv2
from djitellopy import Tello

LIMITE_SEG = 30
MIN_AREA_PX = 1000


def detectar(imagen, detector):
    esquinas, ids, _ = detector.detectMarkers(imagen)
    encontrados = []
    if ids is not None:
        for i, identificador in enumerate(ids.flatten()):
            area = abs(cv2.contourArea(esquinas[i].reshape(-1, 2)))
            if area >= MIN_AREA_PX:
                encontrados.append(int(identificador))
        cv2.aruco.drawDetectedMarkers(imagen, esquinas, ids)
    return encontrados


def main():
    dic = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    detector = cv2.aruco.ArucoDetector(dic, cv2.aruco.DetectorParameters())
    drone = Tello()
    video_on = False
    try:
        drone.connect()
        print('Batería:', drone.get_battery(), '%')
        drone.streamon()
        video_on = True
        lector = drone.get_frame_read()
        inicio = time.monotonic()
        while time.monotonic() - inicio < LIMITE_SEG:
            cuadro = lector.frame
            if cuadro is None or cuadro.size == 0:
                time.sleep(0.1)
                continue
            vista = cuadro.copy()
            ids = detectar(vista, detector)
            cv2.putText(vista, f'Marcas: {ids}   Q: salir', (15, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50, 220, 30), 2)
            cv2.imshow('Tello estandar - monitor sin vuelo', vista)
            if cv2.waitKey(50) & 0xFF == ord('q'):
                break
    finally:
        cv2.destroyAllWindows()
        if video_on:
            try:
                drone.streamoff()
            except Exception as exc:
                print('Aviso al cerrar video:', exc)
        drone.end()

if __name__ == '__main__':
    main()
