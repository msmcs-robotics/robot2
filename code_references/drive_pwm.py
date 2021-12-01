 import RPi.GPIO as gp  
 from time import sleep  
 gp.setmode(gp.BOARD)  
 gp.setup(12,gp.OUT)  
 gp.setup(32,gp.OUT)  
 pwm=gp.PWM(12,50)  
 pwm1=gp.PWM(32,50)  
 pwm.start(0)  
 pwm1.start(0)  
 for i in range(0,101):  
   pwm.ChangeDutyCycle(i)  
   sleep(0.1)  
 for i in range(100,-1,-1):  
   pwm.ChangeDutyCycle(i)  
   sleep(0.1)  
 for j in range(0,101):  
   pwm1.ChangeDutyCycle(j)  
   sleep(0.1)  
 for j in range(100,-1,-1):  
   pwm1.ChangeDutyCycle(j)  
   sleep(0.1);  
 pwm.ChangeDutyCycle(0)  
 pwm1.ChangeDutyCycle(0)  
 pwm.stop()  
 pwm1.stop()  
 gp.cleanup()  