<<<<<<< HEAD
import asyncio
import rotaryio
import busio
import board
import usb_hid


from adafruit_mcp230xx.mcp23017 import MCP23017
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from digitalio import Direction, Pull

from config import (ENC_A, ENC_B, I2C_SDA, I2C_SCL,MCP_BTN1, MCP_BTN2, MCP_ENC_BTN, INPUT_INTERVAL, ENC_SCALE)


class InputHandler:
    
    def __init__(self, state):
        self._state = state
        
        self._cc = ConsumerControl(usb_hid.devices)
        
        self._enc = rotaryio.IncrementalEncoder(ENC_A, ENC_B)
        self._last_pos = 0
        
        i2c = busio.I2C(I2C_SCL, I2C_SDA)
        mcp = MCP23017(i2c)
        
        self._btn1 = mcp.get_pin(MCP_BTN1)
        self._btn1.direction = Direction.INPUT
        self._btn1.pull = Pull.UP
        
        self._btn2 = mcp.get_pin(MCP_BTN2)
        self._btn2.direction = Direction.INPUT
        self._btn2.pull = Pull.UP
        
        self._enc_btn = mcp.get_pin(MCP_ENC_BTN)
        self._enc_btn.direction = Direction.INPUT
        self._enc_btn.pull = Pull.UP
        
        self._btn1_last = True
        self._btn2_last = True
        self._btn1_ms = 0
        self._btn2_ms = 0
        
    async def run(self):
        import time
        while True:
            await asyncio.sleep(INPUT_INTERVAL)
            now = time.monotonic()
            
            
            
            pos = self._enc.position
            delta = pos - self._last_pos
            
            steps = 0
            if abs(delta) >= ENC_SCALE:
                steps = delta // ENC_SCALE
                self._last_pos = pos - (delta % ENC_SCALE)
                
            if steps != 0:
                code = (ConsumerControlCode.VOLUME_INCREMENT if steps > 0 else ConsumerControlCode.VOLUME_DECREMENT)
                for _ in range(abs(steps)):
                    self._cc.send(code)
                    
            b1 = self._btn1.value
            if not b1 and self._btn1_last and (now - self._btn1_ms) > 0.5:
                self._btn1_ms = now
                self._state.toggle_play()
            self._btn1_last = b1
            
            
            b2 = self._btn2.value   
            if not b2 and self._btn2_last and (now - self._btn2_ms) > 0.5:
                self._btn2_ms = now
                self._state.toggle_play()
=======
import asyncio
import rotaryio
import busio
import board
import usb_hid


from adafruit_mcp230xx.mcp23017 import MCP23017
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from digitalio import Direction, Pull

from config import (ENC_A, ENC_B, I2C_SDA, I2C_SCL,MCP_BTN1, MCP_BTN2, MCP_ENC_BTN, INPUT_INTERVAL, ENC_SCALE)


class InputHandler:
    
    def __init__(self, state):
        self._state = state
        
        self._cc = ConsumerControl(usb_hid.devices)
        
        self._enc = rotaryio.IncrementalEncoder(ENC_A, ENC_B)
        self._last_pos = 0
        
        i2c = busio.I2C(I2C_SCL, I2C_SDA)
        mcp = MCP23017(i2c)
        
        self._btn1 = mcp.get_pin(MCP_BTN1)
        self._btn1.direction = Direction.INPUT
        self._btn1 = Pull.UP
        
        self._btn2 = mcp.get_pin(MCP_BTN2)
        self._btn2.direction = Direction.INPUT
        self._btn2.pull = Pull.UP
        
        self._enc_btn = mcp.get_pin(MCP_ENC_BTN)
        self._enc_btn.direction = Direction.INPUT
        self._enc_btn.pull = Pull.UP
        
        self._btn1_last = True
        self._btn2_last = True
        self._btn1_ms = 0
        self._btn2_ms = 0
        
    async def run(self):
        import time
        while True:
            await asyncio.sleep(INPUT_INTERVAL)
            now = time.monotonic()
            
            
            
            pos = self._enc_position
            delta = pos - self._last_pos
            
            if abs(delta) >= ENC_SCALE:
                steps = delta // ENC_SCALE
                self._last_pos = pos - (delta % ENC_SCALE)
                
                
            code = (ConsumerControlCode.VOLUME_INCREMENT if steps > 0 else ConsumerControlCode.VOLUME_DECREMENT)
            for _ in range(abs(steps)):
                self._cc.send(code)
                    
            b1 = self._btn1.value
            if not b1 and self._btn1_last and (now - self._btn1_ms) > 0.5:
                self._btn1_ms = now
                self.state.toggle_play()
            self._btn1_last = b1
            
            
            b2 = self._btn2.value   
            if not b2 and self._btn2_last and (now - self._btn2_ms) > 0.5:
                self._btn2_ms = now
                self.state.toggle_play()
>>>>>>> 1278d2b57e44c250325702984b0e62a3c63bf3e6
            self._btn2_last = b2