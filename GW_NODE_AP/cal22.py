import sys
import time
import socketserver

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
            print(data_list)
            define_order(data_list)

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




#conan's part
node_list = dict()
sensors_list = list()
distab = dict()
distdest = dict()
ab_order = list()
ta = 0
tb = 0
tdiff = 0
pa = ''
pb = ''
sum_dist = 0
speed = 0
LENRM = 3736
LENT =  480


def define_order(line):
    print("LINE=",line)
    global pa
    global pb
    global ta
    global tb
    global sum_dist
    global speed
    global distab
    global distdest,ab_order
    global sensors_list
    ddist = 0
    tdiff = 0

    try:

        data_type = line[0]
        uid = line[1]
        dtime = line[2]
        if data_type == 1:
            ddtime = line[3][1]
        elif data_type == 0:
            ddtime = line[4][1]

#print(data_type,uid,dtime,ddtime)

        if data_type == 0:
            pa = pb
            pb = uid
            tb = float(dtime)
            tdiff = tb-ta
#            print("tdiff=",tdiff)
            if tdiff < 0.0001 or tdiff == 0 :
                return
            ta = tb
            # if len(line) == 6:
            # print(line[2],line[5])
            # speed = 48/line[6]
            if uid not in sensors_list:
                sensors_list.append(uid)
#                print("add",uid);
#        print(len(sensors_list))
        sensors_text = ""
        for sr in sensors_list:
            sensors_text+=sr+' '

        if data_type == 1:
            speed = LENT/float(ddtime)
 #           print("speed",speed)
                # else:
                #     speed = 0

        if data_type == 0:
            ddist = tdiff*speed
            if ddist<1:
                return
            sum_dist+=ddist

        tag = "%s-%s"%(pa,pb)

        if tag in distab:
            print(tag,ddist)
            dd = distab[tag]
            if dd > 0:
                dd = (dd+ddist)/2
            else:
                dd = ddist

            distab[tag]=dd

        else:
            distab[tag]=ddist

        if pb in distdest:
            dds = distdest[pb]
            dds = (dds+sum_dist)/2
            distdest[pb]=dds
        else:
            distdest[pb] = sum_dist

        print(len(sensors_list),data_type,uid,"|",pa,pb,"|tdiff=","%01.06f"%tdiff,"|v=","%03.06f"%speed,"|s=","%03.06f"%(ddist),"|ss=","%04.04f"%sum_dist,end='\r')
        print(sensors_text)

#        send_speed(uid,speed)
        if sum_dist>LENRM:
            sum_dist = 0
            # print(data_type,uid,speed,end='\r')
        sensors_text = ""

    except Exception as e:
        print(e)














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
