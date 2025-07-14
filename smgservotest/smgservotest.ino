//wifi
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClientSecure.h>

#include <Arduino_JSON.h>
//display
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>


//servo 
#include <Servo.h>

//wifi
const char* ssid = "laptopwifi";
const char* password = "laptoppassword";


const int buttonPin = 14;
bool buttonState = HIGH;


ESP8266WebServer server(80);

const char* apiUrl = "https://192.168.137.1:5000";

void handleRoot() {
  server.send(200, "text/plain", "Hello from ESP32");
}

//screen
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 32

 bool recordit = false;

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire ,-1);


//servo
// Servo myServo;


void setup() {
  Serial.begin(115200);
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.clearDisplay();
  display.setTextSize(1);
  display.setRotation(2);

  display.setTextColor(SSD1306_WHITE);

  // wifi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    
    Serial.println(WiFi.localIP());
    Serial.print(".");
    display.clearDisplay();
    display.setCursor(0,0);
    display.println("connecting to wifi...");
    display.display();
  }

  Serial.println(WiFi.gatewayIP());
  Serial.println("Connected");
  //display


    pinMode(buttonPin, INPUT_PULLUP);  // Use internal pull-up resistor

  display.clearDisplay();
      display.setCursor(0,0);

  display.println("Conneeeeected!");
  display.display();
  delay(1000);
}

void loop() {
   
  bool stoploop = false;
  server.handleClient();
  if (WiFi.status() == WL_CONNECTED) {
      buttonState = digitalRead(buttonPin);

      if (buttonState == LOW || recordit) {  // Button pressed (connected to GND)
     Serial.println("buttonpress");
     delay(400);
         WiFiClient client;
  //   WiFiClientSecure client;
  // client.setInsecure();

    HTTPClient http;
       buttonState = digitalRead(buttonPin);

    // Call the trigger endpoint
    String serverurl = String(apiUrl) + "/trigger";
    Serial.println(serverurl);
    http.begin(client, serverurl);
    int triggerHttpCode = http.POST("");
    Serial.println(triggerHttpCode);
    if (triggerHttpCode > 0) {
           buttonState = digitalRead(buttonPin);

      Serial.println("Trigger endpoint called successfully");
      display.clearDisplay();
      display.setCursor(0, 0);
      display.println("recording...");
      display.display();
    } else {
      // Serial.println("Trigger endpoint call failed");
      Serial.println("HTTP Response Code: " + String(triggerHttpCode));
      Serial.println("HTTP Response Body: " + http.getString());
           buttonState = digitalRead(buttonPin);
if(buttonState == LOW){
  stoploop = true;
  delay(200);
}
    }
    http.end();
         buttonState = digitalRead(buttonPin);
if(buttonState == LOW){
  stoploop = true;
        display.clearDisplay();
      display.setCursor(0, 0);
      display.println("disconnecting...");
      display.display();

  delay(200);
}

    // Poll the response endpoint until a non-empty message is returned
    String response = "";
     buttonState = digitalRead(buttonPin);
if(buttonState == LOW){
  stoploop = true;
        display.clearDisplay();
      display.setCursor(0, 0);
      display.println("disconnecting...");
      display.display();

  delay(200);
}
    while (response == "") {
           buttonState = digitalRead(buttonPin);
if(buttonState == LOW){
  stoploop = true;
        display.clearDisplay();
      display.setCursor(0, 0);
      display.println("disconnecting...");
      display.display();

  break;
  delay(200);
}
      http.begin(client, String(apiUrl) + "/get_response");
      int responseHttpCode = http.GET();
      if (responseHttpCode > 0) {
        String payload = http.getString();
        Serial.println("Polling response: " + payload);
        JSONVar json = JSON.parse(payload);
        Serial.println(json["response"]);
        Serial.println("Payload.response:" + String(json["response"]));
        response = String(json["response"]);
        
      } else {
        Serial.println("Response endpoint call failed");
      }
      http.end();
      delay(2000); // Wait 1 second before polling again
    }
         buttonState = digitalRead(buttonPin);
if(buttonState == LOW){
  stoploop = true;
        display.clearDisplay();
      display.setCursor(0, 0);
      display.println("disconnecting ...");
      display.display();

  delay(200);
}

    Serial.println("Response received: " + response);

    // Display the response message on the OLED
    // Scrolling config
    int charsPerLine = 21;
    int linesVisible = 3;
    int scrollOffset = 0;
    unsigned long lastScrollTime = 0;
    int scrollDelay = 3000; // ms between scrolls

    display.clearDisplay();
    display.setCursor(0, 0);
    // display.println(response.substring(0, 21));
    // if (response.length() > 21)
    //   display.println(response.substring(21, 42));
    // display.display();
         buttonState = digitalRead(buttonPin);
if(buttonState == LOW){
  stoploop = true;
  delay(200);
}
    bool cont = true;
    while (cont) {
           buttonState = digitalRead(buttonPin);
if(buttonState == LOW){
  stoploop = true;
  continue;
  delay(200);
}
  
      display.clearDisplay();
      display.setCursor(0, 0);
  
      for (int i = 0; i < linesVisible; i++) {
        int start = (scrollOffset + i) * charsPerLine;
        if (start < response.length()) {
          String line = response.substring(start, min(start + charsPerLine, (int)response.length()));
          display.println(line);
        }
      }
  
      display.display();
  
      // Advance scroll position if not at end
      if ((scrollOffset + linesVisible) * charsPerLine < response.length()) {
        delay(scrollDelay);
        scrollOffset++;
      } else {
        Serial.println("scrolling stopped");
        if(!stoploop){
          recordit = true;
          Serial.println("rerording");
          delay(2000);

        }else{
          recordit = false;
        }
        cont = false; 
      }
    }

    delay(200);  // Debounce delay
  
  }

 
  } else {
    Serial.println("WiFi Disconnected");
  }
  
}
