import base64
import xmlrpc.client
import os

SERVER_URL = "http://127.0.0.1:9000"
proxy = xmlrpc.client.ServerProxy(SERVER_URL, allow_none=True)

def send_file(file_path):
    if not os.path.exists(file_path):
        print("File not found.")
        return

    filename = os.path.basename(file_path)
    print(f"[CLIENT] Sending file: {filename}")

    with open(file_path, "rb") as f:
        data = f.read()

    data_base64 = base64.b64encode(data).decode()

    response = proxy.upload_file(filename, data_base64)
    print("[SERVER]:", response)

if __name__ == "__main__":
    print(proxy.ping())
    file_path = input("Enter file path to send: ")
    send_file(file_path)
