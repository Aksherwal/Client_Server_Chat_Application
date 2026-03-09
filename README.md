
# Simple Chat Application

A simple multi client chat application build using python socket programming. 

## Files Included
* `server.py` - The central chat server that routes messages.
* `client.py` - The chat client used by individual users to connect to the server.

## How to Run
> Make sure you have python 3.5+ version 

1. **Start the Server**
   Open a terminal go to chat-app directory and run:
   ```bash
   python server.py
   ```

   The server will start on 127.0.0.1 at port 65432 and wait for connections.

2. **Start the Client**
   Open a new terminal window and run:
   ```bash
   python client.py
   ```
   Enter a username when prompted. You can open multiple client terminals to simulate different users chatting.
   **Commands**
   · Just type your message and press Enter to send it to everyone.
   · Type /quit and press Enter to leave the chat cleanly.
