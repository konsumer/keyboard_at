from machine import Pin
from micropython import alloc_emergency_exception_buf

alloc_emergency_exception_buf(100)

print("hi from keeb")

# These are the pins connected to your keyboard
pClock = Pin(5, Pin.IN, Pin.PULL_UP)
# pData = Pin(6, Pin.IN, Pin.PULL_UP)

valClock = 1
valOldClock = 1

valClock = pClock.value()
print(f"clock: {valClock}")

