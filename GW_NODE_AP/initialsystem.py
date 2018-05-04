#!/usr/bin/python3
from TrainController import controller,trainForward,trainStop,call_train
import time

def generatebytime():
    LENRM = 3.736 #mm
    LENT = 0.480  #mm
    SPEED_MAX = 0.630 # mmps  --> 0.593 mps

    timetable = list()
    stime = 20

    SPEED_NORM = 0.492*SPEED_MAX
    # print(SPEED_NORM)
    timefora = 5
    timeframe = 0.5
    timeslot = int(timefora/timeframe)
    DIST_A = 1
    DIST_B = 1
    DIST_C = LENRM - DIST_A - DIST_B
    a1 = pow(SPEED_NORM,2)/(2*DIST_A)
    a2 = pow(SPEED_NORM,2)/(2*DIST_B)

    ctime = stime - (2*timefora)

    # print(SPEED_NORM,a1,a2)
    u = 0
    z = 0

    sumdist = 0
    li=[LENRM,stime,0,0,0]

    timetable.append(li)

    for x in range(0,timeslot):
        z=z+timeframe
        v = u+(a1*timeframe)
        s = u*timeframe + 0.5*a1*timeframe*timeframe
        sumdist=sumdist + s

    #    print("1",z,"%.4f"%u,"%.4f"%v,sumdist)

        li=[LENRM,stime,u,sumdist,z]
        timetable.append(li)
        u = v


    dist_remain = LENRM - (sumdist*2)

    c = dist_remain/ctime
    for x in range(0,ctime*2):
        z=z+timeframe
        s = v*timeframe
        sumdist=sumdist + s
    #    print("2",z,"%.4f"%u,"%.4f"%v,sumdist)
        li=[LENRM,stime,u,sumdist,z]
        timetable.append(li)


    for x in range(0,timeslot):
        z=z+timeframe
        v = u+(-a1*timeframe)
        s = u*timeframe + 0.5*a1*timeframe*timeframe
        sumdist=sumdist + s

    #    print("3",z,"%.4f"%u,"%.4f"%v,sumdist)
        li=[LENRM,stime,u,sumdist,z]
        timetable.append(li)
        u = v

    #print(timetable)
    return timetable

def init_system(): #track length, target time, cur speed, cur position(from start point), cur time
    TargetTime = 15
    RailLength = 3.726
    v = 0  #current speed
    p = 0  #current position
    t = 0  #current time
    d = 0  #duty
    trainForward()
    # Call_train(rail length,target time,position,speed,time,duty)
    # while True:
        # p,v,t,d = call_train(RailLength,TargetTime,p,v,t,d)
        # print(p,v,t,d)
        # if t > TargetTime:
            # trainStop()
            # break
    # time.sleep(5)
    tbl = generatebytime()
    for elm in tbl:
        p,v,t,d = call_train(elm[0],elm[1],elm[3],elm[2],elm[4],d)
        print(p,v,t,d)
    trainStop()

if __name__ == "__main__":
    while True:
        init_system()
