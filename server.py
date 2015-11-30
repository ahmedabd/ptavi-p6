#!/usr/bin/python3
# -*- coding: utf-8 -*-


import socketserver
import sys
import os

try:
    sys.argv[0] = 'server.py'
    IP = sys.argv[1]
    PUERTO = int(sys.argv[2])
    FICH_AUDIO = sys.argv[3]
except IndexError:
    sys.exit('Usage: python3 server.py IP port audio_file')


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    RecibimoS peticiones SIP y enviamos mensajes o servicios
    """

    def handle(self):
        while 1:
            line = self.rfile.read()
            linea = line.decode('utf-8')
            linea_lista = linea.split()

            print("El cliente nos manda " + line.decode('utf-8'))
            if not line:
                break
            if linea_lista[0] == 'INVITE':
                self.wfile.write(b'SIP/2.0 100 Trying' + b'\r\n\r\n' + b'SIP/2.0 180 Ring' + b'\r\n\r\n' + b'SIP/2.0 200 OK' + b'\r\n\r\n')

            elif linea_lista[0] == 'ACK':
                aEjecutar = './mp32rtp -i 127.0.0.1 -p 23032 < ' + FICH_AUDIO
                print('Vamos a ejecutar', aEjecutar)
                os.system(aEjecutar)

            elif linea_lista[0] == 'BYE':
                self.wfile.write(b'SIP/2.0 200 OK' + b'\r\n\r\n')

            elif linea_lista[0] != 'INVITE' or 'ACK' or 'BYE':
                self.wfile.write(b'SIP/2.0 Method Not Allowed' + b'\r\n\r\n')

            else:
                self.wfile.write(b'SIP/2.0 Bad Request' + b'\r\n\r\n')

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer((IP, PUERTO), EchoHandler)
    print("Listening...")
    serv.serve_forever()
