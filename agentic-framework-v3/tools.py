
import json
import time
import asyncio


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


def handle_client(conn, addr):
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

            # Simulate a slow operation (for concurrency testing)
            time.sleep(5)

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
            print(f"Connection error from {addr}: {e}")
            return

        # Python dictionary -> JSON string -> Bytes
        response_bytes = (
            json.dumps(response) + "\n"
        ).encode("utf-8")

        # Send the complete response
        try:
            conn.sendall(response_bytes)

        except OSError as e:
            print(f"Failed to send response to {addr}: {e}")

async def handle_client(reader, writer):

    addr = writer.get_extra_info("peername")
    print("Agent connected:", addr)

    try:
        # Read until newline is received
        data = await reader.readline()

        if not data:
            raise ConnectionError("Client disconnected")

        # Bytes -> String -> Python dictionary
        data_obj = json.loads(data.decode("utf-8"))

        # Simulate a slow operation
        await asyncio.sleep(5)

        # Execute requested operation
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
        return

    finally:
        # Connection cleanup is handled below
        pass

    response_bytes = (
        json.dumps(response) + "\n"
    ).encode("utf-8")

    try:
        writer.write(response_bytes)
        await writer.drain()

    finally:
        writer.close()
        await writer.wait_closed()

