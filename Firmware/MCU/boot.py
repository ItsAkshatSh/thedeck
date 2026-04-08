import usb_hid
import usb_cdc

usb_hid.enable((
    usb_hid.Device.KEYBOARD,
    usb_hid.Device.MOUSE,
    usb_hid.Device.CONSUMER_CONTROL
))

usb_cdc.enable(console=True, data=True)