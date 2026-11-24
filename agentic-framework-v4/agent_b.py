import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from tools import operation
import time


class AgentBHandler(BaseHTTPRequestHandler):

    def do_POST(self):

        # Step 1: Check if self.path == "/calculate"
        if self.path != "/calculate":
            self.send_error(404, "Endpoint not found")
            return


        # Step 2: Read Content-Length
        length = int(self.headers["Content-Length"]) #e.g., 32 Bytes


        # Step 3: Read JSON request body using self.rfile
        body = self.rfile.read(length) #read all 32 bytes

        # Step 4: Decode JSON into a dictionary
        #data_object = json.loads(body.decode("utf-8")) #data_object is a python dictionary


        # Step 5: Call operation(**data_obj)
        #result = operation(**data_object)

        # Step 6: Serialize the result to JSON bytes
        #result_json=json.dumps({
        #    "status":"success",
        #    "message":result
        #})
        #result_bytes = result_json.encode("utf-8")

        try:
            # Step 1: Deserialize the request body
            data_object = json.loads(body.decode("utf-8"))

            agent = data_object.pop("agent")

            if agent == "A1":
                time.sleep(5)
            elif agent == "A2":
                time.sleep(10)

            # Step 2: Execute operation(**data_object)
            result = operation(**data_object)

            # Step 3: Create a success response
            response = {
                "status": "success",
                "message": result
            }
            status_code = 200

        except (ValueError, TypeError) as e:
            # Step 4: Create an error response
            response = {
                "status": "error",
                "message": str(e)
            }
            status_code = 400
        result_bytes = json.dumps(response).encode("utf-8")

        # Step 7: Send HTTP status, headers and body
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(result_bytes)))
        self.end_headers()
        self.wfile.write(result_bytes)



server = HTTPServer(
    ("127.0.0.1", 8001),
    AgentBHandler
)

server.serve_forever()