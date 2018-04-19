import serial
import time

port = '/dev/ttyS10'

def connect(b_rate):
    try:
        return serial.Serial(port, b_rate, timeout=10)
    except Exception as e:
        print("!!ERR: connect", e)

def calcLRC(input):
    lrc = 0x0
    for b in input:
        lrc += b
        lrc %= 0xFFFF+1
    return "%04X"%(0xFFFF - lrc)

def processData(t_stamp, chip_id, pin_id, d_type, value):
    print(t_stamp, chip_id, pin_id, d_type, value)
    # print("processData")
    
    
def decodeData(recv):
    try:
        timestamp = recv[1:5]
        chip_id = recv[5:9]
        pin_id = recv[9]
        d_type = recv[10]
        value = recv[11:19]
        lrc = recv[19:23]
        LRCval = calcLRC([int(timestamp, 16), 
                int(chip_id, 16), int(pin_id, 16), 
                int(d_type, 16), int(value, 16)])
        if (LRCval == lrc):
            if (pin_id == 'F' and d_type == 'F' and value == "FFFFFFFF"):
                print(chip_id, "OK")
            else:
                processData(int(timestamp, 16), 
                chip_id, int(pin_id, 16), 
                int(d_type, 16), int(value, 16))
        else:
            print("!!ERR: Incorrect LRC")
    except Exception as e:
        print("!!ERR: decodeData", e)

def commLoop():
    comm = connect(115200)
    if comm:
        while True:
            try:
                if comm.readable():
                    rcv = comm.readline().decode("ascii")
                    if (len(rcv) == 25):
                        if rcv[0] == ':':
                            decodeData(rcv)
                    elif (len(rcv) > 4):
                        if rcv[0] == "!":
                            print(rcv)
            except Exception as e:
                print("!!ERR: commLoop", e)

try:
    commLoop()
except Exception as e:
    print("!!ERR: MAIN", e)