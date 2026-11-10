# smn-conagua-resumenes

Descarga automática de los resúmenes mensuales de **lluvia** y **temperatura** (mínima, media y máxima) que publica el [Servicio Meteorológico Nacional (SMN) de CONAGUA](https://smn.conagua.gob.mx/).

Cada archivo es un CSV con una fila por estación climatológica (longitud, latitud, estado, clave, nombre y valor del mes).

## Datos incluidos

El repositorio ya trae los CSV descargados en [`Data/`](Data/), organizados en una carpeta por año, de **enero de 2013 a octubre de 2026** (166 meses × 4 variables = 664 archivos), así que puedes usarlos directamente sin correr el script.

Para traer los meses más recientes, ejecuta `python descarga.py`: solo descarga los archivos que todavía no existen.

## Requisitos

- Python 3.9 o superior

## Instalación

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Uso

```bash
python descarga.py                 # de 2013 al mes actual
python descarga.py --desde 2026    # solo desde 2026
python descarga.py --forzar        # vuelve a descargar archivos ya existentes
```

Los archivos se guardan en una carpeta por año dentro de `Data/`, con el nombre que usa el SMN (`AAAAMM010000<variable>.csv`):

```
Data/
├── 2013/
│   ├── 201301010000Lluv.csv
│   ├── 201301010000TMax.csv
│   └── ...
├── ...
└── 2026/
    └── 202610010000Lluv.csv
```

| Abreviatura | Variable            |
|-------------|---------------------|
| `Lluv`      | Lluvia acumulada    |
| `TMin`      | Temperatura mínima  |
| `TMed`      | Temperatura media   |
| `TMax`      | Temperatura máxima  |

Los archivos que ya existen se omiten, así que puedes correr el script cada mes para traer solo lo nuevo. El SMN publica cada mes después de que termina; los meses aún no publicados se reportan como "no disponible". El script espera 1 segundo entre peticiones para no saturar el servidor.

## Fuente de los datos

Los datos son propiedad del SMN / CONAGUA. Este proyecto solo automatiza su descarga.

## Licencia

[MIT](LICENSE)
