'''

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
 
def ultradist(ut, ue):
    # set Trigger to HIGH
    GPIO.output(ut, True)
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(ut, False)
    StartTime = time.time()
    StopTime = time.time()
    # save StartTime
    while GPIO.input(ue) == 0:
        StartTime = time.time()
    # save time of arrival
    while GPIO.input(ue) == 1:
        StopTime = time.time()
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    return distance


if __name__ == '__main__':
    try:
        while True:
            dist1 = ultradist(u1t, u1e)
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()