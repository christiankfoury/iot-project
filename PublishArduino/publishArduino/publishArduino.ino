#include <WiFi.h>
#include <PubSubClient.h>
//#include "DHTesp.h"
#include "DHT.h"

// needed for rfid tag
#include <SPI.h>
#include <MFRC522.h>


// needed for rfid tag 
#define SS_PIN  5  // ESP32 pin GIOP5 
#define RST_PIN 27 // ESP32 pin GIOP27 

MFRC522 rfid(SS_PIN, RST_PIN);

//DHTesp dht;
#define DHTTYPE DHT11   // DHT 11
DHT dht(32, DHTTYPE);
//const char* ssid = "TP-Link_2AD8";
//const char* password = "14730078";
//const char* ssid = "VIDEOTRON3407";
//const char* password = "34CKA4CRAP4WC";
//const char* ssid = "Saleh 2021";
//const char* password = "canada2015";
//const char* ssid = "YaAli";
//const char* password = "yahussein";
const char* ssid = "Bear";
const char* password = "getyourownwifi";  


//const char* mqtt_server = "192.168.0.125";
//const char* mqtt_server = "192.168.0.176";
const char* mqtt_server = "192.168.156.164";

WiFiClient vanieriot;
PubSubClient client(vanieriot);

//cosntants for the pins where sensors are plugged into.
const int sensorPin = 12;
const int ledPin = 14;

//Set up some global variables for the light level an initial value.
int lightInit;  // initial value
int lightVal;   // light reading
String lightValString;
char lightValChar[50];
char tempChar[50];
char humChar[50];
char tagChar[50];


void setup()
{
  // We'll set up the LED pin to be an output.
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  pinMode(sensorPin, INPUT);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  //dht.setup(34, DHTesp::DHT11);
  dht.begin();

  SPI.begin(); // init SPI bus
  // initializing rfid tag 
  rfid.PCD_Init(); // init MFRC522

//  lightInit = analogRead(sensorPin);
  //we will take a single reading from the light sensor and store it in the lightCal        //variable. This will give us a prelinary value to compare against in the loop
//  Serial.begin(115200);
//  setup_wifi();
//  client.setServer(mqtt_server, 1883);
//  client.setCallback(callback);
}


void loop()
{
  if (!client.connected()) {
    reconnect();
  }
  if(!client.loop())
    client.connect("vanieriot");

//  client.publish("IoTlab/E  SP","Hello IoTlab");
//  String myString = String(lightVal);
//
//  char lightValArr[8];
//  dtostrf(lightVal,6,2,lightValArr);
  lightVal = analogRead(35); // read the current light levels
  Serial.println(lightVal);

  //if lightVal is less than our initial reading withing a threshold then it is dark.
//  if (lightVal <  3000)
//  {
//    digitalWrite (14, HIGH); // turn on light
//  }
//
//  //otherwise, it is bright
//  else
//  {
//    digitalWrite (14, LOW); // turn off light
//  }
  lightValString = String(lightVal); //converting ftemp (the float variable above) to a string 
  lightValString.toCharArray(lightValChar, lightValString.length() + 1); //packaging up the data to publish to mqtt whoa...
  client.publish("IoTlab/light", lightValChar);
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  float f = dht.readTemperature(true);

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  // Compute heat index in Fahrenheit (the default)
  float hif = dht.computeHeatIndex(f, h);
  // Compute heat index in Celsius (isFahreheit = false)
  float hic = dht.computeHeatIndex(t, h, false);

  Serial.println("temp " + String(hic));
  Serial.println("hum " + String(h));

  String tempString = String(hic);
  tempString.toCharArray(tempChar, tempString.length() + 1); //packaging up the data to publish to mqtt whoa...
  String humString = String(h);
  humString.toCharArray(humChar, humString.length() + 1); //packaging up the data to publish to mqtt whoa...  

  String tagString = "";
  // read rfid tag and store it in a variable
  if (rfid.PICC_IsNewCardPresent()) { // new tag is available
    if (rfid.PICC_ReadCardSerial()) { // NUID has been readed
      MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);
      Serial.print("RFID/NFC Tag Type: ");
      //Serial.println(rfid.PICC_GetTypeName(piccType));

      // print UID in Serial Monitor in the hex format
      Serial.print("UID:");
      for (int i = 0; i < rfid.uid.size; i++) {
        Serial.print(rfid.uid.uidByte[i] < 0x10 ? " 0" : " ");
        Serial.print(rfid.uid.uidByte[i], HEX);
        tagString.concat(String(rfid.uid.uidByte[i] < 0x10 ? " 0" : " "));
        tagString.concat(String(rfid.uid.uidByte[i], HEX));
        
      }
      Serial.println();

      rfid.PICC_HaltA(); // halt PICC
      rfid.PCD_StopCrypto1(); // stop encryption on PCD

    }
  }
  // make it all uppercase 
  tagString.toUpperCase();
  // remove space that is automatically there
  tagString = tagString.substring(1);
  tagString.toCharArray(tagChar, tagString.length() + 1);
  client.publish("IoTlab/rfid", tagChar);
  client.publish("IoTlab/temperature", tempChar);
  client.publish("IoTlab/humidity", humChar);
  delay(2000);
}



void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WiFi connected - ESP-8266 IP address: ");
  Serial.println(WiFi.localIP());
}


void callback(String topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messagein;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messagein += (char)message[i];
  }

  if(topic=="room/light"){
    if (messagein == "ON") 
      Serial.println("Light is ON");
  }else{
          Serial.println("Light is OFF");

  }
  
}


void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
 
    
   //  String clientId = "ESP8266Client-";
   // clientId += String(random(0xffff), HEX);
    // Attempt to connect
   // if (client.connect(clientId.c_str())) {
           if (client.connect("vanieriot")) {

      Serial.println("connected");  
      client.subscribe("room/light");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}


