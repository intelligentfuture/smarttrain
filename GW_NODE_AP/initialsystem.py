from TrainController import controller,trainForward,trainStop,call_train
import time

def init_system():


#track lenm, target time, cspeed, curposition(from start point), curtime

#     TargetTime = 20
#     RailLength = 3.736
#     x[0] = 0
#     y[0] = 0
    #
    # TargetTime = 7
    # RailLength = 3.736
    # x = 0
    # y = 0
    TargetTime = 15
    RailLength = 3.726
    v = 0  #current speed
    p = 0  #current position
    t = 0  #current time
    d = 0  #duty
    trainForward()
    # while True:
        # #Call_train(raillength,targettime,pos,speed,time,duty)
        # x,y,z,d = call_train(RailLength,TargetTime,p,v,t,d)
        # print(x,y,z,d)
        # if z > TargetTime:
            # trainStop()
            # break
    # time.sleep(5)
    x,y,z,d = call_train(RailLength,TargetTime,0,0,0,d)
    x,y,z,d = call_train(RailLength,TargetTime,0.133,0.224,3.37,d)
    x,y,z,d = call_train(RailLength,TargetTime,0.211,0.562,5.33,d)
    x,y,z,d = call_train(RailLength,TargetTime,0.310,1.212,7.83,d)
    x,y,z,d = call_train(RailLength,TargetTime,0.310,1.851,9.89,d)
    x,y,z,d = call_train(RailLength,TargetTime,0.310,2.156,10.88,d)
    x,y,z,d = call_train(RailLength,TargetTime,0.310,2.385,11.62,d)
    x,y,z,d = call_train(RailLength,TargetTime,0.218,3.071,14.22,d)

if __name__ == "__main__":
    while True:
        init_system()
