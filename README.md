This is a USB HID keyboard-adapter for IBM AT that runs on ESP32 with micropython.

# micropython setup

```
# get the tools
sudo pip install esptool adafruit-ampy

# mac is like this
PORT=/dev/cu.usbserial-0001

# linux is more like this
PORT=dev/ttyUSB0

wget https://micropython.org/resources/firmware/ESP32_GENERIC-20240602-v1.23.0.bin

esptool.py --chip esp32 --port ${PORT} erase_flash
esptool.py --chip esp32 --port ${PORT} --baud 460800 write_flash -z 0x1000 ESP32_GENERIC-20240602-v1.23.0.bin

# connect to REPL
screen ${PORT} 115200

# or use another serial-terminal program
picocom --baud 115200 ${PORT}
```

now disconnect (in `screen`, use `ctrl + A` then press `K`, or `Ctrl-Shift-A/X` in picocom) and you can push your firmware:


```
# push file & test
ampy --port ${PORT} run keeb.py
```

if it seems to work right (press keys on your keyboard and see codes) then you can make a boot.py that does this:

```
import keeb
keeb.start(5, 6)
```

and push them both:

```
ampy --port ${PORT} put keeb.py
ampy --port ${PORT} put boot.py
```