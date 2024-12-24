#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <WiFi.h>
#include <HTTPClient.h>

// WiFi credentials (replace with your actual credentials)
const char* ssid = "network_ssid";
const char* password = "network_password";

// Server details (replace with your server's details)
const char* serverIP = "server_ip";
const int serverPort = 8080;

// Button and LED pins
const int buttonPin = 26;
const int ledPin = 27;

// Variables
bool buttonPressed = false;

// Initialize the LCD (address 0x27 and 16x2 size; adjust if your LCD differs)
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  // Initialize serial monitor
  Serial.begin(115200);
  Wire.setPins(21, 22);

  
  // Configure the button pin and LED pin
  pinMode(buttonPin, INPUT_PULLUP); // Button is active-low
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  // Initialize the LCD
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Connecting to");
  lcd.setCursor(0, 1);
  lcd.print("WiFi...");

  // Connect to WiFi
  Serial.print("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  // Update LCD after connecting
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("WiFi Connected!");
  lcd.setCursor(0, 1);
  lcd.print("IP: ");
  lcd.print(WiFi.localIP());

  Serial.println("\nWiFi Connected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  delay(2000); // Allow time to read the display
  lcd.clear();
  lcd.print("Ready for input");
}

void loop() {
  // Check if the button is pressed
  if (digitalRead(buttonPin) == LOW) { // Button is active-low
    if (!buttonPressed) { // Only handle on the first press
      digitalWrite(ledPin, HIGH);
      buttonPressed = true;
      Serial.println("Button pressed! Sending GET request...");
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Sending request");
      sendGETRequest();
    }
  } else {
    if (buttonPressed) {
      digitalWrite(ledPin, LOW);
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Ready for input");
    }
    buttonPressed = false; // Reset when button is released
  }
  delay(100); // Debouncing delay
}

void sendGETRequest() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    // Construct the URL
    String url = String("http://") + serverIP + ":" + serverPort;

    // Begin the HTTP GET request
    http.begin(url);
    int httpResponseCode = http.GET();

    // Check the response
    if (httpResponseCode > 0) {
      Serial.println("GET request sent successfully!");
      Serial.print("Response Code: ");
      Serial.println(httpResponseCode);
      String response = http.getString();
      Serial.println("Response: " + response);

      // Display response code on LCD
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Request Sent!");
      lcd.setCursor(0, 1);
      lcd.print("Resp Code: ");
      lcd.print(httpResponseCode);
    } else {
      Serial.print("Error sending GET request: ");
      Serial.println(http.errorToString(httpResponseCode));

      // Display error on LCD
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Req Error!");
      lcd.setCursor(0, 1);
      lcd.print(http.errorToString(httpResponseCode));
    }

    http.end(); // Close the connection
  } else {
    Serial.println("WiFi not connected!");

    // Display WiFi error on LCD
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("WiFi Error!");
  }

  delay(2000); // Allow time to read the display
  lcd.clear();
  lcd.print("Ready for input");
}
