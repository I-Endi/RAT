import socket
import time


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
