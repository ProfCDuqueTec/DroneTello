# Evidencia de verificación offline

**Fecha:** 2026-10-28.

- 8 scripts Python: sintaxis válida.
- Marcas 1, 2 y 3: generadas y reconocidas correctamente mediante OpenCV 4.13 en este entorno.
- Máquina de estados: acepta secuencia correcta y rechaza una marca fuera de orden.
- Los dos scripts que contemplan motores inician con vuelo bloqueado.
- Su modo simulación funciona sin importar DJITelloPy ni conectarse a una aeronave.
- No se incluyen llamadas a reconocimiento nativo de marcas no compatible.

**Limitación:** no se ha realizado un ensayo de vuelo físico ni mediciones con la cámara de un Tello real. El proyecto avanzado es un patrón didáctico supervisado con tramos prevalidables, no un sistema de navegación autónoma segura universal.
