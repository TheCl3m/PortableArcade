import serial
from evdev import UInput, AbsInfo, ecodes as e

cap = {e.EV_KEY: [e.KEY_0, e.KEY_1, e.KEY_2, e.KEY_3],
       e.EV_ABS: [(e.ABS_X, AbsInfo(0, -512, 512,
                                    0, 0, 0)),
                  (e.ABS_Y, AbsInfo(0, -512, 512, 0, 0, 0)),
                  (e.ABS_MT_POSITION_X, (0, 128, 255, 0))]}

devices = ['/dev/ttyACM0', '/dev/ttyACM1']


def create_controller():
    return UInput(cap, "VirtualController", version=0x1)


def decode_command(string, cntrl):
    cmd = string.split("-")

    if cmd[0] == "BTN":

        if cmd[1] == "A:ON":
            cntrl.write(e.EV_KEY, e.KEY_0, 1)

        elif cmd[1] == "A:OFF":
            cntrl.write(e.EV_KEY, e.KEY_0, 0)

        elif cmd[1] == "B:ON":
            cntrl.write(e.EV_KEY, e.KEY_1, 1)

        elif cmd[1] == "B:OFF":
            cntrl.write(e.EV_KEY, e.KEY_1, 1)

        elif cmd[1] == "C:ON":
            cntrl.write(e.EV_KEY, e.KEY_2, 1)

        elif cmd[1] == "C:OFF":
            cntrl.write(e.EV_KEY, e.KEY_2, 1)

        elif cmd[1] == "D:ON":
            cntrl.write(e.EV_KEY, e.KEY_3, 1)

        elif cmd[1] == "D:OFF":
            cntrl.write(e.EV_KEY, e.KEY_3, 1)

    elif cmd[0] == "JST":
        coord = cmd[1].split(";")
        cntrl.write(e.EV_ABS, e.ABS_X, coord[0])
        cntrl.write(e.EV_ABS, e.ABS_Y, coord[1])

    return cmd


def setup():
    serials = [serial.Serial(port=name, baudrate=9600, timeout=1) for name in devices]
    index = -1

    while index == -1:
        for i, ser in enumerate(serials):
            ser.write("CHECK")
            if ser.readline().decode('utf-8').rstrip() is None:
                index = i
                ser.write("LINKED")
                break

    return serials[index]


if __name__ == '__main__':
    ser = setup()
    ser.flush()
    controller = create_controller()

    while True:
        if ser.in_waiting > 0:
            command = ser.readline().decode('utf-8').rstrip()
            print(decode_command(command, cntrl=controller))
