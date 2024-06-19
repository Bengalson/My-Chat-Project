import socket
import threading
import sqlite3
import datetime

clients = []

def update_clients(client_socket, action):
    if action == "add":
        clients.append(client_socket)
    elif action == "remove":
        if client_socket in clients:
            clients.remove(client_socket)

def handle_client(client_socket):
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
                print(f"{username}: {timestamped_message}")
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
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f"[{timestamp}] {message}"

def broadcast(message, sender_socket, sender_name):
    for client in clients:
        if client != sender_socket:
            try:
                if sender_name == "Server":
                    styled_message = f"\033[92m{message}\033[0m"  # Green for server messages
                else:
                    styled_message = f"\033[94m{message}\033[0m"  # Blue for user messages
                client.send(styled_message.encode('utf-8'))
            except:
                update_clients(client, "remove")

def save_message_to_db(message, username):
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (content, username) VALUES (?, ?)", (message, username))
    conn.commit()
    conn.close()

def start_server():
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
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT, username TEXT)")
    conn.close()
    
    start_server()
