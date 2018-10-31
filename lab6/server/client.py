import socket
import json

HOST = '127.0.0.1'    # The remote host
PORT = 8080            # The same port as used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    l = {
  "label": "o",
  "n": 12,
  "number": 8,
  "content": {
    "data": {
      "x": [0,
  0,
  0,
  0,
  0,
  -9,
  -4,
  -4,
  3,
  8,
  10,
  6,
  2,
  -1,
  -8,
  -4,
  -7,
  -2,
  3,
  9,
  8,
  6,
  4,
  0,
  -3,
  -4,
  -3,
  0,
  0,
  0],
      "y": [0,
  0,
  0,
  0,
  0,
  -4,
  3,
  6,
  7,
  0,
  0,
  -2,
  -5,
  -3,
  -6,
  6,
  2,
  7,
  4,
  2,
  0,
  -3,
  -1,
  -4,
  -2,
  0,
  -1,
  0,
  0,
  0]
    }
  }
}
    l = json.dumps(l).encode()
    s.sendall(l)
    data = s.recv(1024)
print('Received', repr(data))