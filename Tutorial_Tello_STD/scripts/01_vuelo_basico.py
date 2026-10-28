"""Primer vuelo. Deshabilitado hasta aprobación física del operador."""
import argparse
import time

AUTORIZADO_POR_OPERADOR = False  # activar solo tras preparar recinto y trayectoria

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fly', action='store_true')
    args = parser.parse_args()
    plan = ['DESPEGAR', 'ESPERAR 3 s', 'ATERRIZAR']
    if not (args.fly and AUTORIZADO_POR_OPERADOR):
        print('SIMULACION / PLAN SIN VUELO:')
        print('\n'.join(plan))
        return
    if input('Operador, escriba VOLAR: ').strip() != 'VOLAR':
        print('Cancelado')
        return
    from djitellopy import Tello
    dron = Tello()
    airborne = False
    try:
        dron.connect()
        bateria = dron.get_battery()
        print('Batería:', bateria)
        if bateria < 60:
            raise RuntimeError('Batería inferior al mínimo de laboratorio (60%)')
        dron.takeoff()
        airborne = True
        time.sleep(3)
    finally:
        if airborne:
            try:
                dron.land()
            except Exception as err:
                print('ATENCIÓN: aterrizaje no confirmado:', err)
        dron.end()

if __name__ == '__main__':
    main()
