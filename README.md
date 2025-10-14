# hardware device base class
Base class for low-level hardware device modules.  It includes logging with a console logger and optional file logger.

HardwareDeviceBase

This class has these abstract methods:
   - connect(host, port)
   - disconnect()
   - _send_command()
   - _read_reply()
   - _set_connected()
   - get_atomic_value(item)

This class also has these concrete methods:
   - set_verbose()
   - is_connected()
