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


import RPi.GPIO as gp
import time
from time import sleep
gp.setmode(gp.BOARD)

logfile = "log.txt"


pwm_mode_bool = 0 # zero or one


#----------------------------------------------------------------------------------------------------
#                                       Pins
#----------------------------------------------------------------------------------------------------

# Ultrasonic Sensor Pins
# BCM - 4,17,18,27,22,23

u1t = 7
u1e = 11
u2t = 12
u2e = 13
u3t = 15
u3e = 16

# Motor Pins
# BCM - 12,16,20,21 

m1 = 32 
m2 = 36
m3 = 38
m4 = 40

# Servo Pin
# BSM - 24

serv1 = 18

# Set Distance Pinmodes
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

# Set Servo Pinmode
gp.setup(servoPIN, gp.OUT)

#----------------------------------------------------------------------------------------------------
#                                       Distance Functions
#----------------------------------------------------------------------------------------------------
 
def ultradist(ut, ue):
    gp.output(ut, True)
    time.sleep(0.00001)
    gp.output(ut, False)
    StartTime = time.time()
    StopTime = time.time()
    while gp.input(ue) == 0:
        StartTime = time.time()
    while gp.input(ue) == 1:
        StopTime = time.time()
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
    return distance

def gd():
     #   Front
     gd.dist1 = ultradist(u1t, u1e)
     #   Rear Left
     gd.dist2 = ultradist(u2t, u2e)
     #   Rear Right
     gd.dist3 = ultradist(u3t, u3e)

     #check if at or closer than 10cm
     gd.idist1 = dist1 <= 10
     gd.idist2 = dist2 <= 10
     gd.idist3 = dist3 <= 10

#----------------------------------------------------------------------------------------------------
#                                       Drive Functions
#----------------------------------------------------------------------------------------------------

dirforw="Going Forward..."
dirbakw="Going Backward..."
dirlefw="Turning Left..."
dirrihw="Turning Right..."


# these need to be tested for the L298N
def forw():
    gp.output(m1,gp.HIGH)
    gp.output(m2,gp.LOW)
    gp.output(m3,gp.HIGH)
    gp.output(m4,gp.LOW)

def bakw():
    gp.output(m1,gp.LOW)
    gp.output(m2,gp.HIGH)
    gp.output(m3,gp.LOW)
    gp.output(m4,gp.HIGH)

def lefw():
    gp.output(m1,gp.LOW)
    gp.output(m2,gp.HIGH)
    gp.output(m3,gp.HIGH)
    gp.output(m4,gp.LOW)

def rihw():
    gp.output(m1,gp.HIGH)
    gp.output(m2,gp.LOW)
    gp.output(m3,gp.LOW)
    gp.output(m4,gp.HIGH)
    
def pwm_forw():


def pwm_bakw():


def pwm_lefw():


def pwm_rihw():

def stopw():
    gp.output(m1,gp.LOW)
    gp.output(m2,gp.LOW)
    gp.output(m3,gp.LOW)
    gp.output(m4,gp.LOW)

#----------------------------------------------------------------------------------------------------
#                                       Logic Functions
#----------------------------------------------------------------------------------------------------

# Scan with Servo


# See which rear sensor is closer to an object

def chicken(chick):
    dist.gd()
    left = gd.dist2
    right = gd.dist3
    if left > right:
        lefw()
    elif right > left:
        rihw()
    else:
        if chick==1:
            rihw()
        elif chick==2:
            lefw()

# See if sensor is 10cm or less away from object

def ifclose(): 
    dist.gd()

    if dist.gd.idist1 == True:
        bakw()
    if dist.gd.idist2 == True:
        chicken(1) 
    if dist.gd.idist3 == True:
        chicken(2)
    log()
    clean()



def clean():
    gp.cleanup()

#----------------------------------------------------------------------------------------------------
#                                       Main Function
#----------------------------------------------------------------------------------------------------

def log():

def main():
    if pwm_mode_bool==0:
        print("Running in Normal mode")
    elif pwm_mode_bool==1:
        print("Running in PWM mode")
    else:
        print("pwm_mode_bool not set to zero or one...")

main()