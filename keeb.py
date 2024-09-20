from machine import Pin

# TODO: translate these all into char-codes (not strings)
translationTable = [
  0,     # Not Used
  0xB1,  # esc
  '1',
  '2',
  '3',
  '4',
  '5',
  '6',
  '7',
  '8',
  '9',
  '0',
  '-',  # ' and ?
  0xb6,
  0xB2,  # backspace

  0xB3,  # tab
  'q',
  'w',
  'e',
  'r',
  't',
  'y',
  'u',
  'i',
  'o',
  'p',
  0xb7,
  0xb8,
  0xB0,  # return

  0x80,  # left ctrl
  'a',
  's',
  'd',
  'f',
  'g',
  'h',
  'j',
  'k',
  'l',
  0xbb,
  0xbc,
  'ù',

  0x81,  # left shift
  0x60,
  'z',
  'x',
  'c',
  'v',
  'b',
  'n',
  'm',
  ',',
  '.',
  0xc0,
  0x85,  # right shift
  0x87,  # right GUI

  0x82,  # left alt
  ' ',
  0xC1,  # caps lock

  0xC2,  # f1
  0xC3,  # f2
  0xC4,  # f3
  0xC5,  # f4
  0xC6,  # f5
  0xC7,  # f6
  0xC8,  # f7
  0xC9,  # f8
  0xCA,  # f9
  0xCB,  # f10

  0xdb,  # Num Lock
  0x84,  # right ctrl
  0xe7,
  0xe8,
  0xe9,
  0xde,
  0xe4,
  0xe5,
  0xe6,
  0xdf,
  0xe1,
  0xe2,
  0xe3,
  0xea,
  0xeb
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


