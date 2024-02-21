// This file only runs on the ArduinoIDE

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <Servo.h>


Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVOMIN_X  145 // This is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX_X  322 // This is the 'maximum' pulse length count (out of 4096)
#define SERVOMIN_Y  150 // This is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX_Y  330 // This is the 'maximum' pulse length count (out of 4096)
#define USMIN  600 // This is the rounded 'minimum' microsecond length based on the minimum pulse of 150
#define USMAX  2400 // This is the rounded 'maximum' microsecond length based on the maximum pulse of 600
#define SERVO_FREQ 50 // Analog servos run at ~50 Hz updates


uint8_t servonum = 0;
String command;

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;

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
        command = Serial.readString();
        if(command == "OXOY"){
          pwm.setPWM(0,0,SERVOMIN_X);
          pwm.setPWM(1,0,SERVOMIN_Y);
          delay(200);
          Serial.println("openedX_openedY");
        }
        if(command == "CXOY"){
          pwm.setPWM(0,0,SERVOMAX_X);
          pwm.setPWM(1,0,SERVOMIN_Y);
          delay(200);
          Serial.println("closedX_openedY");
        }
        if(command == "OXCY"){
          pwm.setPWM(0,0,SERVOMIN_X);
          pwm.setPWM(1,0,SERVOMAX_Y);
          delay(200);
          Serial.println("openedX_closedY");
        }
        if(command == "CXCY"){
          pwm.setPWM(0,0,SERVOMAX_X);
          pwm.setPWM(1,0,SERVOMAX_Y);
          delay(200);
          Serial.println("closedX_closedY");
        }
}