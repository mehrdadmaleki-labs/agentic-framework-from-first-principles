
# Agent A2 is a TCP client (send request to Agent B)

import socket
import json

client_2=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP connection

client_2.connect(("127.0.0.1", 9000)) #connect to the server

#------agent A2-----------
input_data_2={"x":5, "y":70, "op":"ADD"}

input_json_2=json.dumps(input_data_2)+"\n"

client_2.sendall(input_json_2.encode())
print('Agent A2 just sent the request')
print("&&&&&&&&&&&")

respond_data_2=client_2.makefile("r").readline()
respond_2=json.loads(respond_data_2)
print("The result from server is: ", respond_2)

client_2.close()
