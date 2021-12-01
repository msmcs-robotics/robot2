import RPi.GPIO as GPIO
from dist import *
from drive import *

### GPIO Table
#
#   Ultrasonic Sensor Pins
#   Usage: dist.'pin'
#
#   u1t = 17
#   u1e = 18
#   u2t = 27
#   u2e = 22
#   u3t = 23
#   u3e = 24
#
#
#   Motor Pins 
#   Usage: drive.'pin'
#   
#   m1 = 1
#   m2 = 2
#   m3 = 3
#   m4 = 4

logfile = ""

def main(): 
    dist.gd()

    if dist.gd.idist1 == True:
        
    if dist.gd.idist2 == True:
        run_chicken() 
    if dist.gd.idist3 == True:
        run_chicken()
    log()
    clean()

def run_chicken():
    if dist.chicken.left > dist.chicken.right:
    elif dist.chicken.right > dist.chicken.left
def log():

def clean():
    GPIO.cleanup()
