# hardware device template
Template for low-level hardware device modules, which includes the abstract class

HardwareDeviceBase

This class has three abstract methods:
   - connect(self, host, port)
   - disconnect(self)
   - get_atomic_value(item)
