from TrainController import controller,trainForward,trainStop
import time

def init_system():

    trainStop()
    trainForward()
    controller(20,0,0,0)
#    trainStop()
#    time.sleep(5)
#    trainForward()
#    controller(20,0,0,0)
#    trainStop()




if __name__ == "__main__":
    init_system()
