#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "Your_SSID";
const char* password = "Your_PASSWORD";

const char* serverIP = "192.168.1.100"; // Replace with your server's IP address
const int serverPort = 8080;           // Replace with your server's port (default: 8080)

// Button pin
const int buttonPin = 26;

bool buttonPressed = false;

void setup() {
  // Initialize serial monitor
  Serial.begin(115200);
  
  // Configure the button pin
  pinMode(buttonPin, INPUT_PULLUP); // Assuming the button is active-low

  // Connect to WiFi
  Serial.print("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
}

void loop() {
  // Check if the button is pressed
  if (digitalRead(buttonPin) == LOW) { // Button is active-low
    if (!buttonPressed) { // Only handle on the first press
      buttonPressed = true;
      Serial.println("Button pressed! Sending GET request...");
      sendGETRequest();
    }
  } else {
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
    } else {
      Serial.print("Error sending GET request: ");
      Serial.println(http.errorToString(httpResponseCode));
    }

    http.end(); // Close the connection
  } else {
    Serial.println("WiFi not connected!");
  }
}
