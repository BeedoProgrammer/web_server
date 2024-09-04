import socket as sk
import threading

def handle_client(client_socket):
    request = b''
    while b'\r\n\r\n' not in request:
        request += client_socket.recv(1024)
    
    headers, body = request.split(b'\r\n\r\n', 1)

    try:
        headers_text = headers.decode('utf-8')
    except UnicodeDecodeError:
        print("Error decoding headers")
        client_socket.close()
        return

    print(f"Received headers: {headers_text}")

    request_lines = headers_text.splitlines()
    if len(request_lines) > 0:
        request_line = request_lines[0]
        method, path, _ = request_line.split()
        if method == 'GET':
            get_request(client_socket, path)
        elif method == "POST":
            content_length = 0
            filename = 'uploaded_file'  
            content_type = 'application/octet-stream'  

            for line in request_lines:
                if line.startswith('Content-Length:'):
                    content_length = int(line.split(':')[1].strip())
                elif line.startswith('Content-Disposition:'):
                    filename = line.split('filename=')[1].strip('"')

            if len(body) < content_length:
                body += client_socket.recv(content_length - len(body))
            post_request(client_socket, filename, body)
        else:
            send_response(client_socket, 'HTTP/1.1 405 Method Not Allowed', 'Method Not Allowed', 'text/plain')

    client_socket.close()

def get_request(client_socket, path):
    try:
        if path == '/':
            path = '/index.html'
        with open('.' + path, "rb") as file:
            content = file.read()
        send_response(client_socket, 'HTTP/1.1 200 OK', content, "text/html")
    except FileNotFoundError:
        send_response(client_socket, 'HTTP/1.1 404 Not Found', 'File Not Found', 'text/plain')

def post_request(client_socket, filename, body):
    try:
        with open(filename, 'wb') as file:
            file.write(body)
        send_response(client_socket, 'HTTP/1.1 200 OK', 'File Uploaded Successfully', 'text/plain')
    except IOError as e:
        print(f"Error saving file: {e}")
        send_response(client_socket, 'HTTP/1.1 500 Internal Server Error', 'Error Saving File', 'text/plain')

def send_response(client_socket, status, content, content_type):
        response_header = f"{status}\r\nContent-Type: {content_type}\r\nContent-Length: {len(content)}\r\n\r\n"
        client_socket.sendall(response_header.encode())

def start_server(host="192.168.1.4", port=65535):
    server_socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    while True:
        client_socket, client_add = server_socket.accept()
        print(f"Connected to {client_add}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()