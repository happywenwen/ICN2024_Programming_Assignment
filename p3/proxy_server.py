import socket

# Set the server IP address and port
# TODO Start
HOST, PORT = "127.0.0.1", 9999
# TODO end

# Create a server socket, bind it to the specified IP and port, and start listening
# TODO Start
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((HOST, PORT))
serverSocket.listen(0)
# TODO end

while True:
    print('Ready to serve...')
    # Accept an incoming connection and get the client's address
    # TODO Start
    client_socket, client_address = serverSocket.accept()
    # TODO end

    print('Received a connection from:', client_address)

    try:
        # Receive request from the client
        # TODO Start
        request = client_socket.recv(1000).decode("utf-8")
        # TODO end
        print(request)

        # Extract the filename from the request
        if request == "":
            request = "/ /"
        filename = request.split()[1].partition("/")[2]
        print(filename)
        file_path = "/" + filename
        print(file_path)

        file_exist = "false"
        try:
            # Check whether the file exists in the cache
            with open(file_path[1:], "r") as cache_file:
                output_data = cache_file.readlines()
            file_exist = "true"

            # ProxyServer finds a cache hit and generates a response message
            # Send the file data to the client
            client_socket.send("HTTP/1.1 200 OK\r\n".encode('utf-8'))
            client_socket.send("Content-Type:text/html\r\n\r\n".encode('utf-8'))
            # TODO Start
            for response_body in output_data:
                client_socket.send(response_body.encode("utf-8"))
            # TODO End
            print('Read from cache')

        # Error handling if the file is not found in cache
        except FileNotFoundError:
            if file_exist == "false":
                # Create a socket on the proxy server
                # TODO Start
                proxy_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # TODO End

                host_name = filename.replace("www.", "", 1)
                print("Host name is " + host_name)

                try:
                    print("Trying to connect to the web server")
                    # Connect the socket to the web server port
                    # TODO Start
                    proxy_server_socket.connect(("127.0.0.1", 7777))
                    # TODO End
                    print("Connected successfully")

                    # Create a temporary file on this socket
                    file_obj = proxy_server_socket.makefile('rw', None)

                    # Create the HTTP GET request message to fetch the file from the web server
                    # Write the request to the file-like object
                    request_message = f"GET {file_path} HTTP/1.0\r\n"
                    print(request_message)
                    file_obj.write(request_message)  # Write the request to the file-like object
                    file_obj.flush()
                    print("Sent the request to the web server successfully")

                    # Read the response into buffer
                    # TODO Start
                    server_message = file_obj.readlines()
                    html_content = server_message[server_message.index('<!DOCTYPE html>\n'):]
                    print("Read the file from the web server successfully")

                    # Create a new file in the cache for the requested file
                    # TODO Start
                    with open(file_path[1:], "w") as cache_file:
                        cache_file.writelines(html_content)
                    # TODO End
                    print("Wrote the file to the cache successfully")

                    # Send the response to the client socket
                    # TODO Start
                    client_socket.send("HTTP/1.1 200 OK\r\n".encode('utf-8'))
                    client_socket.send("Content-Type:text/html\r\n\r\n".encode('utf-8'))
                    for response_body in html_content:
                        client_socket.send(response_body.encode("utf-8"))
                    # TODO End
                    print("Sent the data from the web server to the client")
                except:
                    print("Illegal request")
            else:
                # HTTP response message for file not found
                # TODO Start
                response_header = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html; encoding=utf8\r\n\r\n"
                client_socket.send(response_header.encode("utf-8"))
                response_body = "<!DOCTYPE html>\n<html>\n<head>\n<title>404 Not Found</title>\n</head>\n<body>\n<h1>404 Not Found</h1>\n</body>\n</html>"
                client_socket.send(response_body.encode("utf-8"))
                # TODO End

    finally:
        # Close the client socket
        client_socket.close()

# Close the server socket
serverSocket.close()
