import sys
import time
import json
import math
import re

from time import sleep

LENRM = 3736 #mm
LENT = 480  #mm
SPEED_MAX = 630 # mmps  --> 0.593 mps
NUM_OF_SENSORS = 24
SPEED_NORM_RATIO = 0.492 #12=0.492
SPEED_NORM = SPEED_NORM_RATIO*SPEED_MAX # --> 296.5 mmps
#with a = 0, use t = LENR/SPEED_NORM for 1 round (12.06 s)
# -->
NUM_OF_STATION = 0

RANGE_FOR_A = 1000


SA = 4
SB = 6

#time table parameters

TIME_ALL = 5 #min
STATIONS = 12
TIME_WAIT = 5 #sec

DURATION = TIME_ALL*60

sensors = list()
sensors_list = list()
sensors_name = list()
distab = dict()
distdest = dict()
ab_order = list()

duration = 0
station = 0

a1 = 0
a2 = 0

tm1 = 0
tm2 = 0

DIST_A = 0
DIST_B = 0


def predefine():
    DURATION = TIME_ALL*60 #sec
    # RANGE_A = 0.1*LENR
    # a = pow(SPEED_NORM,2)/(2*RANGE_A)
    # t_m = math.sqrt(RANGE_A/(0.5*a))
    # duration = TIME_ALL*60 #sec
    # tpr = 2*t_m+((LENR-2*RANGE_A)/SPEED_NORM)
    # num_of_round  = round((SPEED_NORM*(duration-2*t_m)+(2*RANGE_A))/LENR) #source and destination, no any stations on the trip
    # station_max = duration/tpr
    #
    # AVG_DIST = LENR/NUM_OF_SENSORS


def read_config():
        with open("sensors.list","r") as f:
            for line in f:
                line = line.strip()
                sensors_list.append(line)
                # print(line)

        with open("distab.list","r") as f:
            for line in f:
                line = line.strip()

                lns = line.split("\t")
                key = lns[0].strip()
                val = lns[1].strip()
                # print(key,val)
                distab[key]=float(val)
                ab_order.append(key)




def define_sensor():
    predefine()
    # read_init()
    read_config()
    # print(">> ",duration,a,t_m,num_of_round,tpr,station_max)


    ratio =  SPEED_NORM_RATIO
    efficiency = -1
    efficiency = calculate_speedtable(ratio)
    rat = 1000
    if abs(efficiency) > 0.05:
        while True:
            if NUM_OF_STATION < STATIONS: #too slow
                ratio = ratio+1/rat
                # print(NUM_OF_STATION,efficiency)

            elif NUM_OF_STATION > STATIONS: #too fast
                ratio = ratio-1/rat

            elif efficiency < 0:
                ratio = ratio+1/rat
            elif efficiency > 0:
                ratio = ratio-1/rat
            else:
                ratio = ratio+1/rat



            efficiency = calculate_speedtable(ratio)
            print("[efficiency]",efficiency,-0.01,efficiency<-0.01)

            if abs(efficiency)<0.01:
                if NUM_OF_STATION==STATIONS:
                    break



