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
    feature is also included (see _send_command method).

    Subclasses must implement the following public methods:
        * `connect()`: Establish a connection.
        * `disconnect()`: Gracefully close the connection.
        * `get_atomic_value()`: Get an atomic telemetry value.

    Subclasses must also implement the following private methods:
        * `_send_command()`: Send a command.
        * `_read_reply()`: Receive a reply.

    Subclasses may optionally override or use the following concrete methods:
        * `set_verbose()`: Set the verbose level to include DEBUG logging (True) or not (False).
        * `is_connected()`: Return True if the connection is active.
        * `_set_connected()`: Set the connected status.


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

    # public abstract methods
    @abstractmethod
    def connect(self, *args, con_type: str ="tcp") -> None:
        """Establishes a connection to the device.

        :param args: Positional arguments to pass to the constructor.
        :param str con_type: Type of connection to establish: serial or tcp.

        The arguments should only provide what is needed to establish a connection.
        Socket Example:
            self.connect("127.0.01", 9999)
        Serial Example:
            self.connect("/dev/tty1", 9600, con_type="serial")
        """
        self.connected = True

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnects from the device."""
        self.connected = False

    @abstractmethod
    def get_atomic_value(self, item: str ="") -> Union[float, int, str, None]:
        """Returns the value from the specified item.
        :param str item: item to get the value from.
        :return: value from the specified item.
        """
        return NotImplemented

    # private abstract methods
    @abstractmethod
    def _send_command(self, command: str, *args) -> bool:
        """Send a command to the device.

        :param str command: Command to send.
        :param args: Positional arguments to pass to the constructor.
        :return: True if command was sent, False otherwise.

        This command should lock the thread when sending the command
        Example:
            with self.lock:
                self.sock.sendall(command.encode())
        """
        return NotImplemented

    @abstractmethod
    def _read_reply(self) -> Union[str, None]:
        """Receive a reply from the device.
        :return: The reply or None if no reply was received."""
        return NotImplemented

    # public concrete methods
    def set_verbose(self, verbose: bool =True) -> None:
        """Sets verbose mode.
        :param bool verbose: Verbose mode: True (default) DEBUG level or False INFO level.
        """
        self.verbose = verbose
        self.logger.setLevel(logging.DEBUG if verbose else logging.INFO)
        self.logger.debug("Verbose mode: %s", verbose)

    def is_connected(self) -> bool:
        """Optional concrete method that subclasses may override.

        Returns:
            bool: Connection status.
        """
        return self.connected

    def validate_connection_params(self, *args) -> bool:
        """Validates connection parameters.
        :param args: Positional arguments for connect method.
        """
        if len(args[0]) < 2:
            self.logger.error("connect requires two connection parameters: %s", args)
            return False
        if not isinstance(args[0][0], str):
            self.logger.error("First argument must be a string.")
            return False
        if not isinstance(args[0][1], int):
            self.logger.error("Second argument must be a integer.")
            return False
        return True

    # private concrete methods
    def _set_connected(self, connected: bool) -> None:
        """Optional concrete method that subclasses may override.

        :param bool connected: Whether the device connection has already been established.
        :return: None
        """
        self.connected = connected
