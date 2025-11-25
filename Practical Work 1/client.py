import os
import socket
import logging

BUFFER = 4096
PORT = 5001

logging.basicConfig(level=logging.INFO)


def create_client_socket(server_addr, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_addr, port))
    logging.info(f"Connected to server {server_addr}:{port}")
    return s


def send_file(sock, file_path):
    if not os.path.isfile(file_path):
        print("File does not exist.")
        return
    
    filename = os.path.basename(file_path)
    filesize = os.path.getsize(file_path)

    logging.info(f"Preparing to send '{filename}' ({filesize} bytes)")

    sock.send(len(filename).to_bytes(4, "big"))

    sock.send(filename.encode())

    sock.send(filesize.to_bytes(8, "big"))

    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(BUFFER)
            if not chunk:
                break
            sock.send(chunk)

    logging.info("File sent. Waiting for server response...")

    response = sock.recv(BUFFER).decode()
    print("Server:", response)


if __name__ == "__main__":
    server_address = "localhost"
    client_socket = create_client_socket(server_address, PORT)

    file_to_send = input("Enter file path: ")
    send_file(client_socket, file_to_send)

    client_socket.close()
