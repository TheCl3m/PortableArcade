import serial
from uinput import Device
import uinput

events = (
    uinput.BTN_A,
    uinput.BTN_B,
    uinput.BTN_X,
    uinput.BTN_Y,
    uinput.BTN_JOYSTICK,
    uinput.ABS_X + (-512, 512, 0, 0),
    uinput.ABS_Y + (-512, 512, 0, 0),
)

devices = ['/dev/ttyACM0', '/dev/ttyACM1']


def create_controller():
    return Device(events)


def decode_command(string, cntrl):
    cmd = string.split("-")

    if cmd[0] == "BTN":

        if cmd[1] == "A:ON":
            cntrl.emit(uinput.BTN_A, 1)
        else:
            cntrl.emit(uinput.BTN_A, 0)

        if cmd[1] == "B:ON":
            cntrl.emit(uinput.BTN_B, 1)
        else:
            cntrl.emit(uinput.BTN_B, 0)

        if cmd[1] == "C:ON":
            cntrl.emit(uinput.BTN_X, 1)
        else:
            cntrl.emit(uinput.BTN_X, 0)

        if cmd[1] == "D:ON":
            cntrl.emit(uinput.BTN_Y, 1)
        else:
            cntrl.emit(uinput.BTN_Y, 0)


        #if cmd[1] == "L3:ON":
         #   cntrl.write(e.EV_KEY, e.KEY_4, 1)
        #else:
         #   cntrl.write(e.EV_KEY, e.KEY_4, 0)




    elif cmd[0] == "JST":
        coord = cmd[1].split(";")
        cntrl.emit(uinput.ABS_X, coord[0])
        cntrl.emit(uinput.ABS_Y, coord[1])

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
    #ser = setup()
    print("Code started successfully\n")

    name = '/dev/ttyACM0'
    ser = serial.Serial(port=name, baudrate=9600, timeout=1)
    print("Found serial " + ser)

    ser.flush()
    print("Flushed serial successfully")

    controller = create_controller()
    print("Controller created")

    while True:
        if ser.in_waiting > 0:
            command = ser.readline().decode('utf-8').rstrip()
            print(decode_command(command, cntrl=controller))


