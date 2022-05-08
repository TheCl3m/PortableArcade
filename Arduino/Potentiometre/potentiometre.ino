/* Potentiometer reading program for steering wheel*/

// Constants
#define DELAY 500 // Delay between two measurements in ms
#define VIN 5 // V power voltage
#define R 10000 //ohm resistance value
#define BTN_0 2

// Parameters
const int sensorPin = A0; // Pin connected to sensor
const int sensorLevier=A1;

//Variables
int sensorValX=0;      // Analog value from the sensor
uint32_t res = 0;     //resistance value
bool configured = false;



uint32_t btn = 0;
bool btn0 = false;
bool btn1 = false;
bool btn2 = false;

bool needToUpdate(int old, int n);


bool needToUpdate(int old, int n){
      return abs(old-n) > 20;
}


bool buttonNb(float analogValue){
  if(analogValue > 0 && analogValue < 3500 ) return true; //button 1
  else if(analogValue > 6500 && analogValue < 10000) return false; //button 2
}


void setup(void) {
  pinMode(BTN_0, INPUT_PULLUP);

  Serial.begin(9600);
}



void loop(void) {
  if (!configured || Serial.available > 0){
    Serial.println("HELLO");
    configured = true;
  } else {




        int Sensor_valX_new  = analogRead(sensorPin);


        bool btn0_new = digitalRead(BTN_0) == HIGH;
        bool btn1_new = buttonNb(analogRead(sensorLevier));
        bool btn2_new = !btn1_new;
  
        if (btn0 != btn0_new || btn1 != btn1_new || btn2 != btn2_new  || needToUpdate(sensorValX, Sensor_valX_new) 
        ){
          
            btn0 = btn0_new;
            btn1 = btn1_new;
            btn2 = btn2_new;
            sensorValX = sensorRawToPhys(Sensor_valX_new) * (1023/10000);

            btn = 0;
            if (btn0) {btn = btn + 1;}
            btn = btn << 1;
            if (btn1) { btn = btn + 1;}
            btn = btn << 1;
            if (btn2) { btn = btn + 1;}
            btn = btn << 1;
    
            uint32_t cmd = btn;
            cmd = cmd << 20;
            cmd = cmd + sensorValX;


            Serial.println(cmd);
    
            delay(10);
        }

     



   

  
  
  
  }
  

 
  
}


float sensorRawToPhys(int raw) {
  // Conversion rule
  float Vout = float(raw) * (VIN / float(1023));// Conversion analog to voltage
  float phys = R * ((Vout)) / VIN; // Conversion voltage to resistance between GND and signal
  float phys2 = R * ((VIN - Vout)) / VIN; // Conversion voltage to resistance between 5V and signal
  return phys;
}
