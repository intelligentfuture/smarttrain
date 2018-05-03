from TrainController import controller,trainForward,trainStop,call_train
import time

def init_system():


#track lenm, target time, cspeed, curposition(from start point), curtime
    TargetTime = 7
    RailLength = 3.736
    x = 0
    y = 0
    z = 0
    d = 0
    trainForward()
    while True:
        x,y,z,d = call_train(RailLength,TargetTime,x,y,z,d)
        print(x,y,z,d)
        if z > TargetTime:
            trainStop()
            break
    #call_train(3.736,60,0.1,0,0)

    time.sleep(5)


if __name__ == "__main__":

    while True:

        init_system()
