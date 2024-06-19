import socket
import threading
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def receive_messages(client_socket):
    """Receive messages from the server and display them"""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                break
        except:
            break

def send_message(client_socket):
    """Send messages to the server"""
    while True:
        message = input("")
        try:
            client_socket.send(message.encode('utf-8'))
        except:
            break

def connect_to_server():
    """Connect to the server"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    return client_socket

def start_receiving_thread(client_socket):
    """Start a thread for receiving messages"""
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

def start_sending_thread(client_socket):
    """Start a thread for sending messages"""
    send_thread = threading.Thread(target=send_message, args=(client_socket,))
    send_thread.start()

def close_connection(client_socket):
    """Close the connection to the server"""
    client_socket.close()

if __name__ == "__main__":
    client_socket = connect_to_server()
    start_receiving_thread(client_socket)
    start_sending_thread(client_socket)
