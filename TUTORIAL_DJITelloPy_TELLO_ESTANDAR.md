# DRONE COMMANDER · Programación del DJI Tello estándar con Python

**Guía de referencia de principiante a avanzado · Tec de Monterrey, Campus León · Escuela de Ingeniería y Ciencias**  
**Entorno:** Windows, Visual Studio Code, Python y biblioteca `djitellopy`  
**Objetivo:** dominar control, fotografía, video, pilotaje asistido y rutas condicionadas por **marcadores visuales ArUco detectados con la cámara frontal y OpenCV**.

> **Alcance del hardware:** este material está diseñado **exclusivamente para el DJI Tello estándar disponible en el taller**. Utiliza su conexión Wi-Fi, sus comandos básicos del SDK y la cámara frontal. La detección de marcas la hace **Python en la computadora**, no el firmware del dron. Los movimientos programados no garantizan posicionamiento preciso ni detección de obstáculos. Los ejemplos de visión y lógica son aptos para enseñar autonomía, pero la ruta física requiere calibración y autorización independientes.

## Índice y progresión

| Etapa | Tema | Práctica / archivo | ¿Dron necesario? |
|---|---|---|---|
| 1 | Conexión y telemetría | `00_conexion.py` | Sí, sin despegar |
| 2 | Primer programa de vuelo | `01_vuelo_basico.py` | Solo en prueba física autorizada; simulación sin dron |
| 3 | Cámara y fotografía | `02_captura_foto.py` | Sí, sin despegar |
| 4 | Video y control manual | Ejemplos de repositorio | Sí, bajo supervisión |
| 5 | Fabricación de marcas ArUco | `03_crear_marcadores_aruco.py` | No |
| 6 | Identificación de marcas en fotos | `04_reconocer_marca_en_foto.py` | No |
| 7 | Cámara del Tello + detección en vivo | `05_monitor_marcas_camara.py` | Sí, sin despegar |
| 8 | Máquina de estados: ruta de 3 estaciones | `06_ruta_visual_simulada.py` | No |
| 9 | Ruta visual con movimientos supervisados | `07_ruta_visual_supervisada.py` | Solo en recinto ensayado, operador autorizado |

