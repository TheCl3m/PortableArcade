/* Potentiometer reading program for steering wheel*/

// Constants
#define DELAY 500 // Delay between two measurements in ms
#define VIN 5 // V power voltage
#define R 10000 //ohm resistance value

// Parameters
const int sensorPin = A0; // Pin connected to sensor


//Variables
int sensorVal; // Analog value from the sensor
float res; //resistance value


void setup(void) {
  Serial.begin(9600);
}


void loop(void) {
  sensorVal = analogRead(sensorPin);
  res = sensorRawToPhys(sensorVal);
  if (res > 0 && res < 4000) {
    where = GAUCHE;
    Serial.println("DROITE");
  } else if (res >= 4000 && res < 6000) {
    where = GAUCHE;
    Serial.println("Milieu");
  } else if (res >= 6000 && res <= 10000) {
    where = GAUCHE;
    Serial.println("GAUCHE");
  }
  /*Serial.print(F("Raw value from sensor= "));
    Serial.println(sensorVal); // the analog reading
    Serial.print(F("Physical value from sensor = "));
    Serial.print(res); // the analog reading
    Serial.println(F(" ohm")); // the analog reading*/
  delay(DELAY);
}


float sensorRawToPhys(int raw) {
  // Conversion rule
  float Vout = float(raw) * (VIN / float(1023));// Conversion analog to voltage
  float phys = R * ((Vout)) / VIN; // Conversion voltage to resistance between GND and signal
  float phys2 = R * ((VIN - Vout)) / VIN; // Conversion voltage to resistance between 5V and signal
  return phys;
}
