/* Program for the glove controller : 2 flexometers and a gyroscope*/

#include <Arduino_LSM9DS1.h>

int i = 0;
int j = 0;
float x, y, z;
double moy_x, moy_y, moy_z = 0;
int aux = 0;

const int flexPin1 = A0;
const int flexPin2 = A1;

int val1;
int val2;

uint32_t btn = 0;
bool btn0 = false;
bool btn1 = false;
bool btn2 = false;
bool btn3 = false;
int x_pos = 0;
int x_neg = 0;


int droite(int i);
int gauche(int i);
bool isButton1(int j);
bool isButton2(int j);
bool isFlexButton(int j);
void readGyro();

void setup() {
  Serial.begin(9600);
  while (!Serial);
  //Serial.println("Started");

  if (!IMU.begin()) {
    //Serial.println("Failed to initialize IMU!");
    while (1);
  }
  /*
  Serial.print("Gyroscope sample rate = ");
  Serial.print(IMU.gyroscopeSampleRate());
  Serial.println(" Hz");
  Serial.println();
  Serial.println("Gyroscope in degrees/second");
  Serial.println("X\tY\tZ");*/
}

void loop() {
  

  

  readGyro();
   
  val1 = analogRead(flexPin1);
  val2 = analogRead(flexPin2);

  /*Serial.print("flex 1 = ");
  Serial.print('\t');
  Serial.print(val1);
  Serial.print('\t');
  Serial.print(", flex 2 = ");
  Serial.print('\t');
  Serial.println(val2);*/
  
  bool btn0_new = isButton1(j);
  bool btn1_new = isButton2(j);
  bool btn2_new = isFlexButton(val1);
  bool btn3_new = isFlexButton(val2);
  int x_pos_new = getXValue(i);

  if (btn0 != btn0_new || btn1 != btn1_new || btn2 != btn2_new  || btn3 != btn3_new || x_pos_new != 
  x_pos){
    
  
    btn0 = btn0_new;
    btn1 = btn1_new;
    btn2 = btn2_new;
    btn3 = btn3_new;
    x_pos = x_pos_new;
    btn = 0;
    if (btn2) {btn = btn + 1;}
    btn = btn << 1;
    if (btn3) { btn = btn + 1;}
    btn = btn << 1;
    if (btn0) { btn = btn + 1;}
    btn = btn << 1;
    if(btn1){btn+=1;}

    uint32_t cmd = btn;
    cmd = cmd << 10;
    cmd = cmd + 512;
    cmd = cmd << 10;
    cmd = cmd + x_pos;
    Serial.println(cmd);
  }
  
  
  delay(100);
}

int getXValue(int a){
  if(a <= -1){
    //Serial.println(a);
    //Serial.println("gauche");
    i = -1;
    return 0;
  }else if(a >= 1){
    i = 1;
    return 1022;
  }
  //Serial.println("normal");

  //Serial.println(a);
  return 512;
}

bool isButton1(int a){
  if(a >= 1){
    //Serial.println(a);
    j = 1;
    //Serial.println("button 1");
    return true;
  }
  return false;
}

bool isButton2(int a){
  if(a <= -1){
    //Serial.println(a);
    j = -1;
    //Serial.println("button 2");
    return true;
  }
  return false;
}

bool isFlexButton(int a){
  if(a < 250){
    //Serial.println("Je te flex dessus");
    //Serial.println(a);
    return true;
  }
  return false;
}

void readGyro(){
  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(x, y, z);
    
    if(x>200){
        i += 1;
        x=0;
    }else if(x < -200){
        i -= 1;
        x=0;
    }

    if(y>200){
        j += 1;
        y=0;
    }else if(y < -200){
        j -= 1;
        y=0;
    }
    
  }
}
