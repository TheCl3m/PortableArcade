
#include <Arduino_LSM9DS1.h>


  // Constants
  #define BTN_0 2 // ?? 

  // Parameters
  float x_start, y_start, z_start;


  //Variables
  bool configured = false;


  uint32_t btn = 0;
  bool btn1 = false;
  bool btn2 = false;



  /**
   * @brief 
   * This functions is going to tell us if the levier is up.
   * We are going to emulate a button thanks to this
   * 
   * 
   * @param analogValue 
   * @return true if its up 
   * @return false  if not
   */
  bool button1(float y){
    //&& (z/z_start) < 0.8
    if((y/y_start) > 1.5 ){
      Serial.println("droite");
      return true;
    }else{
      return false;}
  }
  /**
   * @brief 
   *This functions is going to tell us if the levier is down.
  * We are going to emulate a button thanks to this 
  * @param analogValue 
  * @return true if its down
  * @return false  if not
  */
  bool button2(float y){
    //&& (z/z_start) < 0.6
    if((y/y_start) < 0){
      Serial.println("gauche");
      return true;
    }else{
      return false;}
  }




  /**
   * @brief this function setup the arduino
   * 
   * @return ** void 
   */
  void setup(void) {
    Serial.begin(9600);
    while (!Serial);
    Serial.println("Started");
  
    if (!IMU.begin()) {
      Serial.println("Failed to initialize IMU!");
      while (1);
    }
    Serial.print("Magnetic field sample rate = ");
    Serial.print(IMU.magneticFieldSampleRate());
    Serial.println(" Hz");
    Serial.println();
    Serial.println("Magnetic Field in uT");
    Serial.println("X\tY\tZ");
    if (IMU.magneticFieldAvailable()) {
      IMU.readMagneticField(x_start, y_start, z_start);
    }
    pinMode(BTN_0, INPUT_PULLUP); //??? 

  }



  void loop(void) {
    float x, y, z;
    if (IMU.magneticFieldAvailable()) {
        IMU.readMagneticField(x, y, z);
        bool btn1_new = button1(y);
        bool btn2_new = button2(y);
    
        if (btn1 != btn1_new || btn2 != btn2_new) {
              btn1 = btn1_new;
              btn2 = btn2_new;

              btn = 0;
              btn = btn << 1;
              if (btn1) { btn = btn + 1;}
              btn = btn << 1;
              if (btn2) { btn = btn + 1;}
              btn = btn << 1;
     
              btn = btn << 20;


              Serial.println(btn);
      
              delay(40);
          }
    }
  }

  
    

/*

float x_start, y_start, z_start;
  

#include <Arduino_LSM9DS1.h>

void setup() {
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Started");

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
  Serial.print("Magnetic field sample rate = ");
  Serial.print(IMU.magneticFieldSampleRate());
  Serial.println(" Hz");
  Serial.println();
  Serial.println("Magnetic Field in uT");
  Serial.println("X\tY\tZ");
  if (IMU.magneticFieldAvailable()) {
    IMU.readMagneticField(x_start, y_start, z_start);
  }
}

void loop() {
  float x, y, z;

  if (IMU.magneticFieldAvailable()) {
    IMU.readMagneticField(x, y, z);

    Serial.print(x);
    Serial.print('\t');
    Serial.print(y);
    Serial.print('\t');
    Serial.println(z);
    //&& (z/z_start) < 0.8
    if((y/y_start) > 1.5 ){
      Serial.println("droite");
    }
     //&& (z/z_start) < 0.6
    if((y/y_start) < 0){
      Serial.println("gauche");
    }
    
  }
  delay(500);
}*/
