"""
hardware_motion_base.py

Defines an abstract base class for any motion device.
"""
from abc import abstractmethod
from typing import Union, Tuple

from hardware_device_base import HardwareDeviceBase

class HardwareMotionBase(HardwareDeviceBase):
    """
    Abstract base class for any hardware motion device.

    This class defines the interface for interacting with the hardware motion device.

    Subclasses must implement the following public methods:
        * `close_loop()`: Close the loop for the hardware motion device.
        * `is_closed_loop()`: Check if the hardware motion device is closed loop.
        * `home()`: Home the hardware motion device.
        * `is_homed()`: Check if the hardware motion device is homed.
        * `get_pos()`: Get the position of the hardware motion device.
        * `set_pos(pos)`: Set the position of the hardware motion device.
        * `get_limits()`: Get the limits of the hardware motion device.
        * `set_limits(limits)`: Set the limits of the hardware motion device.

    The following methods are from the general HardwareDeviceBase class defined in
    hardware_device_base.py:

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

    See example_hardware_stage.py for example usage.
    """

    @abstractmethod
    def close_loop(self) -> bool:
        """Close the loop for the hardware motion device."""
        return NotImplemented

    @abstractmethod
    def is_closed_loop(self) -> bool:
        """Check if the hardware motion device is closed loop."""
        return NotImplemented

    @abstractmethod
    def home(self) -> bool:
        """Home the hardware motion device."""
        return NotImplemented

    @abstractmethod
    def is_homed(self) -> bool:
        """Check if the hardware motion device is homed."""
        return NotImplemented

    @abstractmethod
    def get_pos(self) -> Union[float, int, None]:
        """Get the position of the hardware motion device."""
        return NotImplemented

    @abstractmethod
    def set_pos(self, pos: Union[float, int]) -> None:
        """Set the position of the hardware motion device."""
        return NotImplemented

    @abstractmethod
    def get_limits(self):
        """Get the limits of the hardware motion device."""
        return NotImplemented

    @abstractmethod
    def set_limits(self, limits: Tuple[Union[float, int]]) -> None:
        """Set the limits of the hardware motion device."""
        return NotImplemented
