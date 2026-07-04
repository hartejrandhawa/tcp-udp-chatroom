import argparse
import socket
import threading
import sys ,select

def server_messages(client_socket, client_name, exit_event):
    while not exit_event.is_set():
        try:
            if select.select([client_socket], [], [], 1)[0]:
                sys.stdout.write('\r' + ' ' * (len(client_name + ': ')) + '\r')
                message = client_socket.recv(1024).decode()
                if client_name != message.split(':')[0]:
                    print(message)
                display_input_prompt(client_name)
        except KeyboardInterrupt:
            print("socket of thread will terminate")
            client_socket.close()

def send_message(message, client_socket):
    client_socket.send(message.encode())

def display_input_prompt(client_name):
    sys.stdout.write(client_name + ': ')
    sys.stdout.flush()

def run_client(client_socket, client_name):
    send_message(client_name, client_socket)

    exit_event = threading.Event()
    server_thread = threading.Thread(target=server_messages, args=(client_socket, client_name, exit_event))
    server_thread.start()
    
    try:
        display_input_prompt(client_name)
        while True:
            line = input()
            if line.lower().strip() == 'exit':
                send_message('exit', client_socket)
                break
            send_message(line, client_socket)
    except KeyboardInterrupt:
        send_message('exit', client_socket)
        print('\ninterrupt client: shutting down')

    print("Client Closing.........")
    exit_event.set()
    server_thread.join()
    client_socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Argument Parser')
    parser.add_argument('name')  # to use: python client.py name
    args = parser.parse_args()
    client_name = args.name
    server_addr = '127.0.0.1'
    server_port = 9301

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', server_port))

    run_client(client_socket, client_name)
 
