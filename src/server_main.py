import socket


class Server:
    """
    Not sure what this does lol
    """

    def __init__(self, host: str, port: int, sock: socket) -> None:
        """
        Constructor

        :param host: the server's address
        :param port:
        :param sock:
        """
        self.host = host
        self.port = port
        self.sock = sock

    def run(self) -> None:
        """
        Endi pls explain this
        """

        # Create file 'output.txt' and open int in writable binary
        file = open("output.txt", "wb")

        s = self.sock.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.host, self.port)
        s.bind(server_address)
        s.listen()
        conn, client_address = s.accept()
        data = conn.recv(15)
        file.write(data)
        print(data)
