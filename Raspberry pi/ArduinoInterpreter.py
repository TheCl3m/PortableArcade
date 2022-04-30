
import serial
from evdev import _uinput, ecodes as e
from evdev.device import AbsInfo

cap = {e.EV_KEY: [e.KEY_0, e.KEY_1, e.KEY_2, e.KEY_3],
       e.EV_ABS: [(e.ABS_X, AbsInfo(0, -512, 512,
                                    0, 0, 0)),
                  (e.ABS_Y, AbsInfo(0, -512, 512, 0, 0, 0)),
                  (e.ABS_MT_POSITION_X, (0, 128, 255, 0))]}

devices = ['/dev/ttyACM0', '/dev/ttyACM1']


def create_controller():
    return _uinput(cap, "VirtualController", version=0x1)


def decode_command(string, cntrl):
    cmd = string.split("-")

    if cmd[0] == "BTN":

        if cmd[1] == "A:ON":
            cntrl.write(e.EV_KEY, e.KEY_0, 1)
        else:
            cntrl.write(e.EV_KEY, e.KEY_0, 0)

        if cmd[1] == "B:ON":
            cntrl.write(e.EV_KEY, e.KEY_1, 1)
        else:
            cntrl.write(e.EV_KEY, e.KEY_1, 0)

        if cmd[1] == "C:ON":
            cntrl.write(e.EV_KEY, e.KEY_2, 1)
        else:
            cntrl.write(e.EV_KEY, e.KEY_2, 0)

        if cmd[1] == "D:ON":
            cntrl.write(e.EV_KEY, e.KEY_3, 1)
        else:
            cntrl.write(e.EV_KEY, e.KEY_3, 0)


        #if cmd[1] == "L3:ON":
         #   cntrl.write(e.EV_KEY, e.KEY_4, 1)
        #else:
         #   cntrl.write(e.EV_KEY, e.KEY_4, 0)




    elif cmd[0] == "JST":
        coord = cmd[1].split(";")
        cntrl.write(e.EV_ABS, e.ABS_X, coord[0])
        cntrl.write(e.EV_ABS, e.ABS_Y, coord[1])

    return cmd


def setup():

    while True:
        for name in devices:
            try:
                srl = serial.Serial(port=name, baudrate=9600, timeout=1)
                srl.write("CHECK")

                # Si on recoit une reponse on envoie un msg a l'arduino correspondante et on sort de la boucle
                if srl.readline().decode('utf-8').rstrip() is None:
                    ser.write("LINKED")
                    return srl
            except:
                continue


if __name__ == '__main__':
    print("Code started\n")
    ser = setup()
    print("Found serial " + ser)
    ser.flush()
    controller = create_controller()
    print("controller created")
    while True:
        if ser.in_waiting > 0:
            command = ser.readline().decode('utf-8').rstrip()
            print(decode_command(command, cntrl=controller))

