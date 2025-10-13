"""
example_hardware_device.py
"""
import socket
from typing import Union

from hardware_device_base import HardwareDeviceBase


class ExampleHardwareDevice(HardwareDeviceBase):
    """Example device class."""

    def __init__(self, log: bool = True, logfile: str = __name__.rsplit(".", 1)[-1],
                 read_timeout: float = 1.0) -> None:
        super().__init__(log, logfile)
        self.sock: socket.socket | None = None
        self.read_timeout = read_timeout

    def connect(self, host: str, port: int) -> None:
        """Connects to the device."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((host, port))
        self.sock.settimeout(self.read_timeout)
        self.set_connected(True)
        self.logger.info("Connected to %s:%d", host, port)

    def disconnect(self) -> None:
        """Disconnects from the device."""
        self.sock.close()
        self.sock = None
        self.set_connected(False)
        self.logger.info("Disconnected from device")

    def get_atomic_value(self, item: str ="") -> Union[float, int, str, None]:
        """Returns the value from the specified item.
        :param item: The item to get the value from.
        :return: The value from the specified item.
        """
        if not self.is_connected():
            self.logger.error("Device is not connected")
            return None
        if "temperature" in item:
            # Code for retrieving the temperature from the device.
            temp = 10.5
            return temp
        self.logger.error("Unknown item '%s'", item)
        return None
