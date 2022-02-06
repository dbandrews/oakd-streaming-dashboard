import socket
import sys

HOST, PORT = "192.168.0.13", 8070
data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))

    # # Receive data from the server and shut down
    while True:
        received = str(sock.recv(1024), "utf-8")
        print("Received: {}".format(received))

# print("Sent:     {}".format(data))
# print("Received: {}".format(received))