**Fuente del código base:** [DJITelloPy](https://github.com/damiafuentes/DJITelloPy) (biblioteca comunitaria), [ejemplos](https://github.com/damiafuentes/DJITelloPy/tree/master/examples), [API de Tello](https://djitellopy.readthedocs.io/en/latest/tello/). **Referencia oficial del equipo:** [Tello SDK 1.3](https://dl-cdn.ryzerobotics.com/downloads/tello/20180910/Tello%20SDK%20Documentation%20EN_1.3.pdf). **Instalación de OpenCV:** [documentación](https://docs.opencv.org/4.x/db/dd1/tutorial_py_pip_install/py_pip_install.html). Los ejercicios originales se explican por su intención y funcionamiento, no se reproducen íntegramente.

---

## 1. Preparación del entorno en VS Code

1. Instala [Python](https://www.python.org/downloads/) y [VS Code](https://code.visualstudio.com/); agrega la extensión **Python** de Microsoft.
2. Crea una carpeta llamada `TelloPython` en Documentos y ábrela en **File → Open Folder**.
3. En **Terminal → New Terminal** (PowerShell), escribe:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

> Copia `requirements.txt` y la carpeta `scripts` del kit dentro de `TelloPython` antes del último comando. Alternativamente: `...python.exe -m pip install djitellopy opencv-contrib-python pygame`. Elegimos `opencv-contrib-python` para disponer explícitamente de las funciones ArUco; **no instales simultáneamente `opencv-python` y `opencv-contrib-python`** en el mismo entorno.

4. Presiona `Ctrl+Shift+P` → **Python: Select Interpreter** → selecciona `.venv`.
5. Comprueba:

```powershell
.\.venv\Scripts\python.exe -c "from djitellopy import Tello; import cv2, pygame; print('Python OK',cv2.__version__,'ArUco:',hasattr(cv2,'aruco'))"
```

**Estructura esperada:**

```text
TelloPython/
├── .venv/
├── requirements.txt
├── scripts/
│   ├── 00_conexion.py
│   ├── 01_vuelo_basico.py
│   ├── 02_captura_foto.py
│   ├── 03_crear_marcadores_aruco.py
│   ├── 04_reconocer_marca_en_foto.py
│   ├── 05_monitor_marcas_camara.py
│   ├── 06_ruta_visual_simulada.py
│   └── 07_ruta_visual_supervisada.py
├── marcadores/            (se crea automáticamente)
└── resultados/            (opcional)
```

Para operar, enciende el Tello y conecta la PC a la red `TELLO-XXXXXX`. El aviso «Sin Internet» es normal; el enlace es directo. No uses otra aplicación que controle simultáneamente la misma aeronave.

## 2. Seguridad indispensable

- Antes de cualquier vuelo: recinto segregado, operador capacitado, protectores de hélice, iluminación y suelo adecuados, espacio medido, ausencia de personas y animales en las trayectorias, batería suficiente. **60 % es una política conservadora de este taller**, no una exigencia universal del SDK.
- Los programas preparados **no vuelan por defecto**. No actives sus opciones físicas hasta validar de manera separada el recinto, la orientación del dron, las marcas y cada movimiento.
- Una captura de cámara no proporciona por sí sola distancia absoluta confiable, percepción de profundidad ni capacidad de evitar obstáculos. Las marcas pueden perderse por movimiento, brillo, desenfoque, giro o baja resolución.
- Un fallo de red puede impedir confirmar aterrizaje. El operador requiere un procedimiento de contingencia ensayado; `Ctrl+C` no garantiza interrupción instantánea de una orden en curso. `emergency()` detiene motores y puede causar una caída: **no equivale a un aterrizaje seguro**.
- Para el proyecto visual, ubica las marcas **verticales y orientadas a la cámara frontal** y mantén libre todo el corredor aéreo. La mera detección de una marca no significa que sea seguro acercarse a ella.

---

# PARTE I · Control básico

## 3. Primer contacto: `simple.py`

**Referencia:** [`examples/simple.py`](https://github.com/damiafuentes/DJITelloPy/blob/master/examples/simple.py).

El ejemplo muestra un patrón fundamental: crear `Tello()`, ejecutar `connect()`, despegar con `takeoff()`, trasladarse lateralmente con `move_left(100)`, girar con `rotate_counter_clockwise(90)`, avanzar con `move_forward(100)` y aterrizar con `land()`. Es una secuencia abierta, no una ruta con corrección visual.

**Conceptos:** (a) centímetros para movimientos, (b) grados para giros, (c) desplazamiento lateral no modifica el rumbo, (d) las instrucciones se ejecutan consecutivamente, (e) la posición final es estimada y puede diferir de la ideal.

**Práctica guiada:** ejecuta la simulación de `01_vuelo_basico.py`:

```powershell
.\.venv\Scripts\python.exe .\scripts\01_vuelo_basico.py
```

Mostrará DESPEGAR → ESPERAR → ATERRIZAR, **sin conectar ni despegar**. El vuelo físico se habilita exclusivamente por el operador después de preparar el recinto. **Reto:** traza una ruta con norte, este, sur y oeste y calcula la posición ideal final.

## 4. Conectar sin despegar: `00_conexion.py`

```python
from djitellopy import Tello

dron = Tello()
try:
    dron.connect()
    print('Batería:', dron.get_battery(), '%')
    print('Altura:', dron.get_height(), 'cm')
finally:
    dron.end()
```

Ejecuta:

```powershell
.\.venv\Scripts\python.exe .\scripts\00_conexion.py
```

**Aprendizaje:** qué hace `connect()`, lectura de telemetría y liberación de recursos `end()`. Al desconectar el Wi-Fi se producirá un error; comprobarlo **sin vuelo**.

## 5. Funciones de control esenciales

| Método | Qué hace | Unidad |
|---|---|---|
| `connect()` / `end()` | Abrir / cerrar la comunicación | — |
| `get_battery()` / `get_height()` | Leer batería / altura reportada | % / cm |
| `takeoff()` / `land()` | Despegar / aterrizar | — |
| `move_forward(30)` / `move_back(30)` | Avanzar / retroceder | cm |
| `move_left(30)` / `move_right(30)` | Desplazamiento lateral sin girar | cm |
| `move_up(30)` / `move_down(30)` | Subir / bajar | cm |
| `rotate_clockwise(90)` / `rotate_counter_clockwise(90)` | Giro horario / antihorario | grados |
| `set_speed(20)` | Configurar velocidad admitida | cm/s |
| `streamon()` / `streamoff()` | Encender / apagar transmisión | — |
| `get_frame_read().frame` | Fotograma reciente | Matriz BGR |
| `send_rc_control(lr,fb,ud,yaw)` | Control de velocidades (no distancias) | -100…100 |

La especificación de desplazamientos admite rangos de 20–500 cm para comandos básicos y admite giros de amplitud limitada por el firmware. Los ejercicios reducen deliberadamente el tamaño de las maniobras. No envíes múltiples programas de control a un mismo dron.

---

# PARTE II · Imagen, video y pilotaje asistido

## 6. `take-picture.py`: fotografía desde la cámara

**Referencia:** [`examples/take-picture.py`](https://github.com/damiafuentes/DJITelloPy/blob/master/examples/take-picture.py).

El original activa `streamon()`, lee `get_frame_read().frame`, guarda un fotograma con `cv2.imwrite()` y contiene órdenes de vuelo. Para la primera clase **no necesitamos despegar**: utiliza `02_captura_foto.py`, que espera un fotograma válido y guarda `foto_tello.png`.

```powershell
.\.venv\Scripts\python.exe .\scripts\02_captura_foto.py
```

La imagen guardada proviene del video, no de un disparo fotográfico independiente. **Reto:** capturar la misma señal con diferente luz y comparar cuál permite distinguir mejor sus bordes.

## 7. `record-video.py`: grabar el recorrido

**Referencia:** [`examples/record-video.py`](https://github.com/damiafuentes/DJITelloPy/blob/master/examples/record-video.py).

Usa `cv2.VideoWriter` para escribir los fotogramas, un `Thread` para hacerlo concurrentemente y un programa principal que envía órdenes de vuelo. Conceptos: FPS deseados frente a cuadros reales, resolución, codec, liberación del archivo con `release()` y cierre de la transmisión. **Ejercicio:** adaptar el patrón para grabar primero 10 s con el dron inmóvil en tierra. Revisar en la PC que el archivo se reproduzca y no quede vacío.

## 8. `manual-control-opencv.py`: teclado y video

**Referencia:** [`examples/manual-control-opencv.py`](https://github.com/damiafuentes/DJITelloPy/blob/master/examples/manual-control-opencv.py).

Muestra video con `cv2.imshow()`, lee teclado con `cv2.waitKey()` y envía movimientos discretos. El código original **despega al inicio**: no lo ejecutes sin adaptar primero ese comportamiento. Teclas originales: W/S adelante/atrás, A/D lateral, E/Q giro, R/F subida/bajada, Esc terminar. **Reto:** separa «vista de cámara» de «autorizar despegue»; al iniciar debe mostrar video sin activar motores.

## 9. `manual-control-pygame.py`: control continuo

**Referencia:** [`examples/manual-control-pygame.py`](https://github.com/damiafuentes/DJITelloPy/blob/master/examples/manual-control-pygame.py).

Gestiona `KEYDOWN` y `KEYUP` y envía velocidades mediante `send_rc_control`. Integra video y estado de batería en una interfaz más rica que OpenCV. Conceptos: **evento** (tecla presionada), **estado** (velocidad deseada), **lazo** (actualizar comandos periódicamente) y retorno a ceros cuando se suelta la tecla. **Reto previo al vuelo:** estudiar si la interfaz deja velocidades en cero cuando se cierra la ventana o falla la transmisión.

## 10. `panorama.py` y `panoramaModule.py`: secuencia de imágenes

**Referencias:** [`panorama.py`](https://github.com/damiafuentes/DJITelloPy/blob/master/examples/panorama/panorama.py) · [`panoramaModule.py`](https://github.com/damiafuentes/DJITelloPy/blob/master/examples/panorama/panoramaModule.py).

El lanzador conecta y llama a una variante de barrido. El módulo contiene cuatro funciones para tomar varias fotografías mientras el dron gira. **No genera automáticamente una imagen panorámica fusionada**: guarda fotos. Una versión original incluye un ascenso de 500 cm: **no se debe ejecutar esa maniobra en un aula**. Estudia primero la secuencia de ángulos y fotografías en papel. Para unir las fotos se requiere un proceso de *stitching* adicional en OpenCV.

**Nota sobre el repositorio:** no todos sus archivos de ejemplo corresponden al hardware de este taller. Aquí se desarrollan únicamente aquellos aplicables al Tello estándar; los demás no forman parte del itinerario.

---

# PARTE III · Reconocimiento visual de marcas con OpenCV

## 11. ¿Qué es ArUco y por qué lo usamos?

Un marcador **ArUco** es un patrón cuadrado blanco y negro con un ID digital, identificable en la imagen. Podemos imprimir varios y colocarlos verticalmente como estaciones de inspección. **No se necesita ningún accesorio electrónico ni comando especial del Tello**: el dron solo transmite video y **Python procesa los fotogramas en la computadora**.

La cámara frontal da una observación *relativa a lo que ve*, pero sin calibración adicional no ofrece una posición métrica fiable respecto de la habitación. En la secuencia formativa, el marcador responde «¿qué estación veo?», mientras que los tramos de desplazamiento siguen siendo órdenes medidas, ensayadas y autorizadas por el operador.

## 12. Crear las marcas 1, 2 y 3 sin conectar el dron

```powershell
.\.venv\Scripts\python.exe .\scripts\03_crear_marcadores_aruco.py
```

Se crean archivos `marcadores/marca_1.png`, `marca_2.png`, `marca_3.png`. Utilizamos el diccionario `DICT_4X4_50`; conserva el borde blanco exterior, imprime en papel mate, registra el tamaño físico y evita deformar la figura. Antes de volar, comprueba el tamaño mínimo reconocible desde la distancia real.

## 13. Reconocer una marca dentro de una fotografía

```powershell
.\.venv\Scripts\python.exe .\scripts\04_reconocer_marca_en_foto.py .\marcadores\marca_1.png
```

El programa usa `cv2.aruco.ArucoDetector()` para identificar las esquinas y el ID y guarda `resultado_deteccion.png`. Repite con las marcas 2 y 3 y después con una foto que contenga dos. **Pregunta:** ¿qué ocurre si el papel aparece muy pequeño, oscuro o parcialmente tapado?

## 14. Reconocer marcas desde el video real, sin despegar

Coloca una marca **frente a la cámara frontal del dron apoyado en el suelo**. Conecta la computadora a su Wi-Fi y ejecuta:

```powershell
.\.venv\Scripts\python.exe .\scripts\05_monitor_marcas_camara.py
```

La ventana mostrará el ID detectado durante un máximo de 30 s; presiona `Q` para terminar. Filtra marcas demasiado pequeñas por área en píxeles. **Este programa no activa motores.** Registra en qué distancia, inclinación e iluminación deja de reconocerse.

## 15. Ruta lógica por estaciones, totalmente simulada

```powershell
.\.venv\Scripts\python.exe .\scripts\06_ruta_visual_simulada.py
```

El programa simula las observaciones y exige tres confirmaciones consecutivas para validar cada ID en este orden:

```text
ESTACIÓN 1 (partida) ──► ESTACIÓN 2 (giro) ──► ESTACIÓN 3 (destino)
```

**Máquina de estados:**

```text
ESPERAR_1  --detectar 1 tres veces-->  TRAMO_1
TRAMO_1   --termina-->               ESPERAR_2
ESPERAR_2 --detectar 2 tres veces-->  GIRO + TRAMO_2
TRAMO_2   --termina-->               ESPERAR_3
ESPERAR_3 --detectar 3 tres veces-->  FINALIZAR
Cualquier etapa --timeout-->         ABORTAR
```

Tres lecturas reducen respuestas a una detección aislada, pero no garantizan que el contenido del video sea nuevo ni que el ID sea infalible. **Reto:** introduce lecturas de marcas fuera de orden y comprueba que no se avance.

## 16. Ruta física visual supervisada (nivel avanzado)

El script `07_ruta_visual_supervisada.py` demuestra cómo unir **detección ArUco en la PC** con **maniobras programadas del Tello estándar**.

```powershell
.\.venv\Scripts\python.exe .\scripts\07_ruta_visual_supervisada.py
```

De forma predeterminada **solo imprime el plan**; no conecta ni despega. Si el instructor desea una prueba física, deberá medir la posición de las tres marcas, validar cada tramo por separado, asegurar que la cámara pueda observar la marca siguiente **sin maniobras exploratorias**, comprobar que el recinto tiene espacio suficiente, disponer de un plan de contingencia y activar dos autorizaciones en el código (`AUTORIZACION_OPERADOR` y `TRAMOS_MEDIDOS_Y_ENSAYADOS`). Además deberá confirmar mediante `VOLAR` antes del despegue. El umbral conservador es 60 % de batería.

**Comportamiento físico pretendido, únicamente después de ensayo:**

1. Despegar y mantener estabilidad con marcador 1 visible al frente.
2. Reconocer ID 1 varias veces; ejecutar un **tramo corto, fijo y prevalidado**.
3. Detectar ID 2. Si aparece estable, ejecutar el giro y otro tramo corto previsto.
4. Detectar ID 3. Terminar y aterrizar.
5. Si algún ID no se confirma a tiempo, **no realizar una búsqueda a ciegas**: abortar la misión e intentar el aterrizaje supervisado.

**Límites técnicos importantes:** esto es **automatización por eventos visuales y tramos discretos**. No es seguimiento continuo de una línea de visión, navegación de precisión, planificación de obstáculos ni corrección automática del error de posición. `get_frame_read()` puede proporcionar un fotograma rezagado o repetido; la visión frontal no permite detectar todo lo que hay debajo o detrás del dron. La rutina está **sin validar en un Tello físico**.

### Hacia autonomía visual más avanzada (actividad de diseño, no de vuelo)

Para estudiar corrección de rumbo a partir de la imagen, los alumnos pueden calcular el error horizontal normalizado entre el centro del marcador y el centro del video:

\[
e_x=\frac{u_{marca}-u_{centro}}{W/2}
\]

La ley proporcional conceptual es \(\omega_z=-K_p e_x\), con saturación y una zona muerta. El signo depende de la convención de coordenadas y debe verificarse en simulación. **No copies esta fórmula directamente a los motores**: primero hay que calibrar cámara, retardo del video, ganancias, distancia, límites de control y prevención de colisiones. La detección de una marca nunca autoriza por sí misma un acercamiento.

---

## 17. Proyecto integrador: inspección inteligente de tres estaciones

**Problema:** una instalación de servicio tiene tres puntos con señales ArUco. Un equipo diseña la secuencia de inspección, verifica el reconocimiento y comprueba si una misión puede completarse sin saltarse estaciones.

**Entregables del estudiante:**

1. Tres marcadores ArUco impresos, visibles desde las posiciones predefinidas.
2. Evidencias `resultado_deteccion.png` y registro del monitor frontal sin vuelo.
3. Máquina de estados con secuencia 1 → 2 → 3, lecturas erróneas y condición de tiempo máximo.
4. Plano físico medido y checklist firmado por el operador si se propone vuelo real.
5. Conclusión: diferencia entre «ver una señal», «saber dónde estoy» y «poder llegar con seguridad».

### Rúbrica mínima

| Criterio | Evidencia |
|---|---|
| Configuración correcta | El `.venv` importa DJITelloPy y ArUco |
| Visión | Reconoce las tres marcas en fotografías |
| Orden | La FSM rechaza etapas fuera de secuencia |
| Confiabilidad | Ante falta de marca, la misión expira y no inventa coordenadas |
| Seguridad | Demuestra simulación antes del vuelo y autorización previa |
| Comunicación técnica | Explica limitaciones de cámara y deriva |

## 18. Solución de problemas

| Síntoma | Solución |
|---|---|
| `Import "djitellopy" could not be resolved` | Selecciona `.venv` en VS Code e instala en **ese mismo intérprete** |
| `No such file or directory` | Abre `TelloPython` como carpeta y ejecuta rutas con `scripts\` |
| `No module named cv2` | Instala `opencv-contrib-python` en `.venv` |
| `cv2.aruco` no disponible | No combines paquetes OpenCV: conserva **solo `opencv-contrib-python`** |
| `streamon` devuelve `Unknown command` | Revisa firmware mediante la app de Tello y prueba Wi-Fi |
| ID no reconocido | Verifica diccionario, borde blanco, enfoque, tamaño aparente y luz |
| ID cambia entre cuadros | Marca pequeña, reflejos, desenfoque, interferencia o imagen rezagada |
| La ruta parece correcta en papel pero deriva | Distancias y giros de SDK no garantizan posición absoluta |

## 19. Propuesta de impartición (cuatro sesiones)

| Sesión | Duración de referencia | Foco |
|---|---|---|
| 1 · Primer contacto | 50–70 min | Instalación, conexión, seguridad, comandos |
| 2 · Cámara y control | 60–90 min | Captura, video, panoramas, teclado |
| 3 · Marcas visuales | 60–90 min | Generar, fotografiar y reconocer ArUco |
| 4 · Autonomía supervisada | 75–100 min | Máquina de estados, estaciones, fallos, recorrido lógico |

La cuarta sesión solo incorpora un vuelo físico si la revisión de seguridad y el ensayo técnico lo permiten; de otro modo puede completarse mediante simulación y análisis de imágenes. No es necesario modificar MissionLab 1.0, 2.0 o 3.0 para realizar los ejercicios.

---

**Referencias:**
- DJITelloPy, https://github.com/damiafuentes/DJITelloPy
- Ejemplos originales, https://github.com/damiafuentes/DJITelloPy/tree/master/examples
- Referencia de la biblioteca, https://djitellopy.readthedocs.io/en/latest/tello/
- Ryze, *Tello SDK 1.3*, https://dl-cdn.ryzerobotics.com/downloads/tello/20180910/Tello%20SDK%20Documentation%20EN_1.3.pdf
- OpenCV, *Installation with pip*, https://docs.opencv.org/4.x/db/dd1/tutorial_py_pip_install/py_pip_install.html
- OpenCV, ArUco detection, https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html

**Versión:** 2.0 de este tutorial · DJI Tello estándar exclusivamente · 28-oct-2026. Este material no afirma haber validado físicamente ninguna trayectoria de vuelo.
