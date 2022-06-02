#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import OrderedDict
import serial
from uinput import Device
import uinput
import time
import pyudev
import os
import RPi.GPIO as GPIO

#--------GLOBALS----------
pending_devices = set()
devices = OrderedDict()
controllers = {}
serials = {}
#----CONTROLLER CONFIG----

events = (
    uinput.BTN_A,
    uinput.BTN_B,
    uinput.BTN_X,
    uinput.BTN_Y,
    uinput.BTN_JOYSTICK, #coin
    uinput.BTN_START, #start
    uinput.BTN_SELECT, #select
    uinput.ABS_X + (0, 1023, 0, 0),
    uinput.ABS_Y + (0, 1023, 0, 0),
    )

#-----GPIO CALLBACKS-------

def start_callback(channel):
    if len(controllers) > 0:
        dev = next(iter(devices))
        if (GPIO.input(23) == GPIO.LOW):
            controllers[dev].emit(uinput.BTN_START, 1)
        else:
            controllers[dev].emit(uinput.BTN_START, 0)

def select_callback(channel):
    if len(controllers) > 0:
        dev = next(iter(devices))
        if (GPIO.input(24) == GPIO.LOW):
            controllers[dev].emit(uinput.BTN_SELECT, 1)
        else:
            controllers[dev].emit(uinput.BTN_SELECT, 0)

def coin_callback(channel):
    if len(controllers) > 0:
        dev = next(iter(devices))
        if (GPIO.input(25) == GPIO.LOW):
            controllers[dev].emit(uinput.BTN_JOYSTICK, 1)
        else:
            controllers[dev].emit(uinput.BTN_JOYSTICK, 0)

#-----CREATE CONTROLLER-----

def create_controller():
    return Device(events)

#-----EXECUTE COMMAND-------

def decode_command(vector, cntrl):
    cmd = vector
    x_coord = cmd & 1023
    cmd = cmd >> 10
    y_coord = cmd & 1023
    cmd = cmd >> 10
    y_btn = cmd & 1
    cmd = cmd >> 1
    x_btn = cmd & 1
    cmd = cmd >> 1
    b_btn = cmd & 1
    cmd = cmd >> 1
    a_btn = cmd & 1

    cntrl.emit(uinput.BTN_A, a_btn)
    cntrl.emit(uinput.BTN_B, b_btn)
    cntrl.emit(uinput.BTN_X, x_btn)
    cntrl.emit(uinput.BTN_Y, y_btn)

    cntrl.emit(uinput.ABS_X, x_coord)
    cntrl.emit(uinput.ABS_Y, y_coord)

    return vector

#-----DEVICE CALLBACK--------

def device_change(action, device):

    # check if it is an arduino

    if device.device_type == 'usb_device':
        id = device.get('ID_VENDOR_ID')
        if id == '1a86' or id == '2341':
            pending_devices.add(device.sys_path)
    elif action == 'remove':
        if device in devices:
            dev = devices.pop(device)
            ctr = controllers.pop(device)
            ser = serials.pop(device)
            ctr.destroy()
            del(dev)
            del(ctr)
            del(ser)
        if device in pending_devices:
            pending_devices.remove(device)
    elif device.device_type == 'usb_interface':
                if action == 'add':
                     for pending_device in pending_devices.copy():
                        if pending_device == device.sys_path[:len(pending_device)]:
                            ctr = controllers.pop(device, None)
                            if ctr is not None:
                                ctr.destroy()
                                del(ctr)
                            controllers[device] = create_controller()
                            path = [os.path.join('/dev', f) for f in
                                    os.listdir(device.sys_path)
                                    if f.startswith('tty')]
                            serials[device] = serial.Serial(path[0], 9600,
                                        timeout=1)
                            devices[device] = None
                            pending_devices.remove(pending_device)


#------MAIN--------------

if __name__ == '__main__':

    #----GPIO----
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP) #start Button
    GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP) #select Button
    GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP) #coin Button
    GPIO.add_event_detect(23, GPIO.BOTH, callback=start_callback)
    GPIO.add_event_detect(24, GPIO.BOTH, callback=select_callback)
    GPIO.add_event_detect(25, GPIO.BOTH, callback=coin_callback)

    #-----DEVICES---
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by('usb')
    observer = pyudev.MonitorObserver(monitor, device_change)
    observer.start()

    #---SETUP ACK----
    print("Code started successfully")

    #----LOOP--------

    while True:
        for dev in devices.copy():
            ser = serials[dev]
            controller = controllers[dev]
            try:
                if ser.in_waiting > 0:
                    command = ser.readline().decode('utf-8').rstrip()
                    decode_command(int(command), cntrl=controller)
            except:
                time.sleep(0.1)
        time.sleep(0.01)

    #-----END--------