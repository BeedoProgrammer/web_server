Web server
Part 1: Multi-threaded Web Server
Objective: Develop a multi-threaded web server in Python that handles basic HTTP requests.
Requirements:
The server should accept incoming connections, handle GET and POST requests, and respond appropriately.
For GET requests, the server should fetch and send the requested file if it exists or return a 404 error if not.
For POST requests, the server should acknowledge and save the uploaded file.
Implement persistent connections and handle multiple requests over a single connection.
You may need to implement a multi-threaded using Python's threading.
Part 2: HTTP Web Client
Objective: Create a web client in Python that communicates with your server using the HTTP protocol.
Requirements:
The client should handle GET and POST commands.
Establish a TCP connection with the server, send requests, and handle responses accordingly.
The client should store received files in the local directory and close the connection after all operations are completed.
