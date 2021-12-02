import RPi.GPIO as gp
import time
from time import sleep
import sys
import os

gp.setmode(gp.BCM)

# Debugging Log
# /full/path/to/log.ex
logfile = "log.txt"
if not os.path.exists(logfile):
    os.mknod(logfile)
lognow = open(logfile, "a")  # append mode
def debug_log(message):
    lognow.write(message)


pwm_mode_bool = 0 # zero or one, off or on

servo_range_of_motion = 180 # normally 90, 180, or 360 degrees

#----------------------------------------------------------------------------------------------------
#                                       Pins
#----------------------------------------------------------------------------------------------------

# Ultrasonic Sensor Pins
# BOARD - 7,11,13,15,16,22
# BCM
u1t = 4
u1e = 17
u2t = 27
u2e = 22
u3t = 23
u3e = 25

# Motor Pins
# BOARD - 12,32,33,35
# BCM
m1 = 18
m2 = 12
m3 = 13
m4 = 19


# Servo Pin
# BOARD - 29
# BCM
serv1 = 5

# Ultrasonic Sensor Pinmodes
gp.setup(u1t, gp.OUT)
gp.setup(u1e, gp.IN)
gp.setup(u2t, gp.OUT)
gp.setup(u2e, gp.IN)
gp.setup(u3t, gp.OUT)
gp.setup(u3e, gp.IN)

# Set Motor Pinmodes
gp.setup(m1, gp.OUT)
gp.setup(m2, gp.OUT)
gp.setup(m3, gp.OUT)
gp.setup(m4, gp.OUT)
# PWM Only takes effect if pwm is set to 1
motor_freq = 100
pwm1 = gp.PWM(m1,motor_freq)  
pwm2 = gp.PWM(m2,motor_freq)
pwm3 = gp.PWM(m3,motor_freq)  
pwm4 = gp.PWM(m4,motor_freq)

# Set Servo Pinmode
gp.setup(serv1, gp.OUT)
servo_freq = 50
pwmS = gp.PWM(serv1,servo_freq)

#----------------------------------------------------------------------------------------------------
#                                       Distance Function
#----------------------------------------------------------------------------------------------------
 
def distance(tg, eh):
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
    debug_log(dirforw)
    debug_log("Voltage - | HIGH | LOW | HIGH | LOW |")

def bakw():
    gp.output(m1,gp.LOW)
    gp.output(m2,gp.HIGH)
    gp.output(m3,gp.LOW)
    gp.output(m4,gp.HIGH)
    debug_log(dirforw)
    debug_log("Voltage - | LOW | HIGH | LOW | HIGH |")

def lefw():
    gp.output(m1,gp.LOW)
    gp.output(m2,gp.HIGH)
    gp.output(m3,gp.HIGH)
    gp.output(m4,gp.LOW)
    debug_log(dirlefw)
    debug_log("Voltage - | LOW | HIGH | HIGH | LOW |")

def rihw():
    gp.output(m1,gp.HIGH)
    gp.output(m2,gp.LOW)
    gp.output(m3,gp.LOW)
    gp.output(m4,gp.HIGH)
    debug_log(dirrihw)
    debug_log("Voltage - | HIGH | LOW | LOW | HIGH |")

def stopw():
    gp.output(m1,gp.LOW)
    gp.output(m2,gp.LOW)
    gp.output(m3,gp.LOW)
    gp.output(m4,gp.LOW)
    debug_log(dirstop)
    debug_log("Voltage - | LOW | LOW | LOW | LOW |")

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
    debug_log("PWM - "," | ",val1," | ",val2," | ",val3," | ",val4," |")
    pwm1.ChangeDutyCycle(val1)
    pwm2.ChangeDutyCycle(val2)
    pwm1.ChangeDutyCycle(val3)
    pwm2.ChangeDutyCycle(val4)

#----------------------------------------------------------------------------------------------------
#                                       Servo Function
#----------------------------------------------------------------------------------------------------

