# Hardware Device Base Classes
Base classes for low-level hardware device modules.  The parent base class
includes logging with an optional console and file logger.  There is a child
base class for sensor devices and another for motion devices.

In the diagram below the methods in italics (with the *) are abstract while the
others are concrete.  Those that begin with a '+' are public while those that
begin with an underscore ,'_', are private.  Methods return None unless
otherwise indicated.

NOTE: The abstract methods must be implemented, but the concrete methods
can be used as is, or overridden.

See example_hardware_device.py for specific implementation examples.

```mermaid
classDiagram
    HardwareDeviceBase <|-- HardwareSensorBase
    HardwareDeviceBase <|-- HardwareMotionBase
    class HardwareDeviceBase {
        +bool connected
        +bool initialized
        +lock lock
        +Logger logger
        +int status
        +str status_string
        +bool verbose
        +connect()*
        +disconnect()*
        _send_command()* bool
        _read_reply()* Union[str, None]
        +get_status() Union[Tuple[int, str], None]
        +is_connected() bool
        +initialize() bool
        +is_initialized() bool
        +report_debug() 
        +report_info()
        +report_warning()
        +report_error()
        +set_verbose()
        +validate_connection_params() bool
        _set_status() 
        _set_connected()
    }

    class HardwareSensorBase {
        +get_atomic_value()* Union[float, int, str, None]
    }
    
    class HardwareMotionBase {
        +home()* bool
        +is_homed()* bool
        +set_pos()* bool
        +get_pos()* Union[float, int, None]
        +close_loop()* bool
        +is_loop_closed()* bool
        +get_limits()* Union[Dict[str, Tuple[float, float]], None]
    }

```