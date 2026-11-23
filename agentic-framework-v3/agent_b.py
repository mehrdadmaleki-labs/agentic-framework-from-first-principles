
# Agent B: TCP Server
# Receives JSON requests, performs calculations,
# and returns JSON responses.

import socket
import json
import threading
from tools import *


HOST = "127.0.0.1"
PORT = 9000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:

    # Assign the server's IP address and port
    server.bind((HOST, PORT))

    # Listen for incoming TCP connections
    server.listen(5)

    print(f"Agent B listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()

        thread = threading.Thread(
            target=handle_client,
            args=(conn, addr)
        )

        thread.start()




        
