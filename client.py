# coding=utf-8
import sys
import socket
import time
import thread

HOST = '127.0.0.1'
RECV_BUFFER = 1024
PORT = 9000

def send_message(socket, message):
    message = raw_input()
    socket.send(message)
    #time.sleep(5)
    send_message(socket,message)


def client():
    addr = (HOST, PORT)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #client_socket.settimeout(30)
    nombre=raw_input("Ingrese su nombre:")
    client_socket.connect(addr)
    client_socket.send(nombre)
    thread.start_new_thread(send_message, (client_socket,""))

    while 1:
        data = client_socket.recv(RECV_BUFFER)
        print data

if __name__ == "__main__":
    sys.exit(client())
