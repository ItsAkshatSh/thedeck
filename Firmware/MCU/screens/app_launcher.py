import displayio
from adafruit_display_text.label import Label
from adafruit_display_shapes.rect import Rect
from adafruit_bitmap_font import bitmap_font
import config as C

COLS = 2
ROWS = 3
MARGIN = 14
GAP = 8
TILE_W = (C.SCREEN_W - MARGIN * 2 - GAP) // COLS
TILE_H = 72
TILE_START_Y = 38


def _tile_rect(col, row):
    x = MARGIN + col * (TILE_W + GAP)
    y = TILE_START_Y + row * (TILE_H + GAP)
    return x, y


def _hit(tx, ty, x, y):
    return x <= tx <= x + TILE_W and y <= ty <= y + TILE_H


class AppLauncherScreen:
    def __init__(self):
        small = bitmap_font.load_font(C.FONT_SMALL)
        medium = bitmap_font.load_font(C.FONT_MEDIUM)

        self.group = displayio.Group()
        self.group.append(Rect(0, 0, C.SCREEN_W, C.SCREEN_H, fill=C.BG))

        self.group.append(Label(small, text="Launcher", color=C.TEXT3, x=MARGIN, y=16))
        self.group.append(Rect(MARGIN, 26, C.SCREEN_W - MARGIN * 2, 1, fill=C.BG2))

        apps = C.APPS
        for idx in range(ROWS * COLS):
            col = idx % COLS
            row = idx // COLS
            tx, ty = _tile_rect(col, row)

            if idx < len(apps):
                label_text, color, _, _ = apps[idx]

                self.group.append(Rect(tx, ty, TILE_W, TILE_H, fill=color))

                self.group.append(Rect(tx, ty, TILE_W, 1, fill=C.BG3))
                self.group.append(Rect(tx, ty + TILE_H - 1, TILE_W, 1, fill=C.BG3))
                self.group.append(Rect(tx, ty, 1, TILE_H, fill=C.BG3))
                self.group.append(Rect(tx + TILE_W - 1, ty, 1, TILE_H, fill=C.BG3))

                lbl = Label(medium, text=label_text, color=C.TEXT)
                lbl.x = tx + TILE_W // 2 - lbl.bounding_box[2] // 2
                lbl.y = ty + TILE_H // 2 + lbl.bounding_box[3] // 4
                self.group.append(lbl)

            else:
                self.group.append(Rect(tx, ty, TILE_W, TILE_H, fill=C.BG1))
                self.group.append(Rect(tx, ty, TILE_W, 1, fill=C.BG2))
                self.group.append(Rect(tx, ty, 1, TILE_H, fill=C.BG2))

        total_w = (C.SCREEN_COUNT - 1) * 14 + 16
        start_x = C.SCREEN_W // 2 - total_w // 2
        for i in range(C.SCREEN_COUNT):
            active = i == C.SCREEN_LAUNCHER
            color = C.TEXT if active else C.TEXT3
            w = 16 if active else 6
            x = start_x + i * 14 - (w - 6) // 2
            self.group.append(Rect(x, 308, w, 6, fill=color))

    def handle_tap(self, tx, ty, state):
        apps = C.APPS
        for idx in range(min(len(apps), ROWS * COLS)):
            col = idx % COLS
            row = idx // COLS
            x, y = _tile_rect(col, row)
            if _hit(tx, ty, x, y):
                state.launch_action = apps[idx]
                return True
        return False

    def update(self, state):
        pass

    def step(self, dt):
        pass
