#include <ESP8266WiFi.h>
#include <AntaresESP8266HTTP.h >   // Inisiasi library HTTP Antares

//#define ACCESSKEY "58df1234661edc2d:dfea3b44527ed1b1"       // Akun Antares Luthfy
#define ACCESSKEY "c01538e56fc59f94:eff9cd5d2fee545c"       // Akun Antares LabIot

#define WIFISSID "LabIoT2022"
#define PASSWORD "iottelyu"   

#define applicationName "EnergyPowerMonitor"
#define deviceNameStatus "SLA_14"
#define deviceNameRead "slca4naufal"
#define token "e28f1df147da42ee0bd1675af12ec9fc"

#define LED_INTERVAL        2000
#define SENDAMPS_INTERVAL   300000
#define GET_INTERVAL        20000
#define CHECKAMPS_INTERVAL  10000

AntaresESP8266HTTP antares(ACCESSKEY);    // Buat objek antares

const int analogIn = A0;
const int relay = 16;
const int led = 2;

int mVperAmp = 185; // use 100 for 20A Module and 66 for 30A Module and 185 for 5A Module
//int RawValue= 0;
//int ACSoffset = 2500;
float offset = 0;
double Voltage = 0;
double VRMS = 0;
double AmpsRMS = 0;
double Wattage = 0;
bool LedState = false;
unsigned long led_millis = 0;
unsigned long amps_millis = 0;
unsigned long getantares_millis = 0;
unsigned long checkamps_millis = 0;
String RelayStatus, device_token;

void setup() {
  Serial.begin(115200);           // Buka komunikasi serial dengan baudrate 115200
  pinMode(analogIn, INPUT);
  pinMode(relay, OUTPUT);
  digitalWrite(relay, LOW);
  pinMode(led, OUTPUT);
//  antares.setDebug(true);         // Nyalakan debug. Set menjadi "false" jika tidak ingin pesan-pesan tampil di serial monitor
//  antares.wifiConnection(WIFISSID,PASSWORD);  
//  antares.wifiConnectionNonSecure(WIFISSID,PASSWORD);
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFISSID,PASSWORD);
  Serial.print("Connecting to ");
  Serial.print(WIFISSID);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println('\n');
  Serial.println("Connection established!");  
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());
  WiFi.setAutoReconnect(true);
  WiFi.persistent(true);
}

void loop() {  
  if(millis() >= led_millis + LED_INTERVAL)
  {
    led_millis += LED_INTERVAL;
    
    LedState = !LedState;
    digitalWrite(led, LedState);
  }

  if(millis() >= checkamps_millis + CHECKAMPS_INTERVAL)
  {
    checkamps_millis += CHECKAMPS_INTERVAL;
    
    Serial.println("Start Check Amps");
    Voltage = getVPP();
    VRMS = (Voltage/2.0) *0.707;          //sq root
    float AmpsReal = (VRMS * 1000)/mVperAmp;
    float RoundAmps = (int) (AmpsReal * 1000);
    AmpsRMS = RoundAmps / 1000;
    if(RelayStatus == "ON"){
      offset = 27.82;
    }
    else if(RelayStatus == "OFF"){
      offset = 32.84;
    }
    float WattReal = (220*AmpsReal)-offset;     //Observed 18-20 Watt when no load was connected, so substracting offset value to get real consumption.
    float RoundWatt = (int) (WattReal * 1000);
    Wattage = RoundWatt / 1000;
    if(Wattage < 0){
      Wattage = 0;
    }
    
    Serial.print("Volt = "); Serial.println((float)VRMS);
    Serial.print("Amps = "); Serial.print(AmpsRMS); Serial.print(" / "); Serial.println(AmpsReal);
    Serial.print("Watt = "); Serial.print(Wattage); Serial.print(" / "); Serial.println(WattReal);
    Serial.println();
    delay(1);
  }

  if(millis() >= amps_millis + SENDAMPS_INTERVAL)
  {
    amps_millis += SENDAMPS_INTERVAL;
    Serial.println("Start Send Amps to Antares");
    Voltage = getVPP();
    VRMS = (Voltage/2.0) *0.707;          //sq root
    float AmpsReal = (VRMS * 1000)/mVperAmp;
    float RoundAmps = (int) (AmpsReal * 1000);
    AmpsRMS = RoundAmps / 1000;
    if(RelayStatus == "ON"){
      offset = 27.82;
    }
    else if(RelayStatus == "OFF"){
      offset = 32.84;
    }
    float WattReal = (220*AmpsReal)-offset;     //Observed 18-20 Watt when no load was connected, so substracting offset value to get real consumption.
    float RoundWatt = (int) (WattReal * 1000);
    Wattage = RoundWatt / 1000;
    if(Wattage < 0){
      Wattage = 0;
    }
    //Serial.println(AmpsReal);
    //Serial.println(WattReal);
    Serial.print(AmpsRMS);
    Serial.println(" Amps RMS ");
    Serial.print(Wattage); 
    Serial.println(" Watt ");
  
    // Memasukkan nilai-nilai variabel ke penampungan data sementara
    antares.add("token", token);
    antares.add("Amps RMS", AmpsRMS);
    antares.add("Watt", Wattage);

    // Kirim dari penampungan data ke Antares
    antares.sendNonSecure(applicationName, deviceNameStatus);
    delay(1);
  }

  if(millis() >= getantares_millis + GET_INTERVAL)
  {
    getantares_millis += GET_INTERVAL;
    Serial.println("Start Read Antares");
    antares.getNonSecure(applicationName, deviceNameRead);
    if(antares.getSuccess()) {
      device_token = antares.getString("device_token");
      RelayStatus = antares.getString("mode");
      Serial.print("StatusRelay: ");
      Serial.println(RelayStatus);
      Serial.print("Device_Token:");
      Serial.println(device_token);
      if(device_token == token)
      {
        Serial.println("Device Token Benar");
        if(RelayStatus == "ON")
        {
          digitalWrite(relay, LOW);
          Serial.println("Relay Switch ON");
          Serial.println();
        } else if(RelayStatus == "OFF") {
          digitalWrite(relay, HIGH);
          Serial.println("Relay Switch OFF");
          Serial.println();
        }
      }
      delay(1);
    }
  }
}

float getVPP()
{
  float result;
  
  int readValue;             //value read from the sensor
  int maxValue = 0;          // store max value here
  int minValue = 1024;          // store min value here
  
   uint32_t start_time = millis();

   while((millis()-start_time) < 1000) //sample for 1 Sec
   {
       readValue = analogRead(analogIn);
       // see if you have a new maxValue
       if (readValue > maxValue) 
       {
           /*record the maximum sensor value*/
           maxValue = readValue;
       }
       if (readValue < minValue) 
       {
           /*record the maximum sensor value*/
           minValue = readValue;
       }
       //delay(1);
   }
   
   // Subtract min from max
   Serial.println(maxValue);
   Serial.println(minValue);
   result = ((maxValue - minValue) * 5)/1024.0; 
   Serial.println((float)result);
   Serial.println();     
   return result;
}
