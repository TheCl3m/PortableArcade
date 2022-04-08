import serial
import vgamepad as gp

gamepad = gp.VX360Gamepad()

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

    while True:
        if ser.in_waiting > 0:
            command = ser.readline().decode('utf-8').rstrip()
            print(decode_command(command))
