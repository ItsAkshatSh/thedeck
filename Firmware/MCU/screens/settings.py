import displayio
from adafruit_display_text.label import Label
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_bitmap_font import bitmap_font
from ui.progress_bar import ProgressBar
import config as C

class SettingsScreen:
    def __init__(self):
        small = bitmap_font.load_font(C.FONT_SMALL)
        medium =  bitmap_font.load_font(C.FONT_MEDIUM)
        
        self.group = displayio.Group()
        self.group.append(Rect(0, 0, C.SCREEN_W, C.SCREEN_H, fill=C.BG))
        
        
        self.group.append(Label(medium, text="Settings", color=C.TEXT, x=14, y=20))
        self.group.append(Rect(14,34, C.SCREEN_W - 28, 1, fill=C.BG2))
        
        
        
        
        self.group.append(Label(small, text="Display", color=C.TEXT2, x=14, y=48))
        
        self._bright_val = Label(small, text="80%", color=C.TEXT2)
        self._bright_val.x = C.SCREEN_W - self._bright_val.bounding_box[2] - 14
        self._bright_val.y = 64
        self.group.append(self._bright_val)
        
        self._bright_bar = ProgressBar(
            x=14, y=76, width=C.SCREEN_W - 28, height=3, fill=C.ACCENT3, bg_color=C.BG2, initial_pct=0.8
        )
        
        self.group.append(self._bright_bar.group)
        self.group.append(Rect(14,88, C.SCREEN_W - 28, 1, fill=C.BG2))
        
        
        
        
        self.group.append(Label(small, text="Appearence", color=C.TEXT3, x=14, y=102))
        
        self.group.append(Label(small, text="Dynamic BG", color=C.TEXT2, x=14, y=118))
        
        self._dyn_sub = Label(small, text="Album art color - off", color = C.TEXT3)
        self._dyn_sub.x = 14
        self._dyn_sub.y = 132
        self.group.append(self._dyn_sub)
        
        PILL_W, PILL_H = 44, 22
        pill_x = C.SCREEN_W - 14 - PILL_W
        pill_y = 112
        
        self._pill_bg = Rect(pill_x, pill_y, PILL_W, PILL_H, fill = C.BG3)
        self.group.append(self._pill_bg)
        
        self._pill_knob = Circle(pill_x + 11, pill_y + 11, 9, fill=C.TEXT3, outline=None)
        self.group.append(self._pill_knob)
        
        self.group.append(Rect(14, 152, C.SCREEN_W - 28, 1, fill=C.BG2))
        
        
        
        
        
        self.group.append(Label(small, text="Controls", color=C.TEXT3, x=14, y=166))
        
        ctrl_rows = [
            ("Encoder", "Volume")
            ("MX1/MX2", "Play/Pause")
            ("Swipe", "Change Screen")
        ]
        
        for i, (k,v) in enumerate(ctrl_rows):
            y = 188 + i * 18
            self.group.append(Label(small, text=k, color=C.TEXT2, x=14, y=y))
            vl = Label(small, text=v, color=C.TEXT3)
            vl.x = C.SCREEN_W - vl.bounding_box[2] - 14
            vl.y = y
            self.group.append(vl)
            
        self.group.append(Rect(14, 174, C.SCREEN_W - 28, 1, fill=C.BG2))
        
        
        for i in range(3):
            active = (i == C.SCREEN_SETTINGS)
            color = C.TEXT if active else C.TEXT3
            w = 16 if active else 6
            x = C.SCREEN_W // 2 - 14 + i * 14 - w // 2
            self.group.append(Rect(x, 308, w, 6, fill=color))
    
    
    
    
    
    def update(self, state):
        self._bright_bar.set_pct(state.brightness / 100, animate=True)
        self._bright_val.text = f"{state.brightness}%"
        self._bright_val.x = C.SCREEN_W - self._bright_val.bounding_box[2] - 14
        
    def step(self, dt):
        self._bright_bar.step(dt)
            