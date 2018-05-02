from TrainController import controller,trainForward,trainStop,call_train
import time

def init_system():

    call_train(7.5,25,0,0,0)
    time.sleep(5)
    call_train(7.525,0,0,0)


if __name__ == "__main__":
    init_system()
