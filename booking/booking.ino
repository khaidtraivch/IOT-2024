#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN 9           // Reset pin for RFID module
#define SS_PIN 10           // Slave select pin for RFID module

MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create MFRC522 instance

// Define parking slots and their availability
bool parkingSlotAvailable[4] = { true, true, true, true };
unsigned long parkingStartTime[4] = { 0, 0, 0, 0 };
float hourlyRate = 5.0;     // Define hourly rate

// Mock user data for RFID
const String authorizedRFID[] = { "123456789", "987654321" }; // Example RFIDs

void setup() {
  Serial.begin(9600);       // Initialize serial communications
  SPI.begin();              // Init SPI bus
  mfrc522.PCD_Init();       // Init MFRC522
  Serial.println("Parking System Initialized. Scan your card to start.");
}

void loop() {
  // Check for an RFID card
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    String rfidTag = getRFIDTag();
    int slot = getAvailableSlot();

    if (isAuthorized(rfidTag)) {
      if (slot != -1) {
        // Book the available slot and start timing
        parkingSlotAvailable[slot] = false;
        parkingStartTime[slot] = millis();
        Serial.print("Booking confirmed for Slot ");
        Serial.println(slot + 1);
        Serial.println("You may enter.");
      } else {
        Serial.println("No available slots. Please wait.");
      }
    } else {
      Serial.println("Access denied. Unauthorized RFID card.");
    }

    mfrc522.PICC_HaltA(); // Stop reading
  }

  // Mock checkout logic (would typically happen on button press or sensor trigger)
  for (int i = 0; i < 4; i++) {
    if (!parkingSlotAvailable[i] && millis() - parkingStartTime[i] > 5000) {  // Simulate 5 seconds as parking duration
      float cost = calculateCost(i);
      Serial.print("Slot ");
      Serial.print(i + 1);
      Serial.print(" checkout. Total cost: $");
      Serial.println(cost);
      parkingSlotAvailable[i] = true; // Free up the slot
    }
  }
}

// Helper function to calculate cost
float calculateCost(int slot) {
  unsigned long durationMillis = millis() - parkingStartTime[slot];
  float durationHours = (float)durationMillis / 3600000;  // Convert milliseconds to hours
  return durationHours * hourlyRate;
}

// Helper function to get RFID tag as a string
String getRFIDTag() {
  String tag = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    tag += String(mfrc522.uid.uidByte[i], HEX);
  }
  return tag;
}

// Check if RFID is authorized
bool isAuthorized(String tag) {
  for (String authorizedTag : authorizedRFID) {
    if (tag == authorizedTag) {
      return true;
    }
  }
  return false;
}

// Get the first available slot
int getAvailableSlot() {
  for (int i = 0; i < 4; i++) {
    if (parkingSlotAvailable[i]) {
      return i;
    }
  }
  return -1;  // No slots available
}
