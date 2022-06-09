/* Program for the glove controller : 2 flexometers and a gyroscope*/

#include <Arduino_LSM9DS1.h>

int i = 0;
int j = 0;
float x, y, z;

const int flexPin1 = A0;
const int flexPin2 = A1;

int val1;
int val2;

uint32_t btn = 0;
bool btn0 = false;
bool btn1 = false;
bool btn2 = false;
bool btn3 = false;
int x_pos = 512;
int y_pos = 512;


void setup() {
  Serial.begin(9600);
  while (!Serial);

  if (!IMU.begin()) {
    while (1);
  }
}

void loop() {
  
  readGyro();
   
  val1 = analogRead(flexPin1);
  val2 = analogRead(flexPin2);
  
  bool btn0_new = false ;///isButton1(j) ;
  bool btn1_new = false; //isButton2(j);
  bool btn2_new = isFlexButton(val1);
  bool btn3_new = isFlexButton(val2);
  int x_pos_new = getXValue(i);
  int y_pos_new = getYValue(j);

  if (btn0 != btn0_new || btn1 != btn1_new || btn2 != btn2_new  || btn3 != btn3_new || x_pos_new != x_pos || y_pos_new != y_pos){
    
  
    btn0 = btn0_new;
    btn1 = btn1_new;
    btn2 = btn2_new;
    btn3 = btn3_new;
    x_pos = x_pos_new;
    y_pos = y_pos_new;
    
    btn = 0;
    if (btn2) {btn = btn + 1;}
    btn = btn << 1;
    if (btn3) { btn = btn + 1;}
    btn = btn << 2;
    /*if (btn0) { btn = btn + 1;}
    btn = btn << 1;
    if(btn1){btn+=1;}*/

    uint32_t cmd = btn;
    cmd = cmd << 10;
    cmd = cmd + y_pos;
    cmd = cmd << 10;
    cmd = cmd + x_pos;
    Serial.println(cmd);
  }
  
  
  delay(50);
}

int getXValue(int a){
  //going left
  if(a <= -1){
    i = -1;
    return 0;
  }
  //Going right
  else if(a >= 1){
    i = 1;
    return 1022;
  }
  //Not moving in th x axis
  
  return 512;
}

int getYValue(int a){
  //Going up
  if(a <= -1){
    j = -1;
    return 1022;
  }
  //Going down
  else if(a >= 1){
    j = 1;
    return 0;
  }
  //Not moving in th y axis
  return 512;
}

//is flex sensor flexing
bool isFlexButton(int a){
  if(a < 250){
    return true;
  }
  return false;
}

//reads gyroscope and sets the i and j value that gives the orientation
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
