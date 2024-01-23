# NetCombine v1.0

## Descripción
NetCombine es una herramienta de escaneo y análisis de red diseñada para usuarios avanzados en ciberseguridad y pentesting. Integrando diversas herramientas como nmap, testssl, fierce, theHarvester, sublist3r, entre otras, NetCombine permite realizar un análisis exhaustivo de objetivos de red y la detección de vulnerabilidades.

**Creador:** thiak0s - 2024

## Características Principales
- Escaneo de objetivos individuales o subredes completas.
- Realiza escaneos específicos como ping, whois, nslookup, dig, host, fierce, theHarvester, sublist3r, y testssl.
- Integración de escaneos NSE Nmap con opciones como OS fingerprinting, aggressive scan, service version detection, entre otros.
- Opción para guardar resultados en un archivo externo.
- Soporte para especificar puertos a escanear.

## Requisitos
- Python 3.x
- Módulos requeridos: argparse, subprocess, logging, termcolor, pyfiglet, concurrent.futures, ipaddress, platform.

## Instalación de Dependencias
```bash
pip install termcolor pyfiglet
```

## Uso
```bash
python netcombine.py <objetivo> [-o <output_file>] [-p <puertos>]
```

### Parámetros
- `<objetivo>`: La dirección IP, subred o archivo con lista de objetivos a escanear.
- `-o, --output <output_file>`: Guardar resultados en un archivo externo.
- `-p, --puertos <puertos>`: Puertos a escanear, separados por coma.

### Ejemplos de Uso
1. Escanear una dirección IP:
   ```bash
   python netcombine.py 192.168.1.1 -o output.txt -p 80,443
   ```

2. Escanear una subred:
   ```bash
   python netcombine.py 192.168.1.0/24 -o output.txt -p 80,443
   ```

3. Escanear desde un archivo:
   ```bash
   python netcombine.py targets.txt -o output.txt -p 80,443
   ```

4. Obtener información de ayuda:
   ```bash
   python netcombine.py --help
   ```

## Información del Autor
Herramienta creada por [thiak0s](https://github.com/thiak0s) en 2024. NetCombine está diseñada para ser utilizada de manera ética y responsable en actividades de ciberseguridad y pentesting.

Recuerda utilizar esta herramienta de manera ética y responsable
