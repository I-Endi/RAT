import socket
import time

class Listener:
    """
    Listens for connections in a port and sends data
    """
    
    def __init__(self, port: int) -> None:
        """
        Constructor
        
        :param port: The port to listen to
        """
        
        self.port = port
        
        # Selects family IPv4 to connect to with TCP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    
    def listen(self) -> None:
        """
        Listens for connections on a port and enables data transfer
        """
        
        # Listens to local port
        listen_address = ("0.0.0.0", self.port)
        
        self.sock.bind(listen_address)
        self.sock.listen()
        conn = self.sock.accept()
        
        while 1:  # Infinite loop
            try:
                # Receives messages from client
                data = conn.recv(1024).decode("UTF-8")
                data = data.strip('\n')
                
                # Sends data through socket
                msg = input()
                conn.send(str.encode(str(msg)))
                
                conn.recv(1024).decode("UTF-8")
                
            except socket.error:
                # Wait and retry
                time.sleep(1)
