# DJI Tello estándar · Programación con Python

**Drone Commander | Tecnológico de Monterrey, Campus León**

Repositorio didáctico para aprender a programar el **DJI Tello estándar** con Python, desde la conexión y el control de vuelo hasta la captura de imágenes y el reconocimiento de marcadores visuales con OpenCV.

El material está organizado de lo básico a lo avanzado y se puede utilizar en **VS Code**. Incluye ejercicios que funcionan sin dron, pruebas de cámara con el equipo en tierra y demostraciones de vuelo que requieren supervisión.

## Requisitos

- Python 3 y Visual Studio Code (con la extensión **Python**).
- Para las pruebas con hardware: DJI Tello estándar y conexión a su red Wi-Fi.
- Bibliotecas indicadas en [`requirements.txt`](requirements.txt): `djitellopy`, `opencv-contrib-python` y `pygame`.

## Instalación en Windows

Abre esta carpeta como proyecto en VS Code y ejecuta en su terminal PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Selecciona el intérprete `.venv` con **Python: Select Interpreter**.

## Primeros ejercicios

**Sin conectar el dron:**

```powershell
.\.venv\Scripts\python.exe scripts\03_crear_marcadores_aruco.py
.\.venv\Scripts\python.exe scripts\04_reconocer_marca_en_foto.py marcadores\marca_1.png
.\.venv\Scripts\python.exe scripts\06_ruta_visual_simulada.py
```

**Con el Tello encendido y conectado por Wi-Fi, pero sin despegar:**

```powershell
.\.venv\Scripts\python.exe scripts\00_conexion.py
.\.venv\Scripts\python.exe scripts\02_captura_foto.py
.\.venv\Scripts\python.exe scripts\05_monitor_marcas_camara.py
```

## Ejemplos incluidos

| Archivo | Objetivo |
|---|---|
| [`00_conexion.py`](Tutorial_Tello_STD/scripts/00_conexion.py) | Conectar y consultar batería y altura. |
| [`01_vuelo_basico.py`](scripts/01_vuelo_basico.py) | Ensayar despegue y aterrizaje; **vuelo deshabilitado por defecto**. |
| [`02_captura_foto.py`](scripts/02_captura_foto.py) | Obtener una foto de la cámara frontal. |
| [`03_crear_marcadores_aruco.py`](scripts/03_crear_marcadores_aruco.py) | Generar marcadores ArUco para impresión. |
| [`04_reconocer_marca_en_foto.py`](scripts/04_reconocer_marca_en_foto.py) | Detectar identificadores de marcadores en imágenes. |
| [`05_monitor_marcas_camara.py`](scripts/05_monitor_marcas_camara.py) | Reconocer marcas desde el video del Tello en tierra. |
| [`06_ruta_visual_simulada.py`](scripts/06_ruta_visual_simulada.py) | Validar una secuencia de estaciones sin hardware. |
| [`07_ruta_visual_supervisada.py`](scripts/07_ruta_visual_supervisada.py) | Estudiar una ruta por estaciones con tramos preensayados; **bloqueada por defecto**. |

## Tutorial completo

Lee **[`TUTORIAL_DJITelloPy_TELLO_ESTANDAR.md`](TUTORIAL_DJITelloPy_TELLO_ESTANDAR.md)** para encontrar las explicaciones paso a paso, los comandos esenciales y la progresión de actividades.

## Importante: reconocimiento visual y seguridad

Este proyecto utiliza **marcadores ArUco y OpenCV** para reconocer estaciones mediante la cámara frontal. **No utiliza Mission Pads ni posicionamiento relativo nativo a marcadores.** Reconocer una marca no significa que el dron pueda navegar automáticamente hacia ella: los ejercicios físicos avanzados usan tramos fijos, previamente medidos y autorizados.

Nunca ejecutes maniobras físicas sin un operador capacitado, espacio controlado y un plan de contingencia. La simulación no garantiza la seguridad de la trayectoria real.

## Referencias

- [DJITelloPy — repositorio de código abierto de terceros](https://github.com/damiafuentes/DJITelloPy)
- [Documentación de DJITelloPy](https://djitellopy.readthedocs.io/en/latest/)
- [OpenCV — detección de marcadores ArUco](https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html)

> Material educativo de **Drone Commander · Tec de Monterrey, Campus León**. La biblioteca DJITelloPy es un proyecto independiente de DJI y del Tecnológico de Monterrey.
