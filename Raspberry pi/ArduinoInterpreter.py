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
    if string is None:
        cntrl.emit(uinput.BTN_A, 0)
        cntrl.emit(uinput.BTN_B, 0)
        cntrl.emit(uinput.BTN_X, 0)
        cntrl.emit(uinput.BTN_Y, 0)

    else:
        cmd = string
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

    return string


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
    # ser = setup()
    print("Code started successfully\n")

    name = '/dev/ttyUSB0'
    ser = serial.Serial(port=name, baudrate=9600, timeout=1)
    print("Found serial " + ser.name)

    ser.flush()
    print("Flushed serial successfully")

    controller = create_controller()
    print("Controller created")

    tryneeded = True

    while True:
        if ser.in_waiting > 0:
            if tryneeded:
                try:
                    command = ser.readline().decode('utf-8').rstrip()
                    decode_command(command, cntrl=controller)
                except:
                    print("UTF-8 error, retrying...")
            else:
                command = ser.readline().decode('utf-8').rstrip()
                decode_command(command, cntrl=controller)
