#include <LiquidCrystal.h>

#define SSID "Rasi k p"     // "SSID-WiFiname"
#define PASS "rafasafa2" // "password"
#define IP "184.106.153.149"      // thingspeak.com ip
#include <SoftwareSerial.h>
#include "Timer.h" 
#include <Wire.h>
#include "MAX30100_PulseOximeter.h"
#include "max32664.h"  
#define RESET_PIN 04
#define MFIO_PIN 02
#define RAWDATA_BUFFLEN 250
max32664 MAX32664(RESET_PIN, MFIO_PIN, RAWDATA_BUFFLEN);

Timer t;
String msg = "GET /update?key=1Q1VJBJ1Q28U2KMR"; 
SoftwareSerial esp8266(9,10);

#define REPORTING_PERIOD_MS     1000
 
PulseOximeter pox;
uint32_t tsLastReport = 0;
float hr,ret;
int i,j,num_samples;
float diastolicBP = 0;
boolean newData = false;

const int soil =  0;
int ir1state = 0;
int ir2state = 0;
int vout = 0;
int xout = 0;
int yout = 0;
int zout = 0;
int a = 0;
void glucose();
void UpdateInfo();
void pressure();
const int rs = 12, en = 11, d4 = 2, d5 = 3, d6 = 4, d7 = 5;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void loadAlgomodeParameters()
{
  algomodeInitialiser algoParameters;

  algoParameters.calibValSys[0] = 120;
  algoParameters.calibValSys[1] = 122;
  algoParameters.calibValSys[2] = 125;

  algoParameters.calibValDia[0] = 80;
  algoParameters.calibValDia[1] = 81;
  algoParameters.calibValDia[2] = 82;

  algoParameters.spo2CalibCoefA = 1.5958422;
  algoParameters.spo2CalibCoefB = -34.659664;
  algoParameters.spo2CalibCoefC = 112.68987;

  MAX32664.loadAlgorithmParameters(&algoParameters);
}
void pressure()
{
  loadAlgomodeParameters();
  ret = MAX32664.configAlgoInEstimationMode();
  if(num_samples)
  {

    Serial.print("sys = ");
    Serial.print(MAX32664.max32664Output.sys);
    Serial.print(", dia = ");
    Serial.print(MAX32664.max32664Output.dia);
  }
    // Calculate systolic and diastolic blood pressure
  lcd.setCursor(0,0);
         lcd.print("Blood Pressure :");
         lcd.setCursor(6, 1);
         lcd.print(diastolicBP);
         Serial.println(diastolicBP); 
         delay(1000);
         lcd.clear();
}

boolean connectWiFi()
{
  Serial.println("AT+CWMODE=1");
  lcd.setCursor(0,0);
  lcd.print("AT+CWMODE=1");
  esp8266.println("AT+CWMODE=1");
  delay(1000);
  String cmd="AT+CWJAP=\"";
  cmd+=SSID;
  cmd+="\",\"";
  cmd+=PASS;
  cmd+="\"";
  Serial.println(cmd);
  esp8266.println(cmd);
  Serial.println("Connection OK");
  lcd.setCursor(0,0);
  lcd.print("Connection OK");
  delay(2000);
  lcd.clear();
  if(esp8266.find("OK"))
  {
    return true;
  }
  else
  {
    return false;
  }
}
void setup() {
  analogWrite(6,90);
  lcd.begin(16, 2);
  // Print a message to the LCD.
  lcd.clear();
  lcd.setCursor(1,0);
  lcd.print("Patient Health");
  lcd.setCursor(3,1);
  lcd.print("Monitoring !");
  delay(2000);
  lcd.clear();
  
  pinMode(A0, INPUT);
  Serial.begin(9600);
  esp8266.begin(115200);
  Serial.println("AT");
  lcd.setCursor(7, 0);
  lcd.print("AT");
  
  esp8266.println("AT");
  delay(1000);
  if(esp8266.find("OK"))
  {
    connectWiFi();
  }
  
   Serial.begin(9600);
    Serial.print("Initializing pulse oximeter..");
    lcd.setCursor(0,0);
    lcd.print("Initializing");
    lcd.setCursor(0,1);
    lcd.print("pulse oximeter..");
    delay(1000);
    lcd.clear();
 
    // Initialize the PulseOximeter instance
    // Failures are generally due to an improper I2C wiring, missing power supply
    // or wrong target chip
    if (!pox.begin()) {
        Serial.println("FAILED");
        for(;;);
    } else {
        Serial.println("SUCCESS");
        lcd.setCursor(5,0);
        lcd.print("SUCCESS");
        lcd.setCursor(0,1);
        lcd.print("Put the Finger..");
        
    }
     pox.setIRLedCurrent(MAX30100_LED_CURR_7_6MA);
}

