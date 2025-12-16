"""
hardware_sensor_base.py

Defines an abstract base class for any sensor device.
"""

from abc import abstractmethod
from typing import Union
from hardware_device_base import HardwareDeviceBase


class HardwareSensorBase(HardwareDeviceBase):
    """
    Abstract base class for sensor device.

    This class defines the interface for getting an atomic telemetry item from the sensor device.

    Subclasses must implement the following public methods:
        * `get_atomic_value()`: Get an atomic telemetry value.

    The following methods are from the general HardwareDeviceBase class defined in
    hardware_device_base.py:

    def __init__(self, log: bool =True, logfile: str = None):

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
        * `initialize()`: Initialize the hardware sensor device.
        * `is_initialized()`: Return True if the hardware sensor device is initialized.
        * `validate_connection_params()`: Validate the connection parameters.
        * `_set_connected()`: Set the connected status.
        * `_set_status()`: Set the status of the device.

    See example_sensor_device_base.py for example usage.
    """

    @abstractmethod
    def get_atomic_value(self, item: str ="") -> Union[float, int, str, None]:
        """Returns the value from the specified item.
        :param str item: item to get the value from.
        :return: value from the specified item.
        """
        return NotImplemented
