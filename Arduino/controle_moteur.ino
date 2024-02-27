
  #include <Dynamixel2Arduino.h>

#if defined(ARDUINO_AVR_UNO) || defined(ARDUINO_AVR_MEGA2560) // When using DynamixelShield
  #include <SoftwareSerial.h>
  SoftwareSerial soft_serial(7, 8); // DYNAMIXELShield UART RX/TX
  #define DXL_SERIAL   Serial
  #define DEBUG_SERIAL soft_serial
  const int DXL_DIR_PIN = 2; // DYNAMIXEL Shield DIR PIN
#elif defined(ARDUINO_SAM_DUE) // When using DynamixelShield
  #define DXL_SERIAL   Serial
  #define DEBUG_SERIAL SerialUSB
  const int DXL_DIR_PIN = 2; // DYNAMIXEL Shield DIR PIN
#elif defined(ARDUINO_SAM_ZERO) // When using DynamixelShield
  #define DXL_SERIAL   Serial1
  #define DEBUG_SERIAL SerialUSB
  const int DXL_DIR_PIN = 2; // DYNAMIXEL Shield DIR PIN
#elif defined(ARDUINO_OpenCM904) // When using official ROBOTIS board with DXL circuit.
  #define DXL_SERIAL   Serial3 //OpenCM9.04 EXP Board's DXL port Serial. (Serial1 for the DXL port on the OpenCM 9.04 board)
  #define DEBUG_SERIAL Serial
  const int DXL_DIR_PIN = 22; //OpenCM9.04 EXP Board's DIR PIN. (28 for the DXL port on the OpenCM 9.04 board)
#elif defined(ARDUINO_OpenCR) // When using official ROBOTIS board with DXL circuit.
  // For OpenCR, there is a DXL Power Enable pin, so you must initialize and control it.
  // Reference link : https://github.com/ROBOTIS-GIT/OpenCR/blob/master/arduino/opencr_arduino/opencr/libraries/DynamixelSDK/src/dynamixel_sdk/port_handler_arduino.cpp#L78
  #define DXL_SERIAL   Serial3
  #define DEBUG_SERIAL Serial
  const int DXL_DIR_PIN = 84; // OpenCR Board's DIR PIN.
#elif defined(ARDUINO_OpenRB)  // When using OpenRB-150
  //OpenRB does not require the DIR control pin.
  #define DXL_SERIAL Serial1
  #define DEBUG_SERIAL Serial
  const int DXL_DIR_PIN = -1;
#else // Other boards when using DynamixelShield
  #define DXL_SERIAL   Serial1
  #define DEBUG_SERIAL Serial
  const int DXL_DIR_PIN = 2; // DYNAMIXEL Shield DIR PIN
#endif

String command;

const uint8_t DXL_ID21 = 50;
const uint8_t DXL_ID37 = 37;
const uint8_t DXL_ID26 = 1;
const uint8_t DXL_ID27 = 15;

const uint8_t M1 = DXL_ID21;
const uint8_t M2 = DXL_ID37;
const uint8_t M3 = DXL_ID26;
const uint8_t M4 = DXL_ID27;

const float DXL_PROTOCOL_VERSION = 2.0;
Dynamixel2Arduino dxl(DXL_SERIAL, DXL_DIR_PIN);
using namespace ControlTableItem;

int offset21 = 80;
int offset37 = -46;
int offset26 = 45;
int offset27 = 45;

int compteur = 0;

void setup() {

  Serial.begin(57600);

  //DEBUG_SERIAL.begin(115200);
  while(!DEBUG_SERIAL);
  dxl.begin(57600);
  // Set Port Protocol Version. This has to match with DYNAMIXEL protocol version.
  dxl.setPortProtocolVersion(DXL_PROTOCOL_VERSION);
  // Get DYNAMIXEL information

  dxl.ping(DXL_ID21);
  dxl.ping(DXL_ID37);
  dxl.ping(DXL_ID26);
  dxl.ping(DXL_ID27);

  // Turn off torque when configuring items in EEPROM area
  dxl.torqueOff(DXL_ID21);
  dxl.torqueOff(DXL_ID37);
  dxl.torqueOff(DXL_ID26);
  dxl.torqueOff(DXL_ID27);



  dxl.setOperatingMode(DXL_ID21, OP_EXTENDED_POSITION	);
  dxl.setOperatingMode(DXL_ID37, OP_EXTENDED_POSITION);
  dxl.setOperatingMode(DXL_ID26, OP_EXTENDED_POSITION);
  dxl.setOperatingMode(DXL_ID27, OP_EXTENDED_POSITION);


  dxl.torqueOn(DXL_ID21);
  dxl.torqueOn(DXL_ID37);
  dxl.torqueOn(DXL_ID26);
  dxl.torqueOn(DXL_ID27);

  HOMING();

}

