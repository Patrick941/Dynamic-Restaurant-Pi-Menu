#include <wiringPi.h>
#include <stdio.h>

#define LED_PIN 0

int main() {
    if (wiringPiSetup() == -1) {
        printf("WiringPi setup failed!\n");
        return 1;
    }

    pinMode(LED_PIN, OUTPUT);

    for (int i = 0; i < 10; i++) {
        digitalWrite(LED_PIN, HIGH);
        delay(500);
        digitalWrite(LED_PIN, LOW);
        delay(500);
    }

    return 0;
}
