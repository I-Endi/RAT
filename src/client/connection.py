import os
import socket
import time
import sys

class Connection:
    '''
    Opens a socket conection between server and client
    '''
    
    def __init__(self, host: str, port: int) -> None:
        '''
        Constructor
        
        :param host: IP of server
        :param port: Port of server
        '''
        
        self.host = host
        self.port = port


    def connect(self) -> socket:
        '''
        Creates socket connection between client and server
        '''
        
        # Selects family IPv4 to connect to with TCP 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Creates tuple with address and port
        server_address = (self.host, self.port)
        
        while True: # Try until it connects
            try:            
                # Connect to host
                self.sock.connect(server_address)
                break
            except socket.error:
                # Wait 5 seconds and retry
                time.sleep(5)

        # Connection succesful
        self.sock.send(str.encode("Succesfully connected\n"))
        
        return self.sock