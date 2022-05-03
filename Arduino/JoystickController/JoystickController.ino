/*
* This file will be the arduino controller for the
* joystick and buttons input
* it will communicate the inputs to the Raspberry Pi via USS
* @Author Clément Husler
*/


#define vrX A0
#define vrY A1
#define SW 2

#define BTN_0 2
#define BTN_1 3
#define BTN_2 4
#define BTN_3 5


int xPos = 0;
int yPos = 0;
int SW_state = 0;
int mapX = 0;
int mapY = 0;
bool configured = false;
uint32_t btn = 0;

bool btn0 = false;
bool btn1 = false;
bool btn2 = false;
bool btn3 = false;

bool needToUpdate(int old, int n);


void setup(){
    //prepare usb communication
    Serial.begin(9600); 

    //prepare the joystick
    pinMode(vrX, INPUT);
    pinMode(vrY, INPUT);
    pinMode(SW, INPUT_PULLUP); 

    //enable pinmode for buttons as INPUT
    pinMode(BTN_0, INPUT_PULLUP);
    pinMode(BTN_1, INPUT_PULLUP);
    pinMode(BTN_2, INPUT_PULLUP);
    pinMode(BTN_3, INPUT_PULLUP);
    
    pinMode(BTN_0, INPUT_PULLUP);
    pinMode(LED_BUILTIN, OUTPUT);



}


bool needToUpdate(int old, int n){
      return abs(old-n) > 20;
}

void loop(){
    if (!configured && Serial.available() > 0){
        Serial.println("HELLO");
        configured = true;
    }
    else {
        SW_state = digitalRead(SW);
        int mapX_new = analogRead(vrX);
        int mapY_new = analogRead(vrY);

        bool btn0_new = digitalRead(BTN_0) == HIGH;
        bool btn1_new = digitalRead(BTN_1) == HIGH;
        bool btn2_new = digitalRead(BTN_2) == HIGH;
        bool btn3_new = digitalRead(BTN_3) == HIGH;
  
        if (btn0 != btn0_new || btn1 != btn1_new || btn2 != btn2_new || btn3 != btn3_new || needToUpdate(mapX, mapX_new) || needToUpdate(mapY, mapY_new)){
          
            btn0 = btn0_new;
            btn1 = btn1_new;
            btn2 = btn2_new;
            btn3 = btn3_new;
            mapY = mapY_new;
            mapX = mapX_new;

            btn = 0;
            if (btn0) {btn = btn + 1;}
            btn = btn << 1;
            if (btn1) { btn = btn + 1;}
            btn = btn << 1;
            if (btn2) { btn = btn + 1;}
            btn = btn << 1;
            if (btn3) { btn = btn + 1;}
    
            uint32_t cmd = btn;
            cmd = cmd << 10;
            cmd = cmd + mapY;
            cmd = cmd << 10;
            cmd = cmd + mapX;


            Serial.println(cmd);
    
            delay(10);
        }

     }

}
