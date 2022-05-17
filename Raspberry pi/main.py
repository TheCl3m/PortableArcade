#!/usr/bin/python
# -*- coding: utf-8 -*-
import serial
from uinput import Device
import uinput
import time
import pyudev
import os

events = (
    uinput.BTN_A,
    uinput.BTN_B,
    uinput.BTN_X,
    uinput.BTN_Y,
    uinput.BTN_JOYSTICK,
    uinput.ABS_X + (0, 1023, 0, 0),
    uinput.ABS_Y + (0, 1023, 0, 0),
    )

pending_devices = []
devices = []
controllers = []
serials = []


def create_controller():
    return Device(events)


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


def device_change(action, device):

    # check if it is an arduino

    if device.device_type == 'usb_device':
        if device.get('ID_VENDOR_ID') == '1a86':
            pending_devices.append(device.sys_path)
    elif device.device_type == 'usb_interface':
        # if pending_device starts with device.sys_path
                idx = (devices.index(device) if device
                       in devices else -1)
                if action == 'remove':
                    if idx != -1:
                        dev = devices.pop(idx)
                        ctr = controllers.pop(idx)
                        ser = serials.pop(idx)
                        del(dev)
                        del(ctr)
                        del(ser)
                elif action == 'add':
                     for pending_device in pending_devices:
                        if pending_device == device.sys_path[:len(pending_device)]:
                            controllers.append(create_controller())
                            path = [os.path.join('/dev', f) for f in
                                    os.listdir(device.sys_path)
                                    if f.startswith('tty')]
                            serials.append(serial.Serial(path[0], 9600,
                                        timeout=1))
                            devices.append(device)
                            pending_devices.remove(pending_device)


if __name__ == '__main__':
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by('usb')
    observer = pyudev.MonitorObserver(monitor, device_change)
    observer.start()

    print("Code started successfully")

    while True:
        for (i, dev) in enumerate(devices):
            ser = serials[i]
            controller = controllers[i]
            try:
                if ser.in_waiting > 0:
                    command = ser.readline().decode('utf-8').rstrip()
                    decode_command(int(command), cntrl=controller)
            except:
                time.sleep(0.1)
        time.sleep(0.01)
