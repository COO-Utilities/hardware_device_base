"""
example_device.py
"""
import socket
from device_base import DeviceBase


class ExampleDevice(DeviceBase):
    """Example device class."""

    def __init__(self, log: bool = True, logfile: str = None, read_timeout: float = 1.0) -> None:
        super().__init__(log, logfile)
        self.sock: socket.socket | None = None
        self.read_timeout = read_timeout

    def connect(self, host: str, port: int) -> None:
        """Connects to the device."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((host, port))
        self.sock.settimeout(self.read_timeout)
        self.connected = True
        self.logger.info("Connected to %s:%d", host, port)

    def disconnect(self) -> None:
        """Disconnects from the device."""
        self.sock.close()
        self.sock = None
        self.connected = False
        self.logger.info("Disconnected from device")

    def is_connected(self) -> bool:
        """Checks if the device is connected."""
        return self.sock is not None
