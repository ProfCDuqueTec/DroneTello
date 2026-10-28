# DJI Tello estándar · Python desde cero hasta reconocimiento visual

Guía actualizada para el hardware real del taller Drone Commander, **DJI Tello estándar**.

1. Lee `TUTORIAL_DJITelloPy_TELLO_ESTANDAR.md`.
2. Copia `scripts/` y `requirements.txt` en una carpeta abierta en VS Code.
3. Instala las dependencias dentro de `.venv`.
4. Comienza con `00_conexion.py` y `03_crear_marcadores_aruco.py`.
5. Prueba la máquina de estados `06_ruta_visual_simulada.py` antes de cualquier maniobra física.

Incluye ocho programas. `07_ruta_visual_supervisada.py` **no vuela por defecto** y requiere aprobación, calibración y ensayo físico de los tramos. La lógica de reconocimiento se realiza con Python y OpenCV, no con funciones nativas de reconocimiento del dron.

Fuente base de la biblioteca: https://github.com/damiafuentes/DJITelloPy (terceros).
