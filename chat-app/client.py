import socket
import threading
import sys

msg_len = 4096 # 4kb message

# handles the mesaage recieved from server
def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(msg_len).decode('utf-8')
            if msg.startswith("MSG "):
                print(msg[4:])
            else:
                print(msg)
        except:
            print("\nConnection closed by server.")
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # using our servers address
    s.connect(('127.0.0.1', 65432))
    # taking username input for identification
    username = input("Enter your username: ")
    s.send(f"JOIN {username}".encode('utf-8'))

    # again using multi threading here to test for multiple clients
    thread = threading.Thread(target=receive_messages, args=(s,))
    thread.start()

    print("Connected! Type your messages below. Type '/quit' to exit.")

    while True:
        try:
            text = input()
            if text == "/quit":
                s.send("QUIT".encode('utf-8'))
                break
            else:
                s.send(f"MSG {text}".encode('utf-8'))
        # Handling keyboard interruption
        except KeyboardInterrupt:
            s.send("QUIT".encode('utf-8'))
            break
            
# finally exit the program
sys.exit()

