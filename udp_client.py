# Assignment: Simple Chat Room - Client Code Implementation

# **Libraries and Imports**: 
#    - Import the required libraries and modules. 
#    You may need the below libraries for the client.
#    Feel free to use any libraries as well.
import sys
import argparse
import select
import socket
import threading
 # u can use '_thread'

# **Global Variables**:
#    - IF NEEDED, Define any global variables that will be used throughout the code.

# **Function Definitions**:
#    - In this section, you will implement the functions you will use in the client side.
#    - If you will use and implement the below functions, please don't edit the namings.
#    - Feel free to add more other functions, and more variables.
#    - Make sure that names of functions and variables are meaningful.
#    - Take into consideration error handling, interrupts, client shutdown, and documentation.

def receive_messages(socket, client_name, message_history, exit_event):
    # Function to handle incoming messages from the server.
    while not exit_event.is_set():
        try:
            if select.select([socket], [], [], 1)[0]:
                sResponse, sAddr = socket.recvfrom(2048)
                sys.stdout.write('\r' + ' ' * (len(client_name + ': ')) + '\r')
                display_message(sResponse.decode(), message_history, client_name)
                display_input_prompt(client_name)
        except KeyboardInterrupt:
            break
    print("socket of thread will terminate")
    socket.close()

def send_message(message, clientSocket, sName, sPort):
    # Function to send a message to the server.
    clientSocket.sendto(message.encode(), (sName, sPort))

def display_message(raw_message, message_history, username):
    # Function to display a message from the server.
    t, name, msg = raw_message.split('*')
    message_history.append((float(t), name, msg))
    if name!=username:
        print(name + ': ' + msg)

def display_input_prompt(client_name):
    sys.stdout.write(client_name + ': ')
    sys.stdout.flush()

def run_client(clientSocket, clientname, serverAddr, serverPort):
    # The main client function.
    # It should handle incoming server messages, send messages to the server,
    # manage the client's connection, and gracefully exit.
    exit_event = threading.Event()
    server_thread = threading.Thread(target=receive_messages,args= (clientSocket, clientname, [], exit_event))
    server_thread.start()

    send_message("joining:"+clientname, clientSocket, serverAddr, serverPort)

    while True:
        try:
            display_input_prompt(clientname)
            line = input()
            if line.lower().strip() == 'exit':
                send_message("leaving:" + ":" + clientname, clientSocket, serverAddr, serverPort)
                break
            send_message(clientname + ':' + line, clientSocket, serverAddr, serverPort) 
        except KeyboardInterrupt:
            send_message("leaving:" + ":" + clientname, clientSocket, serverAddr, serverPort)
            print('\ninterrupt client: shutting down')
            break

    print("Client Closing.........")
    exit_event.set()
    server_thread.join()
    clientSocket.close()

# **Main Code**:  
if __name__ == "__main__":
    
    # Arguments: name address
    parser = argparse.ArgumentParser(description='argument parser')
    parser.add_argument('name')  # to use: python client.py name
    args = parser.parse_args()
    clientname = args.name
    serverAddr = '127.0.0.1'
    serverPort = 9301
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    run_client(clientSocket, clientname, serverAddr, serverPort)  # Calling the function to start the client.
