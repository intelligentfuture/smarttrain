from TrainController import controller,trainForward,trainStop,call_train
import time

def init_system():



# 1 3.37 BFC95 BFC96 224.5771 3747.9522 0.0000 133.3564 3.3681
# 1 5.33 BFC96 BFC94 338.1414 3523.3751 133.3564 211.0943 1.9634
# 1 7.83 BFC94 BFC93 650.5289 3185.2337 211.0943 309.9600 2.4970
# 2 9.89 BFC93 010D6 639.547 2534.7048 309.9600 309.9600 2.0633
# 2 10.88 010D6 010D5 305.1626 1895.1578 309.9600 309.9600 0.9845
# 2 11.62 010D5 010D4 229.5498 1589.9952 309.9600 309.9600 0.7406
# 3 14.22 010D4 010D3 686.6537 1360.4454 309.9600 218.1363 2.6005
# 3 20.40 010D3 BFC95 673.7917 673.7917 218.1363 0.0000 6.1777
# 0 stop for 5 sec. at station 1

#call_train(Distant,TargetTime,CurrentPos,CurrentSpd,CurrentTime)
    call_train(0.224,3.37,0,0,0)
    call_train(0.338,1.96,0,0.133,3.37)
    call_train(0.650,2.5,0,0,0.211,5.33)
    call_train(0.639,2,0,0.310,0,7.83)
    call_train(0.305,0.98,0,0.310,9.89)
    call_train(0.229,0.74,0,0.310,10.88)
    call_train(0.686,2.6,0,0.310,11.62)
    call_train(0.673,6.17,0,0.218,14.22)
    # time.sleep(5)
    call_train(12,40,0,0,0)


if __name__ == "__main__":
    init_system()
