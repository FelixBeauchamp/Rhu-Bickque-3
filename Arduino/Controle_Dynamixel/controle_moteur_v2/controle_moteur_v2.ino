
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

int offset21 = -(10*(512/45)); //80;
int offset37 = 500; //-46;
int offset26 = -512; //45;
int offset27 = -512; //45;

int degree_90_thick = 512 *2;

int compteur_pos = 0;
int32_t goal_position_M1 = 0;
int32_t goal_position_M2 = 0;
int32_t goal_position_M3 = 0;
int32_t goal_position_M4 = 0;

//Test PID
int32_t goal_position_PID = 0;
int8_t direction = 0;
unsigned long timer = 0;

//PID
uint16_t position_p_gain = 1000;
uint16_t position_i_gain = 2;
uint16_t position_d_gain = 700;

//Communication
int receivedValue;

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
  //HOMING_VELOCITY();

}

void loop() {

  Serial.readBytes((char*)&receivedValue, 4);
  command = receivedValue;

  // pour retourner info, Serial.println("");

  // //Test 1
  // dxl.setGoalPosition(M2, 0);
  // DEBUG_SERIAL.println("Position 0 : ");
  // delay(1000);
  // dxl.setGoalPosition(M2, 4095);
  //     DEBUG_SERIAL.println("Position 2 : ");
  // delay(1000);
  // dxl.setGoalPosition(M2, 4096);
  //     DEBUG_SERIAL.println("Position 3 : ");
  // delay(1000);
  // dxl.setGoalPosition(M2, 4100);
  //     DEBUG_SERIAL.println("Position 4 : ");
  // delay(1000);
  // dxl.setGoalPosition(M2, 0);
  //     DEBUG_SERIAL.println("Position 5 : ");
  // delay(1000);

  //Test HOMING
  // DEBUG_SERIAL.print("Position 0 : ");
  // DEBUG_SERIAL.println(dxl.getPresentPosition(M2));
  // delay(100);
  // dxl.setGoalPosition(M2, 0);
  // delay(250);
  // DEBUG_SERIAL.print("Position 1 : ");
  // DEBUG_SERIAL.println(dxl.getPresentPosition(M2));
  // delay(2000);
  // dxl.setGoalPosition(M2, 500);
  // delay(250);
  // DEBUG_SERIAL.print("Position 2 : ");
  // DEBUG_SERIAL.println(dxl.getPresentPosition(M2));
  // delay(3000);
  // dxl.setGoalPosition(M2, 1000);
  // delay(250);
  // DEBUG_SERIAL.print("Position 3 : ");
  // DEBUG_SERIAL.println(dxl.getPresentPosition(M2));
  // delay(2000);
  // dxl.setGoalPosition(M2, 0);
  // delay(250);;
  // DEBUG_SERIAL.print("Position 4 : ");
  // DEBUG_SERIAL.println(dxl.getPresentPosition(M2));
  // delay(2000);
  // dxl.setGoalPosition(M2, -500);
  // delay(250);
  // DEBUG_SERIAL.print("Position 5 : ");
  // DEBUG_SERIAL.println(dxl.getPresentPosition(M2));
  // delay(2000);
  // dxl.setGoalPosition(M2, 1500);
  // delay(250);
  // DEBUG_SERIAL.print("Position 6 : ");
  // DEBUG_SERIAL.println(dxl.getPresentPosition(M2));
  // delay(2000);

  // Test 3
  // if(direction >= 1) {
  //   direction = 0;
  //   delay(100);
  //   goal_position_PID = dxl.getPresentPosition(M2) + degree_90_thick ;

  // } else {
  //   direction = 1;
  //   delay(100);
  //   goal_position_PID = dxl.getPresentPosition(M2) + degree_90_thick ;
  // }
  // while(true) {
  //   DEBUG_SERIAL.print("Goal_Position:");
  //   DEBUG_SERIAL.print(dxl.readControlTableItem(GOAL_POSITION, M2));
  //   DEBUG_SERIAL.print(",");
  //   DEBUG_SERIAL.print("Present_Position:");
  //   DEBUG_SERIAL.print(dxl.getPresentPosition(M2));
  //   DEBUG_SERIAL.print(",");
  //   DEBUG_SERIAL.println();
  //   delay(10);

  //   if (millis() - timer >= 2000) {
  //     dxl.setGoalPosition(M2, goal_position_PID);
  //     timer = millis();
  //     break;
  //   }
  // }

  // Test 4

  // droite_2(M2,&goal_position_M2);
  // DEBUG_SERIAL.print("Present_Position:");
  // DEBUG_SERIAL.println(dxl.getPresentPosition(M2));
  // delay(10);

  if (command == 0) //HOMING
  {
    HOMING();
    done();
  }

  if (command == 1) //M1_L
  {
    gauche(M1, &goal_position_M1);
    done();
  }
  if (command == 11) //M1_R
  {
    droite(M1, &goal_position_M1);
    done();
  }
  if (command == 2) //M2_L
  {
    gauche(M2, &goal_position_M2);
    done();
  }
  if (command == 22) //M2_R
  {
    droite(M2, &goal_position_M2);
    done();
  }
  if (command == 3) //M3_L
  {
    gauche(M3, &goal_position_M3);
    done();
  }
  if (command == 33) //M3_R
  {
    droite(M3, &goal_position_M3);
    done();
  }
  if (command == 4) //M4_L
  {
    gauche(M4, &goal_position_M4);
    done();
  }
  if (command == 44) //M4_R
  {
    droite(M4, &goal_position_M4);
    done();
  }


  if (command == 5) //M1M3_L
  {
    gauche_2M(M1, goal_position_M1, M3, goal_position_M3); //À voir si l'Entrée de goal position est pointeur ou pas
    done();
  }
  if (command == 55) //M1M3_R
  {
    droite_2M(M1,goal_position_M1, M3, goal_position_M3);
    done();
  }
  if (command == 6) //M2M4_L
  {
    gauche_2M(M2, goal_position_M2, M4, goal_position_M4);
    done();
  }
  if (command == 66) //M2M4_R
  {
    droite_2M(M2, goal_position_M2, M4, goal_position_M4);
    done();
  }

  Serial.flush();
  receivedValue = 69;

}

