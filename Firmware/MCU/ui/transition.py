from ui.animator import AnimatedValue
from config import SCREEN_W

class Transition:
    def __init__(self):
        self._active = False
        self._old = self._new = self.root = None
        self._anim = AnimatedValue(0.0)
        self._dir  = "left"
        
        
    def start(self, root_group, old_group, new_group, direction="left"):
        self._root = root_group
        self._old = old_group
        self._new = new_group
        self._dir = direction
        new_group.x = SCREEN_W if direction == "left" else -SCREEN_W
        root_group.append(new_group)
        self._anim.snap(0.0)
        self._anim.to(1.0, duration=0.22, easing="ease_in_out")
        self._active = True
        
    def step(self, dt):
        if not self._active:
            return True
        self._anim.step(dt)
        t = self._anim.value
        if self._dir == "left":
            self._old.x = int(-t * SCREEN_W)
            self._new.x = int(SCREEN_W - t * SCREEN_W)
        else:
            self._old.x = int(t * SCREEN_W)
            self._new.x = int(-SCREEN_W + t * SCREEN_W)
        if self._anim.done:
            self._old.x = -SCREEN_W if self._dir == "left" else SCREEN_W
            self._new.x = 0
            try:
                self._root.remove(self._old)
            except ValueError:
                pass
            self._active = False
            return True
        return False
    
    @property
    def active(self):
        return self._active
