#include "KeyboardATSerial.h"

// IBM keyboard is on pins 5 & 6 (clock, data)
#define PIN_CLOCK 5
#define PIN_DATA 6

KeyboardATSerial* keeb;

// I do this in an interupt on clock-pin
void IRAM_ATTR clk_down() {
  keeb->update();
}

void setup() {
  Serial.begin(9600);
  Serial.println("Starting logger for IBM XT Keyboard");

  keeb = new KeyboardATSerial();
  keeb->begin(PIN_CLOCK, PIN_DATA);
  attachInterrupt(digitalPinToInterrupt(PIN_CLOCK), clk_down, FALLING);
}

void loop() {}
