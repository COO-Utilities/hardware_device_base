"""
example_device.py
"""
import socket
from device_base import DeviceBase


class ExampleDevice(DeviceBase):
    """Example device class."""

    def __init__(self, read_timeout: float = 1.0) -> None:
        self.connected = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.read_timeout = read_timeout

    def connect(self, host: str, port: int) -> None:
        """Connects to the device."""
        self.sock.connect((host, port))
        self.sock.settimeout(self.read_timeout)
        self.connected = True

    def disconnect(self) -> None:
        """Disconnects from the device."""
        self.sock.close()
        self.connected = False
