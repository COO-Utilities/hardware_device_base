"""
device_base.py

Defines an abstract base class for any device.
"""
from abc import ABC, abstractmethod


class DeviceBase(ABC):
    """
    Abstract base class for any device.
    All subclasses must implement connect(), disconnect() methods.
    """

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
        return False

    def _log(self) -> None:
        """Logs information about the device."""
        pass

    def _send_command(self, command:str) -> None:
        """Sends a command to the device."""
        pass

    def _read_reply(self) -> bytes:
        """Reads a reply from the device."""
        pass
