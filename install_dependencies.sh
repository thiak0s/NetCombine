#!/bin/bash

echo "Este script instalará las dependencias necesarias para la herramienta ScanFull v1.0."
echo "Asegúrate de tener los privilegios necesarios para instalar paquetes en el sistema."
echo "Presiona Enter para continuar o Ctrl+C para cancelar."
read -r

# Función para instalar pip y herramientas de Python
install_python_packages() {
    apt-get install -y python3 python3-pip
    pip3 install termcolor pyfiglet platform
}

# Función para instalar herramientas mediante APT
install_apt_packages() {
    apt-get update
    apt-get install -y nmap fierce theharvester sublist3r testssl.sh
}

# Función para descargar e instalar nikto
install_nikto() {
    apt-get install -y nikto
}

# Función principal
main() {
    # Instalar herramientas mediante APT
    install_apt_packages

    # Instalar pip y herramientas de Python
    install_python_packages

    # Instalar nikto
    install_nikto

    # Agregar directorios al PATH
    echo 'export PATH=$PATH:/usr/share/nmap/scripts' >> ~/.bashrc
    echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc

    # Recargar la configuración del shell
    source ~/.bashrc

    echo "Herramientas instaladas y configuradas correctamente."
}

# Ejecutar el script principal
main
