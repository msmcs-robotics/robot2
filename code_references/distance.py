'''
https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi

https://tutorials-raspberrypi.com/raspberry-pi-ultrasonic-sensor-hc-sr04/
'''
#Libraries
import RPi.GPIO as GPIO
import time
import math


#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
u1t = 4
u1e = 17
u2t = 18
u2e = 27
u3t = 22
u3e = 23

GPIO.setup(u1t, GPIO.OUT)
GPIO.setup(u1e, GPIO.IN)
GPIO.setup(u2t, GPIO.OUT)
GPIO.setup(u2e, GPIO.IN)
GPIO.setup(u3t, GPIO.OUT)
GPIO.setup(u3e, GPIO.IN)

def distance(GPIO_TRIGGER, GPIO_ECHO):
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    StartTime = time.time()
    StopTime = time.time()
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
    return distance

if __name__ == '__main__':
    try:
        while True:
            dist1 = distance(u1t, u1e)
            dist2 = distance(u2t, u2e)
            dist3 = distance(u3t, u3e)
            print (dist1, " | ", dist2, " | ", dist3)
            time.sleep(0.3)
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
