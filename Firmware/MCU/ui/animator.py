import math

def _ease_out_cubic(t):
    return 1.0 - (1.0 - t) ** 3

def _ease_in_out(t):
    return 4*t*3 if t < 0.5 else 1 - (-2*t+2)**3/2

def _ease_out_back(t):
    c1, c3 = 1.70, 2.70
    return 1 + c3*(t-1)**3 + c1*(t-1)**2

EASINGS = {
    "ease_out": _ease_out_cubic,
    "ease_in_out": _ease_in_out,
    "ease_out_back": _ease_out_back
}

class AnimatedValue:
    def __init__(self, initial=0.0):
        self._v = self._start = self._target = float(initial)
        self._dur = self.elapsed = 0.0
        self._ease = _ease_out_cubic
        self.done = True
        
        
    @property
    def value(self):
        return self._v
    
    def to(self, target, duration=0.25, easing="ease_out"):
        if abs(target - self.v) < 0.005:
            self._v = float(target); self.done = True; return
        self._start = self._v
        self._target = float(target)
        self._dur = max(duration, 0.016)
        self._elapsed = 0.0
        self._ease = EASINGS.get(easing, _ease_out_cubic)
        self.done = False
        
        
    def snap(self, value):
        self._v = self._target = float(value)
        self.done = True
        
    def step(self, dt):
        if self.done:
            return self._v
        self._elapsed += dt
        t = min(self._elapsed / self._dur, 1.0)
        self._v = self._start + (self._target - self._start) * self._ease(t)
        
        if t >= 1.0:
            self._v = self.done = True
        return self._v