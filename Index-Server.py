import socket
import threading
import os
import pathlib
import copy

fileNameTable = {

}

userTable = {

}


server_ip = 'localhost'
server_port = 3200
buffer_size = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen()

def handle_request(connection_socket):
    print("User is Registering...")
    userInfoRec = connection_socket.recv(buffer_size).decode('utf-8')
    userInfo = userInfoRec.split(",")
    userName = userInfo[0]
    internetSpeed = userInfo[1]
    userIP = userInfo[2]
    userPort = userInfo[3]
    dataIP = userInfo[4]
    dataPort = userInfo[5]
    print(userInfo)
    userTable[userName] = [internetSpeed, userIP, userPort, dataIP, dataPort]
    print(userName + " Joined")
    confirmationMessage = "Registered"
    #server_socket.send(confirmationMessage.encode('utf-8'))

    fileInfoRec = "PlacesHolder"
    while(fileInfoRec.upper() != "DONE"):
        fileInfoRec = connection_socket.recv(buffer_size).decode('utf-8')
        if((fileInfoRec.upper() != "DONE") and (fileInfoRec.upper() != "QUIT")):
            fileInfo = fileInfoRec.split(",")
            fileName = fileInfo[0]
            fileDesc = fileInfo[1]
            fileNameTable[fileName] = [fileDesc, userName]
            print(fileNameTable)

    command = "PlaceHolder"
    while(command.upper() != "QUIT"):
        command = connection_socket.recv(buffer_size).decode('utf-8')

        if command.upper() == "QUIT":

            fileNameTable_copy = copy.copy(fileNameTable)
            userTable_copy = copy.copy(userTable)

            for key, val in fileNameTable.items():
                if val[1] == userName:
                    del fileNameTable_copy[key]

            for key, val in userTable.items():
                if key == userName:
                    del userTable_copy[key]

            print(userName + " Left")

        else:
            searchResults = {}
            searchResultsString = ""

            for key, val in fileNameTable.items():
                if (command in key) or (command in val[0]):
                    searchResults[key] = [userTable[val[1]][1], userTable[val[1]][2], userTable[val[1]][0], val[0]]
                    searchResultsString = searchResultsString + key + "," + userTable[val[1]][2] + "," + userTable[val[1]][3] + "," + userTable[val[1]][0] + "," + val[0] + "/"

            data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            data_socket.connect((dataIP, int(dataPort)))

            if len(searchResultsString) > 1:
                searchResultsString = searchResultsString.strip(searchResultsString[-1])

            data_socket.send(searchResultsString.encode('utf-8'))

            data_socket.close()

    connection_socket.close()

while True:
    connection_socket, addr = server_socket.accept()
    threading.Thread(target=handle_request, args=(connection_socket,)).start()
