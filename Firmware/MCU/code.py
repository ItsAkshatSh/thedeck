import asyncio
import time
import displayio
import busio

from adafruit_mcp230xx.mcp23017 import MCP23017

from config import I2C_SCL, I2C_SDA, MCP_I2C_ADDR
from state import State, SCREEN_NOW_PLAYING, SCREEN_POMODORO, SCREEN_SETTINGS, SCREEN_LAUNCHER
from display_driver import DisplayDriver
from touch_handler import TouchHandler, SWIPE_LEFT, SWIPE_RIGHT, SWIPE_NONE
from input_handler import InputHandler
from serial_handler import SerialHandler
from ui.transition import Transition
from screens.now_playing import NowPlayingScreen
from screens.pomodoro import PomodoroScreen
from screens.settings import SettingsScreen
from screens.app_launcher import AppLauncherScreen

state = State()
state.launch_action = None

_i2c = busio.I2C(I2C_SCL, I2C_SDA, frequency=400_000)
_mcp = MCP23017(_i2c, address=MCP_I2C_ADDR)
_mcp_lock = asyncio.Lock()

display = DisplayDriver(_i2c, _mcp)
trans = Transition()

screens = [
    NowPlayingScreen(),
    PomodoroScreen(),
    SettingsScreen(),
    AppLauncherScreen(),
]

display.root.append(screens[SCREEN_NOW_PLAYING].group)

touch_handler = TouchHandler()
input_handler = InputHandler(state, _mcp, _mcp_lock)
serial_handler = SerialHandler(state)

SCREEN_COUNT = 4


def switch_screen(direction):
    if trans.active:
        return
    old = state.screen
    new = (old + 1) % SCREEN_COUNT if direction == SWIPE_LEFT else (old - 1) % SCREEN_COUNT

    state.prev_screen = old
    state.screen = new
    screens[new].update(state)
    trans.start(
        root_group=display.root,
        old_group=screens[old].group,
        new_group=screens[new].group,
        direction="left" if direction == SWIPE_LEFT else "right",
    )


async def input_task():
    await input_handler.run()


async def touch_task():
    await touch_handler.run()


async def serial_task():
    await serial_handler.run()


async def pomo_task():
    while True:
        await asyncio.sleep(1.0)
        if state.pomo_running:
            state.pomo_tick()
            if state.screen == SCREEN_POMODORO:
                screens[SCREEN_POMODORO].update(state)


async def render_task():
    last = time.monotonic()
    while True:
        await asyncio.sleep(0.033)
        now = time.monotonic()
        dt = now - last
        last = now

        swipe = touch_handler.swipe_event
        if swipe != SWIPE_NONE:
            touch_handler.swipe_event = SWIPE_NONE
            switch_screen(swipe)

        tap = touch_handler.tap_event
        if tap is not None:
            touch_handler.tap_event = None

            if state.screen == SCREEN_SETTINGS:
                consumed = screens[SCREEN_SETTINGS].handle_tap(tap[0], tap[1], state)
                if consumed and not state.dynamic_bg:
                    screens[SCREEN_NOW_PLAYING].update_bg(state)
            elif state.screen == SCREEN_LAUNCHER:
                screens[SCREEN_LAUNCHER].handle_tap(tap[0], tap[1], state)

        if state.launch_action is not None:
            action = state.launch_action
            state.launch_action = None
            input_handler.launch(action)

        if trans.active:
            trans.step(dt)

        if state.media_dirty:
            state.media_dirty = False
            screens[SCREEN_NOW_PLAYING].update(state)

        screens[state.screen].step(dt)

        async with _mcp_lock:
            display.refresh()


async def main():
    await asyncio.gather(
        asyncio.create_task(input_task()),
        asyncio.create_task(touch_task()),
        asyncio.create_task(serial_task()),
        asyncio.create_task(pomo_task()),
        asyncio.create_task(render_task()),
    )


asyncio.run(main())
