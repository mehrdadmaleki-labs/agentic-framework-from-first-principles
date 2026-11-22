# agent B is the server (always listen to the upcoming requests)

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

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket.SOCK_STREAM=TCP connection

server.bind(("127.0.0.1", 9000)) #server listen from the address 127.0.0.1 on port 9000

server.listen(5) #listen to upcoming 5 requests at most

while True:
    conn, addr = server.accept()
    print("Agent A is Connected Now...", addr)

    with conn:

        data = conn.recv(1024) #reciev up to 1024 bytes from client/Byte

        data_decode=data.decode()
        
        data_obj=json.loads(data_decode)

        try:
            result=operation(**data_obj)
            out_succs={"status":"success", "message": result}
            conn.sendall(json.dumps(out_succs).encode())
        except ValueError as e:
            out_err={"status": "error", "message": str(e)}
            json_string=json.dumps(out_err).encode()
            
            conn.sendall(json_string)



