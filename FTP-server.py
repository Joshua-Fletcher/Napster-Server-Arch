import socket
import threading
import os
import pathlib

server_ip = 'localhost'
server_port = 3299
buffer_size = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen()

def handle_request(connection_socket):
    print("connected")
    request = "placeholder"
    while request.upper() != "QUIT":

        request = connection_socket.recv(buffer_size).decode('utf-8')
        print(request)

        if "GET" in request.upper():
            split_request = request.split()
            requestType = split_request[0]
            fileName = split_request[1]

            data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            data_socket.connect((requestIP, int(requestPort)))

            try:
                open_file = open(fileName,'rb')
                requested_file = open_file.read()
                open_file.close()
                data_socket.send(requested_file)
            except FileNotFoundError:
                error_message = "File Not Found on Server"
                data_socket.send(error_message.encode('utf-8'))
            
            data_socket.close()

        elif "CONNECT" in request.upper():
            split_request = request.split()
            requestType = split_request[0]
            requestIP = split_request[1]
            requestPort = split_request[2]

    connection_socket.close()

while True:
    connection_socket, addr = server_socket.accept()
    threading.Thread(target=handle_request, args=(connection_socket,)).start()