# Scan with Servo

def servo_scan():
    stopw()

    av1r = []
    av2r = []
    av3r = []
# sweep forwards
    move1 = (servo_range_of_motion / 3)
    move2 = (servo_range_of_motion / 3) * 2
    move3 = servo_range_of_motion
    for i in (0,move1):
        # sweep servo
        dist1 = distance(u1t, u1e)
        dist2 = distance(u2t, u2e)
        dist3 = distance(u3t, u3e)
        # average the distances
        a1 = (dist1 + dist2 + dist3) / 3
        av1r.append(a1)
    for i in (move1,move2):
        # sweep servo
        dist1 = distance(u1t, u1e)
        dist2 = distance(u2t, u2e)
        dist3 = distance(u3t, u3e)
        # average the distances
        a2 = (dist1 + dist2 + dist3) / 3
        av2r.append(a2)
    for i in (move2,move3):
        # sweep servo
        dist1 = distance(u1t, u1e)
        dist2 = distance(u2t, u2e)
        dist3 = distance(u3t, u3e)
        # average the distances
        a3 = (dist1 + dist2 + dist3) / 3
        av3r.append(a3)

    # Average the ranges of averages
    av1 = float(sum(av1r))/len(av1r)
    av2 = float(sum(av2r))/len(av2r)
    av3 = float(sum(av3r))/len(av3r)

    # If quadrant1 (left) is closer
    if av1 > max(av2, av3):
        rihw()
    # If quadrant2 (middle) is closer
    elif av2 > max(av1, av3): 
        bakw()
    # If quadrant1 (right) is closer
    elif av3 > max(av1, av2):
        lefw()

# sweep backwards

    for i in (servo_range_of_motion,0):
        # sweep servo
        print("sweep servo")

#----------------------------------------------------------------------------------------------------
#                                       Sensor -> Logic Functions
#----------------------------------------------------------------------------------------------------

# If less than 10cm, and if one rear sensor is closer than the other

def dir_opt_pwm(dist1, dist2, dist3):
    if dist1 <= 10:
        servo_scan()
    else:
        forw()

    if dist2 <= 10 or dist3 <= 10:
        if dist2 < dist3:
            rihw()
        elif dist3 < dist2:
            lefw()
        else:
            forw()
    val1, val2, val3, val4 = 255
    drive_pwm(val1, val2, val3, val4)

# If less than 10, and if one rear sensor is closer than the other

def dir_opt_normal(dist1, dist2, dist3):
    if dist1 <= 10:
        servo_scan()

    if dist2 <= 10 or dist3 <= 10:
        if dist2 < dist3:
            rihw()
        elif dist3 < dist2:
            lefw()
        else:
            forw()


def normal_run(): 
    
    while True:

        dist1 = distance(u1t, u1e)
        dist2 = distance(u2t, u2e)
        dist3 = distance(u3t, u3e)

        dir_opt_normal(dist1, dist2, dist3)

def pwm_run(): 
    dc = 0
    pwm1.start(dc)
    pwm2.start(dc)
    pwm3.start(dc)
    pwm4.start(dc)

    while True:

        dist1 = distance(u1t, u1e)
        dist2 = distance(u2t, u2e)
        dist3 = distance(u3t, u3e)

        dir_opt_pwm(dist1, dist2, dist3)

#----------------------------------------------------------------------------------------------------
#                                       Main Functions
#----------------------------------------------------------------------------------------------------

def main():
    # Start off moving forward regardless
    try:
        if pwm_mode_bool==0:
            print("Running in Normal mode")
            forw()
            normal_run()
        elif pwm_mode_bool==1:
            print("Running in PWM mode")
            forw()
            pwm_run()
        else:
            print("pwm_mode_bool not set to zero or one...")
            sys.exit()
            lognow.close()
            gp.cleanup()
    except KeyboardInterrupt:
        stopw()
        lognow.close()
        gp.cleanup()
        print("Robot Stopped")

main()