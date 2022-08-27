# Enable serial data port
import usb_cdc
if not usb_cdc.data:
    usb_cdc.enable(console=True, data=True)

# Storage
import storage
storage.remount("/", readonly=False, disable_concurrent_write_protection=True)
storage.remount("/data", readonly=False, disable_concurrent_write_protection=False)