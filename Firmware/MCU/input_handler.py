import asyncio
import usb_hid
import time

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from digitalio import Direction, Pull

from config import (
    MCP_BTN1,
    MCP_BTN2,
    MCP_PIN_ENC_A,
    MCP_PIN_ENC_B,
    MCP_PIN_ENC_SWITCH,
    INPUT_INTERVAL,
    ENC_SCALE,
)

_ENC_TABLE = (0, -1, 1, 0, 1, 0, 0, -1, -1, 0, 0, 1, 0, 1, -1, 0)


class InputHandler:

    def __init__(self, state, mcp, mcp_lock):
        self._state = state
        self._mcp = mcp
        self._mcp_lock = mcp_lock

        self._kbd = Keyboard(usb_hid.devices)
        self._layout = KeyboardLayoutUS(usb_hid.devices)
        self._cc = ConsumerControl(usb_hid.devices)

        self._btn1 = mcp.get_pin(MCP_BTN1)
        self._btn1.direction = Direction.INPUT
        self._btn1.pull = Pull.UP

        self._btn2 = mcp.get_pin(MCP_BTN2)
        self._btn2.direction = Direction.INPUT
        self._btn2.pull = Pull.UP

        self._enc_btn = mcp.get_pin(MCP_PIN_ENC_SWITCH)
        self._enc_btn.direction = Direction.INPUT
        self._enc_btn.pull = Pull.UP

        self._enc_a = mcp.get_pin(MCP_PIN_ENC_A)
        self._enc_a.direction = Direction.INPUT
        self._enc_a.pull = Pull.UP

        self._enc_b = mcp.get_pin(MCP_PIN_ENC_B)
        self._enc_b.direction = Direction.INPUT
        self._enc_b.pull = Pull.UP

        self._enc_last = self._enc_state_bits()
        self._enc_accum = 0

        self._btn1_last = True
        self._btn2_last = True
        self._enc_btn_last = True
        self._btn1_ms = 0
        self._btn2_ms = 0
        self._enc_btn_ms = 0

    def _enc_state_bits(self):
        a = self._enc_a.value
        b = self._enc_b.value
        return (1 if a else 0) << 1 | (1 if b else 0)

    def launch(self, action):
        _, _, launch_type, launch_value = action

        if launch_type == "path":
            self._kbd.press(Keycode.WINDOWS, Keycode.R)
            self._kbd.release_all()
            time.sleep(0.4)

            self._layout.write(launch_value)
            time.sleep(0.05)
            self._kbd.press(Keycode.ENTER)
            self._kbd.release_all()

        elif launch_type == "shortcut":
            self._kbd.press(*launch_value)
            time.sleep(0.05)
            self._kbd.release_all()

    async def run(self):
        while True:
            await asyncio.sleep(INPUT_INTERVAL)
            async with self._mcp_lock:
                now = time.monotonic()

                s = self._enc_state_bits()
                idx = (self._enc_last << 2) | s
                self._enc_accum += _ENC_TABLE[idx]
                self._enc_last = s

                steps = 0
                if abs(self._enc_accum) >= ENC_SCALE:
                    steps = self._enc_accum // ENC_SCALE
                    self._enc_accum -= steps * ENC_SCALE

                if steps != 0:
                    code = (
                        ConsumerControlCode.VOLUME_INCREMENT
                        if steps > 0
                        else ConsumerControlCode.VOLUME_DECREMENT
                    )
                    for _ in range(abs(steps)):
                        self._cc.send(code)

                b1 = self._btn1.value
                b2 = self._btn2.value
                eb = self._enc_btn.value

            if not b1 and self._btn1_last and (now - self._btn1_ms) > 0.5:
                self._btn1_ms = now
                self._state.toggle_play()
            self._btn1_last = b1

            if not b2 and self._btn2_last and (now - self._btn2_ms) > 0.5:
                self._btn2_ms = now
                self._state.toggle_play()
            self._btn2_last = b2

            if not eb and self._enc_btn_last and (now - self._enc_btn_ms) > 0.5:
                self._enc_btn_ms = now
                self._state.toggle_play()
            self._enc_btn_last = eb
