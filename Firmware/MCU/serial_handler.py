import asyncio
import usb_cdc
from config import SERIAL_INTERVAL


class SerialHandler:
    def __init__(self, state):
        self._state = state
        self._serial = usb_cdc.data
        
    def _parse(self, line):
        line = line.strip()
        if not line:
            return
        parts = line.split("|")
        
        if len(parts) < 4:
            return
        
        s = self._state
        s.title = parts[0][:65]
        s.artist = parts[1][:65]
        
        try:
            s.progress_sec = int(parts[2])
            s.duration_sec = int(parts[3])
        except ValueError:
            return
        
        if len(parts) >= 5:
            s.playing = parts[4].strip() == "1"
        s.media_dirty = True
        
        if len(parts) >= 6:
            hex_str = parts[5].strip()
            if len(hex_str) == 6:
                try:
                    s.bg_color = int(hex_str, 16)
                except ValueError:
                    s.bg_color = 0x000000
        s.media_dirty = True
        
        
    async def run(self):
        while True:
            await asyncio.sleep(SERIAL_INTERVAL)
            
            if not self._serial or not self._serial.in_waiting:
                continue
            
            try:
                chunk = self._serial.read(self._serial.in_waiting)
                self._buf += chunk.decode("utf-8", "ignore")
                
            except Exception:
                continue
            
            while "\n" in self._buf:
                line, self._buf = self._buf.split("\n", 1)
                self._parse(line)