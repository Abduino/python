#include "WiFiEsp.h"
#include <SPI.h> 
#include <Adafruit_BMP085.h>
Adafruit_BMP085 bmp;
#include<dht.h>
#define DHT11_PIN 2
dht DHT;


//#ifndef HAVE_HWSERIAL1
#include "SoftwareSerial.h"
SoftwareSerial softserial(4, 5); // RX, TX
//#endif

int moisture_sensor_pin = A0;
int light_sensor_pin = A1;
int gas_sensor_pin = A2;

//int moisture_sensor_pin = A0;

int moisture_sensor_analog_value;
float moisture_sensor_value;
float temperature_sensor_value=10.0;
float humidity_sensor_value=10.0;
float light_sensor_value=10.0;

float gas_sensor_value;

float air_pressure_sensor_value=10;
float sealevel_pressure_sensor_value=10;
float altitude_sensor_value=10;
float altitude_sensor_value_2=10;

char ssid[] = "D-Link";//"ccicsdept";            // your network SSID (name)
char pass[] = "abdre3343";//"12345678"; 
//char ssid[] = "ccicsdept";            // your network SSID (name)
//char pass[] = "12345678";// your network password
int status = WL_IDLE_STATUS;
int reqCount = 0;                // number of requests received

WiFiEspServer server(80);


void setup()
{
  // initialize serial for debugging
      pinMode(DHT11_PIN,INPUT);
  pinMode(moisture_sensor_pin,INPUT);
  pinMode(light_sensor_pin,INPUT);
  pinMode(gas_sensor_pin,INPUT);
  Serial.begin(9600);
  // initialize serial for ESP module
  softserial.begin(115200);
  softserial.write("AT+CIOBAUD=9600\r\n");
  softserial.write("AT+RST\r\n");
  softserial.begin(9600);
  // initialize ESP module
  WiFi.init(&softserial);

  // check for the presence of the shield
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present");
    // don't continue
    while (true);
  }

  // attempt to connect to WiFi network
  while ( status != WL_CONNECTED) {
    Serial.print("Attempting to connect to WPA SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network
    status = WiFi.begin(ssid, pass);
  }

  Serial.println("You're connected to the network");
  printWifiStatus();
  bmp.begin();
  
  // start the web server on port 80
  server.begin();
}


void loop()
{
  // listen for incoming clients
  WiFiEspClient client = server.available();
  if (client) {
    Serial.println("New client");
    boolean currentLineIsBlank = true;
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        Serial.write(c);
        if (c == '\n' && currentLineIsBlank) {
          Serial.println("Sending response");
          float temperature =bmp.readTemperature(); //*c
          air_pressure_sensor_value = bmp.readPressure(); //pa
          altitude_sensor_value = bmp.readAltitude(); //meters
          altitude_sensor_value_2 = bmp.readAltitude(101500);
          sealevel_pressure_sensor_value = bmp.readSealevelPressure(); //pa
          int chk = DHT.read11(DHT11_PIN);
          temperature_sensor_value = DHT.temperature;
          humidity_sensor_value = DHT.humidity;
          moisture_sensor_analog_value = analogRead(moisture_sensor_pin);
          moisture_sensor_value = ( 100 - ( (moisture_sensor_analog_value/1023.00) * 100 ) );
          light_sensor_value = map(analogRead(light_sensor_pin), 0, 1023, 100, 0);
          gas_sensor_value = map(analogRead(gas_sensor_pin), 0, 1023, 0, 100);
          float sensor_volt;
          float RS_gas;
          sensor_volt=gas_sensor_value/1024*5.0;
          RS_gas = (5.0-sensor_volt)/sensor_volt;
          
          client.print(
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            "Connection: close\r\n"  // the connection will be closed after completion of the response
            "Refresh: 20\r\n"        // refresh the page automatically every 20 sec
            "\r\n");
          client.print("<!DOCTYPE HTML>\r\n");
          client.print("<html>\r\n");
          client.print("<h4>ESP8266 Wifi IoT lesson 1</h4>\r\n");
          client.print("<h1>Hello World!</h1>\r\n");
          client.print("<h2>");
          client.print(moisture_sensor_value);
          client.print("</h2>");
          client.print("<h2>");
          client.print(temperature_sensor_value);
          client.print("</h2>");
          client.print("<h2>");
          client.print(humidity_sensor_value);
          client.print("</h2>");
          client.print("<h2>");
          client.print(light_sensor_value);
          client.print("</h2>");
          client.print("<h2>");
          client.print(gas_sensor_value);
          client.print("</h2>");
          client.print("<h2>");
          client.print(air_pressure_sensor_value);
          client.print("</h2>");
          client.print("<h2>");
          client.print(altitude_sensor_value);
          client.print("</h2>");
          client.print("<h2>");
          client.print(sealevel_pressure_sensor_value);
          client.print("</h2>");
          client.print("<br>\r\n");
   
    
          client.print("</html>\r\n");
          break;
        }
        if (c == '\n') {
          // you're starting a new line
          currentLineIsBlank = true;
        }
        else if (c != '\r') {
          // you've gotten a character on the current line
          currentLineIsBlank = false;
        }
      }
    }
    // give the web browser time to receive the data
    delay(10);

    // close the connection:
    client.stop();
    Serial.println("Client disconnected");
  }
}


void printWifiStatus()
{
  // print the SSID of the network you're attached to
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
  
  // print where to go in the browser
  Serial.println();
  Serial.print("To see this page in action, open a browser to http://");
  Serial.println(ip);
  Serial.println();
}
