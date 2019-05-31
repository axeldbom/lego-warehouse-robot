
// Include Libraries
#include "Arduino.h"
#include "DHT.h"
#include "Adafruit_SI1145.h"
#include <Wire.h>



// Pin Definitions
#define DHT_PIN_DATA	2

/////////////////////
///Order of output///
//////////////////////////
//TIME|UV|VIS|IR|TMP|HUM//
//////////////////////////

////Arduino features 
//Warnings
//User set warning values
//User set time delay on data
//Request data manually
//
//

// Global variables and defines

// object initialization
HardwareSerial& bthc06(Serial1);
DHT dht(DHT_PIN_DATA);
Adafruit_SI1145 uv = Adafruit_SI1145();


// define vars for testing menu
const int DATA_TIMEOUT = 5000;       //define timeout of 5 sec
const int WARN_TIMEOUT = 2000;       //define timeout of 2 sec

const int UV_WARN = 1;
const int VIS_WARN = 500;
const int IR_WARN = 1000;
const int TMP_WARN = 25; //C
const int HUM_WARN = 50; //%
//sensorWarning[]: [0]t, [1]UV_WARN, [2]VIS_WARN,
//            [3]IR_WARN,[4]TMP_WARN,[5]HUM_WARN  
const float sensorWarning[6] = {0, UV_WARN,VIS_WARN,IR_WARN,TMP_WARN,HUM_WARN};
const String warningTxt[6] = {"0","UV","VIS","IR","TMP","HUM"};

bool danger = false;

//sensor[]: [0]t, [1]UV, [2]VIS,
//          [3]IR,[4]TMP,[5]HUM
float sensor[6]; 
int arraySize = sizeof(sensor) / sizeof(sensor[0]);

int decimal = 2;
char seperator = ':';
char eol = '/';
char warnSep = ' ';

String dataRequest = "1";
long time0;
String outputString = " ";

// Setup the essentials for your circuit to work.
//It runs first every time your circuit is powered with electricity.
void setup() {
  // Setup Serial which is useful for debugging
  // Use the Serial Monitor to view printed messages
  Serial.begin(9600);
  while (!Serial) ; // wait for serial port to connect. Needed for native USB
  Serial.println("start");
  //This example uses HC-06 Bluetooth to communicate with an Android device.
  //Download bluetooth terminal from google play store,
  //https://play.google.com/store/apps/details?id=Qwerty.BluetoothTerminal&hl=en
  //Pair and connect to 'HC-06', the default password for connection is '1234'.
  //You should see this message from your arduino on your android device
  bthc06.begin(9600);
  displayToSerialBT("HC-06 Bluetooth: On");

  dht.begin();
  Serial.println("DHT22/11 Humidity and Temperature Sensor: On");

  if (uv.begin()) {
    Serial.println("SI1145 Digital UV Index / IR / Visible Light Sensor: On");
  } else {
    Serial.println("SI1145 Digital UV Index / IR / Visible Light Sensor: NA");
  }

}

// Main logic of the circuit.
//It defines the interaction between the components selected.
//After setup, it runs over and over again, in an eternal loop.
void loop() {
  getSensorData();
  checkWarnings();
  
  if(millis() > time0 + DATA_TIMEOUT){
    time0 = millis();
    displaySensorVals();
  }
  else if (danger || dataRequest == "1") {
    displaySensorVals();
  }

  dataRequest = readBT();

}

String readBT() {
  String bthc06Str = "";
  //Receive String from bluetooth device
  while (bthc06.available())
  {
    Serial.println("Reading");
    //Read a complete line from bluetooth terminal
    bthc06Str = bthc06.readStringUntil('\n');
    // Print raw data to serial monitor
    Serial.print("BT Raw Data: ");
    Serial.println(bthc06Str);
  }
  return bthc06Str;
}

void getSensorData(){
  sensor[0] = float(millis());
  sensor[1] = getUV();
  sensor[2] = getVIS();
  sensor[3] = getIR();
  sensor[4] = getTMP();
  sensor[5] = getHUM();
}

void displaySensorVals() {
  int i;
  outputString = "";
  
  for(i = 0; i < arraySize; i++){
    outputString += String(sensor[i], decimal);
    if (i < arraySize-1){
      outputString += seperator;
    } else {
      outputString += eol;
    }
  }

  displayToSerialBT(outputString);
  delay(WARN_TIMEOUT);
}

void checkWarnings(){
  int i;
  danger = false;
  outputString = "WARNINGS:";

  for(i = 1; i < arraySize; i++){
    if(sensor[i]>sensorWarning[i]){
      danger = true;
      outputString += warningTxt[i]+warnSep;
    }
  }

  if (danger){
    displayToSerialBT(outputString);
  }
  
}

void displayToSerialBT(String msg){
  Serial.println(msg);
  bthc06.println(msg);
  return true;
}

float getUV(){
  float UV = uv.readUV();
  // the index is multiplied by 100 so to get the
  // integer index, divide by 100!
  UV /= 100.0;
  return UV;
}

float getVIS(){
  return uv.readVisible();
}

float getIR(){
  return uv.readIR();
}

float getTMP(){
  // Read temperature in Celsius, for Fahrenheit use .readTempF()
  return dht.readTempC();
}

float getHUM(){
  // Reading humidity in %
  return dht.readHumidity();
}
