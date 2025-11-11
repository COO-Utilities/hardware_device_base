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

    See example_sensor_device_base.py for example usage.
    """

    @abstractmethod
    def get_atomic_value(self, item: str ="") -> Union[float, int, str, None]:
        """Returns the value from the specified item.
        :param str item: item to get the value from.
        :return: value from the specified item.
        """
        return NotImplemented
