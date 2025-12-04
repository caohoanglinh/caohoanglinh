from xmlrpc.server import SimpleXMLRPCServer
import base64

HOST = "0.0.0.0"
PORT = 9000

def upload_file(filename, data_base64):
    data = base64.b64decode(data_base64)
    with open(filename, "wb") as f:
        f.write(data)
    print(f"[SERVER] Received file: {filename}")
    return "File uploaded successfully."

def ping():
    return "RPC Server alive!"

print(f"[SERVER] Starting XML-RPC server on {HOST}:{PORT}")
server = SimpleXMLRPCServer((HOST, PORT), allow_none=True)
server.register_function(upload_file, "upload_file")
server.register_function(ping, "ping")

server.serve_forever()
