This is a USB HID keyboard-adapter for IBM AT that runs on ESP32 with micropython.

## installation

### micropython setup

```sh
# get the tools
sudo pip3 install --break-system-packages esptool adafruit-ampy

# mac is like this
PORT=/dev/cu.usbserial-0001

# linux is more like this
PORT=/dev/ttyUSB0

wget https://micropython.org/resources/firmware/ESP32_GENERIC-20240602-v1.23.0.bin

esptool.py --chip esp32 --port ${PORT} erase_flash
esptool.py --chip esp32 --port ${PORT} --baud 460800 write_flash -z 0x1000 ESP32_GENERIC-20240602-v1.23.0.bin

# connect to REPL
screen ${PORT} 115200

# or use another serial-terminal program
picocom --baud 115200 ${PORT}
```

now disconnect (in `screen`, use `ctrl + A` then press `K`, or `Ctrl-Shift-A/X` in picocom) and you can push your keyboard firmware.

### upload firmware


Now, you can make a boot.py that does this at end:

```py
import keeb
keeb.start(4, 5)
```

and push them both:

```sh
ampy --port ${PORT} put keeb.py
ampy --port ${PORT} put boot.py
```

### customization

I use a [standard keymap](https://github.com/konsumer/keyboard_at/blob/main/keeb.py#L4-L12), which you can modify, but you can also just modify `onKeyUp`/`onKeyDown` to do whatever you want. Currently, it only prints code to serial, but you could make it send bluetooth or USB HID keyboard messages (these 2 modes are in the works.) The idea is that "the firmware is the configuration", so really, go wild, and make it do whatever you want.

### WebREPL

This is optional, but makes it easier to mess with the adapter (change firmware and inspect code and stuff.)


Login over serial and run `import webrepl_setup`. Go through wizard, then make a boot.py file that looks like this: 
```py
# This file is executed on every boot (including wake-boot from deepsleep)

import webrepl
import network
import keeb

ssid='<YOURS>'
key='<YOURS>'
network.hostname("espkeeb")

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, key)
        while not wlan.isconnected():
            pass

do_connect()
webrepl.start()
keeb.start(4, 5)
```

Now, upload with `ampy --port ${PORT} put boot.py` and you can access it at port 8266 on the device (example `http://espkeeb:8266/`.)
