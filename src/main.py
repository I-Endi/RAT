import os
import socket,subprocess

def main(ip: str, port: int):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_address = (ip, port)
    s.bind(server_address)
    s.listen()
    conn, client_address = s.accept()
    data = conn.recv(15)
    print(data)

if __name__ == "__main__":
    main("172.20.10.2", 4444)
