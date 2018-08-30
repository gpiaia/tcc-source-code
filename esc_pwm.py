import time
import pigpio
import RPi.GPIO as GPIO

# Set up BCM GPIO numbering
GPIO.setmode(GPIO.BCM)

# Connect to pigpio
pi = pigpio.pi() 

# Calibrate ESC
ESC_GPIO = 13
pi.set_servo_pulsewidth(ESC_GPIO, 2000) # Maximum throttle.
time.sleep(2)
pi.set_servo_pulsewidth(ESC_GPIO, 1000) # Minimum throttle.
time.sleep(2)

i = 0
j = 1
s = 1

while i<100 :

	pi.set_servo_pulsewidth(ESC_GPIO, j*100 + 1000)
	
	if s == 1 :
		j = j + 1;
	else :
		j = j - 1;

	if j == -5 :
		s = 1
	if j == 11 :
		s = 0		

	i = i + 1;
	time.sleep(1)
