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

    def connect(self, *args, con_type="tcp") -> None:
        """Connects to the device."""
        if con_type == "tcp":
            if len(args) < 2:
                self.logger.error("connect requires 2 arguments: host and port")
            host = args[0]
            if not isinstance(host, str):
                self.logger.error("connect requires host as a string")
                return
            port = args[1]
            if not isinstance(port, int):
                self.logger.error("connect requires port as an integer")
                return
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))
            self.sock.settimeout(self.read_timeout)
            self._set_connected(True)
            self.logger.info("Connected to %s:%d", host, port)
        elif con_type == "serial":
            self.logger.error("serial connection not implemented.")
            return
        else:
            self.logger.error("unknown con_type: %s", con_type)

    def _send_command(self, command: str, *args) -> bool:
        """Send a command to the device."""
        if not self.is_connected():
            self.logger.error("Device is not connected")
            return False
        if len(args) > 0:
            command = command + " ".join(args)
        self.sock.sendall(command.encode())
        self.logger.debug("Sent command: %s", command)
        return True

    def _read_reply(self) -> Union[str, None]:
        """Receive a reply from the device."""
        if not self.is_connected():
            self.logger.error("Device is not connected")
            return None
        reply = self.sock.recv(1024)
        return reply.decode()

    def disconnect(self) -> None:
        """Disconnects from the device."""
        if self.is_connected():
            self.sock.close()
            self.sock = None
            self._set_connected(False)
            self.logger.info("Disconnected from device")
        else:
            self.logger.warning("Already disconnected from device")

    def get_atomic_value(self, item: str ="") -> Union[float, int, str, None]:
        """Returns the value from the specified item.
        :param item: The item to get the value from.
        :return: The value from the specified item.
        """
        if not self.is_connected():
            self.logger.error("Device is not connected")
            retval = None
        elif "temperature" in item:
            # Code for retrieving the temperature from the device.
            retval = 10.5
        else:
            retval = None
            self.logger.error("Unknown item '%s'", item)
        self.logger.debug("Return value: %s", retval)
        return retval
