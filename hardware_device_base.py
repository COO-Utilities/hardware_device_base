"""
hardware_device_base.py

Defines an abstract base class for any device.
"""
import threading
import logging
from abc import ABC, abstractmethod
from typing import Union


class HardwareDeviceBase(ABC):
    """
    Abstract base class for any hardware device.

    This class defines the interface for establishing or closing a connection to a hardware device,
    and getting an atomic telemetry item from the device.  It also provides a logging feature that
    includes a console logger and defaults to logging.INFO level of logging.  A thread locking
    feature is also included.

    Subclasses must implement the following methods:
        * `connect()`: Establish a connection.
        * `disconnect()`: Gracefully close the connection.
        * `get_atomic_value()`: Get an atomic telemetry value.

    Subclasses may optionally override or use the following concrete methods:
        * `is_connected()`: Return True if the connection is active.
        * `set_connected()`: Set the connected status.
        * `set_verbose()`: Set the verbose level to include DEBUG logging (True) or not (False).

    See example_hardware_device_base.py for example usage.
    """

    def __init__(self, log: bool =True, logfile: str = None):
        """Instantiate the device class

        :param bool log: If True, log to file, otherwise log to stdout.
        :param str logfile: filename to log to.

        """
        super().__init__()

        # thread lock
        self.lock = threading.Lock()

        # connection status
        self.connected = False

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
                "%(asctime)s - %(levelname)s - %(funcName)s() - %(message)s"
            )
            file_handler = logging.FileHandler(logfile if ".log" in logfile else logfile + ".log")
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def set_verbose(self, verbose: bool =True) -> None:
        """Sets verbose mode.
        :param bool verbose: Verbose mode: True (default) DEBUG level or False INFO level.
        """
        self.verbose = verbose
        self.logger.setLevel(logging.DEBUG if verbose else logging.INFO)
        self.logger.debug("Verbose mode: %s", verbose)

    @abstractmethod
    def connect(self, *args) -> None:
        """Establishes a connection to the device.

        :param args: Positional arguments to pass to the constructor.

        The arguments should only provide what is needed to establish a connection.
        Examples include host and port for a socket connection, or port and baud rate
        for a direct serial connection.
        """
        self.connected = True

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnects from the device."""
        self.connected = False

    @abstractmethod
    def _send_command(self, command: str, *args) -> bool:
        """Send a command to the device.

        :param str command: Command to send.
        :param args: Positional arguments to pass to the constructor.
        :return: True if command was sent, False otherwise.
        """
        return True

    @abstractmethod
    def _read_reply(self) -> Union[str, None]:
        """Receive a reply from the device.
        :return: The reply or None if no reply was received."""
        return None

    @abstractmethod
    def _set_connected(self, connected: bool) -> None:
        """Optional concrete method that subclasses may override.

        :param bool connected: Whether the device connection has already been established.
        :return: None
        """
        self.connected = connected

    @abstractmethod
    def get_atomic_value(self, item: str ="") -> Union[float, int, str, None]:
        """Returns the value from the specified item.
        :param str item: item to get the value from.
        :return: value from the specified item.
        """
        return NotImplemented

    def is_connected(self) -> bool:
        """Optional concrete method that subclasses may override.

        Returns:
            bool: Connection status.
        """
        return self.connected
