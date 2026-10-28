"""Máquina de estados para 3 marcas: sin dron ni OpenCV.
Cada estación exige 3 detecciones seguidas; timeout ficticio por longitud de lectura.
"""
RUTA = [
    {'marca': 1, 'maniobra': 'INICIAR'},
    {'marca': 2, 'maniobra': 'GIRAR 90 DERECHA'},
    {'marca': 3, 'maniobra': 'REGISTRAR ENTREGA Y FINALIZAR'},
]
LECTURAS = [None, 1, 1, 1, None, 2, 2, 2, None, 3, 3, 3]


def ejecutar(lecturas):
    paso = 0
    confirmaciones = 0
    for lectura in lecturas:
        esperado = RUTA[paso]['marca']
        confirmaciones = confirmaciones + 1 if lectura == esperado else 0
        print(f'Esperando {esperado} | lectura={lectura} | consecutivas={confirmaciones}')
        if confirmaciones == 3:
            print('ESTACIÓN OK:', RUTA[paso]['maniobra'])
            paso += 1
            confirmaciones = 0
            if paso == len(RUTA):
                print('MISIÓN LÓGICA COMPLETA')
                return True
    print('MISIÓN INCOMPLETA: faltan marcas o confirmaciones')
    return False


if __name__ == '__main__':
    assert ejecutar(LECTURAS)
    assert not ejecutar([1, 1, 1, 3, 3, 3])
