import asyncio, argparse, sys, time, io
import serial, serial.tools.list_ports

from winsdk.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager as MediaManager,
    GlobalSystemMediaTransportControlsSessionPlaybackStatus as PlaybackStatus,
)
from winsdk.windows.storage.streams import Buffer, InputStreamOptions, DataReader

from PIL import Image

_PIL = True


async def get_thumbnail_bytes(thumbnail_ref):
    try:
        stream = await thumbnail_ref.open_read_async()
        size = stream.size
        buf = Buffer(size)
        await stream.read_async(buf, size, InputStreamOptions.READ_AHEAD)
        reader = DataReader.from_buffer(buf)
        data = bytearray(size)
        reader.read_bytes(data)
        return bytes(data)
    except Exception:
        return None


def dominant_color_darkened(img_bytes):
    if not _PIL:
        return "000000"
    try:
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        img = img.resize((8, 8), Image.LANCZOS)
        pixels = list(img.getdata())
        r = sum(p[0] for p in pixels) // len(pixels)
        g = sum(p[1] for p in pixels) // len(pixels)
        b = sum(p[2] for p in pixels) // len(pixels)

        brightest = max(r, g, b, 1)
        scale = 50 / brightest
        r = min(255, int(r * scale))
        g = min(255, int(g * scale))
        b = min(255, int(b * scale))

        return f"{r:02X}{g:02X}{b:02X}"
    except Exception:
        return "000000"


def find_port():
    for p in serial.tools.list_ports.comports():
        if any(k in (p.description or "").lower()
               for k in ["circuitpython", "xiao", "rp2040"]):
            return p.device
    ports = serial.tools.list_ports.comports()
    return ports[-1].device if ports else None


def open_serial(port, baud=115200, retries=5):
    for _ in range(retries):
        try:
            return serial.Serial(port, baud, timeout=1)
        except serial.SerialException:
            time.sleep(2)
    sys.exit(1)


async def get_media():
    try:
        sessions = await MediaManager.request_async()
        session = sessions.get_current_session()
        if not session:
            return None

        props = await session.try_get_media_properties_async()
        if not props:
            return None

        title = (props.title or "Unknown").replace("|", "-").strip()
        artist = (props.artist or "Unknown").replace("|", "-").strip()

        pb = session.get_playback_info()
        playing = pb.playback_status == PlaybackStatus.PLAYING if pb else False

        tl = session.get_timeline_properties()
        prog = dur = 0
        if tl:
            prog = int(tl.position.total_seconds())
            if tl.end_time and tl.start_time:
                dur = int((tl.end_time - tl.start_time).total_seconds())

        bg_color = "000000"
        if _PIL and props.thumbnail:
            img_bytes = await get_thumbnail_bytes(props.thumbnail)
            if img_bytes:
                bg_color = dominant_color_darkened(img_bytes)

        return dict(title=title, artist=artist,
                    prog=prog, dur=dur, playing=playing,
                    bg_color=bg_color)
    except Exception:
        return None


async def main_loop(ser, interval):
    last_title = None

    while True:
        t0 = time.monotonic()
        info = await get_media()

        if info:
            line = (f"{info['title']}|{info['artist']}|"
                    f"{info['prog']}|{info['dur']}|"
                    f"{1 if info['playing'] else 0}|"
                    f"{info['bg_color']}\n")
            if info['title'] != last_title:
                last_title = info['title']
        else:
            line = "Not Playing|--|0|0|0|000000\n"

        try:
            ser.write(line.encode())
        except serial.SerialException:
            ser.close()
            time.sleep(3)
            ser.open()

        await asyncio.sleep(max(0.0, interval - (time.monotonic() - t0)))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--port", default=None)
    p.add_argument("--baud", default=115200, type=int)
    p.add_argument("--interval", default=1.0, type=float)
    args = p.parse_args()

    port = args.port or find_port()
    if not port:
        sys.exit(1)

    ser = open_serial(port, args.baud)
    time.sleep(1.5)

    try:
        asyncio.run(main_loop(ser, args.interval))
    except KeyboardInterrupt:
        pass
    finally:
        ser.close()