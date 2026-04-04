<<<<<<< HEAD
import asyncio
import argparse
import sys
import time
import serial
import serial.tools.list_ports
from winsdk.windows.media.control import (GlobalSystemMediaTransportControlsSessionManager as MediaManager,
    GlobalSystemMediaTransportControlsSessionPlaybackStatus as PlaybackStatus)


def find_device_port():
    cp_ports = []
    for p in serial.tools.list_ports.comports():
        desc = (p.description or "").lower()
        if any(k in desc for k in ["circuitpython", "xiao", "rp2040"]):
            cp_ports.append(p.device)
    
    if len(cp_ports) == 2:
        return sorted(cp_ports)[-1]
    
    if cp_ports:
        return cp_ports[0]
    
    ports = serial.tools.list_ports.comports()
    return ports[0].device if ports else None


def open_serial(port, baudrate=115200, retries = 5):
    for attempt in range(retries):
        try:
            ser = serial.Serial(port, baudrate, timeout=1)
            print(f"Connected to {port}")
            return ser
        except serial.SerialException as e:
            print(f"Failed to connect to {port} (attempt {attempt + 1}/{retries}): {e}")
            time.sleep(2)
            
    print(f"Could not connect to {port} after {retries} attempts.")
    sys.exit(1)
    
    
async def get_media_info():
    try:
        sessions = await MediaManager.request_async()
        session = sessions.get_current_session()
        
        if not session:
            return None
        
        props = await session.try_get_media_properties_async()
        if not props:
            return None
        
        title = (props.title or "Unknown").replace("|","-").strip()
        artist = (props.artist or "Unknown").replace("|","-").strip()
        
        pb = session.get_playback_info()
        playing = (pb.playback_status == PlaybackStatus.PLAYING) if pb else False
        
        tl = session.get_timeline_properties()
        progress_sec = 0
        duration_sec = 0
        if tl:
            progress_sec = int(tl.position.total_seconds())
            if tl.end_time and tl.start_time:
                duration_sec = int((tl.end_time - tl.start_time).total_seconds())
                
        
        return dict(title=title, artist=artist, playing=playing, progress_sec=progress_sec, duration_sec=duration_sec)
    
    except Exception as e:
        print(f"Error getting media info: {e}")
        return None
    
async def main_loop(ser, interval):
    print("bridge running")
    last_title= None
    
    while True:
        t0 = time.monotonic()
        info = await get_media_info()
        
        if info:
            line = (f"{info['title']}|{info['artist']}|{'1' if info['playing'] else '0'}\n")
            if info['title'] != last_title:
                last_title = info['title']
                icon = "play" if info['playing'] else "pause"
                print(f"{icon} {info['title']} - {info['artist']}")
        else:
            line = "No media|Unknown|0\n"
            print("No media playing")
            
        try:
            ser.write(line.encode("utf-8"))
        except Exception as e:
            print(f"Error writing to serial: {e}")
            ser.close()
            time.sleep(3)
            ser.open()
            
        await asyncio.sleep(max(0, interval - (time.monotonic() - t0)))
        
def  parse_args():
    p = argparse.ArgumentParser(description="FocusBox bridge")
    p.add_argument("--port", default=None ,help="COM port")
    p.add_argument("--baud", default=115200, type=int)
    p.add_argument("--interval", default=1.0, type=float)
    
    return p.parse_args()

if __name__ == "__main__":
    args = parse_args()
    port = args.port or find_device_port()
    if not port:
        print("No serial devices found.")
        sys.exit(1)
    
    print(f"Using port: {port}")
    ser = open_serial(port, args.baud)
    time.sleep(1)
    
    try:
        asyncio.run(main_loop(ser, args.interval))
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
=======
import asyncio
import argparse
import sys
import time
import serial
import serial.tools.list_ports
from winsdk.windows.media.control import (GlobalSystemMediaTransportControlsSessionManager as MediaManager,
    GlobalSystemMediaTransportControlsSessionPlaybackStatus as PlaybackStatus)


def find_device_port():
    cp_ports = []
    for p in serial.tools.list_ports.comports():
        desc = (p.description or "").lower()
        if any(k in desc for k in ["circuitpython", "xiao", "rp2040"]):
            cp_ports.append(p.device)
    
    if len(cp_ports) == 2:
        return sorted(cp_ports)[-1]
    
    if cp_ports:
        return cp_ports[0]
    
    ports = serial.tools.list_ports.comports()
    return ports[0].device if ports else None


def open_serial(port, baudrate=115200, retries = 5):
    for attempt in range(retries):
        try:
            ser = serial.Serial(port, baudrate, timeout=1)
            print(f"Connected to {port}")
            return ser
        except serial.SerialException as e:
            print(f"Failed to connect to {port} (attempt {attempt + 1}/{retries}): {e}")
            time.sleep(2)
            
    print(f"Could not connect to {port} after {retries} attempts.")
    sys.exit(1)
    
    
async def get_media_info():
    try:
        sessions = await MediaManager.request_async()
        session = sessions.get_current_session()
        
        if not session:
            return None
        
        props = await session.try_get_media_properties_async()
        if not props:
            return None
        
        title = (props.title or "Unknown").replace("|","-").strip()
        artist = (props.artist or "Unknown").replace("|","-").strip()
        
        pb = session.get_playback_info()
        playing = (pb.playback_status == PlaybackStatus.PLAYING) if pb else False
        
        tl = session.get_timeline_properties()
        progress_sec = 0
        duration_sec = 0
        if tl:
            progress_sec = int(tl.position.total_seconds())
            if tl.end_time and tl.start_time:
                duration_sec = int((tl.end_time - tl.start_time).total_seconds())
                
        
        return dict(title=title, artist=artist, playing=playing, progress_sec=progress_sec, duration_sec=duration_sec)
    
    except Exception as e:
        print(f"Error getting media info: {e}")
        return None
    
async def main_loop(ser, interval):
    print("bridge running")
    last_title= None
    
    while True:
        t0 = time.monotonic()
        info = await get_media_info()
        
        if info:
            line = (f"{info['title']}|{info['artist']}|{'1' if info['playing'] else '0'}\n")
            if info['title'] != last_title:
                last_title = info['title']
                icon = "play" if info['playing'] else "pause"
                print(f"{icon} {info['title']} - {info['artist']}")
        else:
            line = "No media|Unknown|0\n"
            print("No media playing")
            
        try:
            ser.write(line.encode("utf-8"))
        except Exception as e:
            print(f"Error writing to serial: {e}")
            ser.close()
            time.sleep(3)
            ser.open()
            
        await asyncio.sleep(max(0, interval - (time.monotonic() - t0)))
        
def  parse_args():
    p = argparse.ArgumentParser(description="FocusBox bridge")
    p.add_argument("--port", default=None ,help="COM port")
    p.add_argument("--baud", default=115200, type=int)
    p.add_argument("--interval", default=1.0, type=float)
    
    return p.parse_args()

if __name__ == "__main__":
    args = parse_args()
    port = args.port or find_device_port()
    if not port:
        print("No serial devices found.")
        sys.exit(1)
    
    print(f"Using port: {port}")
    ser = open_serial(port, args.baud)
    time.sleep(1)
    
    try:
        asyncio.run(main_loop(ser, args.interval))
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
>>>>>>> 1278d2b57e44c250325702984b0e62a3c63bf3e6
        ser.close()