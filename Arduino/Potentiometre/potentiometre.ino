/* Potentiometer reading program for steering wheel*/

// Constants
#define DELAY 500 // Delay between two measurements in ms
#define VIN 5 // V power voltage
#define R 10000 //ohm resistance value

// Parameters
const int sensorPin = A0; // Pin connected to sensor


//Variables
int sensorVal; // Analog value from the sensor
uint32_t res = 0; //resistance value
bool configured = false;


void setup(void) {
  Serial.begin(9600);
}

void loop(void) {
  if (!configured || Serial.available > 0){
    Serial.println("HELLO");
    configured = true;
  } else {
    sensorVal = analogRead(sensorPin);
    uint32_t new_res = sensorRawToPhys(sensorVal) * (1023/10000);
    if (new_res != res) {
      res = new_res;
      Serial.println(res);
    }

    delay(DELAY);
  }
  

  
  /*Serial.print(F("Raw value from sensor= "));
    Serial.println(sensorVal); // the analog reading
    Serial.print(F("Physical value from sensor = "));
    Serial.print(res); // the analog reading
    Serial.println(F(" ohm")); // the analog reading*/
  
}


float sensorRawToPhys(int raw) {
  // Conversion rule
  float Vout = float(raw) * (VIN / float(1023));// Conversion analog to voltage
  float phys = R * ((Vout)) / VIN; // Conversion voltage to resistance between GND and signal
  float phys2 = R * ((VIN - Vout)) / VIN; // Conversion voltage to resistance between 5V and signal
  return phys;
}
