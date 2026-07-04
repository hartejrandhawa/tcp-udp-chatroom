import socket
import threading
import select

def broadcast(message):
    for client in clients:
        client.send(message.encode())

def handle_client(client_socket, client_name):
    print('User ' + client_name + ' joined' )
    while True:
        try:
            if select.select([client_socket], [], [], 1)[0]:
                message = client_socket.recv(1024).decode()
                print("Message received from {}: {}".format(client_name, message))
                if message == 'exit':
                        print('User ' + client_name + ' left')
                        clients.remove(client_socket)
                        break
                else:
                    broadcast(client_name +':'+ message)

        except KeyboardInterrupt:
            break


def run_server(server_socket, server_port):
    print("\nCHATROOM")
    print('\nThis is the server side.\nI am ready to receive connections on port', server_port)

    while True:
        try:
            client_socket, client_addr = server_socket.accept()
            clients.append(client_socket)
            if select.select([client_socket], [], [], 1)[0]:
                client_name=client_socket.recv(1024).decode()
                client_thread = threading.Thread(target=handle_client, args=(client_socket,client_name))
                client_thread.start()
        except KeyboardInterrupt:
            client_thread.join()
            print('\ninterrupt received: shutting down')
            break
    for client_socket in clients:
        client_socket.close()
    server_socket.close()
    print('server shut down')

if __name__ == "__main__":
    clients = []
    server_port = 9301
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', server_port))
    server_socket.listen(5)

    run_server(server_socket,server_port)
