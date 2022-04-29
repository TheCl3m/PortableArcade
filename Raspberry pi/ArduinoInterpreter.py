import serial
from evdev import UInput, AbsInfo, ecodes as e

cap = {  e.EV_KEY : [e.KEY_0, e.KEY_1, e.KEY_2, e.KEY_3],
 e.EV_ABS : [ (e.ABS_X, AbsInfo(value=0, min=-512, max=512, 
fuzz=0, flat=0, resolution=0)),
(e.ABS_Y, AbsInfo(0, -512, 512, 0, 0, 0)),
 (e.ABS_MT_POSITION_X, (0, 128, 255, 0)) ]}


def create_controller():

    return UInput(cap, "VirtualController", version=0x1);


def decode_command(string):
    command = string.split("-")
    match (command[0]):
        case "BTN":
            return command[1]

        case "JST":
            coord = command[1].split(";")
            return coord[0], coord[1]

        case _:
            return "Not recognized"


if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, 1)
    ser.flush()

    controller = create_controller()

    while True:
        if ser.in_waiting > 0:
            command = ser.readline().decode('utf-8').rstrip()
            print(decode_command(command))
