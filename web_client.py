import socket as sk
import os

host = "192.168.1.4"
port = 65535

def send_request(request):
    with sk.socket(sk.AF_INET, sk.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.sendall(request)
        
        response = b''
        while True:
            part = client_socket.recv(1024)
            if not part:
                break
            response += part
    
    return response

def upload_file(filename, file_path):
    if os.path.isdir(file_path):
        file_path = os.path.join(file_path, filename)
    
    if not os.path.isfile(file_path):
        print(f"FileNotFoundError: The file {file_path} does not exist.")
        return

    with open(file_path, 'rb') as file:
            file_data = file.read()

    request = (
        f'POST /upload HTTP/1.1\r\n'
        f'Host: {host}\r\n'
        f'Content-Length: {len(file_data)}\r\n'
        f'Content-Type: application/octet-stream\r\n'
        f'Content-Disposition: attachment; filename="{filename}"\r\n'
        f'\r\n'
    )
    
    request_bytes = request.encode() + file_data
    response = send_request(request_bytes)
    
    headers, _ = response.split(b'\r\n\r\n', 1)
    if b'200 OK' in headers:
        print("Uploaded file successfully")
    else:
        print("File failed to upload")

def download_file(filename, save_path):
    if os.path.isdir(save_path):
        save_path = os.path.join(save_path, filename)
    
    request = (
        f'GET /{filename} HTTP/1.1\r\n'
        f'Host: {host}\r\n'
        f'\r\n'
    )
    
    response = send_request(request.encode())
    
    headers, body = response.split(b'\r\n\r\n', 1)
    
    if b'200 OK' in headers:
        with open(save_path, 'wb') as file:
            file.write(body)
        print('File downloaded successfully.')
    else:
        print('Failed to download file.')

if __name__ == '__main__':
    print("1) Upload image")
    print("2) Download image")
    
    flag = 1
    while flag:
        num = input("\nChoose an option: ")

        if num == '1' or num == '2':
            flag = 0
        else:
            print("Error! Choose from previous numbers.")

    if num == '1':
        filename = input("Enter file name: ")
        file_path = input("Enter file path: ")
        upload_file(filename, file_path)
    if num == '2':
        filename = input("Enter file name: ")
        save_path = input("Enter save path: ")
        download_file(filename, save_path)
    