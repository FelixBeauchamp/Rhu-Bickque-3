// This file only runs on the ArduinoIDE

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVOMIN1  243 // This is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX1  416 // This is the 'maximum' pulse length count (out of 4096)
#define SERVOMIN2  259 // This is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX2  435 // This is the 'maximum' pulse length count (out of 4096)
#define USMIN  600 // This is the rounded 'minimum' microsecond length based on the minimum pulse of 150
#define USMAX  2400 // This is the rounded 'maximum' microsecond length based on the maximum pulse of 600
#define SERVO_FREQ 50 // Analog servos run at ~50 Hz updates

uint8_t servonum = 0;

void setup() {
   Serial.begin(9600);

  pwm.begin();
  
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(SERVO_FREQ);  // Analog servos run at ~50 Hz updates

  delay(10);
  pinMode(LED_BUILTIN, OUTPUT);
  pwm.setPWM(0,0,SERVOMIN1);
  pwm.setPWM(1,0,SERVOMIN2);

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
    if (Serial.available() > 0) {
        String command = Serial.readString();
        if(command == "pushPair1"){
          digitalWrite(LED_BUILTIN,HIGH);
          pwm.setPWM(0,0,SERVOMAX1);
          delay(1000);
          Serial.println("finished push 1");
        }
        if(command == "pullPair1"){
          digitalWrite(LED_BUILTIN,HIGH);
          pwm.setPWM(0,0,SERVOMIN1);
          delay(1000);
          Serial.println("finished pull 1");
        }
        if(command == "pushPair2"){
          digitalWrite(LED_BUILTIN,HIGH);
          pwm.setPWM(1,0,SERVOMAX2);
          delay(1000);
          Serial.println("finished push 2");
        }
        if(command == "pullPair2"){
          digitalWrite(LED_BUILTIN,HIGH);
          pwm.setPWM(1,0,SERVOMIN2);
          delay(1000);
          Serial.println("finished pull 2");
        }
    }
}
