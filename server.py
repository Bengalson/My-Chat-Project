import socket
import threading
import sqlite3
import datetime
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

clients = []

def update_clients(client_socket, action):
    """Update the list of connected clients"""
    if action == "add":
        clients.append(client_socket)
    elif action == "remove":
        if client_socket in clients:
            clients.remove(client_socket)

def handle_client(client_socket):
    """Handle communication with a single client"""
    client_socket.send("Welcome! Please enter your username:".encode('utf-8'))
    username = client_socket.recv(1024).decode('utf-8')
    
    welcome_message = f"{username} has joined the chat!"
    broadcast(welcome_message, client_socket, "Server")
    save_message_to_db(welcome_message, "Server")

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                timestamped_message = add_timestamp(f"{username}: {message}")
                print(timestamped_message)
                save_message_to_db(timestamped_message, username)
                broadcast(timestamped_message, client_socket, username)
            else:
                update_clients(client_socket, "remove")
                leave_message = f"{username} has left the chat."
                broadcast(leave_message, client_socket, "Server")
                save_message_to_db(leave_message, "Server")
                break
        except:
            update_clients(client_socket, "remove")
            leave_message = f"{username} has left the chat."
            broadcast(leave_message, client_socket, "Server")
            save_message_to_db(leave_message, "Server")
            break
    client_socket.close()

def add_timestamp(message):
    """Add a timestamp to a message"""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f"[{timestamp}] {message}"

def broadcast(message, sender_socket, sender_name):
    """Broadcast a message to all clients except the sender"""
    for client in clients:
        if client != sender_socket:
            try:
                styled_message = style_message(message, sender_name)
                client.send(styled_message.encode('utf-8'))
            except:
                update_clients(client, "remove")

def style_message(message, sender_name):
    """Style a message based on the sender"""
    if sender_name == "Server":
        return f"{Fore.GREEN}{message}{Style.RESET_ALL}"  # Green for server messages
    else:
        return f"{Fore.BLUE}{message}{Style.RESET_ALL}"  # Blue for user messages

def save_message_to_db(message, username):
    """Save a message to the database"""
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (content, username) VALUES (?, ?)", (message, username))
    conn.commit()
    conn.close()

def start_server():
    """Start the chat server"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    PORT = 12345
    server_socket.bind(('localhost', PORT))
    server_socket.listen(5)
    print("Server is listening for connections...")
    
    while True:
        client_socket, client_address = server_socket.accept()
        update_clients(client_socket, "add")
        print(f"Connection established with {client_address}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    # Create the messages table in the database if it doesn't exist
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT, username TEXT)")
    conn.close()
    
    start_server()
