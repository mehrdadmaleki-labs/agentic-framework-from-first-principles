import requests
import json

url = "http://127.0.0.1:8000/calculate"

input_data = {
    "x" : 5,
    "y" : 0,
    "op": "DIVISION",
    "agent": "A1"
}

# Step 1: Send HTTP POST request
response = requests.post(url, json = input_data)

# Step 2: Check the HTTP status code
print(response.status_code)

# Step 3: Convert json response to a python dictionary
result = response.json()

print("Result: ", result)


