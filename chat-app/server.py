import socket
import threading
import logging

# basic logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(message)s', 
    datefmt='%H:%M:%S'
)

#storing clients info
clients = []
usernames = {}

#message length (4kb)
msg_len = 4096

# To send broadcast message
def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.send(message.encode('utf-8'))
            except:
                if client in clients:
                    clients.remove(client)

# handle client when connected
def manage_connection(conn, addr):
    with conn:
        while True:
            try:
                msg = conn.recv(msg_len).decode('utf-8')
                if not msg:
                    break
                    
                if msg.startswith("JOIN "):
                    name = msg.split(" ", 1)[1]
                    usernames[conn] = name
                    clients.append(conn)
                    logging.info(f"{name} joined from {addr}")
                    broadcast(f"MSG Server: {name} joined the chat", conn)
                    
                elif msg.startswith("MSG "):
                    name = usernames[conn]
                    text = msg[4:]
                    
                    logging.info(f"{name} sent a message") 
                    broadcast(f"MSG {name}: {text}", conn)
                    
                elif msg == "QUIT":
                    break
                    
            except:
                logging.warning(f"Connection closed unexpectedly for {addr}")
                break
                
        if conn in usernames:
            name = usernames[conn]
            logging.info(f"{name} left the chat")
            broadcast(f"MSG Server: {name} left the chat", conn)
            del usernames[conn]
            
        if conn in clients:
            clients.remove(conn)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    # Using standard address 
    server.bind(('127.0.0.1', 65432))
    # Allow 10 connections
    server.listen(10) 
    logging.info("Server started on port 65432. Waiting for users...")

    while True:
        # waiting for client
        conn, addr = server.accept()
        logging.info(f"New connection from {addr}")
        #Handlint one client in single thread for simultaneous communication 
        thread = threading.Thread(target=manage_connection, args=(conn, addr))
        thread.start()

