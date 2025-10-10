"""
device_base.py

Defines an abstract base class for any device.
"""
import threading
import logging
import socket
from abc import ABC, abstractmethod


class DeviceBase(ABC):
    """
    Abstract base class for any device.
    All subclasses must implement connect(), disconnect() methods.
    """

    def __init__(self, log: bool =True, logfile: str = None):
        """Instantiate the device class

        :param bool log: If True, log to file, otherwise log to stdout.
        :param str logfile: filename to log to.

        """
        super().__init__()

        # thread lock
        self.lock = threading.Lock()

        # set up socket
        self.socket = None
        self.connected = False

        # last error message
        self.last_error =  ""

        # set up logging
        self.verbose = False
        if logfile is None:
            logfile = __name__.rsplit(".", 1)[-1]
        self.logger = logging.getLogger(logfile)
        self.logger.setLevel(logging.INFO)
        # log to console by default
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        # log to file if requested
        if log:
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler = logging.FileHandler(logfile + ".log")
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    @abstractmethod
    def connect(self, host:str, port:int) -> None:
        """Establishes a connection to the specified host and port."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnects from the device."""
        pass

    def is_connected(self) -> bool:
        """Optional concrete method that subclasses may override.

        Returns:
            bool: Connection status (default: False).
        """
        self.connected = False
        return False
