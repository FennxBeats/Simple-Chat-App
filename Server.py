import socket
import threading

HOST = '192.168.0.5'
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []

def broadcast(message):
        for client in clients:
            client.send(message)
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}!")

        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024)

        nicknames.append(nickname)
        clients.append(client)
        print(f"Nickname of the client is {nickname}\n")
        broadcast(f"{nickname} connected to the chat!".encode('utf-8'))  # Removed "\n"
        client.send("Connected to the chat\n".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server Running...")
receive()
