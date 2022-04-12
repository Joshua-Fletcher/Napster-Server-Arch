from tkinter import *
import tkinter as tk
import socket
import threading

personal_server_ip = 'localhost'
personal_server_port = 3299

data_ip = 'localhost'
data_port = 3289
buffer_size = 1024

index_server_ip = 'localhost'
index_server_port = 3200

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
command = "PlaceHolder"


def connectButtonClick():
    hostName = serverHostName.get()
    hostPort = serverPort.get()
    hostUsername = username.get()
    hostNameContents = personal_hostname.get()
    speed = internetSpeed.get()
    personalPort = personal_port.get()
    registrationContent = hostUsername + "," + speed + "," + hostName + "," + hostPort + "," + hostNameContents + "," + personalPort

    client_socket.connect((index_server_ip, index_server_port))

    client_socket.send(registrationContent.encode('utf-8'))

def insertFileClick():
    fileNameInfo = fileName.get()
    fileDescInfo = fileDesc.get()
    fileInfo = fileNameInfo + "," + fileDescInfo
    fileListBox.insert(1, fileNameInfo + ", " + fileDescInfo)

    client_socket.send(fileInfo.encode('utf-8'))

def doneClick():
    doneMessage = "DONE"

    client_socket.send(doneMessage.encode('utf-8'))

def searchButtonClick():
    keywordToSearch = keywordInput.get()
    
    client_socket.send(keywordToSearch.encode('utf-8'))

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((data_ip, data_port))
    server_socket.listen()  

    data_socket, addr = server_socket.accept()

    requestedFileInfo = data_socket.recv(buffer_size).decode('utf-8')

    print(requestedFileInfo)

    data_socket.close()
    server_socket.close()

    if requestedFileInfo != "":
        fileInfoSplit = requestedFileInfo.split("/")
        for x in fileInfoSplit:
            splitArr = x.split(",")
            inputStr = "File Name: " + splitArr[0] + "  |  Desc: " + splitArr[4] + "  |  Host: " + splitArr[1] + "  |  Port: " + splitArr[2] + "  |  Speed: " + splitArr[3]
            NetworkFileListBox.insert(1, inputStr)

def commandButtonClick():
    commandRequest = commandInput.get()

    ftp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    if commandRequest.upper() == "QUIT":
        quitMessage = "QUIT"
        ftp_socket.send(quitMessage.encode('utf-8'))
        ftp_socket.close()

    elif "CONNECT" in commandRequest.upper():
        connection_info = "CONNECT" + " " + data_ip + " " + str(data_port)
        connect_request_array = commandRequest.split()
        host_split = connect_request_array[1].split(":")
        request_host_IP = host_split[0]
        request_host_port = host_split[1]
        ftp_socket.connect((request_host_IP, int(request_host_port)))
        ftp_socket.send(connection_info.encode('utf-8'))

    elif "GET" in commandRequest.upper():
        ftp_socket.send(commandRequest.encode('utf-8'))
        connect_request_array = commandRequest.split()
        fileName = connect_request_array[1]

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((data_ip, data_port))
        server_socket.listen()  

        data_socket, addr = server_socket.accept()

        try:
            with open(str(fileName), 'wb') as f:
                chunk = data_socket.recv(buffer_size)
                while chunk:
                    f.write(chunk)
                    chunk = data_socket.recv(buffer_size)
        except:
            print("Not a file on server")

        data_socket.close()


#create window and title
window = tk.Tk()
window.title("Napster Client")

#frame = tk.Frame(master=window, width=1000, height=500)

#connection section label
Label(text="Please Enter Your Personal Server IP, Port, Prefered Username, Hostname, and Connection Speed Below: ").grid(row=1,columnspan=5)

#server hostname label
Label(text="Server Hostname:").grid(row=2, column=0)

#server hostname entry box
serverHostName = tk.Entry()
serverHostName.grid(row=2, column=1)

#server port label
Label(text="Port:").grid(row=2, column=2)

#server port entry box
serverPort = tk.Entry()
serverPort.grid(row=2, column=3)

#connect button
connectButton = tk.Button(text="Connect", command=connectButtonClick, width=30)
connectButton.grid(row=2, column=4, columnspan=2)

#username label
Label(text="Username:").grid(row=3, column=0)

#username entry box
username = tk.Entry()
username.grid(row=3, column=1)

#personal hostname label
Label(text="Hostname:").grid(row=3,column=2)

#personal hostname entry box
personal_hostname = tk.Entry()
personal_hostname.grid(row=3, column=3)

#personal port label
Label(text="Data Port:").grid(row=3,column=4)

#personal port entry box
personal_port = tk.Entry()
personal_port.grid(row=3, column=5)

#internet speed label
Label(text="Speed:").grid(row=4,column=0)

#internet speed entry box
internetSpeed = tk.Entry()
internetSpeed.grid(row=4, column=1)

#filler labels
Label(text=" ").grid(row=5)

#file registration 
Label(text="Register your files:").grid(row=6,column=0, columnspan=1)

#file name label
Label(text="Filename (Ex: hi.txt):").grid(row=7, column=0)

#file name entry box
fileName = tk.Entry()
fileName.grid(row=7, column=1)

#file dec label
Label(text="File Description:").grid(row=7, column=2)

#file name entry box
fileDesc = tk.Entry()
fileDesc.grid(row=7, column=3)

#insert file button
insertFile = tk.Button(text="Insert", command=insertFileClick, width=20)
insertFile.grid(row=7, column=4)

#file list 
fileListBox = tk.Listbox(width=80)
fileListBox.grid(row=8, columnspan=6)

#done file uploading button
doneButton = tk.Button(text="Click when done uploading files and descriptions", command=doneClick, width=80)
doneButton.grid(row=9, columnspan=6)

#filler labels
Label(text=" ").grid(row=10)
Label(text=" ").grid(row=11)

#search main label
Label(text="Search the Network:").grid(row=12,column=0, columnspan=1)

#keyword label
Label(text="Keyword:").grid(row=13, column=0)

#keyword entry box
keywordInput = tk.Entry(width=30)
keywordInput.grid(row=13, column=1)

#search button
searchButton = tk.Button(text="Search", command=searchButtonClick, width=30)
searchButton.grid(row=13, column=2, columnspan=2)

#list files on network box
NetworkFileListBox = tk.Listbox(width=80)
NetworkFileListBox.grid(row=14, columnspan=6)

#filler labels
Label(text=" ").grid(row=15)

#ftp section label
Label(text="FTP").grid(row=16, column=0)

#command label
Label(text="Enter Command:").grid(row=17, column=0)

#command entry box
commandInput = tk.Entry(width=50)
commandInput.grid(row=17, column=1)

#command button
commandButton = tk.Button(text="Go", command=commandButtonClick, width=30)
commandButton.grid(row=17, column=2, columnspan=2)


window.mainloop()
