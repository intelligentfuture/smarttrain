import serial
import time

port = '/dev/ttyS14'

def connect(b_rate):
    try:
        return serial.Serial(port, b_rate, timeout=10)
    except Exception as e:
        print("!!ERR:", e)

def calcLRC(input):
    input=input.decode('hex')
    lrc = 0
    i = 0
    message = bytearray(input)
    for b in message:
        if(i == 0):
            pass
        else:
            lrc ^= b
        i+=1;
    return lrc

def processData(t_stamp, chip_id, pin_id, d_type, value):

    
    
def decodeData(recv):
    try:
        timestamp = recv[1:5]
        chip_id = recv[5:9]
        pin_id = recv[9]
        d_type = recv[10]
        value = recv[11:19]
        lrc = recv[19:23]
        if calcLRC(recv[1:19]) == int(lrc, 16):
            if (pin_id == 'F' and d_type == 'F' and value == "FFFFFFFF"):
            
            else:
                processData(int(timestamp, 16), 
                int(chip_id, 16), int(pin_id, 16), 
                int(d_type, 16), int(value, 16))
        else:
            print("!!ERR: Incorrect LRC")
    except Exception as e:
        print("!!ERR:", e)

def commLoop():
    comm = connect(115200)
    if comm:
        while True:
            try:
                if comm.readable():
                    rcv = comm.readline().decode("ascii");
                    if (len(rcv) == 25):
                        if rcv[0] == ':':
                            decodeData(rcv)
                    else:
                        if rcv[0:2] == "!!":
                            if rcv.startswith("!!JOIN:"):
                                print(rcv)
                            else if(rcv.startswith("!!ERR:"))
                                print(rcv)
            except Exception as e:
                print("!!ERR:", e)
