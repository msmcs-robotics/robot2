'''
src reference https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi
'''
import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
# Ultrasonic Sensor Pins
u1t = 17
u1e = 18
u2t = 27
u2e = 22
u3t = 23
u4e = 24

#set GPIO direction (IN / OUT)
GPIO.setup(u1t, GPIO.OUT)
GPIO.setup(u1e, GPIO.IN)
GPIO.setup(u2t, GPIO.OUT)
GPIO.setup(u2e, GPIO.IN)
GPIO.setup(u3t, GPIO.OUT)
GPIO.setup(u3e, GPIO.IN)
 
def ultradist(ut, ue):
    GPIO.output(ut, True)
    time.sleep(0.00001)
    GPIO.output(ut, False)
    StartTime = time.time()
    StopTime = time.time()
    while GPIO.input(ue) == 0:
        StartTime = time.time()
    while GPIO.input(ue) == 1:
        StopTime = time.time()
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
    return distance


if __name__ == '__main__':
    try:
        while True:
            dist1 = ultradist(u1t, u1e)
            dist2 = ultradist(u2t, u2e)
            dist3 = ultradist(u3t, u3e)
            print (dist1, " | ", dist2 , " | ", dist3)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()