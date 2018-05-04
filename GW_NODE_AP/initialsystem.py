#!/usr/bin/python3
from TrainController import controller,trainForward,trainStop,call_train
import time

def init_system(): #track length, target time, cur speed, cur position(from start point), cur time
    TargetTime = 15
    RailLength = 3.726
    v = 0  #current speed
    p = 0  #current position
    t = 0  #current time
    d = 0  #duty
    trainForward()
    while True:
        #Call_train(rail length,target time,position,speed,time,duty)
        p,v,t,d = call_train(RailLength,TargetTime,p,v,t,d)
        print(p,v,t,d)
        if t > TargetTime:
            trainStop()
            break
    time.sleep(5)

if __name__ == "__main__":
    while True:
        init_system()
