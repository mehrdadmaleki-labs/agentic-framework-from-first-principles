
# Agent A1 is a TCP client (send request to Agent B)

import socket
import json

client_1=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP connection

client_1.connect(("127.0.0.1", 9000)) #connect to the server

#------agent A1-----------
input_data_1={"x":5, "y":70, "op":"MULTIPLY"}

input_json_1=json.dumps(input_data_1)+"\n"

client_1.sendall(input_json_1.encode())
print('Agent A1 just sent the request')
print("...........")

respond_data_1=client_1.makefile("r").readline()
respond_1=json.loads(respond_data_1)
print("The result from server is: ", respond_1)

client_1.close()
