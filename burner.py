import RPi.GPIO as GPIO
import time
import sys


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

program = []

# Define pins.
a0 = 27
a1 = 22
a2 = 10
a3 = 9
a4 = 11
a5 = 5
a6 = 6
a7 = 13
a8 = 18
a9 = 23
a10 = 8
a11 = 24
a12 = 19
a13 = 15
a14 = 26

d0 = 17
d1 = 4
d2 = 3
d3 = 2
d4 = 21
d5 = 20
d6 = 16
d7 = 12

we = 14
oe = 25
ce = 7


def setAddressPinmode(mode):
    GPIO.setup(a0, mode)
    GPIO.setup(a1, mode)
    GPIO.setup(a2, mode)
    GPIO.setup(a3, mode)
    GPIO.setup(a4, mode)
    GPIO.setup(a5, mode)
    GPIO.setup(a6, mode)
    GPIO.setup(a7, mode)
    GPIO.setup(a8, mode)
    GPIO.setup(a9, mode)
    GPIO.setup(a10, mode)
    GPIO.setup(a11, mode)
    GPIO.setup(a12, mode)
    GPIO.setup(a13, mode)
    GPIO.setup(a14, mode)

    return


def setDataPinmode(mode):
    GPIO.setup(d0, mode)
    GPIO.setup(d1, mode)
    GPIO.setup(d2, mode)
    GPIO.setup(d3, mode)
    GPIO.setup(d4, mode)
    GPIO.setup(d5, mode)
    GPIO.setup(d6, mode)
    GPIO.setup(d7, mode)

    return


def write(address, data):
    time.sleep(0.005)
    GPIO.output(we, GPIO.HIGH)
    GPIO.output(oe, GPIO.HIGH)
    GPIO.output(ce, GPIO.HIGH)
    time.sleep(0.001)

    # Set address pins.
    b_str = format(address, '015b')
    GPIO.output(a0, int(b_str[14]))
    GPIO.output(a1, int(b_str[13]))
    GPIO.output(a2, int(b_str[12]))
    GPIO.output(a3, int(b_str[11]))
    GPIO.output(a4, int(b_str[10]))
    GPIO.output(a5, int(b_str[9]))
    GPIO.output(a6, int(b_str[8]))
    GPIO.output(a7, int(b_str[7]))
    GPIO.output(a8, int(b_str[6]))
    GPIO.output(a9, int(b_str[5]))
    GPIO.output(a10, int(b_str[4]))
    GPIO.output(a11, int(b_str[3]))
    GPIO.output(a12, int(b_str[2]))
    GPIO.output(a13, int(b_str[1]))
    GPIO.output(a14, int(b_str[0]))

    # Set data pins.
    b_str = format(data, '08b')
    GPIO.output(d0, int(b_str[7]))
    GPIO.output(d1, int(b_str[6]))
    GPIO.output(d2, int(b_str[5]))
    GPIO.output(d3, int(b_str[4]))
    GPIO.output(d4, int(b_str[3]))
    GPIO.output(d5, int(b_str[2]))
    GPIO.output(d6, int(b_str[1]))
    GPIO.output(d7, int(b_str[0]))

    time.sleep(0.001)
    GPIO.output(ce, GPIO.LOW)
    time.sleep(0.001)

    GPIO.output(we, GPIO.LOW)
    time.sleep(0.001)
    
    GPIO.output(we, GPIO.HIGH)
    GPIO.output(ce, GPIO.HIGH)
    time.sleep(0.001)

    return


def validate_data():
    setDataPinmode(GPIO.IN)
    time.sleep(0.005)

    address = 0
    for byte in program:
        GPIO.output(we, GPIO.HIGH)
        GPIO.output(oe, GPIO.HIGH)
        GPIO.output(ce, GPIO.HIGH)
        time.sleep(0.001)

        # Set address pins.
        b_str = format(address, '015b')
        GPIO.output(a0, int(b_str[14]))
        GPIO.output(a1, int(b_str[13]))
        GPIO.output(a2, int(b_str[12]))
        GPIO.output(a3, int(b_str[11]))
        GPIO.output(a4, int(b_str[10]))
        GPIO.output(a5, int(b_str[9]))
        GPIO.output(a6, int(b_str[8]))
        GPIO.output(a7, int(b_str[7]))
        GPIO.output(a8, int(b_str[6]))
        GPIO.output(a9, int(b_str[5]))
        GPIO.output(a10, int(b_str[4]))
        GPIO.output(a11, int(b_str[3]))
        GPIO.output(a12, int(b_str[2]))
        GPIO.output(a13, int(b_str[1]))
        GPIO.output(a14, int(b_str[0]))

        time.sleep(0.001)
        GPIO.output(ce, GPIO.LOW)
        time.sleep(0.001)
    
        GPIO.output(oe, GPIO.LOW)
        time.sleep(0.001)

        read_byte = str(GPIO.input(d7)) + str(GPIO.input(d6)) + str(GPIO.input(d5)) + str(GPIO.input(d4)) + \
                     str(GPIO.input(d3)) + str(GPIO.input(d2)) + str(GPIO.input(d1)) + str(GPIO.input(d0))
        read_byte = int(read_byte, 2)

        time.sleep(0.001)
        GPIO.output(oe, GPIO.HIGH)
        GPIO.output(ce, GPIO.HIGH)
        time.sleep(0.001)

        if read_byte != byte:
            print("ERROR! Address {0}, written: {1} read: {2}".format(address, byte, read_byte))

        address += 1

    return


def clean_up():
    setDataPinmode(GPIO.IN)
    setAddressPinmode(GPIO.IN)
    GPIO.output(ce, GPIO.HIGH)
    GPIO.output(oe, GPIO.LOW)
    GPIO.output(we, GPIO.LOW)

    return


def read_program_data_from_file(f):
    with open(f, "rb") as program_file:
        byte = program_file.read(1)
        while byte != b"":
            byte = int.from_bytes(byte, "big")
            program.append(byte)
            byte = program_file.read(1)

    return


def main():
    global program

    # Set initial GPIO state.
    GPIO.setup(we, GPIO.OUT)
    GPIO.setup(oe, GPIO.OUT)
    GPIO.setup(ce, GPIO.OUT)
    setAddressPinmode(GPIO.OUT)
    setDataPinmode(GPIO.OUT)

    # Read in program data.
    print("Reading in program data.")
    read_program_data_from_file(sys.argv[1])
    if sys.argv[2] == "lwasm":
        program = program[5:]

    # Write EEPROM.
    print("Writing EEPROM.")
    address = 0
    for byte in program:
        write(address, byte)
        address += 1

    print("Running validation.")
    validate_data()

    clean_up()
    print("Done!")

    return


if __name__ == "__main__":
    main()
