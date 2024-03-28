// This code need to be uploaded on the OpenRb-150 to control the Dynamixel and allow the communication between the computer and OpenRb-150.
// Arduino IDE was used for this. Some add-ins and Dynamixel libraries are necessary to change and upload the code on the OpenRb-150.
// Dynamixel Setup on Arduino IDE :
//      File -> pref -> URL (https://raw.githubusercontent.com/ROBOTIS-GIT/OpenRB-150/master/package_openrb_index.json)
//
//      tools -> Board manager
//          -> Arduino SAMD
//          -> OpenRB150
//
//      Sketch -> include lib. -> Mangage ->Dynamixel2Arduino


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

int command;

//Motor and offset values
const uint8_t DXL_ID21 = 50;
const uint8_t DXL_ID37 = 37;
const uint8_t DXL_ID26 = 1;
const uint8_t DXL_ID27 = 15;

int offset21 = -(10*(512/45)); //80;
int offset37 = 500; //-46;
int offset26 = -512; //45;
int offset27 = -512; //45;

//Attributing Motor and offset depending on their position
const uint8_t M1 = DXL_ID21; //Front
const uint8_t M2 = DXL_ID26; //Left
const uint8_t M3 = DXL_ID37; //Back
const uint8_t M4 = DXL_ID27; //Right

int offsetM1 = offset21; //80;
int offsetM2 = offset26; //-46;
int offsetM3 = offset37; //45;
int offsetM4 = offset27; //45;

const uint8_t Motor_array[4] = {M1,M2,M3,M4};


const float DXL_PROTOCOL_VERSION = 2.0;
Dynamixel2Arduino dxl(DXL_SERIAL, DXL_DIR_PIN);
using namespace ControlTableItem;

//Global variables to control move
int degree_90_thick = 512 *2;

int32_t goal_position_M1 = 0;
int32_t goal_position_M2 = 0;
int32_t goal_position_M3 = 0;
int32_t goal_position_M4 = 0;

//PID
uint16_t position_p_gain = 1000;
uint16_t position_i_gain = 2;
uint16_t position_d_gain = 700;

//Communication
int receivedValue;

//Max Torque control
int Max_Torque = 0.5; //N*m Calculated to rotate 1 face of the cube with SF of 4.
//int Max_Current = (((1.4-0.2)/(1.5-0.06))*Max_Torque + 0.15)*1000; //Max_current in mA based on the documentation sheet on XL430 with ratio information
int Max_Current = 100;

void setup() {

  Serial.begin(57600);

  //DEBUG_SERIAL.begin(115200);
  while(!DEBUG_SERIAL);
  dxl.begin(57600);
  // Set Port Protocol Version. This has to match with DYNAMIXEL protocol version.
  dxl.setPortProtocolVersion(DXL_PROTOCOL_VERSION);
  // Get DYNAMIXEL information

  setting_up(M1);
  setting_up(M2);
  setting_up(M3);
  setting_up(M4);

  HOMING();
}

void loop() {

  Serial.readBytes((char*)&receivedValue, 4);
  command = receivedValue;
  // delay(1000);
  // command = 8;

  if (command == 0) //HOMING
  {
    HOMING();
    done();
  }

  if (command == 1) //M1_L
  {
    left(M1, &goal_position_M1);
    done();
  }
  if (command == 2) //M1_R
  {
    right(M1, &goal_position_M1);
    done();
  }
  if (command == 3) //M2_L
  {
    left(M2, &goal_position_M2);
    done();
  }
  if (command == 4) //M2_R
  {
    right(M2, &goal_position_M2);
    done();
  }
  if (command == 5) //M3_L
  {
    left(M3, &goal_position_M3);
    done();
  }
  if (command == 6) //M3_R
  {
    right(M3, &goal_position_M3);
    done();
  }
  if (command == 7) //M4_L
  {
    left(M4, &goal_position_M4);
    done();
  }
  if (command == 8) //M4_R
  {
    right(M4, &goal_position_M4);
    done();
  }


  if (command == 9) //M1M3_L
  {
    left_2M_M1M3(M1, &goal_position_M1, M3, &goal_position_M3); 
    done();
  }
  if (command == 10) //M1M3_R
  {
    right_2M_M1M3(M1, &goal_position_M1, M3, &goal_position_M3);
    done();
  }
  if (command == 11) //M2M4_L
  {
    left_2M_M2M4(M2, &goal_position_M2, M4, &goal_position_M4);
    done();
  }
  if (command == 12) //M2M4_R
  {
    right_2M_M2M4(M2, &goal_position_M2, M4, &goal_position_M4);
    done();
  }

  Serial.flush();
  receivedValue = 15;
}

void HOMING () //Placing the motors in initial postion with offset and changing the goal position for every motor to offset value.
{
  dxl.setGoalPosition(M1, offsetM1);
  dxl.setGoalPosition(M2, offsetM2);
  dxl.setGoalPosition(M3, offsetM3);
  dxl.setGoalPosition(M4, offsetM4);
  goal_position_M1 = offsetM1;
  goal_position_M2 = offsetM2;
  goal_position_M3 = offsetM3;
  goal_position_M4 = offsetM4;
}

