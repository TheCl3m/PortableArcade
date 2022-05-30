import os
import time
import RPi.GPIO as GPIO



#-----GPIO CALLBACKS-------

def start_callback(channel):
    print("START PRESSED")

def select_callback(channel):
    print("SELECT PRESSED")

def coin_callback(channel):
    print("COIN PRESSED")


#------MAIN--------------

if __name__ == '__main__':

    #----GPIO----
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP) #start Button
    GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP) #select Button
    GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP) #coin Button
    GPIO.add_event_detect(23, GPIO.FALLING, callback=start_callback)
    GPIO.add_event_detect(24, GPIO.FALLING, callback=select_callback)
    GPIO.add_event_detect(25, GPIO.FALLING, callback=coin_callback)

    #---SETUP ACK----
    print("Code started successfully")

    #----LOOP--------

    while True:
        time.sleep(1)

    #-----END--------