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
int btn = 0;


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


void loop(){
    if (!configured && Serial.available() > 0){
        Serial.println("HELLO");
        configured = true;
    }
    else {
        SW_state = digitalRead(SW);
        int mapX_temp = analogRead(vrX);
        int mapY_temp = analogRead(vrY);

        bool btn0 = digitalRead(BTN_0) == HIGH;
        bool btn1 = digitalRead(BTN_1) == HIGH;
        bool btn2 = digitalRead(BTN_2) == HIGH;
        bool btn3 = digitalRead(BTN_3) == HIGH;

        if (mapX != mapX_temp ||
            mapY != mapY_temp ||
            btn0 ||
            btn1 ||
            btn2 ||
            btn3){

            mapX = mapX_temp;
            mapY = mapY_temp;

            btn = 0;
            if (btn0) {btn = btn + 1;}
            btn = btn << 1;
            if (btn1) { btn = btn + 1;}
            btn = btn << 1;
            if (btn2) { btn = btn + 1;}
            btn = btn << 1;
            if (btn3) { btn = btn + 1;}

            int cmd = btn;
            cmd = cmd << 10;
            cmd = cmd + mapY;
            cmd = cmd << 10;
            cmd = cmd + mapX;

            char b[4];
            String str = String(cmd);

            Serial.println(str.toCharArray(b, 4);

            delay(10);
        }


    }
}
