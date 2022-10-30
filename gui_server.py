import socket
import threading  # Make many threads run at the same time.

# basic setup for server
# ipconfig
HOST = '127.0.0.1'
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []

# broadcast
def broadcast(message):
    # Pass already encoded message
    for client in clients:
        client.send(message)  # Send directly to all clients

# handle
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)

        # Error handling
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

# receive
def receive():
    # Main function running in the main thread
    while True:
        client, address = server.accept()  # Server accepts the connection and return to client.
        print(f"Connected with {str(address)}!")

        # To signal the client we are requesting the nickname.
        # Server plays the host. Client do the communication work.
        client.send("NICK".encode('utf-8'))

        nickname = client.recv(1024)  # If client behaves properly, we will receive the nickname.

        nicknames.append(nickname)  # Add nickname to the nickname list.
        clients.append(client)  # Add client to the client list.

        print(f"Nickname of the client is {nickname}")  # Print as the server message.
        broadcast(f"{nickname} connected to the server!\n".encode('utf-8'))
        client.send("Connected to the server".encode('utf-8'))  # To specific client.

        thread = threading.Thread(target=handle, args=(client,))  # The comma is to make it be treated as tuple.
        thread.start()

print("Server running---")
receive()