void loop() {

    command = Serial.readString();

    // pour retourner info, Serial.println("");

    // DEBUG_SERIAL.print("Present_Position(deg)21 : ");
    // DEBUG_SERIAL.println(dxl.getPresentPosition(DXL_ID21, UNIT_DEGREE));
    // DEBUG_SERIAL.print("Present_Position(deg)37 : ");
    // DEBUG_SERIAL.println(dxl.getPresentPosition(DXL_ID37, UNIT_DEGREE));
    // DEBUG_SERIAL.print("Present_Position(deg)26 : ");
    // DEBUG_SERIAL.println(dxl.getPresentPosition(DXL_ID26, UNIT_DEGREE));
    // DEBUG_SERIAL.print("Present_Position(deg)27 : ");
    // DEBUG_SERIAL.println(dxl.getPresentPosition(DXL_ID27, UNIT_DEGREE));

    //dxl.setGoalPosition(DXL_ID37, 90, UNIT_DEGREE);
    //dxl.setGoalPosition(DXL_ID26, move26+offset26, UNIT_DEGREE);
    //dxl.setGoalPosition(DXL_ID37, 120, UNIT_DEGREE);

    delay(1000); 
    if (command =="HOMING")
    {
      HOMING();
      done();
    }

    if (command == "M1_L")
    {
      gauche(M1);
      done();
    }
    if (command == "M1_R")
    {
      droite(M1);
      done();
    }
    if (command == "M2_L")
    {
      gauche(M2);
      done();
    }
    if (command == "M2_R")
    {
      droite(M2);
      done();
    }
    if (command == "M3_L")
    {
      gauche(M3);
      done();
    }
    if (command == "M3_R")
    {
      droite(M3);
      done();
    }
    if (command == "M4_L")
    {
      gauche(M4);
      done();
    }
    if (command == "M4_R")
    {
      droite(M4);
      done();
    }


    if (command == "M1M3_L")
    {
      gauche_2M(M1, M3);
      done();
    }
    if (command == "M1M3_R")
    {
      droite_2M(M1, M3);
      done();
    }
    if (command == "M2M4_L")
    {
      gauche_2M(M2, M4);
      done();
    }
    if (command == "M2M4_R")
    {
      droite_2M(M2, M4);
      done();
    }

}

void HOMING ()
{
    int home_position = 90;
    dxl.setGoalPosition(DXL_ID21, home_position+offset21, UNIT_DEGREE);
    dxl.setGoalPosition(DXL_ID37, home_position+offset37, UNIT_DEGREE);
    dxl.setGoalPosition(DXL_ID26, home_position+offset26, UNIT_DEGREE);
    dxl.setGoalPosition(DXL_ID27, home_position+offset27, UNIT_DEGREE);
    delay(500);
}

void droite (const uint8_t DXL_ID)
{
    // couter-clockwise pour droite
    int offset = 0;
    int present_position = dxl.getPresentPosition(DXL_ID,UNIT_DEGREE);
    //DEBUG_SERIAL.print("Actual position = ");
    //DEBUG_SERIAL.println(present_position);

    int move = present_position + 90;
    //DEBUG_SERIAL.print("Move = ");
    //DEBUG_SERIAL.println(move);
    //DEBUG_SERIAL.println("Pre-stuck");
    dxl.setGoalPosition(DXL_ID, move, UNIT_DEGREE);
    //DEBUG_SERIAL.println("Je suis stuck");
    //delay(500);

}

void gauche (const uint8_t DXL_ID)
{
    // clockwise pour gauche
    int offset = 0;
    int present_position = dxl.getPresentPosition(DXL_ID,UNIT_DEGREE);

    int move = present_position - 90;
    dxl.setGoalPosition(DXL_ID, move, UNIT_DEGREE);
    //delay(500);

}

void droite_2M (const uint8_t DXL_ID_1, const uint8_t DXL_ID_2)
{
    // Rotation 2 moteurs vers la droite par rapport au premier moteur
    droite(DXL_ID_1);
    gauche(DXL_ID_2);
    //delay(500);

}

void gauche_2M (const uint8_t DXL_ID_1, const uint8_t DXL_ID_2)
{
    // Rotation 2 moteurs vers la gauche par rapport au premier moteur
    gauche(DXL_ID_1);
    droite(DXL_ID_2);
    //delay(500);

}

void done()
{
  while(
    dxl.getPresentVelocity(DXL_ID21) != 0 ||
    dxl.getPresentVelocity(DXL_ID37) != 0 ||
    dxl.getPresentVelocity(DXL_ID26) != 0 ||
    dxl.getPresentVelocity(DXL_ID27) != 0
    )
    {

    }
    Serial.println("t'es laid");
}






