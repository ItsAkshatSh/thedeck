import asyncio
import time

import adafruit_touchscreen

from config import (
    SWIPE_MAX_VERT,
    SWIPE_MIN_DIST,
    SCREEN_W,
    SCREEN_H,
    TOUCH_INTERVAL,
    TOUCH_X1,
    TOUCH_X2,
    TOUCH_Y1,
    TOUCH_Y2,
    TOUCH_CALIBRATION,
    TOUCH_Z_THRESHOLD,
)

SWIPE_NONE = 0
SWIPE_LEFT = 1
SWIPE_RIGHT = 2


class TouchHandler:
    def __init__(self):
        self._ts = adafruit_touchscreen.Touchscreen(
            TOUCH_X1,
            TOUCH_X2,
            TOUCH_Y1,
            TOUCH_Y2,
            calibration=TOUCH_CALIBRATION,
            size=(SCREEN_W, SCREEN_H),
            z_threshold=TOUCH_Z_THRESHOLD,
        )

        self.swipe_event = SWIPE_NONE
        self.tap_event = None

        self._touching = False
        self._start_x = 0
        self._start_y = 0
        self._current_x = 0
        self._current_y = 0
        self._start_time = 0

    def _touch_point(self):
        p = self._ts.touch_point
        if p is None:
            return None
        x, y, _z = p
        return int(x), int(y)

    async def run(self):
        while True:
            await asyncio.sleep(TOUCH_INTERVAL)

            point = self._touch_point()

            if point is not None:
                x, y = point
                x = max(0, min(SCREEN_W - 1, x))
                y = max(0, min(SCREEN_H - 1, y))

                if not self._touching:
                    self._touching = True
                    self._start_x = x
                    self._start_y = y
                    self._start_time = time.monotonic()

                self._current_x = x
                self._current_y = y

            elif self._touching:
                self._touching = False
                elapsed = time.monotonic() - self._start_time

                dx = self._current_x - self._start_x
                dy = self._current_y - self._start_y

                if abs(dx) >= SWIPE_MIN_DIST and abs(dy) <= SWIPE_MAX_VERT and elapsed >= 0.05:
                    self.swipe_event = SWIPE_LEFT if dx < 0 else SWIPE_RIGHT
                elif abs(dx) < 20 and abs(dy) < 20 and elapsed < 0.5:
                    self.tap_event = (self._start_x, self._start_y)
