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
        xPos = analogRead(vrX);
        yPos = analogRead(vrY);
        SW_state = digitalRead(SW);
        int mapX_temp = map(xPos, 0, 1023, -512, 512);
        int mapY_temp = map(yPos, 0, 1023, -512, 512);

        if (mapX != mapX_temp || mapY != mapY_temp){
            mapX = mapX_temp;
            mapY = mapY_temp;
        }
        Serial.print("JST_");
        Serial.print(mapX);
        Serial.print(";");
        Serial.println(mapY);
        //Serial.print("L3:");
        //Serial.println(SW_state);
        
        //BUTTONS ARE ACTIVE HIGH
        Serial.print("BTN_");
        if (digitalRead(BTN_0) == HIGH){
                Serial.println("A:ON");
            }
            if (digitalRead(BTN_1) == HIGH){
                Serial.println("B:ON");
            }
            if (digitalRead(BTN_2) == HIGH){
                Serial.println("C:ON");
            }
            if (digitalRead(BTN_3) == HIGH){
                Serial.println("D:ON");
            }
            delay(10);
    }
}
