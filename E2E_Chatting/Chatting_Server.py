# -*- coding: utf-8 -*-
"""
@author: Philipp

Server script for encrypted chat program
"""

# import socket library
import socket

# import threading library
import threading


# Initializing the server
# Choose a port that is free
PORT = 5000

# Get IP4 address of host for server
SERVER = socket.gethostbyname(socket.gethostname())

# Address as a tuple
ADDRESS = (SERVER, PORT)

# Format for encoding and decoding
FORMAT = "utf-8"

# Creating a new socket for the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Binding the address of the server to the new socket
server.bind(ADDRESS)

# Lists that will contain all the clients and their names
clients, names = [], []


# Function to start the connection
def startChat():

    print("Server is running on " + SERVER + " through port " + str(PORT))

    # listening for connections
    server.listen()

    while True:

        # accept connections and returns a new connection to the client
        # and the address bound to it
        conn, addr = server.accept()
        conn.send("NAME".encode(FORMAT))

        # 1024 represents the max amount
        # of data that can be received (bytes)
        name = conn.recv(1024).decode(FORMAT)

        # append the name and client
        # to the respective list
        names.append(name)
        clients.append(conn)

        print(f"Name is :{name}")

        # broadcast message
        broadcastMessage(f"{name} is available for chatting!".encode(FORMAT))

        conn.send('Connection successful!'.encode(FORMAT))

        # Start the handling thread
        thread = threading.Thread(target=handle,
                                args=(conn, addr))
        thread.start()

        # no. of clients connected
        # to the server
        print(f"active connections {threading.activeCount()-1}")


## method to handle the incoming messages 


def handle(conn, addr):

    print(f"new connection {addr}")
    connected = True

    while connected:
        # receive message
        message = conn.recv(1024)

        # broadcast message
        broadcastMessage(message)

    # close the connection
    conn.close()

# method for broadcasting
# messages to the each clients


def broadcastMessage(message):
    for client in clients:
        client.send(message)
    #print(message) print message for debugging and tracking operations


# call the method to
# begin the communication
if __name__ == '__main__':
    startChat()



