#include <Arduino.h>

#define PIN_A   9
#define PIN_B   11
#define PIN_BTN 10

// === Тайминги одного импульса (как в тесте) ===
const uint32_t PULSE_HIGH_US = 50000;   // 50 мс в HIGH
const uint32_t PULSE_LOW_US  = 50000;   // 50 мс в LOW

// === Прочие задержки (мс) ===
const uint32_t BTN_PRE_MS     = 500;    // пауза перед нажатием кнопки
const uint32_t BTN_HOLD_MS    = 500;    // длительность удержания кнопки
const uint32_t NUMBER_GAP_MS  = 1500;   // пауза после каждого числа
const uint32_t START_DELAY_MS = 5000;   // задержка при старте

// === Выдать один импульс на A (B = 0) ===
inline void onePulse() {
  digitalWrite(PIN_A, 1);
  digitalWrite(PIN_B, 0);
  delayMicroseconds(PULSE_HIGH_US);

  digitalWrite(PIN_A, 0);
  digitalWrite(PIN_B, 0);
  delayMicroseconds(PULSE_LOW_US);
}

// === Выдать N импульсов ===
void sendPulses(uint32_t n) {
  if (n == 0) return;

  // Гарантированный покой перед серией
  digitalWrite(PIN_A, 0);
  digitalWrite(PIN_B, 0);
  delayMicroseconds(5000);

  for (uint32_t i = 0; i < n; i++) {
    onePulse();
  }
}

// === Нажатие кнопки: пауза → нажатие → отпускание ===
inline void pressButton() {
  delay(BTN_PRE_MS);
  digitalWrite(PIN_BTN, HIGH);
  delay(BTN_HOLD_MS);
  digitalWrite(PIN_BTN, LOW);
}

void setup() {
  Serial.begin(115200);
  delay(200);

  pinMode(PIN_A,   OUTPUT);
  pinMode(PIN_B,   OUTPUT);
  pinMode(PIN_BTN, OUTPUT);
  digitalWrite(PIN_A,   0);
  digitalWrite(PIN_B,   0);
  digitalWrite(PIN_BTN, 0);

  Serial.println("=== Encoder emulator 0000..9999 ===");
  Serial.println("Starting in 5 seconds...");

  delay(START_DELAY_MS);

  Serial.println("GO!");
}

void loop() {
  for (uint32_t n = 6059; n <= 9999; n++) {
    // Печать числа с ведущими нулями
    char buf[5];
    buf[0] = '0' + (n / 1000) % 10;
    buf[1] = '0' + (n / 100)  % 10;
    buf[2] = '0' + (n / 10)   % 10;
    buf[3] = '0' +  n         % 10;
    buf[4] = '\0';
    Serial.println(buf);

    // Разряды: тысячи, сотни, десятки, единицы
    sendPulses((n / 1000) % 10);  pressButton();   // A
    sendPulses((n / 100)  % 10);  pressButton();   // B
    sendPulses((n / 10)   % 10);  pressButton();   // C
    sendPulses( n         % 10);  pressButton();   // D

    // Пауза после каждого числа
    delay(NUMBER_GAP_MS);
  }
}
