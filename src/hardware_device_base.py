"""
hardware_device_base.py

Defines an abstract base class for any device.
"""
import threading
import logging
from abc import ABC, abstractmethod
from typing import Union, Tuple


class HardwareDeviceBase(ABC):
    """
    Abstract base class for any hardware device.

    This class defines the interface for establishing or closing a connection to a hardware device,
    and setting and getting the status of the device.  It also provides a logging feature that
    includes a console logger and defaults to logging.INFO level of logging.  A thread locking
    feature is also included (see _send_command method).

    Subclasses must implement the following public methods:
        * `connect()`: Establish a connection.
        * `disconnect()`: Gracefully close the connection.

    Subclasses must also implement the following private methods:
        * `_send_command()`: Send a command.
        * `_read_reply()`: Receive a reply.

    Subclasses may optionally override or use the following concrete methods:
        * `get_status()`: Get the status of the device.
        * `set_verbose()`: Set the verbose level to include DEBUG logging (True) or not (False).
        * `is_connected()`: Return True if the connection is active.
        * `validate_connection_params()`: Validate the connection parameters.
        * `_set_connected()`: Set the connected status.
        * `_set_status()`: Set the status of the device.


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

        # device status
        self.status = 0
        self.status_string = ""

        # set up logging
        self.verbose = False
        if log:
            if logfile is None:
                logfile = __name__.rsplit(".", 1)[-1]
            self.logger = logging.getLogger(logfile)
            self.logger.setLevel(logging.INFO)
            # log to console by default
            console_formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s')
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(console_formatter)
            if not self.logger.hasHandlers():
                self.logger.addHandler(console_handler)
                # log to file if requested

                formatter = logging.Formatter(
                    "%(asctime)s - %(levelname)s - %(funcName)s() - %(message)s"
                )
                file_handler = logging.FileHandler(
                    logfile if ".log" in logfile else logfile + ".log")
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
        else:
            self.logger = None

    # public abstract methods
    @abstractmethod
    def connect(self, *args, **kwargs) -> None:
        """Establishes a connection to the device.

        :param args: Positional arguments to pass to the constructor.
        :param kwargs: Keyword arguments to pass to the constructor.

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

    # private abstract methods
    @abstractmethod
    def _send_command(self, *args, **kwargs) -> bool:
        """Send a command to the device.

        Expects the following arguments:
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
    def get_status(self) -> Union[Tuple[int, str], None]:
        """Get the status of the device."""
        return self.status, self.status_string

    def report_error(self, message: str, errno: int =-1) -> None:
        """Report an error message."""
        if self.logger:
            self.logger.error(message)
        else:
            print(f"ERROR ({errno}): {message}")
        self._set_status((errno, message))

    def report_info(self, message: str, errno: int =0) -> None:
        """Report info message."""
        if self.logger:
            self.logger.info(message)
        else:
            print(f"INFO ({errno}): {message}")
        self._set_status((errno, message))

    def report_warning(self, message: str, errno: int =0) -> None:
        """Report warning message."""
        if self.logger:
            self.logger.warning(message)
        else:
            print(f"WARNING ({errno}): {message}")
        self._set_status((errno, message))

    def report_debug(self, message: str) -> None:
        """Report debug message."""
        if self.logger:
            self.logger.debug(message)
        else:
            if self.verbose:
                print(message)

    def set_verbose(self, verbose: bool =True) -> None:
        """Sets verbose mode.
        :param bool verbose: Verbose mode: True (default) DEBUG level or False INFO level.
        """
        self.verbose = verbose
        if self.logger:
            self.logger.setLevel(logging.DEBUG if verbose else logging.INFO)
            self.logger.debug("Verbose mode: %s", verbose)
        else:
            print(f"Verbose mode: {verbose}.")

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

    def _set_status(self, status: Tuple[int, str]) -> None:
        """Optional concrete method that subclasses may override.
        :param Tuple[int, str] status: Status of the device."""
        if isinstance(status[0], int) and isinstance(status[1], str):
            self.status = status[0]
            self.status_string = status[1]
        else:
            self.logger.error("Status must be a tuple of form (int, string).")