void HOMING ()
{
    dxl.setGoalPosition(M1, offset21);
    dxl.setGoalPosition(M2, offset37);
    dxl.setGoalPosition(M3, offset26);
    dxl.setGoalPosition(M4, offset27);
    DEBUG_SERIAL.println("Position HOMING");
    delay(1000);
}

void droite (const uint8_t DXL_ID, int32_t *goal_position)
{
    // couter-clockwise pour droite
    int offset = 0;
    if (DXL_ID == M1){
      offset = offset21;
    }
    if (DXL_ID == M2){
      offset = offset37;
    }
    if (DXL_ID == M3){
      offset = offset26;
    }
    if (DXL_ID == M4){
      offset = offset27;
    }
    while(dxl.getPresentVelocity(DXL_ID) != 0)
    {
    }
    int move =  *goal_position + degree_90_thick + offset ;
    *goal_position = *goal_position + degree_90_thick;
    dxl.setGoalPosition(DXL_ID, move);
}

void gauche (const uint8_t DXL_ID, int32_t *goal_position)
{
    // Clockwise pour gauche
    int offset = 0;
    if (DXL_ID == M1){
      offset = offset21;
    }
    if (DXL_ID == M2){
      offset = offset37;
    }
    if (DXL_ID == M3){
      offset = offset26;
    }
    if (DXL_ID == M4){
      offset = offset27;
    }
    while(dxl.getPresentVelocity(DXL_ID) != 0)
    {
    }
    int move =  *goal_position - degree_90_thick + offset ;
    *goal_position = *goal_position - degree_90_thick;
    dxl.setGoalPosition(DXL_ID, move);
}
void droite_2 (const uint8_t DXL_ID)
{
    // Clockwise pour gauche
    while(dxl.getPresentVelocity(DXL_ID) != 0)
    {
    }
    int move =  dxl.getPresentPosition(DXL_ID) + degree_90_thick ;
    dxl.setGoalPosition(DXL_ID, move);
}
void gauche_2 (const uint8_t DXL_ID)
{
    // Clockwise pour gauche
    while(dxl.getPresentVelocity(DXL_ID) != 0)
    {
    }
    int move =  dxl.getPresentPosition(DXL_ID) - degree_90_thick ;
    dxl.setGoalPosition(DXL_ID, move);
}

void droite_2M (const uint8_t DXL_ID_1, int32_t goal_position_1, const uint8_t DXL_ID_2, int32_t goal_position_2) //Goal position a revoir si en pointeur ou pas. Sip l'adresse n'est pas envoyé la valeuyr ne sera pas changé
{
    // Rotation 2 moteurs vers la droite par rapport au premier moteur
    droite(DXL_ID_1, &goal_position_1);
    gauche(DXL_ID_2, &goal_position_2);
    //delay(500);

}

void gauche_2M (const uint8_t DXL_ID_1, int32_t goal_position_1, const uint8_t DXL_ID_2, int32_t goal_position_2)
{
    // Rotation 2 moteurs vers la gauche par rapport au premier moteur
    gauche(DXL_ID_1, &goal_position_1);
    droite(DXL_ID_2, &goal_position_2);
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
    int valueToSend = 15;
    Serial.write((uint8_t*)&valueToSend, sizeof(valueToSend));
    delay(10);
    valueToSend = 0;
}

void setting_up(const uint8_t DXL_ID){

  dxl.ping(DXL_ID);

  // Turn off torque when configuring items in EEPROM area
  dxl.torqueOff(DXL_ID);

  dxl.setOperatingMode(DXL_ID, OP_EXTENDED_POSITION);

  dxl.torqueOn(DXL_ID);

  dxl.writeControlTableItem(PROFILE_VELOCITY, DXL_ID, 5000); //Velocity is from 0-32767 Profil_velocity*0.229 rev/min = vitesse

  dxl.writeControlTableItem(POSITION_P_GAIN, DXL_ID, position_p_gain);
  dxl.writeControlTableItem(POSITION_I_GAIN, DXL_ID, position_i_gain);
  dxl.writeControlTableItem(POSITION_D_GAIN, DXL_ID, position_d_gain);
}


// void gauche_v2 (const uint8_t DXL_ID)
// {
//     // cClockwise pour gauche
//     while(dxl.getPresentVelocity(DXL_ID) != 0)
//     {
//     }
//     compteur_pos = compteur_pos - 1;
//     if (compteur_pos < 0){
//       dxl.setGoalPosition(DXL_ID, MIN_POSITION_LIMIT);
//       while(dxl.getPresentVelocity(DXL_ID) != 0)
//         {
//         }
//       dxl.writeControlTableItem(PRESENT_POSITION, DXL_ID, MAX_POSITION_LIMIT);
//       compteur_pos = 3;
//       int move = (compteur_pos * degree_90_thick) + offset37 ;
//       dxl.setGoalPosition(DXL_ID, move);
//     }
//     else{
//       int move = (compteur_pos * degree_90_thick) + offset37 ;
//       dxl.setGoalPosition(DXL_ID, move);
//     }
// }






