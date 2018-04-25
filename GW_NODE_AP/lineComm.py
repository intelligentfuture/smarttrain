import sys
import time
import json
import socket

def listen():
    connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind(('0.0.0.0', 55555))
    while True:
        try:
            while True:
                try:
                    rcv, addr = connection.recvfrom(28)
                    for data in rcv.decode('ascii').split(':'):
                        data = data.replace("\r", "")
                        data = data.replace("\n", "")
                        if data:
                            txt = data.strip()
                            if(len(txt) == 26):
                                decodeData(txt)
                            else:
                                print("!!ERR: RCV", txt, len(txt))
                except Exception as e:
                    print('!!ERR: CONN', e)
                    break
        except Exception as e:
            print('!!ERR: SOCKET', e)
                
def calcLRC(input):
    lrc = 0x0
    for b in input:
        lrc += b
        lrc %= 0xFFFF+1
    return "%04X"%(0xFFFF - lrc)

node_last_seen = dict()
sensor_mem_now = dict()
sensor_mem_past = dict()

node_ocup_time = dict()
node_round_time = dict()

node_list = dict()

def sensorLoopTime(uid):
    try:
        if uid in sensor_mem_now:
            sensor_mem_past[uid] = sensor_mem_now[uid]
        sensor_mem_now[uid] = time.time()
        if uid in sensor_mem_past:
            t_diff = sensor_mem_now[uid] - sensor_mem_past[uid]
            if t_diff > 1: # time difference > 1 s
                return t_diff
            else:
                return 0
        else:
            return 0
    except Exception as e:
        print("!!ERR: sensorTime", e)
        return 0
    
def processData(t_stamp, chip_id, pin_id, d_type, value):
    try:
        uid = str(chip_id)+str(pin_id)
        sens_time = 0
        if d_type == 0 and value == 0:
            sens_time = sensorLoopTime(uid)
            if sens_time > 5: # each loop can't faster than 5 secs
                node_round_time[uid] = (time.time(), sens_time)
                if uid in node_list:
                    node_list[uid] = node_list[uid]+1
                
        elif d_type == 1 and value > 0:
            sens_time = value/1000.0 # in secs
            if sens_time > 0.2: # each occupied time can't faster than 0.2 secs
                node_ocup_time[uid] = (time.time(), sens_time)
                if uid not in node_list:
                    node_list[uid] = 0
        
        # put data into one object
        data_list = []
        if uid in node_list:
            # print("loop_count", node_list[uid])
            if uid in node_ocup_time:
                # print("ocup_time", node_ocup_time[uid])
                if uid in node_round_time:
                    data_list = (
                        time.time(), 
                        node_list[uid], 
                        node_ocup_time[uid], 
                        node_round_time[uid]
                    )

        # do something with data here
        if data_list:
            print(data_list)
        
    except Exception as e:
        print("!!ERR: processData", e)

def decodeData(recv):
    try:
        timestamp = recv[0:8]
        chip_id = recv[8:12]
        pin_id = recv[12]
        d_type = recv[13]
        value = recv[14:23]
        lrc = recv[23:26]
        LRCval = calcLRC([int(timestamp, 16), 
                int(chip_id, 16), int(pin_id, 16), 
                int(d_type, 16), int(value, 16)])
        if (LRCval == lrc):
            if (pin_id == 'F' and d_type == 'F' and value == "FFFFFFFF"):
                node_last_seen[chip_id] = (time.time(), int(timestamp, 16)) # system time, node time
                print(chip_id, node_last_seen[chip_id])
            else:
                processData(int(timestamp, 16), 
                chip_id, int(pin_id, 16), 
                int(d_type, 16), int(value, 16))
        else:
            print("!!ERR: Incorrect LRC")
    except Exception as e:
        print("!!ERR: decodeData", e)

if __name__ == "__main__":
    try:
        listen()
    except Exception as e:
        print("!!ERR: MAIN", e)
    except KeyboardInterrupt:
        print("\r\nExit...OK")
        sys.exit(0)
