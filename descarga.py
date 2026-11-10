"""Descarga los resúmenes mensuales de lluvia y temperatura del SMN (CONAGUA).

Uso:
    python descarga.py                 # de 2013 al mes actual, omite los ya descargados
    python descarga.py --desde 2026    # solo desde 2026
    python descarga.py --forzar        # vuelve a descargar aunque ya existan
"""

import argparse
import time
from datetime import date
from pathlib import Path

import requests

import config

ANIO_INICIAL = 2013

# Variable -> abreviatura usada por el SMN en el nombre del archivo.
VARIABLES = {
    "Lluvia": "Lluv",
    "TemperaturaMinima": "TMin",
    "TemperaturaMedia": "TMed",
    "TemperaturaMaxima": "TMax",
}

# Parte fija del nombre de archivo: AAAAMM + "010000" + variable + ".csv"
CODIGO_ARCHIVO = "010000"

# Los archivos se guardan en Data/<año>/
CARPETA_DATOS = Path(__file__).resolve().parent / "Data"
PAUSA_SEGUNDOS = 1
TIMEOUT_SEGUNDOS = 30


def periodos(desde, hasta):
    """Genera (año, mes) desde enero de `desde` hasta `hasta` (una fecha)."""
    for anio in range(desde, hasta.year + 1):
        ultimo_mes = hasta.month if anio == hasta.year else 12
        for mes in range(1, ultimo_mes + 1):
            yield anio, mes


def descargar(sesion, nombre_archivo, destino):
    """Descarga un archivo. Regresa True si se guardó, False si no existe o falló."""
    url = f"{config.URL_DESCARGA}{nombre_archivo}"
    try:
        respuesta = sesion.get(url, timeout=TIMEOUT_SEGUNDOS)
    except requests.RequestException as error:
        print(f"  Error de conexión con {nombre_archivo}: {error}")
        return False

    if respuesta.status_code != 200:
        print(f"  No disponible ({respuesta.status_code}): {nombre_archivo}")
        return False

    destino.write_bytes(respuesta.content)
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--desde", type=int, default=ANIO_INICIAL,
                        help=f"año inicial (por defecto {ANIO_INICIAL})")
    parser.add_argument("--forzar", action="store_true",
                        help="descargar aunque el archivo ya exista")
    args = parser.parse_args()

    descargados = omitidos = fallidos = 0

    with requests.Session() as sesion:
        for anio, mes in periodos(args.desde, date.today()):
            for variable, abreviatura in VARIABLES.items():
                nombre_archivo = f"{anio}{mes:02d}{CODIGO_ARCHIVO}{abreviatura}.csv"
                destino = CARPETA_DATOS / str(anio) / nombre_archivo

                if destino.exists() and not args.forzar:
                    omitidos += 1
                    continue

                destino.parent.mkdir(parents=True, exist_ok=True)
                if descargar(sesion, nombre_archivo, destino):
                    print(f"Descargado: {variable} {mes:02d}/{anio}")
                    descargados += 1
                else:
                    fallidos += 1
                time.sleep(PAUSA_SEGUNDOS)

    print(f"\nListo. Descargados: {descargados}, ya existían: {omitidos}, "
          f"no disponibles o con error: {fallidos}")


if __name__ == "__main__":
    main()
