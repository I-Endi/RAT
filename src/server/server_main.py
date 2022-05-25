from listen import Listener


class Server:
    """
    Starts the listener on the server
    """

    def __init__(self, port: int) -> None:
        """
        Constructor

        :param port: The server's port
        """

        self.port = port

        # Create listener instance
        self.Listener = Listener(self.port)

    def run(self) -> None:
        """
        Starts to listen for connections from client
        """

        self.Listener.listen()

        # Close connection when finished
        self.Listener.sock.close()


if __name__ == "__main__":
    # Run listener with specified port
    Server(4444).run()
