
'''

4. System requirements:
a. When the button has not been pressed, traffic light 2 stays green
b. When the button is pressed, traffic light 2 turns to blue, blinks 3 times, then
turns red.
c. When Traffic light 2 turns red, traffic light 1 becomes green and the countdown
panel begins to count down from 9 to 0, in seconds. (In the real world it would
be longer)
d. When countdown reaches 4, traffic light 1 flashes with blue light until time 0.
e. When countdown reaches 0, traffic light 1 becomes red, traffic light 2
becomes green.
f. When the button is pressed once there will be a 20 seconds cooldown to be
able to make another valid press.
5. Implementation requirements: implement the system in both two ways as below
a. Read press button state using the polling method
b. Read press button state using the interrupt method

'''


import RPi.GPIO as GPIO
import time

RED_PIN = 17
GREEN_PIN = 18
BLUE_PIN = 19
BUTTON_PIN = 20

def setup():
    """Setup GPIO pins"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RED_PIN, GPIO.OUT)
    GPIO.setup(GREEN_PIN, GPIO.OUT)
    GPIO.setup(BLUE_PIN, GPIO.OUT)
    GPIO.setup(BUTTON_PIN, GPIO.IN)

def red():
    GPIO.output(RED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.LOW)

def green():
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(BLUE_PIN, GPIO.LOW)

def blue():
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.HIGH)

def is_button_pressed():
    return GPIO.input(BUTTON_PIN) == GPIO.LOW

def off():
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.LOW)

def cleanup():
    GPIO.cleanup()

def demo():
    print("RGB LED Demo - Press Ctrl+C to stop")
    
    setup()
    
    try:
        off()

        while True:
            if is_button_pressed():
                green()
            else:
                off()
                red()
                
            
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        cleanup()

if __name__ == "__main__":
    demo()