<<<<<<< HEAD
from adafruit_bitmap_font import bitmap_font
import board

#Pins - TFT
TFT_CS = board.D2
TFT_DC = board.D3
TFT_MOSI = board.D10
TFT_MISO = board.D9
TFT_SCK = board.D8
TFT_BL = board.D1


SWIPE_MIN_DIST = 60
SWIPE_MAX_VERT = 80

I2C_SDA = board.D4
I2C_SCL = board.D5

#MCP
MCP_BTN1 = 1
MCP_BTN2 = 2
MCP_ENC_BTN = 8

#Rotary Encoder
ENC_A = board.D6
ENC_B = board.D7

#Screen
SCREEN_W = 240
SCREEN_H = 320

#Timing
RENDER_INTERVAL = 0.033
INPUT_INTERVAL = 0.02
TOUCH_INTERVAL = 0.016
SERIAL_INTERVAL = 0.05
POMO_TICK = 1.0

#POMO

POMO_WORK_SECS = 25 * 60
POMO_BREAK_SECS = 5 * 60
POMO_SESSIONS_MAX = 4

ENC_SCALE = 2

#touch
TOUCH_CS = board.D2
TOUCH_BAUD = 1000000
TOUCH_CALIBRATION = ((357, 3812), (390, 3555))
TOUCH_PRESSURE_THRESHOLD = 1000


#Color
BLACK = 0x000000
WHITE = 0xFFFFFF
GREEN = 0x00FF00
AMBER = 0xFFBF00
RED = 0xFF0000
BLUE = 0x0000FF
BLUE_DIM = 0x000080

#Font
FONT_SMALL = bitmap_font.load_font("fonts/helvR12.bdf")
FONT_MEDIUM = bitmap_font.load_font("fonts/helvR18.bdf")
FONT_LARGE = bitmap_font.load_font("fonts/helvB24.bdf")
FONT_TIMER = bitmap_font.load_font("fonts/helvB40.bdf")

=======
from adafruit_bitmap_font import bitmap_font
import board

#Pins - TFT
TFT_CS = board.D2
TFT_DC = board.D3
TFT_MOSI = board.D10
TFT_MISO = board.D9
TFT_SCK = board.D8



SWIPE_MIN_DIST = 60
SWIPE_MAX_VERT = 80

I2C_SDA = board.D4
I2C_SCL = board.D5

#MCP
MCP_BTN1 = 1
MCP_BTN2 = 2
MCP_ENC_BTN = 8

#Rotary Encoder
ENC_A = board.D6
ENC_B = board.D7

#Screen
SCREEN_W = 240
SCREEN_H = 320

#Timing
RENDER_INTERVAL = 0.033
INPUT_INTERVAL = 0.02
TOUCH_INTERVAL = 0.016
SERIAL_INTERVAL = 0.05
POMO_TICK = 1.0

#POMO

POMO_WORK_SECS = 25 * 60
POMO_BREAK_SECS = 5 * 60
POMO_SESSIONS_MAX = 4

ENC_SCALE = 2

#touch
TOUCH_CS = board.D2
TOUCH_BAUD = 1000000
TOUCH_CALIBRATION = ((357, 3812), (390, 3555))
TOUCH_PRESSURE_THRESHOLD = 1000


#Color
BLACK = 0x000000
WHITE = 0xFFFFFF
GREEN = 0x00FF00
AMBER = 0xFFBF00
RED = 0xFF0000
BLUE = 0x0000FF
BLUE_DIM = 0x000080

#Font
FONT_SMALL = bitmap_font.load_font("fonts/helvR12.bdf")
FONT_MEDIUM = bitmap_font.load_font("fonts/helvR18.bdf")
FONT_LARGE = bitmap_font.load_font("fonts/helvB24.bdf")
FONT_TIMER = bitmap_font.load_font("fonts/helvB40.bdf")

>>>>>>> 1278d2b57e44c250325702984b0e62a3c63bf3e6
