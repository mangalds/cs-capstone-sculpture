#Mini Basketball Finite State Machine
#Made by Delroy Mangal
from pyb import Pin, ADC, Timer
import pyb

#Initializing servos
servo1 = pyb.Servo(1)
servo2 = pyb.Servo(2)
servo3 = pyb.Servo(3)
servo4 = pyb.Servo(4)

#Timer variables
period = 45000 #Length of game
servoInterval = 2000 #Time for hoop to move back and forth

#Servo variables
lastFlippedTime = 0
servoTracker = 0
startServos = 0

#Pin assignments
sw = pyb.Switch()
sw2 = pyb.Switch()
onButton = pyb.Pin('Y3', pyb.Pin.IN)
crashSensor = pyb.Pin('Y5', pyb.Pin.IN)

#Buzzer variables
buzzer1 = 550 #Frequency value 
b1 = Pin('Y2')
tim = Timer(8, freq = 2000)
ch = tim.channel(2, Timer.PWM, pin=b1)

buzzer2 = 550
b2 = Pin('Y7')
tim2 = Timer(12, freq = 2000)
ch2 = tim.channel(1, Timer.PWM, pin=b2)



#Wait state variable
gameRunning = False

#Game state variables
gameTime = 0
score = 0


#Variables to represent state
WAITING = 0
GAMING = 1

#State variable and initial state
state = WAITING

def wait():
	global servo1
	global servo2
	global servo3
	global servo4
	
    #Halts movement of servos for WAITING state
	servo1.speed(3)
	servo2.speed(3)
	servo3.speed(3)
	servo4.speed(3)
    
	global score 
	score = 0
	
	if onButton.value() == 0:
		global gameRunning 
		gameRunning = True
	
	if gameRunning == True:
		global state 
		state = GAMING
	
def game():
	global score
	global gameRunning
	global state
	
	global servo1
	global servo2
	global servo3
	global servo4
	
	global startServos
	global lastFlippedTime
	global servoTracker
	
	tim.freq(buzzer1)
	tim2.freq(buzzer2)
	ch.pulse_width_percent(80)
	ch2.pulse_width_percent(80)
	pyb.delay(1000) #Allows the buzzer to sound for a second
	ch.pulse_width_percent(0) #Turns off buzzer
	ch2.pulse_width_percent(0)
	
	startMillis = pyb.millis()
	
	while gameRunning == True:
		curMillis = pyb.millis()
		
		#Checks to see if the sensor was triggered and adds to the total score
		if crashSensor.value() == 0:
			score = score + 1
			print("score number: " + str(score))
			pyb.delay(300)
			
		#Initial direction for servos
		if startServos == 0:
			startServos = 1
			servo1.speed(60)
			servo2.speed(-60)
			servo3.speed(60)
			servo4.speed(-60)
			
		#Switches the direction the servos move towards depending on the servoTracker variable
		if curMillis - lastFlippedTime >= servoInterval:
			if servoTracker == 0:
				servo1.speed(-60)
				servo2.speed(60)
				servo3.speed(-60)
				servo4.speed(60)
				lastFlippedTime = curMillis
				servoTracker = 1
			else:
				servo1.speed(60)
				servo2.speed(-60)
				servo3.speed(60)
				servo4.speed(-60)
				lastFlippedTime = curMillis
				servoTracker = 0
				
		#Winning condition
		if score == 3:
			gameRunning = False
			tim.freq(buzzer1)
			tim2.freq(buzzer2)
			ch.pulse_width_percent(40) #Sounds buzzer to signify that the game has ended.
			ch2.pulse_width_percent(40)
			pyb.delay(1000) 
			ch.pulse_width_percent(0)
			ch2.pulse_width_percent(0)
			print("Final score: " + str(score))
			print("Congratulations! You won!")
			score = 0
		
		#Time is up
		if curMillis - startMillis >= period:
			gameRunning = False
			tim.freq(buzzer1)
			tim2.freq(buzzer2)
			ch.pulse_width_percent(40)
			ch2.pulse_width_percent(40)
			pyb.delay(1000) 
			ch.pulse_width_percent(0)
			ch2.pulse_width_percent(0)
			print("Final score: " + str(score))
			print("Better luck next time.")
			score = 0
	
	state = WAITING
	
while True:
    #Loops indefinitely to determine the state of the sculpture
	if state == WAITING:
		wait()
	elif state == GAMING:
		game()
	else:
		state = WAITING