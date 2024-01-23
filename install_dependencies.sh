#!/bin/bash

echo "Este script instalará las dependencias necesarias para la herramienta NetCombine v1.0."
echo "Asegúrate de tener los privilegios necesarios para instalar paquetes en el sistema."
echo "Presiona Enter para continuar o Ctrl+C para cancelar."
read -r
install_python_packages() {
    apt-get install -y python3 python3-pip
    pip3 install termcolor pyfiglet platform
}
install_apt_packages() {
    apt-get update
    apt-get install -y nmap fierce theharvester sublist3r testssl.sh
}
install_nikto() {
    apt-get install -y nikto
}
main() {
    install_apt_packages
    install_python_packages
    install_nikto

    echo 'export PATH=$PATH:/usr/share/nmap/scripts' >> ~/.bashrc
    echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc

    source ~/.bashrc

    echo "Herramientas instaladas y configuradas correctamente."
}
main
