"""
example_hardware_device.py

TESTING:
    Use netcat (nc) on linux/unix to mock a dummy device.

    On one terminal issue the command:

    `nc -l 9999`

    Then run python in another terminal:

    `python`
    `>>> import examples.example_hardware_device as example_device`
    `>>> exdev = example_device.ExampleHardwareDevice()`
    `>>> exdev.connect("localhost", 9999)`
    `>>> exdev._send_command("test")`

    You should see the word "test" show up on the other terminal where nc is listening.
    When done, you can disconnect from the device:

    `>>> exdev.disconnect()`

    The nc command should terminate.
"""
import socket
from typing import Union

from hardware_device_base.hardware_sensor_base import HardwareSensorBase


class ExampleHardwareDevice(HardwareSensorBase):
    """Example device class."""

    def __init__(self, log: bool = True, logfile: str = __name__.rsplit(".", 1)[-1],
                 read_timeout: float = 1.0) -> None:
        super().__init__(log, logfile)
        self.sock: socket.socket | None = None
        self.read_timeout = read_timeout

    def connect(self, *args, con_type="tcp") -> None:  # pylint: disable=W0221
        """Connects to the device."""
        if self.validate_connection_params(args):
            if con_type == "tcp":
                host = args[0]
                port = args[1]
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((host, port))
                self.sock.settimeout(self.read_timeout)
                self._set_connected(True)
                self.logger.info("Connected to %s:%d", host, port)
                self._set_status((0, f"Connected to {host}:{port}"))
            elif con_type == "serial":
                self.logger.error("serial connection not implemented.")
                self._set_status((-1, "Serial connection not implemented."))
                return
            else:
                self.logger.error("unknown con_type: %s", con_type)
                self._set_status((-1, f"Unknown con_type: {con_type}"))
        else:
            self.logger.error("invalid connection params: %s", args)
            self._set_status((-1, f"Invalid connection params: {args}"))

    def disconnect(self) -> None:
        """Disconnects from the device."""
        if self.is_connected():
            self.sock.close()
            self.sock = None
            self._set_connected(False)
            self.logger.info("Disconnected from device")
            self._set_status((0, "Disconnected from device"))
        else:
            self.logger.warning("Already disconnected from device")
            self._set_status((0, "Already disconnected from device"))

    def get_atomic_value(self, item: str ="") -> Union[float, int, str, None]:
        """Returns the value from the specified item.
        :param item: The item to get the value from.
        :return: The value from the specified item.
        """
        if not self.is_connected():
            self.logger.error("Device is not connected")
            self._set_status((-1, "Device is not connected"))
            retval = None
        elif "temperature" in item:
            # Code for retrieving the temperature from the device.
            retval = 10.5
        else:
            retval = None
            self.logger.error("Unknown item '%s'", item)
            self._set_status((-1, f"Unknown item '{item}'"))
        self.logger.debug("Return value: %s", retval)
        self._set_status((0, "Atomic value retrieved"))
        return retval

    def _send_command(self, command: str, *args) -> bool:  # pylint: disable=W0221
        """Send a command to the device."""
        if not self.is_connected():
            self.logger.error("Device is not connected")
            self._set_status((-1, "Device is not connected"))
            return False
        if len(args) > 0:
            command = command + " ".join(args)
        with self.lock:
            self.sock.sendall(command.encode())
        self.logger.debug("Sent command: %s", command)
        self._set_status((0, "Command sent"))
        return True

    def _read_reply(self) -> Union[str, None]:
        """Receive a reply from the device."""
        if not self.is_connected():
            self.logger.error("Device is not connected")
            self._set_status((-1, "Device is not connected"))
            return None
        reply = self.sock.recv(1024)
        self._set_status((0, "Reply received"))
        return reply.decode()
