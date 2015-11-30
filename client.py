#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Cliente SIP
"""

import socket
import sys

try:
    sys.argv[0] = 'client.py'
    METODO = sys.argv[1]
    RECEPTOR = sys.argv[2].split('@')[0]
    IP_RECEPTOR = sys.argv[2].split('@')[1].split(':')[0]
    PUERTO_RECEPTOR = int(sys.argv[2].split('@')[1].split(':')[1])
except IndexError:
    sys.exit('Usage: python3 client.py method receiver@IP:SIPport')


# Contenido que vamos a enviar
LINE = METODO + ' ' + 'sip:' + RECEPTOR + '@' + IP_RECEPTOR + ' ' + 'SIP/2.0'

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((IP_RECEPTOR, PUERTO_RECEPTOR))

print("Enviando: " + LINE)
my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
data = my_socket.recv(1024)
datos = data.decode('utf-8')
print('Recibido -- ', datos)
datos_lista = datos.split('\r\n\r\n')
RCV = datos_lista[0:3]

if RCV == ['SIP/2.0 100 Trying', 'SIP/2.0 180 Ring', 'SIP/2.0 200 OK']:
    ACK = 'ACK' + ' ' + 'sip:' + RECEPTOR + '@' + IP_RECEPTOR + ' ' + 'SIP/2.0'
    print('Enviando: ' + ACK)
    my_socket.send(bytes(ACK, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)
    datos = data.decode('utf-8')
    print('Recibido -- ', datos)


# Cerramos todo
print("Terminando socket...")
my_socket.close()
print("Fin.")
