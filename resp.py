import pygame
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(22,GPIO.OUT) #tyre no 1 near Hbridge
GPIO.setup(27,GPIO.OUT) #tyre no 2
GPIO.setup(10,GPIO.OUT)
GPIO.setup(9,GPIO.OUT)
GPIO.setup(21,GPIO.OUT) #lights
TRIG = 23
ECHO = 24
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
servo_pin = 2 # Initializing the GPIO 02 for servo motor
GPIO.setup(servo_pin, GPIO.OUT) # Declaring GPIO 02 as output pin
p = GPIO.PWM(servo_pin, 50) # Created PWM channel at 50Hz frequency

def music(s):
	pygame.mixer.init()
	pygame.mixer.music.load(s)
	pygame.mixer.music.play()

def l():
	GPIO.output(21,GPIO.HIGH)
	time.sleep(0.5)
	GPIO.output(21,GPIO.LOW)
	
def Ultra():
	GPIO.output(TRIG, False)
	# "Waiting For Sensor To Settle"
	time.sleep(0.25)
	GPIO.output(TRIG, True)
	time.sleep(0.00001)
	GPIO.output(TRIG, False)

	while GPIO.input(ECHO)==0:
		pulse_start = time.time()
		
	while GPIO.input(ECHO)==1:
		pulse_end = time.time()
	pulse_duration = pulse_end - pulse_start
	distance = pulse_duration * 17150
	distance = round(distance, 2)
	return distance
	
def Servo():
	p.start(2.5)
	p.ChangeDutyCycle(2.5)
	time.sleep(1)
	if Ultra()<20.00:
		p.ChangeDutyCycle(7.5)
		return 1
	p.ChangeDutyCycle(7.5)
	time.sleep(1)
	p.ChangeDutyCycle(12.5)
	time.sleep(1)
	if Ultra()<20.00:
		p.ChangeDutyCycle(7.5)
		return 2
	p.ChangeDutyCycle(7.5)
	time.sleep(1)
	return 0
	
def Left():
	GPIO.output(27,GPIO.LOW)
	GPIO.output(22,GPIO.HIGH)
	GPIO.output(10,GPIO.LOW)
	GPIO.output(9,GPIO.LOW)
	
def Right():
	GPIO.output(22,GPIO.LOW)
	GPIO.output(27,GPIO.HIGH)
	GPIO.output(10,GPIO.LOW)
	GPIO.output(9,GPIO.LOW)
	
def fn():
	GPIO.output(27,GPIO.HIGH)
	GPIO.output(22,GPIO.HIGH)
	GPIO.output(10,GPIO.LOW)
	GPIO.output(9,GPIO.LOW)
	time.sleep(1)
	if Ultra()<20.00:
		music("Obstacle.wav")
		time.sleep(0.25)
		GPIO.output(27,GPIO.LOW)
		GPIO.output(22,GPIO.LOW)
		GPIO.output(10,GPIO.LOW)
		GPIO.output(9,GPIO.LOW)
		s=Servo()
		if s==1:
			for l in range(1):
				Left()
				time.sleep(1)
		elif s==2:
			for l in range(1):
				Right()
				time.sleep(1)
		elif s==0:
			Right()
			time.sleep(1)
			for l in range(1):
				GPIO.output(27,GPIO.HIGH)
				GPIO.output(22,GPIO.HIGH)
				GPIO.output(10,GPIO.LOW)
				GPIO.output(9,GPIO.LOW)
				time.sleep(1)
			Left()
			time.sleep(1)
			for l in range(1):
				GPIO.output(27,GPIO.HIGH)
				GPIO.output(22,GPIO.HIGH)
				GPIO.output(10,GPIO.LOW)
				GPIO.output(9,GPIO.LOW)
				time.sleep(1)
			Right()
			time.sleep(0.50)

try:
	list=[[0,0,0],[0,0,5],[1,0.2,8],[0,0,10],[2,1,18]] #Sublist -1st element represent
	direction 0-straight 1-left 2-right,
	#2nd element represent time to turn, 3rd represent
	time to reach
	time.sleep(3)
	music("Source.wav")

	for i in range(1,len(list)):
		k=list[i][2]-list[i-1][2]

		if list[i][0]==1:
			music("Left.wav")
			time.sleep(1)
			Left()
			time.sleep(list[i][1])

		elif list[i][0]==2:
			music("Right.wav")
			time.sleep(1)
			Right()
			time.sleep(list[i][1])

		for j in range(k):
			l()
			time.sleep(0.25)
			fn()
	time.sleep(2)
	music("Dest.wav")
	# If Keyborad Interrupt (CTRL+C) is pressed
	
except KeyboardInterrupt:
	pass # Go to next line
	
GPIO.cleanup() # Make all GPIO pins LOW	
