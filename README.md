This has a basic driver for IBM Model F XT Keyboard, on Arduino.

The idea is that you can extend the class, and make it do whatever you want (bluetooth, wired USB keyboard, etc.)

Here is an example that just prints keycodes to serial:

```cpp
#include "KeyboardAT.h"

class KeyboardATSerial : public KeyboardAT {
public:
  KeyboardATSerial(int clock, int data)
    : KeyboardAT(clock, data) {
    Serial.begin(9600);
  }

  // this is called on every clock-signal, if you need that
  virtual void _update() {}

  virtual void onKeyDown(unsigned char key) {
    // if (key >= 0x80){  // If it is a modifier key
    // }
    Serial.print("UP: ");
    Serial.println(key);
  }

  virtual void onKeyUp(unsigned char key) {
    // if (key >= 0x80){  // If it is a modifier key
    // }
    Serial.print("DOWN: ");
    Serial.println(key);
  }
};
```

Make similar for whatever you want to do.
