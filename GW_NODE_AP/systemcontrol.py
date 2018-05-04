import sys
import time
import socketserver

from cal22 import define_order

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

ttt = time.time()
tmark = -1

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
    global tmark
    try:
        uid = str(chip_id)+str(pin_id)
        sens_time = 0
        apch = time.time()
        data_list = []
        if d_type == 0 and value == 0:
            sens_time = sensorLoopTime(uid)
            if sens_time > 5: # each loop can't faster than 5 secs
                node_round_time[uid] = (apch, sens_time)
                if uid in node_list:
                    node_list[uid] = node_list[uid]+1
                    data_list = (
                        d_type,
                        uid,
                        apch,
                        node_list[uid],
                        node_round_time[uid]
                    )

        elif d_type == 1 and value > 0:
            sens_time = value/1000.0 # in secs
            if sens_time > 0.2: # each occupied time can't faster than 0.2 secs
                node_ocup_time[uid] = (apch, sens_time)
                if uid not in node_list:
                    node_list[uid] = 0
                data_list = (
                        d_type,
                        uid,
                        apch,
                        node_ocup_time[uid]
                    )

        # do something with data here
        if data_list:
            # print(data_list)
            if tmark ==-1:
                tmark = time.time()
            define_order(data_list,time.time())

    except Exception as e:
        print("!!ERR: processData", e)

def decodeData(recv):
    try:
        timestamp = recv[0:8]
        chip_id = recv[8:12]
        pin_id = recv[12]
        d_type = recv[13]
        value = recv[14:22]
        lrc = recv[22:26]
        LRCval = calcLRC([int(timestamp, 16),
                int(chip_id, 16), int(pin_id, 16),
                int(d_type, 16), int(value, 16)])
        #print(recv, recv[0:8], recv[8:12], recv[12], recv[13], recv[14:22], recv[22:26])
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

class nodeUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        rcv = self.request[0]
        socket = self.request[1]
        try:
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

if __name__ == "__main__":
    try:
        server = socketserver.UDPServer(('0.0.0.0', 55555), nodeUDPHandler)
        server.serve_forever()
    except Exception as e:
        print("!!ERR: MAIN", e)
    except KeyboardInterrupt:
        try:
            server.shutdown()
        except Exception as e:
            print("\r\nExit...Error:", e)
        else:
            print("\r\nExit...OK")
        sys.exit(0)
