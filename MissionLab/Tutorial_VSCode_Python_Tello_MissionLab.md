# Guía rápida | Preparar VS Code para Drone Commander MissionLab 1.0 y 2.0
**Tec de Monterrey · Campus León · Taller Drone Commander**  
**Sistema:** Windows 10/11 · **Duración:** instalación inicial breve · **Objetivo:** ejecutar los archivos `.py` exportados por MissionLab.

> **Precisión técnica:** el dron utiliza el **Tello SDK oficial**; la librería de Python que emplea MissionLab es **DJITelloPy**, un proyecto de terceros basado en ese SDK. Para MissionLab 1.0 y 2.0 **solo es necesario instalar `djitellopy`**; no hace falta instalar OpenCV por separado.

## 1. Instala los programas necesarios (una sola vez)
1. Instala **Python** desde <https://www.python.org/downloads/> (si ya tienes Python funcional, no lo reinstales).
2. Instala **Visual Studio Code** desde <https://code.visualstudio.com/>.
3. Abre VS Code → **Extensiones** (`Ctrl+Shift+X`) → busca **Python**, de **Microsoft**, y pulsa **Install**.

## 2. Crea el proyecto
1. En Windows, crea una carpeta, por ejemplo: `Documentos\DroneCommander`.
2. En VS Code ve a **File → Open Folder** (Archivo → Abrir carpeta) y elige `DroneCommander`.
3. Pulsa `Ctrl+Shift+P` → **Python: Create Environment** → **Venv** → selecciona tu instalación de Python.
4. Confirma que apareció la carpeta `.venv` y selecciona ese intérprete con `Ctrl+Shift+P` → **Python: Select Interpreter** → **.venv**.

> Utilizamos un **entorno virtual** para que VS Code, las bibliotecas y los programas exportados utilicen la misma instalación de Python.

## 3. Instala la librería del Tello
En VS Code abre **Terminal → New Terminal**. Verifica que la terminal esté ubicada en `DroneCommander` e introduce:

```powershell
.\.venv\Scripts\python.exe -m pip install djitellopy
```

Comprueba que la instalación funciona:

```powershell
.\.venv\Scripts\python.exe -c "from djitellopy import Tello; print('DJITelloPy lista')"
```

**Resultado esperado:** `DJITelloPy lista`. Estas rutas explícitas evitan confundir distintos intérpretes de Python en Windows.

## 4. Ejecuta el Python exportado desde MissionLab
1. En MissionLab 1.0 o 2.0, termina la misión válida y elige **Exportar Python**.
2. Copia el archivo `.py` descargado a `Documentos\DroneCommander` (la carpeta que abriste en VS Code).
3. Abre el archivo desde el explorador de VS Code. Para **simular sin conectar el dron**, ejecuta en la terminal (cambia el nombre por el de tu archivo):

```powershell
.\.venv\Scripts\python.exe ".\DroneCommander_Equipo_Aguila_A.py"
```

**Resultado esperado:** se imprimen los bloques de la misión y el resumen de la simulación. **No incluyas `--fly`** en esta prueba.

## 5. Comprueba la conexión con el Tello, sin despegar (opcional)
1. Enciende el Tello con batería suficiente y conecta la computadora a la red Wi-Fi `TELLO-XXXXXX`. Es normal que Windows indique **Sin Internet**.
2. Crea en VS Code un archivo `prueba_conexion.py` con este código:

```python
from djitellopy import Tello

dron = Tello()
try:
    dron.connect()
    print("Tello conectado. Batería:", dron.get_battery(), "%")
finally:
    dron.end()
```

3. Ejecútalo desde la terminal:

```powershell
.\.venv\Scripts\python.exe ".\prueba_conexion.py"
```

**Resultado esperado:** mensaje de conexión y porcentaje de batería. **Esta prueba no hace despegar al dron**.

## Errores frecuentes
| Mensaje | Solución |
|---|---|
| `No such file or directory` | El archivo `.py` no está en la carpeta del proyecto o el nombre es distinto. Compruébalo en el explorador de VS Code. |
| `Import "djitellopy" could not be resolved` | Selecciona el intérprete `.venv` y ejecuta la instalación del paso 3. |
| Error de conexión con el Tello | Comprueba encendido, batería, conexión Wi-Fi del Tello y permisos de red/firewall de Windows. |

## Seguridad: simulación ≠ autorización de vuelo
- Los archivos exportados de MissionLab **simulan por defecto**. `--fly` solicita un vuelo físico y el código lo bloquea mediante `AUTORIZACION_OPERADOR = False`.
- **No cambies esa autorización ni ejecutes `--fly` para hacer las pruebas de este tutorial.** Un operador capacitado debe revisar primero el espacio, trayectoria, distancias, batería y procedimiento de aterrizaje/emergencia.
- **Los mapas de MissionLab 2.0 son ciudades ficticias, no planos de vuelo reales.** Una simulación exitosa no autoriza ejecutar esa ruta físicamente.

**Comprobación final:** si la importación funciona, puedes ejecutar el `.py` exportado en simulación y puedes leer la batería mediante Wi-Fi, el entorno de VS Code está preparado.

### Fuentes
- Tello SDK y biblioteca DJITelloPy: <https://github.com/damiafuentes/DJITelloPy>
- Instalación de DJITelloPy: <https://pypi.org/project/djitellopy/>
- Entornos Python de VS Code: <https://code.visualstudio.com/docs/python/environments>
