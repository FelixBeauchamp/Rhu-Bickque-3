// This file only runs on the ArduinoIDE

#include <Wire.h>
#include <
.h>
#include <Servo.h>


Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVOMIN_X  360 // This is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX_X  190 // This is the 'maximum' pulse length count (out of 4096)
#define SERVOMIN_Y  220 // This is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX_Y  400 // This is the 'maximum' pulse length count (out of 4096)
#define USMIN  600 // This is the rounded 'minimum' microsecond length based on the minimum pulse of 150
#define USMAX  2400 // This is the rounded 'maximum' microsecond length based on the maximum pulse of 600
#define SERVO_FREQ 50 // Analog servos run at ~50 Hz updates

int receivedValue;
uint8_t servonum = 0;
int command;

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;
int delais = 500;

void setup() {
  Serial.begin(57600);

  pwm.begin();

  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(SERVO_FREQ);  // Analog servos run at ~50 Hz updates

  delay(10);
  pinMode(LED_BUILTIN, OUTPUT);
  pwm.setPWM(0,0,SERVOMIN_X);
  pwm.setPWM(1,0,SERVOMIN_Y);
  myservo.attach(9);

}

void setServoPulse(uint8_t n, double pulse) {
  double pulselength;

  pulselength = 1000000;   // 1,000,000 us per second
  pulselength /= SERVO_FREQ;   // Analog servos run at ~60 Hz updates
  Serial.print(pulselength); Serial.println(" us per period");
  pulselength /= 4096;  // 12 bits of resolution
  Serial.print(pulselength); Serial.println(" us per bit");
  pulse *= 1000000;  // convert input seconds to us
  pulse /= pulselength;
  Serial.println(pulse);
  pwm.setPWM(n, 0, pulse);
}

void loop() {
        Serial.readBytes((char*)&receivedValue, 4);
        command = receivedValue;
        if(command == 1){
          pwm.setPWM(0,0,SERVOMIN_X);
          pwm.setPWM(1,0,SERVOMIN_Y);
          int time = 0;
          while (time <= delais)
          {
            time = millis();
          }
          int valueToSend = 1;
          Serial.write((uint8_t*)&valueToSend, sizeof(valueToSend));
          valueToSend = 0;
        }
        if(command == 3){
          pwm.setPWM(0,0,SERVOMAX_X);
          pwm.setPWM(1,0,SERVOMIN_Y);
          int time = 0;
          while (time <= delais)
          {
            time = millis();
          }
          int valueToSend = 1;
          Serial.write((uint8_t*)&valueToSend, sizeof(valueToSend));
          valueToSend = 0;
        }
        if(command == 2){
          pwm.setPWM(0,0,SERVOMIN_X);
          pwm.setPWM(1,0,SERVOMAX_Y);
          int time = 0;
          while (time <= delais)
          {
            time = millis();
          }
          int valueToSend = 1;
          Serial.write((uint8_t*)&valueToSend, sizeof(valueToSend));
          valueToSend = 0;
        }
        if(command == 4){
          pwm.setPWM(0,0,SERVOMAX_X);
          pwm.setPWM(1,0,SERVOMAX_Y);
          int time = 0;
          while (time <= delais)
          {
            time = millis();
          }
          int valueToSend = 1;
          Serial.write((uint8_t*)&valueToSend, sizeof(valueToSend));
          valueToSend = 0;
        }
        Serial.flush();
        int receivedValue = 69;
}

void done(){
  int time = 0;
  while (time <= delais)
  {
    time = millis();
  }
  uint8_t valueToSend = 1;
  Serial.write((uint8_t*)&valueToSend, sizeof(valueToSend));
  valueToSend = 0;
}
