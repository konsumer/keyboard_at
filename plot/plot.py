from machine import Pin

pinClock=4
pinData=5

pClock = Pin(pinClock, Pin.IN, Pin.PULL_DOWN)
pData = Pin(pinData, Pin.IN, Pin.PULL_DOWN)
while True:
  print(f"{pClock.value()}{pData.value()}")