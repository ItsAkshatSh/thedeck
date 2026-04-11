import displayio
from ui.animator import AnimatedValue
from adafruit_display_shapes.arc import Arc


class ArcWidget:
    def __init__(self, cx, cy, radius, thickness=0, bg_color=0x1A1A1A, fill_color=0x0A84FF, initial_pct=0.0):
        self._cx = cx; self._cy = cy
        self._r = radius; self._t = thickness
        self._bg = bg_color; self._fill_color = fill_color
        self._anim = AnimatedValue(initial_pct)
        self._last_pct = -1.0
        self._last_color = fill_color
        self.group = displayio.Group()
        self._rebuild(initial_pct)
        
    def _rebuild(self, pct):
        while len(self.group):
            self.group.pop()
        self.group.append(Arc(x=self._cx, y=self._cy, radius=self._r, angle=360, direction=0, segments=60, stroke=self._t, arc_color=self._bg, arc_inner_color=0x000000))
        
        angle = max(1, int(pct * 360))
        self.group.append(
            Arc(
                x=self._cx,
                y=self._cy,
                radius=self._r,
                angle=angle,
                direction=270,
                segments=max(4, angle // 6),
                stroke=self._t,
                arc_color=self._fill_color,
                arc_inner_color=0x000000,
            )
        )

    def set_color(self, color):
        self._fill_color = color

    def set_pct(self, pct, animate=True, duration=0.5):
        pct = max(0.0, min(1.0, pct))
        if animate:
            self._anim.to(pct, duration=duration, easing="ease_in_out")
        else:
            self._anim.snap(pct)
            
    def step(self, dt):
        self._anim.step(dt)
        v = self._anim.value
        if abs(v - self._last_pct) < 0.004 and self._fill_color == self._last_color:
            return
        self._last_pct = v
        self._last_color = self._fill_color
        self._rebuild(v)

    @property
    def done(self):
        return self._anim.done
