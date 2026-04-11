import displayio
from adafruit_display_text.label import Label
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_bitmap_font import bitmap_font

from ui.progress_bar import ProgressBar
import config as C


class NowPlayingScreen:
    def __init__(self):
        small = bitmap_font.load_font(C.FONT_SMALL)
        medium = bitmap_font.load_font(C.FONT_MEDIUM)
        large = bitmap_font.load_font(C.FONT_LARGE)

        self.group = displayio.Group()

        self._bg = Rect(0, 0, C.SCREEN_W, C.SCREEN_H, fill=C.BG)
        self.group.append(self._bg)

        lbl = Label(small, text="Now Playing", fill=C.TEXT3, x=14, y=14)
        self.group.append(lbl)

        self._dot = Circle(C.SCREEN_W - 18, 11, 4, fill=C.TEXT3, outline=None)
        self.group.append(self._dot)

        ART_SIZE = 176
        ART_X = (C.SCREEN_W - ART_SIZE) // 2
        ART_Y = 28

        self.group.append(Rect(ART_X + 2, ART_Y + 2, ART_SIZE, ART_SIZE, fill=C.BG))
        self.group.append(Rect(ART_X, ART_Y, ART_SIZE, ART_SIZE, fill=C.BG1))

        self.group.append(Rect(ART_X, ART_Y, ART_SIZE, 1, fill=C.BG3))
        self.group.append(Rect(ART_X, ART_Y + ART_SIZE - 1, ART_SIZE, 1, fill=C.BG3))
        self.group.append(Rect(ART_X, ART_Y, 1, ART_SIZE, fill=C.BG3))
        self.group.append(Rect(ART_X + ART_SIZE - 1, ART_Y, 1, ART_SIZE, fill=C.BG3))

        note = Label(large, text="?", color=C.TEXT3)
        note.x = ART_SIZE // 2 - note.bounding_box[2] // 2
        note.y = ART_SIZE // 2 + note.bounding_box[3] // 4
        self.group.append(note)

        self._title = Label(large, text="Not Playing", color=C.TEXT2, x=14, y=218)
        self.group.append(self._title)

        self._artist = Label(medium, text="-", color=C.TEXT2, x=14, y=240)
        self.group.append(self._artist)

        self._prog_bar = ProgressBar(
            x=14,
            y=258,
            width=C.SCREEN_W - 28,
            height=2,
            fill_color=C.TEXT,
            bg_color=C.BG2,
            initial_pct=0.0,
        )
        self.group.append(self._prog_bar.group)

        self._t_cur = Label(small, text="0:00", color=C.TEXT3, x=14, y=265)
        self.group.append(self._t_cur)

        self._t_tot = Label(small, text="0:00", color=C.TEXT3)
        self._t_tot.y = 265
        self.group.append(self._t_tot)

        self.group.append(Rect(14, 294, C.SCREEN_W - 28, 1, fill=C.BG2))

        total_w = (C.SCREEN_COUNT - 1) * 14 + 16
        start_x = C.SCREEN_W // 2 - total_w // 2
        self._nav_dots = []
        for i in range(C.SCREEN_COUNT):
            active = i == C.SCREEN_NOW_PLAYING
            color = C.TEXT if active else C.TEXT3
            w = 16 if active else 6
            x = start_x + i * 14 - (w - 6) // 2
            dot = Rect(x, 308, w, 6, fill=color)
            self._nav_dots.append(dot)
            self.group.append(dot)

        self._last_bg = C.BG

    def _fit(self, text, font, max_w):
        if not text:
            return ""
        lbl = Label(font, text=text)
        if lbl.bounding_box[2] <= max_w:
            return text

        lo, hi = 1, len(text)
        while lo < hi - 1:
            mid = (lo + hi) // 2
            lbl.text = text[:mid] + "..."
            if lbl.bounding_box[2] <= max_w:
                lo = mid
            else:
                hi = mid

        return text[:lo] + "..."

    def update(self, state):
        medium = bitmap_font.load_font(C.FONT_MEDIUM)
        large = bitmap_font.load_font(C.FONT_LARGE)
        self._title.text = self._fit(state.title, large, C.SCREEN_W - 28)
        self._artist.text = self._fit(state.artist, medium, C.SCREEN_W - 28)
        self._t_cur.text = state.progress_str
        self._t_tot.text = state.duration_str
        self._t_tot.x = C.SCREEN_W - self._t_tot.bounding_box[2] - 14
        self._prog_bar.set_pct(state.progress_pct, animate=True)
        self.update_play_state(state.playing)

    def update_bg(self, state):
        target = state.bg_color if state.dynamic_bg else C.BG
        if target != self._last_bg:
            self._last_bg = target
            self._bg.fill = target

    def update_play_state(self, playing):
        self._dot.fill = C.ACCENT2 if playing else C.TEXT3

    def step(self, dt):
        self._prog_bar.step(dt)
