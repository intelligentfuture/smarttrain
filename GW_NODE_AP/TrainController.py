import time
import numpy as np
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(12, 1000)
pwm.start(0)

I = 0
dt = 0.05
error_old = 0

def trainStop():
#    GPIO.output(16, False)
#    GPIO.output(18, False)
    pwm.ChangeDutyCycle(0)

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
    v_avg = x/t + 0.07
    return v_avg

def controller(tk,Tref,x0,v0,t0,duty):
  #  print("train controller working")
    global dt
    # trackLength = 3.736
    N = int(0.5/dt)
    t = t0
    #dts = np.zeros((N-1,1))
    xs = np.zeros((N,1))
    vs = np.zeros((N,1))
    ds = np.zeros((N,1))
    xs[0] = x0
    vs[0] = v0
    ds[0] = duty
    for i in range(N-1):
        #TargetSpd = speedPlanner(trackLength - xs[i], Tref - t)
        ds[i+1] = PID(Tref, vs[i])
        vs[i+1] = estimatedSpeed(ds[i])
        xs[i+1] = xs[i] + vs[i]*dt
        pwm.ChangeDutyCycle(ds[i]*100)
        t = t + dt
        time.sleep(dt - 0.0008) #0.0008 is average calculations time

    return xs[-1],vs[-1],t,ds[-1]

def call_train(trackLength,TargetTime,CurrentPos,CurrentSpd,CurrentTime,duty):

    trainForward()
    dx = trackLength - CurrentPos
    dt1 = TargetTime - CurrentTime
    TargetSpd = speedPlanner(dx, dt1)
    tx = time.time()
    rl = controller(TargetTime,TargetSpd,CurrentPos,CurrentSpd,CurrentTime,duty)
    #print(duty, TargetSpd)
    #print(pwm)
   # time.sleep(1)
    return rl[0][0],rl[1][0],rl[2],rl[3][0]
    #print(TargetSpd)
