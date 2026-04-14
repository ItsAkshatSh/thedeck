<h1 align="center">
  <br>
  <img src="https://raw.githubusercontent.com/ItsAkshatSh/thedeck/refs/heads/main/assets/header.jpg" width=90%>
  <br>
  <br>
  TheDeck
  <br>
</h1>
<div align="center">
  
![CircuitPython](https://img.shields.io/badge/Made%20with-CircuitPython-2ec4b6)
![EasyEDA](https://img.shields.io/badge/Made%20with-EasyEDA-07162A)

</div>

The Deck runs on a Seeed Studio XIAO RP2040, which powers a 2.8 inch resistive screen from Adafruit, A rotary Encoder, and Two cherry mx switches, it also uses a MCP23017 for extra pins! It's quite similar to a StreamDeck, but instead of a grid of buttons that launch apps, it includes a screen that show-cases different screens with different functions. Want to make this yours? Head out to [/Hardware](https://github.com/ItsAkshatSh/thedeck/tree/main/Hardware), and Have a look at the schematic, and make your own preferred PCB style! 

### why?
I’ve always wanted a macro pad that felt more dynamic and customizable than the usual grid of buttons — something I would genuinely love to use every day. The Deck was built to do exactly that. Instead of relying on fixed keys like most designs, it uses a touchscreen to create a flexible, ever-changing interface

## Parts!!!
- It uses a _**Seeed Studio XIAO RP2040**_, Pretty budget friendly microcontroller
- A _**Rotary Encoder**_, for all media control purposes
- Two **_Cherry MX Switches_**, for Play/Pause, Stop Timer/Pause Timer, other purposes cooming soooooon!
- A _**MCP23017**_, FOR THEM EXTRA PINS! (only drawback of the XIAO 2040)
- **_Adafruit 1770_**, A resistive touchscreen module, basicallly the only thing that makes it stand out (this one breaks the wallet :soob:)

<div align="center">
<img src="https://github.com/ItsAkshatSh/thedeck/blob/main/assets/randoimage.jpg?raw=true" width=90%>
</div>

## Hardware
head to [/Hardware](https://github.com/ItsAkshatSh/thedeck/tree/main/Hardware)
### Schematic
<div align="center">
<img width="60%" height="60%" alt="image" src="https://github.com/user-attachments/assets/be9427a6-514d-4814-952f-8de7264cecc9" />
</div>

### PCB
<div align='center'>
<img width="50%" height="50%" alt="image" src="https://github.com/ItsAkshatSh/thedeck/blob/main/assets/PCB_TheDeck.png?raw=true" align='Center'/>
<br></br>
<img width="50%" height="50%" alt="image" src="https://github.com/ItsAkshatSh/thedeck/blob/main/assets/pcbthedeck3d.png?raw=true" align='Center'/>
</div>

### CAD ([/CAD](https://github.com/ItsAkshatSh/thedeck/tree/main/CAD))
<div align='center'>
<img width="50%" height="50%" alt="image" src="https://github.com/ItsAkshatSh/thedeck/blob/main/CAD/Preview1.png?raw=true" align='Center'/>
<img width="50%" height="50%" alt="image" src="https://github.com/ItsAkshatSh/thedeck/blob/main/CAD/Preview2.png?raw=true" align='Center'/>
</div>

## Firmware

The firmware is completely written in Python using CircuitPython libraries
```
└── MCU/
    ├── lib/
    │   ├── adafruit_bitmap_font/
    │   ├── adafruit_bus_device/
    │   ├── adafruit_display_shapes/
    │   ├── adafruit_display_text/
    │   ├── adafruit_hid/
    │   ├── adafruit_mcp230xx/
    │   ├── asyncio/
    │   ├── adafruit_binascii.mpy
    │   ├── adafruit_bitbangio.mpy
    │   ├── adafruit_ili9341.mpy
    │   └── adafruit_touchscreen.mpy
    ├── font/
    │   ├── helvB24.bdf
    │   ├── helvR12.bdf
    │   └── helvR18.bdf
    ├── screens/
    │   ├── app_launcher.py
    │   ├── now_playing.py
    │   ├── pomodoro.py
    │   └── settings.py
    ├── ui/
    │   ├── animator.py
    │   ├── arc_widget.py
    │   ├── progress_bar.py
    │   └── transition.py
    ├── boot.py
    ├── code.py
    ├── config.py
    ├── display_driver.py
    ├── input_handler.py
    ├── requirements.txt
    ├── serial_handler.py
    ├── state.py
    └── touch_handler.py
```

I too use a bridge for grabbing Now playing info using winSDK, you can find it under [/Firmware](https://github.com/ItsAkshatSh/thedeck/tree/main/Firmware/MusicBridge), it sends the info through ports, and then `serial_handler.py` parses it and passes that info to the screens!

## BOM

Check it out [here!](https://github.com/ItsAkshatSh/thedeck/blob/main/BOM.csv)


# THANK YOU HACKCLUB! ❤️
