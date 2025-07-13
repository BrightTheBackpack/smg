//wifi
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClientSecure.h>

//display
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>


//servo 
#include <Servo.h>

//wifi
const char* ssid = "GitHub Guest";
const char* password = "octocat11";

ESP8266WebServer server(80);

const char* apiUrl = "https://e-five-kappa.vercel.app/";

void handleRoot() {
  server.send(200, "text/plain", "Hello from ESP32");
}

//screen
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 32
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire ,-1);


//servo
Servo myServo;


void setup() {
  Serial.begin(115200);

  //wifi
  // WiFi.begin(ssid, password);
  // while (WiFi.status() != WL_CONNECTED) delay(1000);
  // Serial.println(WiFi.localIP());
  //   if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
  //   Serial.println(F("SSD1306 allocation failed"));
  //   while (true);
  // }

  //display
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);

  //   display.println("Connecting WiFi...");
  //   display.display();
  //   //  while (WiFi.status() != WL_CONNECTED) {
  //   delay(500);
  //   Serial.print(".");
  // }

  display.clearDisplay();
  display.println("Connected!");
  display.display();
  delay(1000);

  //wifi
  // server.on("/", handleRoot);
  // server.begin();
  // Serial.println(WiFi.localIP());

  //servo
  myServo.attach(D2);

  myServo.write(0);    
  
}

void loop() {
  // myServo.write(30);
  // delay(1000);
  // myServo.write(0);
  // delay(1000);
  server.handleClient();
    if (WiFi.status() == WL_CONNECTED) {
      WiFiClientSecure client;  // Use WiFiClientSecure for HTTPS
    client.setInsecure();     
    HTTPClient http;  
    http.begin(client, apiUrl);
    int httpCode = http.GET();

    if (httpCode > 0) {
      String payload = http.getString();
      Serial.println(payload);

      // Extract joke (naive)
      int start = payload.indexOf("\"value\":\"") + 9;
      int end = payload.indexOf("\",", start);
      String joke = payload.substring(start, end);
      Serial.println("return: ");
      Serial.print(joke);
      // Print to OLED (first 2 lines only due to 32px height)
      display.clearDisplay();
      display.setCursor(0, 0);
      display.println(joke.substring(0, 21));
      if (joke.length() > 21)
        display.println(joke.substring(21, 42));
      display.display();
    } else {
      Serial.println("GET request failed");
    }
    http.end();
  } else {
    Serial.println("WiFi Disconnected");
  }
  display.clearDisplay();
  display.setCursor(0,0);
  display.println("testing, testing");
  display.display();
  delay(10000);
  myServo.write(90);
  delay(1000); 
  myServo.write(90);
  delay(1000);
  myServo.write(0);
  delay(1000);

}
