import RPi.GPIO as gp
import time
from time import sleep
import sys
import os

#----------------------------------------------------------------------------------------------------
#                                       Config
#----------------------------------------------------------------------------------------------------

gp.setmode(gp.BOARD)

cm_threshold = 10 # Distance From Object to Avoid

#----------------------------------------------------------------------------------------------------
#                                       Pins
#----------------------------------------------------------------------------------------------------
# Shutdown Button
shutdown=23
shutdown_command="sudo shutdown -h now"
gp.setup(shutdown, gp.IN, pull_up_down=gp.PUD_DOWN)

# Ultrasonic Sensor Pins
# BOARD - 7,11,13,15,16,22
# BCM - 4,17,27,22,23,25
# BCM
u1t = 7
u1e = 11
u2t = 13
u2e = 15
u3t = 16
u3e = 22
gp.setup(u1t, gp.OUT)
gp.setup(u1e, gp.IN)
gp.setup(u2t, gp.OUT)
gp.setup(u2e, gp.IN)
gp.setup(u3t, gp.OUT)
gp.setup(u3e, gp.IN)

# Motor Pins
# BOARD - 12,32,33,35
# BCM - 18,12,13,19
# BCM
m1 = 12
m2 = 32
m3 = 33
m4 = 35
gp.setup(m1, gp.OUT)
gp.setup(m2, gp.OUT)
gp.setup(m3, gp.OUT)
gp.setup(m4, gp.OUT)
motor_freq = 500
pwm1 = gp.PWM(m1,motor_freq)  
pwm2 = gp.PWM(m2,motor_freq)
pwm3 = gp.PWM(m3,motor_freq)  
pwm4 = gp.PWM(m4,motor_freq)

#----------------------------------------------------------------------------------------------------
#                                       Distance Function
#----------------------------------------------------------------------------------------------------
 
def get_sens(tg, eh):
    gp.output(tg, True)
    time.sleep(0.00001)
    gp.output(tg, False)
    StartTime = time.time()
    StopTime = time.time()
    while gp.input(eh) == 0:
        StartTime = time.time()
    while gp.input(eh) == 1:
        StopTime = time.time()
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
    return distance

#----------------------------------------------------------------------------------------------------
#                                       Drive Functions
#----------------------------------------------------------------------------------------------------

dirforw="Going Forward..."
dirbakw="Going Backward..."
dirlefw="Turning Left..."
dirrihw="Turning Right..."
dirstop="Robot Stopped"


# these need to be tested for the L298N

# Normal Mode

def forw():
    gp.output(m1,gp.HIGH)
    gp.output(m2,gp.LOW)
    gp.output(m3,gp.HIGH)
    gp.output(m4,gp.LOW)
    print(dirforw)

def bakw():
    gp.output(m1,gp.LOW)
    gp.output(m2,gp.HIGH)
    gp.output(m3,gp.LOW)
    gp.output(m4,gp.HIGH)
    print(dirbakw)

def lefw():
    gp.output(m1,gp.LOW)
    gp.output(m2,gp.HIGH)
    gp.output(m3,gp.HIGH)
    gp.output(m4,gp.LOW)
    print(dirlefw)

def rihw():
    gp.output(m1,gp.HIGH)
    gp.output(m2,gp.LOW)
    gp.output(m3,gp.LOW)
    gp.output(m4,gp.HIGH)
    print(dirrihw)

def stopw():
    gp.output(m1,gp.LOW)
    gp.output(m2,gp.LOW)
    gp.output(m3,gp.LOW)
    gp.output(m4,gp.LOW)
    print(dirstop)

# PWM

def drive_pwm(val1, val2, val3, val4):
    if val1 > 255:
        val1 = 255
    elif val1 < 0:
        val1 = 0
    if val2 > 255:
        val2 = 255
    elif val2 < 0:
        val2 = 0
    if val3 > 255:
        val3 = 255
    elif val3 < 0:
        val3 = 0
    if val4 > 255:
        val4 = 255
    elif val4 < 0:
        val4 = 0
    print("PWM - "," | ",val1," | ",val2," | ",val3," | ",val4," |")
    pwm1.ChangeDutyCycle(val1)
    pwm2.ChangeDutyCycle(val2)
    pwm1.ChangeDutyCycle(val3)
    pwm2.ChangeDutyCycle(val4)


#----------------------------------------------------------------------------------------------------
#                                       Sensor Logic Functions
#----------------------------------------------------------------------------------------------------

# PWM Variant

def dir_opt_pwm(dist1, dist2, dist3):
    if dist1 <= cm_threshold:
        bakw()
    if dist2 <= cm_threshold or dist3 <= cm_threshold:
        if dist2 < dist3:
            rihw()
        elif dist3 < dist2:
            lefw()
        else:
            forw()
    val1, val2, val3, val4 = 255
    drive_pwm(val1, val2, val3, val4)

def pwm_run(): 
    dc = 0
    pwm1.start(dc)
    pwm2.start(dc)
    pwm3.start(dc)
    pwm4.start(dc)
    while True:
        dist1 = get_sens(u1t, u1e)
        dist2 = get_sens(u2t, u2e)
        dist3 = get_sens(u3t, u3e)
        dir_opt_pwm(dist1, dist2, dist3)

#----------------------------------------------------------------------------------------------------
#                                       Main Functions
#----------------------------------------------------------------------------------------------------

try:
    print("Running in PWM mode")
    forw()
    pwm_run()
except KeyboardInterrupt:
    stopw()
    gp.cleanup()
    print("Robot Stopped")
