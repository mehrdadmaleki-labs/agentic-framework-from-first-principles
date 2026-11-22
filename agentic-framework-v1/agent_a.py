# agent A is a TCP client (send resuest to agent B)

import socket
import json

client=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP connection

client.connect(("127.0.0.1", 9000)) #connect to the server

input_data={"x":5, "y":70, "op":"MULTIPLY"}

input_json=json.dumps(input_data)

client.sendall(input_json.encode())
print('Agent A just sent the request')
print("...........")
respond_data=client.recv(1024)
respond=json.loads(respond_data.decode())
print("The result from server is: ", respond)


client.close()