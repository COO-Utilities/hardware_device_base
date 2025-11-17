"""
hardware_device_base.py

Defines an abstract base class for any device.
method list:
    Queries:
        is_active
        is_closed_loop
        get_error
        get_pos
        get_named_pos
        get_target
    Commands
        connect
        disconnect
        home
        close_loop
        reference
        set_pos
        load_presets
"""
from abc import abstractmethod
from typing import Union

from hardware_device_base import HardwareDeviceBase

class HardwareMotionBase(HardwareDeviceBase):
    """
    Abstract base class for any hardware motion device.

    This class defines the interface for interacting with the hardware motion device.

    Subclasses must implement the following public methods:
        * `get_status()`: Get a status string of the hardware motion device.

    Subclasses must also implement the following private methods:


    Subclasses may optionally override or use the following concrete methods:


    See example_hardware_stage.py for example usage.
    """
    @abstractmethod
    def get_status(self) -> Union[str, None]:
        """Get the status of the hardware motion device.
        :return: The status of the hardware motion device.
        """
        return NotImplemented

    @abstractmethod
    def is_active(self) -> bool:
        """Check if the hardware motion device is active."""
        return NotImplemented
    @abstractmethod
    def
