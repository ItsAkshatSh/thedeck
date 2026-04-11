import displayio
from adafruit_display_shapes.rect import Rect
from ui.animator import AnimatedValue


class ProgressBar:
    def __init__(self, x, y, width, height, fill_color=0x0A84FF, bg_color=0x2A2A2A, initial_pct=0.0):
        self._x = x
        self.y = y
        self._w = width
        self.height = height
        self._fill_color = fill_color
        self._anim = AnimatedValue(initial_pct)
        self._last = -1.0

        self.group = displayio.Group()
        self._bg = Rect(x, y, width, height, fill=bg_color)
        self._fill = Rect(x, y, max(1, int(initial_pct * width)), height, fill=fill_color)

        self.group.append(self._bg)
        self.group.append(self._fill)

    def set_pct(self, pct, animate=True, duration=0.3, easing="ease_out"):
        pct = max(0.0, min(1.0, pct))
        if animate:
            self._anim.to(pct, duration=duration, easing=easing)
        else:
            self._anim.snap(pct)

    def step(self, dt):
        self._anim.step(dt)
        v = self._anim.value
        if abs(v - self._last) < 0.003:
            return

        self._last = v
        self._fill.width = max(1, int(v * self._w))

    @property
    def done(self):
        return self._anim.done