void glucose()
{
  for( j=0;j<=5;j++)
  {
  ir1state = analogRead(A0);
  ir2state = (8 * 10^-5) * ir1state ^ 2;
  xout = 0.1873 * ir1state;
  yout = ir2state + xout + 46.131;
  vout = yout * (-1);
  zout = (vout / 100) * 2.2;
  i=0;
  
    if ((ir1state <= 300) && (ir1state >= 20)) 
    {

         Serial.println("GLUCOSE LEVEL in mg/dl:");
         lcd.setCursor(0,0);
         lcd.print("Glucose Level :");
         lcd.setCursor(6, 1);
         lcd.print(zout);
         Serial.println(zout); 
         delay(1000);
         lcd.clear();
         
    }
  }      
      if( zout<=200 ) 
       {
               
               updateInfo();
       }   
} 
void updateInfo()
{
                lcd.setCursor(0, 0);
                lcd.print("Sending data..");
                delay(1000);
                lcd.clear();
lcd.setCursor(0, 0);
lcd.print("BP :");
lcd.setCursor(7,0);
lcd.print(diastolicBP);
lcd.setCursor(0,1);
lcd.print("Glucose :");
lcd.setCursor(10,1);
lcd.print(zout);
                
  String cmd = "AT+CIPSTART=\"TCP\",\"";
  cmd += IP;
  cmd += "\",80";
  Serial.println(cmd);
  esp8266.println(cmd);
  delay(2000);
  
  cmd = msg ;
  cmd += "&field1=";    //field 1 for Glucose
  cmd += zout;
  cmd += "&field2=";  //field 2 for BP
  cmd += diastolicBP;
  
  cmd += "\r\n";
  
  Serial.println("AT+CIPSEND=");
  esp8266.print("AT+CIPSEND=");
  lcd.setCursor(0, 0);
  Serial.println(cmd.length());
  esp8266.println(cmd.length());
  Serial.print(cmd);
  esp8266.print(cmd);
  
  lcd.clear();
  lcd.setCursor(5,0);  
  lcd.print("SUCCESS");  
  lcd.setCursor(4, 1);  
  lcd.print("Thank You");
    delay(1000000);
}
void loop() 
{  
    pox.update();
    if (millis() - tsLastReport > REPORTING_PERIOD_MS)
    {   //40 to 90
        hr =  pox.getHeartRate();
        if (hr > 20) 
        {
            newData = true;
            Serial.print("Heart rate:");
            Serial.print(pox.getHeartRate());
            hr = pox.getHeartRate();
            lcd.clear();
            lcd.setCursor(0, 0);
            lcd.print("Heart Rate:");
            lcd.setCursor(6, 1);
            lcd.print(hr);
            Serial.println("Heart Rate: " + String(hr) + " bpm");
        
            i = i + 1;      
        }       
        tsLastReport = millis();
      
        if (i == 5)
        {
            if (newData == true) 
            {
                pressure();
                glucose();
            }
            newData = false;
            i = 0;
            hr = 0;
        }    
    }
}
