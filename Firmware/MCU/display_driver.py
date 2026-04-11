import time
import displayio
import pwmio
from digitalio import DigitalInOut
from fourwire import FourWire
from adafruit_ili9341 import ILI9341

from config import (
    TFT_BL,
    TFT_RST,
    TFT_DC,
    TFT_CS,
    TFT_WR,
    MCP_IODIR,
)

_DISPLAY_DATA = 1
_CS_TOGGLE_EACH_BYTE = 1


class _MCP8080Bus(FourWire):
    def __init__(self, mcp, *, command, chip_select, write, reset=None):
        object.__init__(self)
        self._mcp = mcp
        self._dc = DigitalInOut(command)
        self._dc.switch_to_output(value=False)
        self._cs = DigitalInOut(chip_select)
        self._cs.switch_to_output(value=True)
        self._wr = DigitalInOut(write)
        self._wr.switch_to_output(value=True)
        if reset is not None:
            self._rst = DigitalInOut(reset)
            self._rst.switch_to_output(value=True)
            self.reset()
        else:
            self._rst = None

    def reset(self) -> None:
        if self._rst is None:
            raise RuntimeError("No reset pin")
        self._rst.value = False
        time.sleep(0.002)
        self._rst.value = True
        time.sleep(0.002)

    def _free(self) -> bool:
        return True

    def _begin_transaction(self) -> bool:
        self._cs.value = False
        return True

    def _end_transaction(self) -> None:
        self._cs.value = True

    def _write_byte(self, value: int) -> None:
        g = self._mcp.gpio
        ga = g & 0xFF
        gb = (g >> 8) & 0xFF
        ga = (ga & 0xFE) | ((value >> 7) & 1)
        gb = (gb & 0x01) | ((value & 0x7F) << 1)
        self._mcp.gpio = (gb << 8) | ga
        self._wr.value = False
        self._wr.value = True

    def _send(self, data_type, chip_select, data) -> None:
        self._dc.value = data_type == _DISPLAY_DATA
        if chip_select == _CS_TOGGLE_EACH_BYTE:
            for byte in data:
                self._write_byte(byte)
                self._cs.value = True
                time.sleep(0.000001)
                self._cs.value = False
        else:
            for byte in data:
                self._write_byte(byte)


class DisplayDriver:
    def __init__(self, i2c, mcp):
        displayio.release_displays()

        mcp.iodir = MCP_IODIR

        bus = _MCP8080Bus(
            mcp,
            command=TFT_DC,
            chip_select=TFT_CS,
            write=TFT_WR,
            reset=TFT_RST,
        )

        self.display = ILI9341(
            bus,
            width=240,
            height=320,
            rotation=0,
            auto_refresh=False,
        )

        self.root = displayio.Group()
        self.display.root_group = self.root

        self._bl = pwmio.PWMOut(TFT_BL, frequency=1000, duty_cycle=0)
        self.set_brightness(80)

    def set_brightness(self, percent):
        pct = max(0, min(100, percent))
        self._bl.duty_cycle = int(pct / 100 * 65535)

    def refresh(self):
        self.display.refresh()
