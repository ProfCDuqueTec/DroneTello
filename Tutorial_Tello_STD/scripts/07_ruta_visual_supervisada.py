"""Ruta visual de demostración: Tello estándar + cámara frontal + ArUco.

IMPORTANTE: controlador de investigación bajo SUPERVISIÓN, no navegación libre.
La cámara detecta el marcador en una estación; solo entonces se permite un
tramo fijo configurado, medido y validado previamente por un operador.
Por defecto NO conecta, NO despega y NO mueve el dron.
"""
import argparse
import time
import cv2

AUTORIZACION_OPERADOR = False
TRAMOS_MEDIDOS_Y_ENSAYADOS = False
BATERIA_MINIMA = 60
VENTANA_DETECCION_SEG = 5
MIN_AREA_PX = 1100
CONFIRMACIONES = 3

# DEMOSTRACIÓN, NO CALIBRACIÓN DEL RECINTO.
# El instructor modifica esta ruta tras medir y ensayar cada tramo.
RUTA = [
    {'id': 1, 'accion': 'inicio', 'siguiente_tramo': [('forward', 50)]},
    {'id': 2, 'accion': 'inspección', 'siguiente_tramo': [('right', 90), ('forward', 50)]},
    {'id': 3, 'accion': 'destino', 'siguiente_tramo': []},
]


def marca_estable(lector, detector, esperado, limite=VENTANA_DETECCION_SEG):
    """Observa cámara frontal sin maniobras exploratorias a ciegas."""
    comienzo = time.monotonic()
    consecutivos = 0
    while time.monotonic() - comienzo < limite:
        foto = lector.frame
        if foto is None or foto.size == 0:
            consecutivos = 0
            time.sleep(0.15)
            continue
        esquinas, ids, _ = detector.detectMarkers(foto)
        encontrados = []
        if ids is not None:
            for i, valor in enumerate(ids.flatten()):
                if cv2.contourArea(esquinas[i].reshape(-1, 2)) >= MIN_AREA_PX:
                    encontrados.append(int(valor))
        consecutivos = consecutivos + 1 if esperado in encontrados else 0
        print(f'Esperando marcador {esperado}: {encontrados} ({consecutivos}/{CONFIRMACIONES})')
        if consecutivos >= CONFIRMACIONES:
            return True
        time.sleep(0.15)
    return False


def ejecutar_tramo(dron, instrucciones):
    for nombre, valor in instrucciones:
        # Solo movimientos discretos que debieron ensayarse previamente.
        if nombre == 'forward':
            if not 20 <= valor <= 50:
                raise ValueError('Distancia de tramo no autorizada')
            dron.move_forward(valor)
        elif nombre == 'right':
            if valor != 90:
                raise ValueError('Solo giro de 90 grados configurado')
            dron.rotate_clockwise(valor)
        elif nombre == 'left':
            if valor != 90:
                raise ValueError('Solo giro de 90 grados configurado')
            dron.rotate_counter_clockwise(valor)
        else:
            raise ValueError('Movimiento no permitido en esta práctica')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fly', action='store_true', help='Solo operador autorizado en recinto ensayado')
    args = ap.parse_args()
    if not (args.fly and AUTORIZACION_OPERADOR and TRAMOS_MEDIDOS_Y_ENSAYADOS):
        print('SIMULACIÓN DE PLAN (sin conexión):')
        for etapa in RUTA:
            print(etapa)
        print('Para vuelo real el operador debe autorizar y validar tramos.')
        return

    if input('Escriba VOLAR para aceptar ruta física revisada: ').strip() != 'VOLAR':
        print('Vuelo cancelado')
        return

    from djitellopy import Tello
    dron = Tello()
    volando = False
    video = False
    try:
        dron.connect()
        nivel = dron.get_battery()
        print('Batería:', nivel)
        if nivel < BATERIA_MINIMA:
            raise RuntimeError('Batería insuficiente para laboratorio')
        dic = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        detector = cv2.aruco.ArucoDetector(dic, cv2.aruco.DetectorParameters())
        dron.streamon()
        video = True
        lector = dron.get_frame_read()
        time.sleep(1)
        dron.takeoff()
        volando = True
        for etapa in RUTA:
            if not marca_estable(lector, detector, etapa['id']):
                raise RuntimeError(f'Marca {etapa["id"]} no detectada en tiempo límite')
            print('MARCA CONFIRMADA', etapa['id'], '|', etapa['accion'])
            # No se infiere posición global ni se busca visualmente una marca ausente.
            ejecutar_tramo(dron, etapa['siguiente_tramo'])
        print('Secuencia de estaciones confirmada')
    finally:
        if volando:
            try:
                dron.land()
            except Exception as exc:
                print('ALERTA: no se pudo confirmar aterrizaje:', exc)
        if video:
            try:
                dron.streamoff()
            except Exception:
                pass
        dron.end()


if __name__ == '__main__':
    main()
