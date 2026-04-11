from adafruit_bitmap_font import bitmap_font
import board

TFT_BL = board.D6
TFT_RST = board.D7
TFT_DC = board.D8
TFT_CS = board.D9
TFT_WR = board.D10

MCP_I2C_ADDR = 0x20
MCP_IODIR = 0x01FE

MCP_PIN_ENC_SWITCH = 8
MCP_PIN_ENC_B = 3
MCP_PIN_ENC_A = 4
MCP_BTN1 = 1
MCP_BTN2 = 2

SWIPE_MIN_DIST = 60
SWIPE_MAX_VERT = 80

I2C_SDA = board.D4
I2C_SCL = board.D5

SCREEN_W = 240
SCREEN_H = 320

RENDER_INTERVAL = 0.033
INPUT_INTERVAL = 0.02
TOUCH_INTERVAL = 0.016
SERIAL_INTERVAL = 0.05
POMO_TICK = 1.0

POMO_WORK_SECS = 25 * 60
POMO_BREAK_SECS = 5 * 60
POMO_SESSIONS_MAX = 4

ENC_SCALE = 2

TOUCH_X1 = board.A3
TOUCH_X2 = board.A1
TOUCH_Y1 = board.A2
TOUCH_Y2 = board.A0

TOUCH_CALIBRATION = ((0, 65535), (0, 65535))
TOUCH_Z_THRESHOLD = 10000

BG = 0x000000
BG1 = 0x0D0D0D
BG2 = 0x1A1A1A
BG3 = 0x2A2A2A

TEXT = 0xFFFFFF
TEXT2 = 0x8E8E93
TEXT3 = 0x48484A

ACCENT = 0x0A84FF
ACCENT2 = 0x30D158
ACCENT3 = 0xFF9F0A
ACCENT_DIM = 0x0A3060

FONT_SMALL = bitmap_font.load_font("fonts/helvR12.bdf")
FONT_MEDIUM = bitmap_font.load_font("fonts/helvR18.bdf")
FONT_LARGE = bitmap_font.load_font("fonts/helvB24.bdf")
FONT_TIMER = bitmap_font.load_font("fonts/helvB40.bdf")

SCREEN_NOW_PLAYING = 0
SCREEN_POMODORO = 1
SCREEN_SETTINGS = 2
SCREEN_LAUNCHER = 3
SCREEN_COUNT = 4


APPS = [
    (
        "Spotify",
        0x8E8E93,
        "path",
        r"C:/Program Files/WindowsApps/SpotifyAB.SpotifyMusic_1.283.461.0_x64__zpdnekdrzrea0/Spotify.exe",
    ),
    (
        "Slack",
        0x8E8E93,
        "path",
        r"C:/Program Files/WindowsApps/com.tinyspeck.slackdesktop_4.48.102.0_x64__8yrtsj140pw4g/app/Slack.exe",
    ),
    (
        "VS Code",
        0x8E8E93,
        "path",
        r"C:/Users/USER/AppData/Local/Programs/Microsoft VS Code/Code.exe",
    ),
    (
        "Terminal",
        0x8E8E93,
        "path",
        r"C:/Program Files/WindowsApps/Microsoft.WindowsTerminal_1.23.20211.0_x64__8wekyb3d8bbwe/WindowsTerminal.exe",
    ),
    (
        "Edge",
        0x8E8E93,
        "path",
        r"C:/Program Files (x86)/Microsoft/Edge\Application/msedge.exe",
    ),
    (
        "Epic Games",
        0x8E8E93,
        "path",
        r"C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Epic Games Launcher.lnk",
    ),
]
