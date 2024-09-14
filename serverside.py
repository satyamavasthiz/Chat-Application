import socket
import threading

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            broadcast(message, client_socket)
        except:
            client_socket.close()
            break

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                clients.remove(client)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8080))
server.listen()

clients = []

print("Server started, waiting for connections...")

while True:
    client_socket, client_address = server.accept()
    print(f"New connection from {client_address}")
    clients.append(client_socket)
    threading.Thread(target=handle_client, args=(client_socket,)).start()