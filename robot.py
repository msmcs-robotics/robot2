'''
# References So Far

# BOARD vs BCM for GPIO mode setting

https://raspberrypi.stackexchange.com/questions/12966/what-is-the-difference-between-board-and-bcm-for-gpio-pin-numbering

# HC SR04 Ultrasonic Distance Sensor

https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi

https://pimylifeup.com/raspberry-pi-distance-sensor/

# L298N Motor Driver

https://maker.pro/raspberry-pi/tutorial/how-to-control-a-dc-motor-with-an-l298-controller-and-raspberry-pi

https://techatronic.com/raspberry-pi-motor-control/

# Servo

https://tutorials-raspberrypi.com/raspberry-pi-servo-motor-control/

https://embeddedcircuits.com/raspberry-pi/tutorial/controlling-a-servo-motor-with-raspberry-pi-tutorial
'''

'''
Checklist:
'''

import RPi.GPIO as gp
import time
from time import sleep
import sys

gp.setmode(gp.BCM)


logfile = "log.txt"


pwm_mode_bool = 0 # zero or one
servo_range_of_motion = 180

#----------------------------------------------------------------------------------------------------
#                                       Pins
#----------------------------------------------------------------------------------------------------

# Ultrasonic Sensor Pins
# BCM - 4,17,18,27,22,23

u1t = 4
u1e = 17
u2t = 18
u2e = 27
u3t = 22
u3e = 23

# Motor Pins
# BCM - 12,16,20,21 

m1 = 32 
m2 = 36
m3 = 38
m4 = 40

# Servo Pin
# BSM - 24

serv1 = 18

# Ultrasonic Sensor Pinmodes
GPIO.setup(u1t, GPIO.OUT)
GPIO.setup(u1e, GPIO.IN)
GPIO.setup(u2t, GPIO.OUT)
GPIO.setup(u2e, GPIO.IN)
GPIO.setup(u3t, GPIO.OUT)
GPIO.setup(u3e, GPIO.IN)

# Set Motor Pinmodes
gp.setup(m1, gp.OUT)
gp.setup(m2, gp.OUT)
gp.setup(m3, gp.OUT)
gp.setup(m4, gp.OUT)

# Set Servo Pinmode
gp.setup(servoPIN, gp.OUT)

#----------------------------------------------------------------------------------------------------
#                                       Distance Function
#----------------------------------------------------------------------------------------------------
 
def distance(tg, eh):
    GPIO.output(tg, True)
    time.sleep(0.00001)
    GPIO.output(tg, False)
    StartTime = time.time()
    StopTime = time.time()
    while GPIO.input(eh) == 0:
        StartTime = time.time()
    while GPIO.input(eh) == 1:
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

# PWM

def drive_pwm(val1, val2, val3, val4):
    pwm1.ChangeDutyCycle(val1)
    pwm2.ChangeDutyCycle(val2)
    pwm1.ChangeDutyCycle(val3)
    pwm2.ChangeDutyCycle(val4)

#----------------------------------------------------------------------------------------------------
#                                       Logic Functions
#----------------------------------------------------------------------------------------------------

# Scan with Servo

def servo_scan():
    stopw()

# sweep forwards

    for i in (0,60):
        # sweep servo
        dist1 = distance(u1t, u1e)
        dist2 = distance(u2t, u2e)
        dist3 = distance(u3t, u3e)
        # average the distance
        av1 = ""
    for i in (61,120):
        # sweep servo
        dist1 = distance(u1t, u1e)
        dist2 = distance(u2t, u2e)
        dist3 = distance(u3t, u3e)
        # average the distance
        av2 = ""
    for i in (121,180):
        # sweep servo
        dist1 = distance(u1t, u1e)
        dist2 = distance(u2t, u2e)
        dist3 = distance(u3t, u3e)
        # average the distance
        av3 = ""

    if av1 > max(av2, av3):
        rihw()
    elif av2 > max(av1, av3): 
        bakw()
    elif av3 > max(av1, av2):
        lefw()

# sweep backwards

    for i in (180,0):
        # sweep servo




# If less than 10, and if one rear sensor is closer than the other

def dir_opt_normal(dist1, dist2, dist3):
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

# If less than 10, and if one rear sensor is closer than the other

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

def normal_run(): 
    
    while True:

        dist1 = distance(u1t, u1e)
        dist2 = distance(u2t, u2e)
        dist3 = distance(u3t, u3e)

        dir_opt(dist1, dist2, dist3)

def pwm_run(): 

    init_freq = 100
    dc = 0
    pwm1 = gp.PWM(m1,init_freq)  
    pwm2 = gp.PWM(m2,init_freq)
    pwm3 = gp.PWM(m3,init_freq)  
    pwm4 = gp.PWM(m4,init_freq)

    pwm1.start(dc)
    pwm2.start(dc)
    pwm3.start(dc)
    pwm4.start(dc)

    while True:

        dist1 = distance(u1t, u1e)
        dist2 = distance(u2t, u2e)
        dist3 = distance(u3t, u3e)

        dir_opt_pwm(dist1, dist2, dist3):

#----------------------------------------------------------------------------------------------------
#                                       Main Functions
#----------------------------------------------------------------------------------------------------

def log():

def main():
    try:
        if pwm_mode_bool==0:
                print("Running in Normal mode")
                normal_run()
            elif pwm_mode_bool==1:
                print("Running in PWM mode")
                pwm_run()
            else:
                print("pwm_mode_bool not set to zero or one...")
                sys.exit()

    except KeyboardInterrupt:
        stopw():
        GPIO.cleanup()
        print("Robot Stopped")

main()