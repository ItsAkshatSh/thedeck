<<<<<<< HEAD
import asyncio
import time
import digitalio
import adafruit_stmpe610

from config import (TOUCH_CS, TOUCH_CALIBRATION, TOUCH_BAUD, TOUCH_PRESSURE_THRESHOLD, SWIPE_MAX_VERT, SWIPE_MIN_DIST, SCREEN_H, SCREEN_W, TOUCH_INTERVAL)

SWIPE_NONE = 0
SWIPE_LEFT = 1
SWIPE_RIGHT = 2

class TouchHandler:
    
    def __init__(self, spi):
        cs = digitalio.DigitalInOut(TOUCH_CS)
        
        self._ts = adafruit_stmpe610.Adafruit_STMPE610_SPI(spi, 
                                                           cs, 
                                                           baudrate = TOUCH_BAUD,
                                                           calibration = TOUCH_CALIBRATION,
                                                           size=(SCREEN_W, SCREEN_H),
                                                           disp_rotation=0,
                                                           touch_flip=(False, False)
                                                           )
        
        self.swipe_event = SWIPE_NONE
        
        self._touching = False
        self._start_x = 0
        self._start_y = 0
        self._current_x = 0
        self._current_y = 0
        self._start_time = 0
    
        async def run(self):
            while True:
                await asyncio.sleep(TOUCH_INTERVAL)
                
                point = self._ts.touch_point
                
                if point is not None:
                    x, y, pressure = point
                    
                    if not self._touching:
                        self._touching = True
                        self._start_x = x
                        self._start_y = y
                        self._start_time = time.monotonic()
                        
                    self._current_x = x
                    self._current_y = y
                    
                else:
                    if self._touching:
                        self._touching = False
                        elapsed = time.monotonic() - self._start_time
                        
                        if elapsed < 0.05:
                            continue
                        
                        dx = self._current_x - self._start_x
                        dy = self._current_y - self._start_y
                        
                        if abs(dx) >= SWIPE_MIN_DIST and abs(dy) <= SWIPE_MAX_VERT:
                            self.swipe_event = (SWIPE_LEFT if dx < 0 else SWIPE_RIGHT)
                            
                            
                
=======
import asyncio
import time
import digitalio
import adafruit_stmpe610

from config import (TOUCH_CS, TOUCH_CALIBRATION, TOUCH_BAUD, TOUCH_PRESSURE_THRESHOLD, SWIPE_MAX_VERT, SWIPE_MIN_DIST, SCREEN_H, SCREEN_W, TOUCH_INTERVAL)

SWIPE_NONE = 0
SWIPE_LEFT = 1
SWIPE_RIGHT = 2

class TouchHandler:
    
    def __init__(self, spi):
        cs = digitalio.DigitalInOut(TOUCH_CS)
        
        self._ts = adafruit_stmpe610.Adafruit_STMPE610_SPI(spi, 
                                                           cs, 
                                                           baudrate = TOUCH_BAUD,
                                                           calibration = TOUCH_CALIBRATION,
                                                           size=(SCREEN_W, SCREEN_H),
                                                           disp_rotation=0,
                                                           touch_flip=(False, False)
                                                           )
        
        self.swipe_event = SWIPE_NONE
        
        self._touching = False
        self._start_x = 0
        self._start_y = 0
        self._current_x = 0
        self._current_y = 0
        self._start_time = 0
    
        async def run(self):
            while True:
                await asyncio.sleep(TOUCH_INTERVAL)
                
                point = self._ts.touch_point
                
                if point is not None:
                    x, y, pressure = point
                    
                    if not self._touching:
                        self._touching = True
                        self._start_x = x
                        self._start_y = y
                        self._start_time = time.monotonic()
                        
                    self._current_x = x
                    self._current_y = y
                    
                else:
                    if self._touching:
                        self._touching = False
                        elapsed = time.monotonic() - self._start_time
                        
                        if elapsed < 0.05:
                            continue
                        
                        dx = self._current_x - self._start_x
                        dy = self._current_y - self._start_y
                        
                        if abs(dx) >= SWIPE_MIN_DIST and abs(dy) <= SWIPE_MAX_VERT:
                            self.swipe_event = (SWIPE_LEFT if dx < 0 else SWIPE_RIGHT)
                            
                            
                
>>>>>>> 1278d2b57e44c250325702984b0e62a3c63bf3e6
        