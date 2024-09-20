from machine import Pin

# scan-code keymap
translationTable = [
    0, 177,  49,  50,  51,  52,  53,  54,  55,  56,  57,  48,
   45, 182, 178, 179, 113, 119, 101, 114, 116, 121, 117, 105,
  111, 112, 183, 184, 176, 128,  97, 115, 100, 102, 103, 104,
  106, 107, 108, 187, 188, 249, 129,  96, 122, 120,  99, 118,
   98, 110, 109,  44,  46, 192, 133, 135, 130,  32, 193, 194,
  195, 196, 197, 198, 199, 200, 201, 202, 203, 219, 132, 231,
  232, 233, 222, 228, 229, 230, 223, 225, 226, 227, 234, 235
]

START_BITS_START=0x00
START_BITS_END=0x01
PAYLOAD_RECEIVING=0x02

state = START_BITS_START
val = 0
lastVal = 0
received_bits = 0


# this is called when a key is lifted
def onKeyUp(key):
  print(f"UP: {key}")

# this is called when a key is pressed
def onKeyDown(key):
  print(f"DOWN: {key}")



def handle_interrupt(pin):
  if state == START_BITS_START:
    if pData.value() == 1:
      state = START_BITS_END
    else:
      state = START_BITS_START
  elif state == START_BITS_END:
    if pData.value() == 1:
      state = PAYLOAD_RECEIVING
    else:
      state = START_BITS_END
  elif state == PAYLOAD_RECEIVING:
    if received_bits <= 7:
      val = pData.value() << received_bits
      received_bits = received_bits + 1
    else:
      val = val | pData.value() << received_bits
      if val != lastVal and (val & 0x7f) <= 83:
        #  These instructions prevent Keyboard from sending data during time-consuming operations (BLE connection)
        pData.mode = Pin.OUT
        pData.value(0)
        msb = val & 0x80
        key = ranslationTable[val & 0x7f]
        if msb:
          onKeyUp(key)
        else:
          onKeyDown(key)
        lastVal = val
        pData.mode = Pin.IN
        pData.pull = Pin.PULL_DOWN
      received_bits = 0
      val = 0
      state = START_BITS_START



def start(pinClock, pinData):
  print("hi from keeb")
  global pClock
  global pData
  pClock = Pin(pinClock, Pin.IN, Pin.PULL_DOWN)
  pData = Pin(pinData, Pin.IN, Pin.PULL_DOWN)
  pClock.irq(trigger=Pin.IRQ_FALLING, handler=handle_interrupt)


