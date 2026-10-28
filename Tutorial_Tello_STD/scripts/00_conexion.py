"""Solo conexión, sin vuelo. Compatible con DJI Tello estándar."""
from djitellopy import Tello

dron = Tello()
try:
    dron.connect()
    print('Conectado al Tello')
    print('Batería:', dron.get_battery(), '%')
    print('Altura reportada:', dron.get_height(), 'cm')
finally:
    dron.end()
