from TrainController import controller,trainForward,trainStop,call_train
import time

def init_system():


#track lenm, target time, cspeed, curposition(from start point), curtime

    TargetTime = 15
    RailLength = 3.736
    x = 0
    y = 0
    z = 0
    d = 0

    trainForward()

#    x,y,z,d = call_train(RailLength,TargetTime,x,y,z,0.5)

    while True:
        x,y,z,d = call_train(RailLength,TargetTime,x,y,z,d)
        #Call_train(raillength,targettime,pos,speed,time,duty)
        print(x,y,z,d)
        if z > TargetTime:
            trainStop()
            break
    time.sleep(5)


#    d = 0.38
#    call_train(RailLength,TargetTime,0,0,0,d)
#    call_train(RailLength,TargetTime,0.133,0.224,3.37,d)
#    call_train(RailLength,TargetTime,0.211,0.562,5.33,d)
#    call_train(RailLength,TargetTime,0.310,1.212,7.83,d)
#    call_train(RailLength,TargetTime,0.310,1.851,9.89,d)
#    call_train(RailLength,TargetTime,0.310,2.156,10.88,d)
#    call_train(RailLength,TargetTime,0.310,2.385,11.62,d)
#    call_train(RailLength,TargetTime,0.218,3.071,14.22,d)
    # x,y,z = call_train(RailLength,TargetTime,x,y,z)


    # call_train(RailLength,TargetTime,0,0,0)
    # call_train(RailLength,TargetTime,0.133,0.224,3.37)
    # call_train(RailLength,TargetTime,0.211,0.562,5.33)
    # call_train(RailLength,TargetTime,0.310,1.212,7.83)
    # call_train(RailLength,TargetTime,0.310,1.851,9.89)
    # call_train(RailLength,TargetTime,0.310,2.156,10.88)
    # call_train(RailLength,TargetTime,0.310,2.385,11.62)
    # call_train(RailLength,TargetTime,0.218,3.071,14.22)

    # call_train(0.224,3.37,0,0,0)
    # call_train(0.338,1.96,0,0.133,3.37)
    # call_train(0.650,2.5,0,0,0.211,5.33)
    # call_train(0.639,2,0,0.310,0,7.83)
    # call_train(0.305,0.98,0,0.310,9.89)
    # call_train(0.229,0.74,0,0.310,10.88)
    # call_train(0.686,2.6,0,0.310,11.62)
    # call_train(0.673,6.17,0,0.218,14.22)


    #call_train(3.736,60,0.1,0,0)




if __name__ == "__main__":

    while True:

        init_system()
