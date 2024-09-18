// this just prints to serial when keys are pressed

#include "KeyboardAT.h"

class KeyboardATSerial : public KeyboardAT {
public:
  KeyboardATSerial(int clock, int data)
    : KeyboardAT(clock, data) {
    Serial.begin(9600);
  }

  virtual void _update() {}

  virtual void onKeyDown(unsigned char key) {
    // if (key >= 0x80){  // If it is a modifier key
    // }
    Serial.print("DOWN: ");
    Serial.println(key);
  }

  virtual void onKeyUp(unsigned char key) {
    // if (key >= 0x80){  // If it is a modifier key
    // }
    Serial.print("UP: ");
    Serial.println(key);
  }
};
