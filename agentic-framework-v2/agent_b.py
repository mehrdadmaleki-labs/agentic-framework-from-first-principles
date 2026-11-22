
# Agent B: TCP Server
# Receives JSON requests, performs calculations,
# and returns JSON responses.

import socket
import json


def operation(x: float, y: float, op: str) -> float:
    if op == "ADD":
        return x + y

    elif op == "SUBTRACT":
        return x - y

    elif op == "MULTIPLY":
        return x * y

    elif op == "DIVISION":
        if y == 0:
            raise ValueError("Denominator in division is zero")
        return x / y

    else:
        raise ValueError(f"The operation {op} is not supported")


HOST = "127.0.0.1"
PORT = 9000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:

    # Assign the server's IP address and port
    server.bind((HOST, PORT))

    # Listen for incoming TCP connections
    server.listen(5)

    print(f"Agent B listening on {HOST}:{PORT}")

    while True:

        # Wait for a client connection
        conn, addr = server.accept()
        print("Agent A connected:", addr)

        # Automatically close the connection when finished
        with conn:
            try:
                buffer = b""

                # Read until a complete message arrives
                while True:
                    chunk = conn.recv(1024)

                    if not chunk:
                        raise ConnectionError(
                            "Client disconnected before completing request"
                        )

                    buffer += chunk

                    if b"\n" in buffer:
                        break

                # Extract the complete JSON message
                message = buffer.split(b"\n", 1)[0]

                # Bytes -> String -> Python dictionary
                data_obj = json.loads(message.decode("utf-8"))

                # Execute the requested operation
                result = operation(**data_obj)

                response = {
                    "status": "success",
                    "message": result
                }

            except (ValueError, TypeError) as e:
                response = {
                    "status": "error",
                    "message": str(e)
                }

            except ConnectionError as e:
                print("Connection error:", e)
                continue

            # Python dictionary -> JSON string -> Bytes
            response_bytes = (
                json.dumps(response) + "\n"
            ).encode("utf-8")

            # Send the complete response
            conn.sendall(response_bytes)
