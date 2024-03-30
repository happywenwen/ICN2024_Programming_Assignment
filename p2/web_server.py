import socket
import sys

# Handle HTTP request
class HTTPRequest:
    def __init__(self, request_text):
        self.method = None
        self.path = None
        self.http_version = None
        self.headers = {}
        self.body = None

        # Split the request text into lines
        lines = request_text.split('\r\n')
        
        # Parse the request line
        request_line_parts = lines[0].split()
        self.method = request_line_parts[0]
        self.path = request_line_parts[1]
        self.http_version = request_line_parts[2]

        # Parse headers
        for line in lines[1:]:
            if line.strip():
                key, value = line.split(':', 1)
                self.headers[key.strip()] = value.strip()

        # Parse body (if present)
        if '\r\n\r\n' in request_text:
            body_start_index = request_text.index('\r\n\r\n') + len('\r\n\r\n')
            self.body = request_text[body_start_index:]

# Server setup
# Specify the IP address and port number (Use "127.0.0.1" for localhost on local machine)
# TODO Start
HOST, PORT = "127.0.0.1", 7777
# TODO end


# 1. Create a socket
# 2. Bind the socket to the address
# TODO Start
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((HOST, PORT))
# TODO End

# Listen for incoming connections (maximum of 1 connection in the queue)
# TODO Start
serverSocket.listen(0)
# TODO End

# Start an infinite loop to handle incoming client requests
while True:
    print('Ready to serve...')

    # Accept an incoming connection and get the client's address
    # TODO Start
    connectionSocket, address = serverSocket.accept()
    # TODO End
    print(str(address) + " connected")

    try:
        # Receive and decode the client's request
        # TODO Start
        message = connectionSocket.recv(1000).decode("utf-8")
        # TODO End

        # If the message is empty, set it to a default value
        if message == "":
            message = "/ /"

        # Print the client's request message
        print(f"client's request message: \n {message}")

        # Extract the filename from the client's request
        # TODO Start
        request = HTTPRequest(message)
        filename = request.path.split("/")[1]
        # TODO End
        print(f"Extract the filename: {filename}")

        # Open the requested file
        # Read the file's content and store it in a list of lines
        f = open(filename)
        outputdata = f.readlines()

        # 1. Send an HTTP response header to the client
        # 2. Send the content of the requested file to the client line by line
        # 3. Close the connection to the client
        # TODO Start
        response_header = "HTTP/1.1 200 OK\r\nContent-Type: text/html; encoding=utf8\r\nConnection: close\r\n\r\n"
        connectionSocket.send(response_header.encode("utf-8"))
        for response_body in outputdata:
            connectionSocket.send(response_body.encode("utf-8"))
        connectionSocket.close()
        # TODO End

    except IOError:
        # If the requested file is not found, send a 404 Not Found response
        # TODO Start
        response_header = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html; encoding=utf8\r\n\r\n"
        connectionSocket.send(response_header.encode("utf-8"))
        response_body = "<!DOCTYPE html>\n<html>\n<head>\n<title>404 Not Found</title>\n</head>\n<body>\n<h1>404 Not Found</h1>\n</body>\n</html>"
        connectionSocket.send(response_body.encode("utf-8"))
        connectionSocket.close()
        # TODO End
