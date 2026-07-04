# Assignment: Simple Chat Room - Server Code Implementation

# **Libraries and Imports**: 
#    - Import the required libraries and modules. 
#    You may need the below libraries for the client.
#    Feel free to use any libraries as well.
import socket
import select
import time

# **Global Variables**:
#    - IF NEEDED, Define any global variables that will be used throughout the code.

# **Function Definitions**:
#    - In this section, you will implement the functions you will use in the server side.
#    - If you will use and implement the below functions, please don't edit the namings.
#    - Feel free to add more other functions, and more variables.
#    - Make sure that names of functions and variables are meaningful.
#    - Take into consideration error handling, interrupts, client shutdown, and documentation.

def broadcast_message(socket, last_message, addr_to_name):
    # Broadcasts a message to all connected clients.
    last_message = str(last_message[0]) + '*' + last_message[1] + '*' + last_message[2]
    for clientAddr in addr_to_name.keys():
        socket.sendto(last_message.encode(), clientAddr)

def run_server(serverSocket, serverPort):
    # The main server function.
    # It should handle incoming client messages,
    # manage client connections, and broadcast messages.
    messages_history = [] # list of messages sent by each user
    addr_to_name = {} # maps address to name

    # start server
    serverSocket.setblocking(0)
    serverSocket.bind(('', serverPort))
    print("\nCHATROOM")
    print('\nThis is the server side.\nI am ready to receive connections on port', serverPort)

    while True:
        try:
            if select.select([serverSocket], [], [], 1)[0]:
                message, clientAdr = serverSocket.recvfrom(2048)  # receive message from client
                message = message.decode().lower()
                print("Message received from {}: {}".format(clientAdr, message))

                if ':' in message : 
                    name, message = message.split(':', 1) 
                    if name == 'joining' : # new client
                        name = message
                        addr_to_name[clientAdr] = message
                        message = 'User ' + str(message) + ' joined from address:' + str(clientAdr[0]) + ':'+ str(clientAdr[1])
                        print(message)
                        continue 
                    if name == 'leaving' and clientAdr in addr_to_name : # client leaving
                        name = addr_to_name[clientAdr]
                        del addr_to_name[clientAdr]
                        message = 'User ' + str(name) + ' left from address:' + str(clientAdr[0]) + ':'+ str(clientAdr[1])
                        print(message)
                        continue
                else:
                    if clientAdr not in addr_to_name :
                        print('User', clientAdr, 'did not join')
                        continue
                    else : 
                        name = addr_to_name[clientAdr]

                messages_history.append((time.time(), name, message))  # add message to history
                broadcast_message(serverSocket, messages_history[-1], addr_to_name) # send message to all clients

        except KeyboardInterrupt:
            print('\ninterrupt received: shutting down')
            break   
    serverSocket.close()
    print('server shut down')

# **Main Code**:  
if __name__ == "__main__":
    
    serverPort = 9301  # Set the `serverPort` to the desired port number (e.g., 9301).
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Creating a UDP socket named.
    run_server(serverSocket, serverPort)  # Calling the function to start the server.