void right (const uint8_t DXL_ID, int32_t *goal_position)
{
    // Counter-Clockwise for right rotation
    while(dxl.getPresentVelocity(DXL_ID) != 0)
    {
    }
    int move =  *goal_position + degree_90_thick ;
    *goal_position = *goal_position + degree_90_thick;
    dxl.setGoalPosition(DXL_ID, move);
}

void left (const uint8_t DXL_ID, int32_t *goal_position)
{
    // Clockwise for left roatation
    while(dxl.getPresentVelocity(DXL_ID) != 0)
    {
    }
    int move =  *goal_position - degree_90_thick ;
    *goal_position = *goal_position - degree_90_thick;
    dxl.setGoalPosition(DXL_ID, move);
}

void right_2M_M2M4 (const uint8_t DXL_ID_1, int32_t *goal_position_1, const uint8_t DXL_ID_2, int32_t *goal_position_2)
{
    // Right rotatation from 2 motors based on the first one
    right(DXL_ID_1, goal_position_1);
    left(DXL_ID_2, goal_position_2);

}

void left_2M_M2M4 (const uint8_t DXL_ID_1, int32_t *goal_position_1, const uint8_t DXL_ID_2, int32_t *goal_position_2)
{
    // Right rotatation from 2 motors based on the first one
    left(DXL_ID_1, goal_position_1);
    right(DXL_ID_2, goal_position_2);

}

void left_2M_M1M3 (const uint8_t DXL_ID_1, int32_t *goal_position_1, const uint8_t DXL_ID_2, int32_t *goal_position_2)
{
    // Left rotatation from 2 motors based on the first one
    left(DXL_ID_1, goal_position_1);
    left(DXL_ID_2, goal_position_2);
}

void right_2M_M1M3 (const uint8_t DXL_ID_1, int32_t *goal_position_1, const uint8_t DXL_ID_2, int32_t *goal_position_2)
{
    // Left rotatation from 2 motors based on the first one
    right(DXL_ID_1, goal_position_1);
    right(DXL_ID_2, goal_position_2);
}

void done() //Revoir le while seems sus
{
  delay(25);
  while(
    dxl.getPresentVelocity(DXL_ID21) != 0 ||
    dxl.getPresentVelocity(DXL_ID37) != 0 ||
    dxl.getPresentVelocity(DXL_ID26) != 0 ||
    dxl.getPresentVelocity(DXL_ID27) != 0
    )
    {
      // if (Check_Exceed_Max_Torque()==1){
      //   return;
      // }
    }
    int valueToSend = 1;
    Serial.write((uint8_t*)&valueToSend, sizeof(valueToSend));
    valueToSend = 0;
}

bool Check_Exceed_Max_Torque()
{
  for (int i=0; i<4;i++){
    // dxl.setOperatingMode(Motor_array[i], 	OP_CURRENT);
    // Serial.println(dxl.getPresentCurrent(M4, UNIT_MILLI_AMPERE));
    if (dxl.getPresentCurrent(Motor_array[i], UNIT_MILLI_AMPERE) > Max_Current){
      Stop_rotation();
      delay(25);
      int valueToSend = 2; //Error
      Serial.write((uint8_t*)&valueToSend, sizeof(valueToSend));
      valueToSend = 0;
      return(1);
    }
    // dxl.setOperatingMode(Motor_array[i], 	OP_EXTENDED_POSITION);
  }
  return(0);
}

void Stop_rotation()
{
  Serial.print("Stop rotation");
  for (int i=0; i<4;i++){
    // dxl.setOperatingMode(Motor_array[i], OP_EXTENDED_POSITION);
    int Temp_Pos = 0;
    Temp_Pos = dxl.getPresentPosition(Motor_array[i]);
    dxl.setGoalPosition(Motor_array[i], Temp_Pos);
    dxl.torqueOff(Motor_array[i]);
    dxl.torqueOn(Motor_array[i]);
  }

}

void setting_up(const uint8_t DXL_ID){

  dxl.ping(DXL_ID);

  // Turn off torque when configuring items in EEPROM area
  dxl.torqueOff(DXL_ID);

  dxl.setOperatingMode(DXL_ID, OP_EXTENDED_POSITION);

  dxl.torqueOn(DXL_ID);

  dxl.writeControlTableItem(PROFILE_VELOCITY, DXL_ID, 15000); //Velocity is from 0-32767 Profil_velocity*0.229 rev/min = speed

  dxl.writeControlTableItem(POSITION_P_GAIN, DXL_ID, position_p_gain);
  dxl.writeControlTableItem(POSITION_I_GAIN, DXL_ID, position_i_gain);
  dxl.writeControlTableItem(POSITION_D_GAIN, DXL_ID, position_d_gain);
}


