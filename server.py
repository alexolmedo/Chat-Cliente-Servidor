# coding=utf-8
import socket
import thread
import sys
import time
import struct
import uuid

HOST = '0.0.0.0'
SOCKET_LIST = []
RECV_BUFFER = 1024
PORT = 9001

class Client:
    pass

def manager(client):

    print client.code + " conectado desde: ", client.addr

    # Este bucle se repite cada vez que se encuentran datos en el bufer
    while 1:

        try:
            data = client.socket.recv(RECV_BUFFER)
            #Comprobar si se trata de un mensaje privado
            if ':' in str(data):
                recipient, msg = data.split(":")
                for c in SOCKET_LIST:
                     if c.code == recipient:
                        if not c.socket.send(client.code + ": " + msg):
                            try:
                                c.socket.close()
                            finally:
                                SOCKET_LIST.remove(c)
                                print "Cliente " + c.code + " no encontrado - Socket cerrado"
                                break
                break

            # Hacemos un broadcast de lo que dice el cliente a todos los demás
            # clientes
            for c in SOCKET_LIST:
                if not c.socket.send(client.code + ": " + str(data)):
                    try:
                        c.socket.close()
                    finally:
                        SOCKET_LIST.remove(c)
                        print "Cliente " + c.code + " no encontrado - Socket cerrado"
                        break

            print "Clientes totales: " + str(len(SOCKET_LIST))

        except Exception as e:
            print "Excepcion en socket de cliente:"
            print e
            try:
                client.socket.close()
            finally:
                SOCKET_LIST.remove(client)
                print "Cliente " + client.code + " no encontrado - Socket cerrado - Clientes totales: " + str(len(SOCKET_LIST))
                break
    return


def server():

    server_addr = (HOST, PORT)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(server_addr)
    server_socket.listen(10)

    print "Server is listening for connections\n"
    while 1:

        c = Client()
        c.socket, c.addr = server_socket.accept()
        c.code = c.socket.recv(RECV_BUFFER)
        SOCKET_LIST.append(c)

        thread.start_new_thread(manager, (SOCKET_LIST[-1],))

    server_socket.close()

if __name__ == "__main__":
    sys.exit(server())