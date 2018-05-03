from TrainController import controller
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import json


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
    # print("LINE=",line)
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

            if tdiff < 0.0001 or tdiff == 0 :
                return
            ta = tb

        if data_type == 1:
            if uid not in sensors_list:
                sensors_list.append(uid)

        sensors_text = ""
        for sr in sensors_list:
            sensors_text+=sr+' '

        if data_type == 1:
            speed = LENT/float(ddtime)


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
#        controller(Tref,x0,v0,t0)
# tref=time for loop, x0 = current position, v0 = current speed, t0 = current time
        print(uid,speed)
        send_speed(uid,speed)
        if sum_dist>LENRM:
            sum_dist = 0
            # print(data_type,uid,speed,end='\r')
        sensors_text = ""
        distcount = 0
        for x in range(0,len(sensors_list)-1):
            aabb = "%s-%s"%(sensors_list[x],sensors_list[x+1])
            distcount=distcount+distab[aabb]
            print(aabb,distab[aabb],distcount)

    except Exception as e:
        print(e)


def send_speed(point,speed):
    resp = dict()

    print(point,speed)
    url = 'http://200ok.in.th:7654/api/set-current-speed?point=%s&speed=%.2f'%(point,speed)
    request = Request(url)
    resp['status'] = 'ERROR'
    try:
        with urlopen(request) as response:
            repy = json.loads(response.read().decode('utf-8'))
            resp['status'] = 'OK'
    except Exception as e:
        print(e)
