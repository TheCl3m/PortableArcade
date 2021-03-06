import serial
from uinput import Device
import uinput

events = (
    uinput.BTN_A,
    uinput.BTN_B,
    uinput.BTN_X,
    uinput.BTN_Y,
    uinput.BTN_JOYSTICK,
    uinput.ABS_X + (0, 1023, 0, 0),
    uinput.ABS_Y + (0, 1023, 0, 0),
)

devices = ['/dev/ttyUSB0', '/dev/ttyUSB1']


def create_controller():
    return Device(events)


def decode_command(vector, cntrl):
    if vector is None:
        cntrl.emit(uinput.BTN_A, 0)
        cntrl.emit(uinput.BTN_B, 0)
        cntrl.emit(uinput.BTN_X, 0)
        cntrl.emit(uinput.BTN_Y, 0)

    else:
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


def setup():

    while True:
        for name in devices:
            try:
                print("Trying to connect to " + name)
                srl = serial.Serial(port=name, baudrate=9600, timeout=1)
                srl.write("CHECK\n")

                # Si on recoit une reponse on envoie un msg a l'arduino correspondante et on sort de la boucle
                if srl.readline().decode('utf-8').rstrip() == "HELLO":
                    print("Connected to " + name)
                    ser.write("LINKED\n")
                    return srl
            except:
                continue


if __name__ == '__main__':
    ser = setup()
    print("Code started successfully\n")

    #name = '/dev/ttyUSB0'
    #ser = serial.Serial(port=name, baudrate=9600, timeout=1)
    print("Found serial " + ser.name)

    ser.flush()
    print("Flushed serial successfully")

    controller = create_controller()
    print("Controller created")

    tryneeded = True

    while True:
        if ser.in_waiting > 0:
            if tryneeded:
                try :
                    command = ser.readline()
                    decode_command(command, cntrl=controller)
                except:
                    print("ERROR: Could not read")
            else:
                command = ser.readline()
                decode_command(command, cntrl=controller)
        else:
            decode_command(None, cntrl=controller)
