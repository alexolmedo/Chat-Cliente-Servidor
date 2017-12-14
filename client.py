# coding=utf-8
import sys
import socket
import time
import thread

HOST = '127.0.0.1'
RECV_BUFFER = 1024
PORT = 9001

def send_message(socket):
    message = raw_input()
    socket.send(message)
    send_message(socket)

def client():
    addr = (HOST, PORT)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #server_socket.settimeout(30)
    nombre=raw_input("Ingrese su nombre:")
    server_socket.connect(addr)

    server_socket.send(nombre)
    thread.start_new_thread(send_message, (server_socket,))

    while 1:
        data = server_socket.recv(RECV_BUFFER)
        print data

if __name__ == "__main__":
    sys.exit(client())