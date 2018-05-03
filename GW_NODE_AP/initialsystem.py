from TrainController import controller,trainForward,trainStop,call_train
import time

def init_system():


#track lenm, target time, cspeed, curposition(from start point), curtime
    TargetTime = 60
    x[0] = 0
    y[0] = 0
    z = 0
    while True:
        x,y,z = call_train(3.736,60,x[0],y[0],z)
        if z > 60:
            break
    #call_train(3.736,60,0.1,0,0)

    time.sleep(5)


if __name__ == "__main__":

    while True:

        init_system()
