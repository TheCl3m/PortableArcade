import serial
from evdev import UInput, AbsInfo, ecodes as e

cap = {e.EV_KEY: [e.KEY_0, e.KEY_1, e.KEY_2, e.KEY_3],
       e.EV_ABS: [(e.ABS_X, AbsInfo(0, -512, 512,
                                    0, 0, 0)),
                  (e.ABS_Y, AbsInfo(0, -512, 512, 0, 0, 0)),
                  (e.ABS_MT_POSITION_X, (0, 128, 255, 0))]}


def create_controller():
    return UInput(cap, "VirtualController", 0x1)


def decode_command(string, controller):
    cmd = string.split("-")

    if cmd[0] == "BTN" :

        if cmd[1] == "A:ON" :
            controller.write(e.EV_KEY, e.KEY_0, 1)

        elif cmd[1] == "A:OFF" :
            controller.write(e.EV_KEY, e.KEY_0, 0)

        elif cmd[1] == "B:ON":
            controller.write(e.EV_KEY, e.KEY_1, 1)

        elif cmd[1] == "B:OFF":
            controller.write(e.EV_KEY, e.KEY_1, 1)

        elif cmd[1] == "C:ON":
            controller.write(e.EV_KEY, e.KEY_2, 1)

        elif cmd[1] == "C:OFF":
            controller.write(e.EV_KEY, e.KEY_2, 1)

        elif cmd[1] == "D:ON":
            controller.write(e.EV_KEY, e.KEY_3, 1)

        elif cmd[1] == "D:OFF":
            controller.write(e.EV_KEY, e.KEY_3, 1)

    elif cmd[0] == "JST":
        coord = cmd[1].split(";")
        controller.write(e.EV_ABS, e.ABS_X, coord[0])
        controller.write(e.EV_ABS, e.ABS_Y, coord[1])

    return cmd


if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, 1)
    ser.flush()

    while True:
        if ser.in_waiting > 0:
            command = ser.readline().decode('utf-8').rstrip()
            print(decode_command(command))












