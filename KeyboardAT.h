// This base-class manages a IBM Model F XT Keyboard

// FSM states defining
#define START_BITS_START 0x00
#define START_BITS_END 0x01
#define PAYLOAD_RECEIVING 0x02

unsigned char translationTable[128] = {
  0,     // Not Used
  0xB1,  // esc
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
  '-',  // ' and ?
  0xb6,
  0xB2,  // backspace

  0xB3,  // tab
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
  0xB0,  // return

  0x80,  // left ctrl
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

  0x81,  // left shift
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
  0x85,  // right shift
  0x87,  // right GUI

  0x82,  // left alt
  ' ',
  0xC1,  // caps lock

  0xC2,  // f1
  0xC3,  // f2
  0xC4,  // f3
  0xC5,  // f4
  0xC6,  // f5
  0xC7,  // f6
  0xC8,  // f7
  0xC9,  // f8
  0xCA,  // f9
  0xCB,  // f10

  0xdb,  // Num Lock
  0x84,  // right ctrl
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
};

class KeyboardAT {
public:
  ~KeyboardAT() {}
  KeyboardAT(){}
  
  void begin(int clock, int data) {
    this->clock = clock;
    this->data = data;

    this->state = START_BITS_START;
    this->val = 0;
    this->lastVal = 0;
    this->received_bits = 0;

    pinMode(data, INPUT);  // Data Line Hi
    digitalWrite(data, HIGH);
    pinMode(clock, INPUT);
    digitalWrite(clock, HIGH);
    delay(5);
    digitalWrite(clock, LOW);   // Falling Edge
    delay(21);                  // Wait ~20ms
    digitalWrite(clock, HIGH);  // Rising Edge

    /* RECEIVING PIN MODE */
    pinMode(clock, INPUT_PULLUP);
    pinMode(data, INPUT_PULLUP);
  }

  void update() {
    switch (this->state) {
      case START_BITS_START:
        if (!digitalRead(this->data)) {
          this->state = START_BITS_END;
        } else {
          this->state = START_BITS_START;
        }
        break;

      case START_BITS_END:
        if (digitalRead(this->data)) {
          this->state = PAYLOAD_RECEIVING;
        } else {
          this->state = START_BITS_END;
        }
        break;

      case PAYLOAD_RECEIVING:
        if (this->received_bits < 7) {  // Receiving
          this->val |= (digitalRead(this->data) << this->received_bits);
          this->received_bits++;
        } else {  // Out Key
          this->val |= (digitalRead(this->data) << this->received_bits);

          if (this->val != this->lastVal && (this->val & 0x7f) <= 83) {
            pinMode(this->data, OUTPUT);  // These instructions prevent Keyboard from sending data during time-consuming operations (BLE connection)
            digitalWrite(this->data, LOW);
            int msb = this->val & 0x80;  // Only the byte's MSB is on

            unsigned char key = translationTable[this->val & 0x7f];
            if (msb) {          // msb == 1 --> release
              this->onKeyUp(key);
            } else {                                                         // msb == 0 --> press
              this->onKeyDown(key);
            }

            // if ((this->val & 0x7f) == 0x45 and !msb)
            //  digitalWrite(led, !digitalRead(led));
            
            this->lastVal = this->val;
            pinMode(this->data, INPUT_PULLUP);  // Re-activate Keyboard sending data
          }

          this->received_bits = 0;
          this->val = 0x00;
          this->state = START_BITS_START;
        }
        break;
    }
    this->_update();
  }

  // implement this, to get called on every update
  virtual void _update() {}

  // implement these to callback
  virtual void onKeyDown(unsigned char key) {}
  virtual void onKeyUp(unsigned char key) {}
private:
  int clock;
  int data;
  uint8_t state;
  uint8_t val;
  uint8_t lastVal;
  int received_bits;
};