# Hardware Device Base Classes
Base classes for low-level hardware device modules.  The parent base class
includes logging with an optional console and file logger.  There is a child
base class for sensor devices and another for motion devices.

In the diagram below the methods in italics (with the *) are abstract while the
others are concrete.  Those that begin with a '+' are public while those that
begin with an underscore ,'_', are private.

NOTE: The abstract methods must be implemented, but the concrete methods
can be used as is, or overridden.

See example_hardware_device.py for specific implementation examples.

```mermaid
classDiagram
    HardwareDeviceBase <|-- HardwareSensorBase
    HardwareDeviceBase <|-- HardwareMotionBase
    class HardwareDeviceBase {
        +bool connected
        +lock lock
        +Logger logger
        +int status
        +str status_string
        +bool verbose
        +connect()*
        +disconnect()*
        _send_command()*
        _read_reply()*
        +get_status()
        +is_connected()
        +report_debug()
        +report_info()
        +report_warning()
        +report_error()
        +set_verbose()
        +validate_connection_params()
        _set_status()
        _set_connected()
    }

    class HardwareSensorBase {
        +get_atomic_value()*
    }
    
    class HardwareMotionBase {
        +home()*
        +is_homed()*
        +set_pos()*
        +get_pos()*
        +close_loop()*
        +is_loop_closed()*
        +get_limits()*
    }

```