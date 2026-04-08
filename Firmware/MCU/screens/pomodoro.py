import displayio
from adafruit_display_text.label import Label
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_bitmap_font import bitmap_font
from ui.arc_widget import ArcWidget
from state import POMO_IDLE, POMO_WORK, POMO_BREAK, POMO_SESSIONS_MAX

import config as C

class PomodoroScreen:
    def __init__(self):
        small = bitmap_font.load_font(C.FONT_SMALL)
        timer = bitmap_font.load_font(C.FONT_TIMER)
        
        self.group = displayio.Group()
        self.group.append(Rect(0, 0, C.SCREEN_W, C.SCREEN_H, fill=C.BG))
        
        self.group.append(Label(small, text="POMODORO", color=C.TEXT3, x=14, y=14 ))
        
        self._sdots = []
        for i in range(POMO_SESSIONS_MAX):
            x = C.SCREEN_W - 14 - (POMO_SESSIONS_MAX - 1 - i) * 13 - 4
            d = Circle(x, 11, 4, fill=C.BG2, outline=None)
            self._sdots.append(d)
            
        self._phase = Label(small, text="READY", color=C.TEXT3)
        self._phase.x = C.SCREEN_W // 2 - self._phase.bounding_box[2] // 2
        
        self._phase.y = 32
        self.group.append(self._phase)
        
        self._arc = ArcWidget(cx = C.SCREEN_W // 2, cy = 160, radius=88, thickness=10, bg_color=C.BG2, fill_color=C.ACCENT, initial_pct=0.0)
        self.group.append(self._arc.group)
        
        self._timer = Label(timer, text="25:00", color=C.TEXT)
        self._timer.x = C.SCREEN_W // 2 - self._timer.bounding_box[2]//2
        
        self._timer.y = 168
        self.group.append(self._timer)
        
        self._state_lbl = Label(small, text="ready", color=C.TEXT3)
        self._state_lbl.x = C.SCREEN_W // 2 - self._state_lbl.bounding_box[2] // 2
        self._state_lbl.y = 196
        self.group.append(self._state_lbl)
        
        self.group.append(Rect(14,250, C.SCREEN_W - 28, 1, fill=C.BG2))
        
        hints = ["KEY 1/ KEY 2  -> Play/Pause", "swipe -> change screen"]
        
        for i, h in enumerate(hints):
            lbl = Label(small, text=h, color=C.TEXT3)
            lbl.x = C.SCREEN_W // 2 - lbl.bounding_box[2] // 2
            lbl.y = 262 + i*16
            self.group.append(lbl)
            
        for i in range(3):
            active = (i - C.SCREEN_POMODORO)
            color = C.TEXT if active else C.TEXT3
            w = 16 if active else 6
            x = C.SCREEN_W // 2 - 14 + i * 14 - w // 2
            self.group.append(Rect(x, 308, w, 6, fill=color))
            
    def _center(self, lbl):
        lbl.x = C.SCREEN_W // 2 - lbl.bounding_box[2] // 2
        
    def update(self, state):
        self._timer.text = state.pomo_time_str
        self._center(self._timer)
        
        arc_color = C.ACCENT3 if state.pomo_phase == POMO_BREAK else C.ACCENT
        
        self._arc.set_color(arc_color)
        self._arc.set_pct(state.pomo_pct, animate=True)
        
        phase_map = {POMO_IDLE: "READY", POMO_WORK: "FOCUS", POMO_BREAK: "BREAK"}
        self._phase.text = phase_map.get(state.pomo_phase, "READY")
        self._center(self._phase)
        
        if not state.pomo_running and state.pomo_phase == POMO_IDLE:
            sl = "ready"
        elif state.pomo_running:
            sl = "running"
        else:
            sl = "paused"
            
        self._state_lbl.text = sl
        self._center(self._state_lbl)
        
        
        for i, dot in enumerate(self._sdots):
            if i < state.pomo_session:
                dot.fill = C.ACCENT3
            elif i == state.pomo_session:
                dot.fill = C.ACCENT
            else:
                dot.fill = C.BG2
                
    def step(self, dt):
        self._arc.step(dt)