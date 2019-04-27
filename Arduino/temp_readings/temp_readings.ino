#include <SoftwareSerial.h>
SoftwareSerial client(2,3); //RX, TX

String webpage="";
int i=0,k=0;
String readString;
int x=0;

boolean NO_IP=false;
String IP="";
char temp1='0';

//TMP36 Pin Variables
int sensorPin = 0;

// runs once
void setup() {
  Serial.begin(9600); // Start the serial connection with the computer 
                      // to view the result open the serial monitor
  client.being(9600);
  wifi_init();
}

// runs repeatedly
void loop() {
  // needs to modify Send() function to send the temperature readings
  k=0;
  Serial.println("Please refresh the page");
  while(k<1000) {
    k++;
    while(client.available()) {
      if(client.find("0,CONNECT")) {
        Serial.println("Start Printing");
        Send();
        Serial.println("Done Printing");
        delay(1000);
      }
    }
  }
  // get temperature readings
  while(1){
    getTempReadings();
    
    // wait for 5 minutes before the next iteration
    delay(300000);
  }
}

void getTempReadings() {
  // gets the voltage reading from the temperature sensor
  int reading = analogRead(sensorPin);

  // converting that reading to voltage(for 5.0v arduino)
  float voltage = reading * 5.0;
  voltage /= 1024.0;

  // print out the voltage
  Serial.print(voltage); Serial.println(" volts");

  // now print out the temperature
  // converting from 10mv per degree with 500mV offset to degress
  // ((voltage - 500mV) * 100)
  float temperatureC = (voltage - 0.5) * 100;
  Serial.print(temperatureC); Serial.println(" degrees C");
}

void checkForIP(int t1) {
  int t2=millis();
  while(t2+t1>millis()) {
    while(client.available()>0) {
      if(client.find("WIFI GOT IP")) {
        NO_IP=true;
      }
    }
  }
}

void get_ip() {
  IP="";
  char ch=0;
  while(1) {
    client.println("AT+CIFSR");
    while(client.available()>0) {
      if(client.find("STAIP,")){
        delay(1000);
        Serial.print("IP Address:");
        while(client.available()>0) {
          ch = client.read();
          if(ch=='+') break;
          IP += ch;
        }
      }
      if(ch=='+') break;
    }
    if(ch=='+') break;
    delay(1000);
  }
  Serial.print(IP);
  Serial.print("Port:");
  Serial.print(80);
}

void connect_wifi(String cmd, int t) {
  int temp=0, i=0;
  while(1) {
    Serial.print(cmd);
    client.print(cmd);
    while(client.available()) {
      if(client.find("OK")) i=8;
    }
    delay(t);
    if(i > 5) break;
    i++;
  }
  if(i==8) Serial.println("OK");
  else Serial.println("Error");
}

void wifi_init() {
  connect_wifi("AT",100);
  connect_wifi("AT+CWMODE=3",100);
  connect_wifi("AT+CWQAP",100);  
  connect_wifi("AT+RST",5000);
  check4IP(5000);
  if(!NO_IP) {
    Serial.println("Connecting Wifi....");
    connect_wifi("AT+CWJAP=\"OSGOTANATION_UPUNET\",\"uppsalauni\"",10000); //provide your WiFi username and password here
 // connect_wifi("AT+CWJAP=\"vpn address\",\"wireless network\"",7000);
  }
//  else{}
  Serial.println("Wifi Connected"); 
  get_ip();
  connect_wifi("AT+CIPMUX=1",100);
  connect_wifi("AT+CIPSERVER=1,80",100);
}

void sendwebdata(String webPage)
{
  int ii=0;
  while(1) {
    unsigned int l=webPage.length();
    Serial.print("AT+CIPSEND=0,");
    client.print("AT+CIPSEND=0,");
    Serial.println(l+2);
    client.println(l+2);
    delay(100);
    Serial.println(webPage);
    client.println(webPage);
    while(client.available()) {
      //Serial.print(Serial.read());
      if(client.find("OK")) {
        ii=11;
        break;
      }
    }
    if(ii==11) break;
    delay(100);
  }
}

// Modify this function to send temperature readings
void Send() {
  webpage = "<h1>Welcome to Circuit Digest</h1><body bgcolor=f0f0f0>";
  sendwebdata(webpage);
  webpage=name;
  webpage+=dat;
  sendwebdata(webpage);
  delay(1000);
  webpage = "<a href="http://circuitdigest.com/";
  webpage+="\">Click Here for More projects</a>";
  sendwebdata(webpage);
  client.println("AT+CIPCLOSE=0"); 
}
