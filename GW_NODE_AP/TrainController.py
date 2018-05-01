import time
import numpy as np
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(12, 1000)
duty = 0
pwm.start(duty)

I = 0
dt = 0.05
error_old = 0

def trainStop():
    GPIO.output(16, False)
    GPIO.output(18, False)
    pwm.stop()

def trainForward():
    GPIO.output(16, False)
    GPIO.output(18, True)

def trainBackward():
    GPIO.output(16, True)
    GPIO.output(18, False)

def estimatedSpeed(duty):
#    print("estimate")
    a4 = 2.9289
    a3 = -7.2071
    a2 = 5.8578
    a1 = -1.078
    a0 = 0.1045

    if(duty > 1.0):
        duty = 1.0
    if(duty > 0.2):
        return np.polyval([a4,a3,a2,a1,a0],duty)
    else:
        return 0

def PID(ref, speed):
 #   print("pid")
    Kp = 0.1
    Ki = 5.0

    global dt
    global I
    global error_old

    error = ref - speed

    P = error
    I = I + error*dt

    error_old = error
    if(Kp*P + Ki*I >= 1):
        return 1.0
    elif(Kp*P + Ki*I >= 0):
        return Kp*P + Ki*I
    else:
        return 0

def speedPlanner(x, t):
   # print("speed planner")
    v_avg = x/t
    return v_avg + 0.2

def controller(Tref,x0,v0,t0):
  #  print("train controller working")
    global dt
    trackLength = 3.736
    N = int((Tref-t0)/dt)
    t = t0
    dts = np.zeros((N-1,1))
    xs = np.zeros((N,1))
    vs = np.zeros((N,1))
    ds = np.zeros((N,1))
    xs[0] = x0
    vs[0] = v0
    for i in range(N-1):
        TargetSpd = speedPlanner(trackLength - xs[i], Tref - t)
        ds[i+1] = PID(TargetSpd, vs[i])
        vs[i+1] = estimatedSpeed(ds[i])
        xs[i+1] = xs[i] + vs[i]*dt
        duty = ds[i]
        pwm.ChangeDutyCycle(duty*100)
        t = t + dt
        time.sleep(dt - 0.0008) #0.0008 is average calculations time

    return xs[-1]


def call_train(TargetTime,CurrentPos,CurrentSpd,CurrentTime):
    trainForward()
    # TargetTime = float(input("Target Time : "))
    # CurrentPos = float(input("Current Position : "))
    # CurrentSpd = float(input("Current Speed : "))
    # CurrentTime = float(input("Current Time : "))
    tx = time.time()
    rl = controller(TargetTime,CurrentPos,CurrentSpd,CurrentTime)
    print(time.time() - tx, rl)
    print(time.time() - tx)
