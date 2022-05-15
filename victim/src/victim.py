import os
import socket
import sys

def make_conn():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ipaddr = "172.20.10.2"
    port = 4444

    file = open("test.txt","rb")
    server_address = (ipaddr, port)
    sock.connect(server_address)
    sock.sendfile(file)
    


