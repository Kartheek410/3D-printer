
"""
from time import sleep
import RPi.GPIO as GPIO

DIR = 20   # Direction GPIO Pin
STEP = 21  # Step GPIO Pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 200   # Steps per Revolution (360 / 1.8)

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.output(DIR, CW)

GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)


GPIO.output(DIR, GPIO.LOW)
GPIO.output(STEP, GPIO.LOW)

step_count = SPR
delay = .0208
GPIO.output(STEP, GPIO.HIGH)
for x in range(step_count):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)

sleep(.5)
GPIO.output(STEP, GPIO.LOW)
for x in range(step_count):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)

GPIO.cleanup()
"""
"""
import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 200   # Steps per Revolution (360 / 1.8)

#GPIO.setup(26,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)
GPIO.setup(20,GPIO.OUT)


GPIO.output(21, GPIO.LOW)
GPIO.output(20, GPIO.LOW)

#GPIO.output(26,True)        
GPIO.output(21,False)
#GPIO.output(21,GPIO.LOW)

microStep = 0
step_count = SPR
delay = 0.001

#GPIO.output(20, GPIO.HIGH)
while True:
    for x in range(step_count):
        GPIO.output(20, GPIO.HIGH)
        sleep(delay)
        GPIO.output(20, GPIO.LOW)
        sleep(delay)

    sleep(.5)
    GPIO.output(20, GPIO.LOW)
    for x in range(step_count):
        GPIO.output(20, GPIO.HIGH)
        sleep(delay)
        GPIO.output(20, GPIO.LOW)
        sleep(delay)

    microStep = microStep + 1
    print(microStep)

GPIO.cleanup()
"""
"""
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

SPR = 200
#GPIO.setup(26,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)
GPIO.setup(20,GPIO.OUT)

#GPIO.output(21, GPIO.LOW)
#GPIO.output(20, GPIO.LOW)        
GPIO.output(21,False)
GPIO.output(20,False)
#GPIO.output(21,True)
#GPIO.output(21,GPIO.LOW)

#microStep = 0
step_count = SPR
delay = 0.001

while True:
    print("Stepper Back")
    for x in range(step_count):
        GPIO.output(21, False)
        GPIO.output(20,True)
        sleep(delay)
        GPIO.output(20,False)
        sleep(delay)
#        microStep = microStep + 1
#        print(microStep)

    sleep(1)

    print("Stepper front")
    for x in range(step_count):
        GPIO.output(21,True)
        GPIO.output(20,True)
        sleep(delay)
        GPIO.output(20,False)
        sleep(delay)

GPIO.cleanup()
"""
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD) #read the pin as board instead of BCM pin


LinearActuatorDir = 21
LinearActuatorStepPin = 20
LinearActuatorEnable = 19

GPIO.setwarnings(False)
GPIO.setup(LinearActuatorDir, GPIO.OUT)
GPIO.setup(LinearActuatorStepPin, GPIO.OUT)
GPIO.setup(LinearActuatorEnable, GPIO.OUT)

FastSpeed = 0.00045 #Change this depends on your stepper motor
LowSpeed = 0.00045
Speed = FastSpeed

GPIO.output(LinearActuatorEnable, GPIO.HIGH)

while True:
	print ("Move Backward")
	for i in range (5*200):
		GPIO.output(LinearActuatorDir, 0)
		GPIO.output(LinearActuatorStepPin, 1)
		time.sleep(LowSpeed)
		GPIO.output(LinearActuatorStepPin, 0)
		time.sleep(LowSpeed)
		print ("Moving")
	time.sleep(1)
	print ("Move Forward")
	for i in range (5*200):
		GPIO.output(LinearActuatorDir, GPIO.HIGH)
		GPIO.output(LinearActuatorStepPin, GPIO.HIGH)
		time.sleep(FastSpeed)
		GPIO.output(LinearActuatorStepPin, GPIO.LOW)
		time.sleep(FastSpeed)
	time.sleep(1)