def calculate_speedtable(ratio):
    print("ratio =",ratio)
    SPEED_NORM = ratio*SPEED_MAX # --> 296.5 mmps

    global NUM_OF_STATION
    LENR  = 0
    DIST_B = 0
    DIST_A = 0
    for d in ab_order:
        LENR = LENR+distab[d]
        DIST_B = distab[d]


    ddb = LENR
    dda = 0
    pntx = -1
    pnty = len(sensors_list)-1

    pcount=1



    lprev = 0
    for d in ab_order:
        # print(d,distab[d],dda,lprev,LENR-dda)

        if dda < RANGE_FOR_A:
            DIST_A = dda+distab[d]
            pntx = pcount
        if LENR-dda < RANGE_FOR_A:
            DIST_B = LENR-dda+lprev
            pnty = pcount-2
            break
        dda=dda+distab[d]
        pcount=pcount+1
        lprev = distab[d]

    # print(pntx,pnty)
    print("DISTA =","%.2f"%DIST_A,"DISTB =","%.2f"%DIST_B,"LENRM =",LENRM,"LENRX=","%.2f"%(LENR),"","%ERR =",abs(LENR-LENRM)*100/LENRM)

    a1 = pow(SPEED_NORM,2)/(2*DIST_A)
    a2 = pow(SPEED_NORM,2)/(2*DIST_B)

    acount = 0
    u = 0

    sumdista = 0
    sumdistb = DIST_B
    tprev = 0

    tprev2 = SPEED_NORM/a2

    distanttostation = LENR
    sum_t = 0

    uspeed = 0
    for d in ab_order:
        if acount < pntx:
            sumdista=sumdista+distab[d]
            v = math.sqrt(2*a1*(sumdista))
            temp = (v-u)/a1  #t from full partt
            t = temp-tprev
            tprev = temp
            sum_t = sum_t+t
            print("1","%03.4f"%(sum_t),d,"%3.4f"%(distab[d]),"%3.4f"%(distanttostation),"%3.4f"%(uspeed),"%3.4f"%(v),"%2.4f"%(t))

        elif acount >=pnty :
            sumdistb=sumdistb-distab[d]
            if sumdistb < 0:
                sumdistb = 0
            # print(sumdistb)
            v = math.sqrt(2*a2*(sumdistb))
            temp = v/a2
            t = tprev2-temp
            tprev2 = temp
            sum_t = sum_t+t
            print("3","%03.4f"%(sum_t),d,"%3.4f"%(distab[d]),"%3.4f"%(distanttostation),"%3.4f"%(uspeed),"%3.4f"%(v),"%2.4f"%(t))


        else :
            t = distab[d]/v
            sum_t = sum_t+t
            print("2","%03.4f"%(sum_t),d,"%3.4f"%(distab[d]),"%3.4f"%(distanttostation),"%3.4f"%(uspeed),"%3.4f"%(v),"%2.4f"%(t))

        distanttostation = distanttostation - distab[d]
        acount=acount+1
        uspeed = v

    print()
    tm1 = math.sqrt(DIST_A/(0.5*a1))
    tm2 = math.sqrt(DIST_B/(0.5*a2))

    time_for_station = sum_t + TIME_WAIT


    NUM_OF_STATION = round(DURATION/time_for_station)

    sumtime = (NUM_OF_STATION*time_for_station)-TIME_WAIT
    efficiency = (sumtime-DURATION)/DURATION

    print("TIME_FOR_TRIP =",DURATION)
    print("EXPECTED STATION =",STATIONS)
    print("TIME_AT_STATION =",TIME_WAIT)
    print("TIME_TO_STATION =",sum_t,)
    print("TIME_FOR_STATION =",time_for_station)
    print("NUM_OF_STATION =",NUM_OF_STATION)
    print("TOTAL_TIME =",sumtime)
    # print("TOTAL_TIME+1 =",sumtime+time_for_station)
    print("EFFICIENCY =",efficiency)


    print(SPEED_NORM,DIST_A,a1,tm1,"|",DIST_B,a2,tm2)
    print(SPEED_NORM,DIST_A,"|",DIST_B,"|",LENR)
    return efficiency


def read_init():
    ta = 0
    tb = 0
    tdiff = 0
    pa = ''
    pb = ''
    sum_dist = 0
    speed = 0
    with open("run1.log","r") as f:
        for line in f:
            sleep(0.01)
            line = line.strip()

            try:
                line = line.replace("(","")
                line = line.replace(")","")
                line = line.replace("'","")
                line = line.replace(",","")

                line = line.split()
                data_type = line[0]
                uid = line[1]
                dtime = line[2]

                if data_type == '0':
                    pa = pb
                    pb = uid
                    tb = float(dtime)
                    tdiff = tb-ta
                    #print(tdiff)
                    if tdiff < 0.01 :
                        continue
                    ta = tb
                # if len(line) == 6:
                    # print(line[2],line[5])
                    # speed = 48/line[6]
                if uid not in sensors_list:
                    sensors_list.append(uid)

                sensors_text = ""
                for sr in sensors_list:
                    sensors_text+=sr+' '

                if data_type == '1':
                    speed = LENT/float(line[4])
                # else:
                #     speed = 0

                if data_type == '0':
                    ddist = tdiff*speed
                    if ddist<1:
                        continue
                    sum_dist+=ddist

                    tag = "%s-%s"%(pa,pb)
                    if tag in distab:
                        # print(tag,ddist)
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

                    print(len(sensors_list),data_type,uid,"|",pa,pb,"|","%1.6f"%tdiff,"|v=","%3.6f"%speed,"|s=","%3.6f"%(ddist),"|ss=","%04.4f"%sum_dist,"|",sensors_text,end='\r\n')
                    if sum_dist>LENRM:
                        sum_dist = 0
                # print(data_type,uid,speed,end='\r')
                sensors_text = ""

            except Exception as e:
                print(e)

    for dd in range(0,len(sensors_list)-1):
        aa = sensors_list[dd]
        bb = sensors_list[dd+1]
        ab = "%s-%s"%(aa,bb)
        # print(ab)
        ab_order.append(ab)
    ab = "%s-%s"%(sensors_list[len(sensors_list)-1],sensors_list[0])
    # print(ab)
    ab_order.append(ab)

    fwsensors = open("sensors.list","w")
    for d in sensors_list:
        print(">",d)
        fwsensors.write("%s\n"%(d))
    fwsensors.close()

    fwdistab = open("distab.list","w")
    for d in ab_order:
        dab = distab[d]
        print(d,"%.4f"%(dab))
        ab = "%s\t%.4f\n"%(d,distab[d])
        fwdistab.write(ab)
    fwdistab.close()

define_sensor()
