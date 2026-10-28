"""Verificaciones offline: no requiere dron, ni Wi-Fi, ni djitellopy."""
from pathlib import Path
import ast
import importlib.util
import cv2

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check():
    files = sorted(SCRIPTS.glob('*.py'))
    assert len(files) == 8
    for path in files:
        ast.parse(path.read_text(encoding='utf-8'))
        s = path.read_text(encoding='utf-8').lower()
        assert all(word not in s for word in ('enable_mission_pads','get_mission_pad_id','tello edu'))
    print('[OK] 8 scripts analizados y sin API incompatible')

    dic = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    detector = cv2.aruco.ArucoDetector(dic, cv2.aruco.DetectorParameters())
    for i in (1,2,3):
        img = cv2.imread(str(ROOT/'marcadores'/f'marca_{i}.png'))
        assert img is not None
        _, ids, _ = detector.detectMarkers(img)
        assert ids is not None and ids.flatten().tolist() == [i]
    print('[OK] Marcas 1, 2 y 3 detectadas en OpenCV')

    m = load('06_ruta_visual_simulada')
    assert m.ejecutar(m.LECTURAS)
    assert not m.ejecutar([1,1,1,3,3,3])
    print('[OK] FSM aprueba la ruta y rechaza marca fuera de orden')

    for filename in ('01_vuelo_basico.py','07_ruta_visual_supervisada.py'):
        code=(SCRIPTS/filename).read_text()
        assert 'AUTORIZACION_OPERADOR = False' in code or 'AUTORIZADO_POR_OPERADOR = False' in code
        assert 'from djitellopy import Tello' in code
    assert 'TRAMOS_MEDIDOS_Y_ENSAYADOS = False' in (SCRIPTS/'07_ruta_visual_supervisada.py').read_text()
    print('[OK] Modalidades de vuelo bloqueadas por defecto')

if __name__ == '__main__':
    check()
