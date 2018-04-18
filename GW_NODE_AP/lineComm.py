import serial
import time

port = '/dev/ttyS14'

def connect(b_rate):
    try:
        return serial.Serial(port, b_rate, timeout=10)
    except Exception as e:
        print("Error: ", e)

def decodeData(recv):
    timestamp = recv[1:5]
    chip = recv[5:9]
    pin_id = recv[9]
    dtype = recv[10]
    value = int(recv[11:19], 16)
    lrc = recv[19:23]
    print(chip, pin_id, dtype, value)
    # print(recv)

comm = connect(115200)

if comm:
    while True:
        try:
            if comm.readable():
                rcv = comm.readline();
                if (len(rcv) == 25):
                    decodeData(rcv.decode("ascii"))
                else:
                    print(rcv)
        except Exception as e:
            print("Error: ", e)
