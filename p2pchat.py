# coding=utf-8
import sys
import socket
import time
import thread

HOST = '127.0.0.1'
SOCKET_LIST = []
RECV_BUFFER = 1024
PORT = 9001

def send_message(socket):
    message = raw_input()
    socket.send(message)
    send_message(socket)

def send_message_server(nombre):
    global SOCKET_LIST
    message = raw_input()
    try:
        data = message
        # Hacemos un broadcast de lo que dice el cliente a todos los demás
        # clientes
        for c in SOCKET_LIST:
            if not c.socket.send(nombre+ ": " + str(data)):
                try:
                    c.socket.close()
                finally:
                    SOCKET_LIST.remove(c)
                    print "Cliente " + c.code + " no encontrado - Socket cerrado"


    except Exception as e:
        print "Excepcion en socket de cliente:"
        print e
        try:
            client.socket.close()
        finally:
            SOCKET_LIST.remove(client)
            print "Cliente " + client.code + " no encontrado - Socket cerrado - Clientes totales: " + str(len(SOCKET_LIST))

    send_message_server(nombre)


class Client:
    pass

def manager(client):

    #print client.code + " conectado desde: ", client.addr

    # Este bucle se repite cada vez que se encuentran datos en el bufer
    while 1:

        try:
            data = client.socket.recv(RECV_BUFFER)
            # Hacemos un broadcast de lo que dice el cliente a todos los demás
            # clientes
            print client.code + ": " + str(data)
            for c in SOCKET_LIST:
                if not c.socket.send(client.code + ": " + str(data)):
                    try:
                        c.socket.close()
                    finally:
                        SOCKET_LIST.remove(c)
                        print "Cliente " + c.code + " no encontrado - Socket cerrado"
                        break

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

def client():
    addr = (HOST, PORT)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #server_socket.settimeout(30)
    nombre=raw_input("Ingrese su nombre:")
    try: 
        server_socket.connect(addr)
    except:
        print 'No hay nadie conectado, usted es el primero en la red'
        server(nombre)
        return

    server_socket.send(nombre)
    thread.start_new_thread(send_message, (server_socket,))

    while 1:
        data = server_socket.recv(RECV_BUFFER)
        print data

def server(nombre):
    global SOCKET_LIST
    server_addr = (HOST, PORT)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(server_addr)
    server_socket.listen(10)

    #Hilo para manejar los mensajes del peer inicial
    thread.start_new_thread(send_message_server, (nombre,) )

    while 1:
        c = Client()
        c.socket, c.addr = server_socket.accept()
        c.code = c.socket.recv(RECV_BUFFER)
        SOCKET_LIST.append(c)
        thread.start_new_thread(manager, (SOCKET_LIST[-1],))

    server_socket.close()




if __name__ == "__main__":
    sys.exit(client())
