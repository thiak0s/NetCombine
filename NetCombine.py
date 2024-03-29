import argparse
import concurrent.futures
import ipaddress
import logging
import platform
import subprocess
from termcolor import colored

logging.basicConfig(filename='NetCombine.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def print_author_info():
    print(colored("_____   __    ______________                ______ _____             ", color="green", attrs=["bold"]))
    print(colored("___  | / /______  /__  ____/____________ ______  /____(_)___________ ", color="green", attrs=["bold"]))
    print(colored("__   |/ /_  _ \\  __/  /    _  __ \\_  __ `__ \\_  __ \\_  /__  __ \\  _ \\", color="green", attrs=["bold"]))
    print(colored("_  /|  / /  __/ /_ / /___  / /_/ /  / / / / /  /_/ /  / _  / / /  __/", color="green", attrs=["bold"]))
    print(colored("/_/ |_/  \\___/\\__/ \\____/  \\____//_/ /_/ /_//_.___//_/  /_/ /_/\\___/ ", color="green", attrs=["bold"]))
    print(colored("\t\t\t\t\t\t\t\t\tv1.0.1\n", color="red", attrs=["bold"]))

    print(colored("--- Información del Autor y Descripción ---", color="cyan"))
    print(colored("***************** NetCombine **************\n", color="green"))
    print(colored("[Herramienta creada por thiak0s - 2024]\n", color="yellow"))
    print(colored("Utilidad para Escaneo y Análisis de Red que integra nmap, testssl, fierce, theHarvester, sublist3r", color="cyan"))
    print(colored("y otras más, para el análisis exhaustivo de objetivos de red y detección de vulnerabilidades.", color="cyan"))
    print(colored("Diseñada para colaboradores en ciberseguridad y pentesting.", color="cyan"))
    print(colored("***** Recuerda utilizar esta herramienta de manera ética y responsable. *****\n", color="cyan"))

def ejecutar_comando(comando):
    try:
        resultado = subprocess.check_output(comando, text=True, shell=True)
        return resultado
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al ejecutar el comando: {e}")
        return f"Error al ejecutar el comando: {e}"

def ejecutar_comandos_y_guardar_resultados(comandos, objetivo, output_file=None):
    for comando in comandos:
        try:
            print("-" * 150)
            resultado = ejecutar_comando(comando.format(ip=objetivo, output=output_file))
            print(colored(f"Resultados de {comando.split()[0]}:", color="yellow"))
            print(resultado)
            if output_file:
                with open(output_file, 'a') as file:
                    file.write("-" * 100 + '\n')
                    file.write(f"Resultados de {comando.split()[0]}:\n{resultado}\n")
        except FileNotFoundError:
            logging.warning(f"{comando.split()[0]} no está disponible en este sistema.")
        except Exception as e:
            logging.error(f"Error al ejecutar el comando {comando}: {e}")

def escanear_objetivo(ip_objetivo, output_file=None, puertos=None):
    comandos_adicionales = [
        f'ping -c 3 {ip_objetivo}' if platform.system().lower() != 'windows' else f'ping -n 3 {ip_objetivo}',
        f'whois {ip_objetivo}',
        f'nslookup {ip_objetivo}',
        f'dig {ip_objetivo}',
        f'host -a {ip_objetivo}',
        f'fierce --domain {ip_objetivo}',
        f'theHarvester -d {ip_objetivo} -b crtsh -v',
        f'sublist3r -d {ip_objetivo}',
        f'testssl {ip_objetivo}'
    ]

    for comando_adicional in comandos_adicionales:
        try:
            resultado_comando_adicional = ejecutar_comando(comando_adicional)
            print("-" * 150)
            print(colored(f"Resultados de {comando_adicional.split()[0]}:", color="yellow"))
            print(resultado_comando_adicional)
            if output_file:
                with open(output_file, 'a') as file:
                    file.write(f"Resultados de {comando_adicional.split()[0]}:\n{resultado_comando_adicional}\n")
        except FileNotFoundError:
            logging.warning(f"{comando_adicional.split()[0]} no está disponible en este sistema.")
        except Exception as e:
            logging.error(f"Error al ejecutar el comando {comando_adicional}: {e}")

    print(colored("\n\nEscaneos NSE Nmap", color="yellow"))

    scripts_nmap = [
        ('-O', 'OS fingerprinting'),
        ('-A', 'Aggressive scan'),
        ('-sV', 'Service version detection'),
        ('--script default', 'Default scripts'),
        ('--script vuln', 'Vulnerability scripts'),
        ('--script malware', 'Malware scripts'),
        ('--script ssl-enum-ciphers', 'SSL/TLS ciphers'),
        ('--script brute', 'Brute force scripts'),
        ('--script dos', 'Denial of Service scripts')
    ]

    for script, description in scripts_nmap:
        comando_nmap = f'nmap -Pn {script} {ip_objetivo}' if not puertos else f'nmap -Pn {script} -p {puertos} {ip_objetivo}'
        print(colored(f"\n{description}", color="yellow", attrs=["bold"]))
        print("-" * 200)
        print(colored(f"Command: {comando_nmap}", color="cyan"))
        resultado_nmap = ejecutar_comando(comando_nmap)
        print(resultado_nmap)
        if output_file:
            with open(output_file, 'a') as file:
                file.write(f"\n{description}:\nCommand: {comando_nmap}\n{'-' * 100}\n{resultado_nmap}\n")

def escanear_red(subnet, output_file=None, puertos=None):
    objetivos = [str(ip) for ip in ipaddress.IPv4Network(subnet, strict=False)]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda objetivo: escanear_objetivo(objetivo, output_file, puertos), objetivos)

def escanear_desde_archivo(archivo, output_file=None, puertos=None):
    with open(archivo, 'r') as file:
        lineas = file.readlines()

    for linea in lineas:
        objetivo = linea.strip()
        if '/' in objetivo:
            escanear_red(objetivo, output_file, puertos)
        else:
            escanear_objetivo(objetivo, output_file, puertos)

def main():
    print_author_info()

    parser = argparse.ArgumentParser(description='Herramienta de Escaneo y Análisis de Red')
    parser.add_argument('objetivo', metavar='objetivo', type=str, help='La dirección IP, subred o archivo con lista de objetivos a escanear')
    parser.add_argument('-o', '--output', metavar='output_file', type=str, help='Guardar resultados en un archivo externo')
    parser.add_argument('-p', '--puertos', metavar='puertos', type=str, help='Puertos a escanear (separados por coma)')

    args = parser.parse_args()

    if args.objetivo.lower() == '--help' or args.objetivo.lower() == '-h':
        print_author_info()
        return

    objetivo = args.objetivo
    output_file = args.output
    puertos = args.puertos

    try:
        if '/' in objetivo:
            escanear_red(objetivo, output_file, puertos)
        elif objetivo.lower().endswith('.txt'):
            escanear_desde_archivo(objetivo, output_file, puertos)
        else:
            escanear_objetivo(objetivo, output_file, puertos)
    except Exception as e:
        logging.exception(f"Error durante el escaneo: {e}")

if __name__ == "__main__":
    main()
