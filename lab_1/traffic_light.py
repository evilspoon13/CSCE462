
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

LIGHT_1_RED_PIN = 17
LIGHT_1_GREEN_PIN = 18
LIGHT_1_BLUE_PIN = 19

LIGHT_2_RED_PIN = 4
LIGHT_2_GREEN_PIN = 5
LIGHT_2_BLUE_PIN = 6

BUTTON_PIN = 20
A_PIN = 21
B_PIN = 22
C_PIN = 23
D_PIN = 24
E_PIN = 25
F_PIN = 26
G_PIN = 27

last_button_press_time = 0

def setup():
    """Setup GPIO pins"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LIGHT_1_RED_PIN, GPIO.OUT)
    GPIO.setup(LIGHT_1_GREEN_PIN, GPIO.OUT)
    GPIO.setup(LIGHT_1_BLUE_PIN, GPIO.OUT)
    GPIO.setup(LIGHT_2_RED_PIN, GPIO.OUT)
    GPIO.setup(LIGHT_2_GREEN_PIN, GPIO.OUT)
    GPIO.setup(LIGHT_2_BLUE_PIN, GPIO.OUT)
    GPIO.setup(BUTTON_PIN, GPIO.IN)
    GPIO.setup(A_PIN, GPIO.OUT)
    GPIO.setup(B_PIN, GPIO.OUT)
    GPIO.setup(C_PIN, GPIO.OUT)
    GPIO.setup(D_PIN, GPIO.OUT)
    GPIO.setup(E_PIN, GPIO.OUT)
    GPIO.setup(F_PIN, GPIO.OUT)
    GPIO.setup(G_PIN, GPIO.OUT)

def light_1_red():
    GPIO.output(LIGHT_1_RED_PIN, GPIO.HIGH)
    GPIO.output(LIGHT_1_GREEN_PIN, GPIO.LOW)
    GPIO.output(LIGHT_1_BLUE_PIN, GPIO.LOW)

def light_1_green():
    GPIO.output(LIGHT_1_RED_PIN, GPIO.LOW)
    GPIO.output(LIGHT_1_GREEN_PIN, GPIO.HIGH)
    GPIO.output(LIGHT_1_BLUE_PIN, GPIO.LOW)

def light_1_blue():
    GPIO.output(LIGHT_1_RED_PIN, GPIO.LOW)
    GPIO.output(LIGHT_1_GREEN_PIN, GPIO.LOW)
    GPIO.output(LIGHT_1_BLUE_PIN, GPIO.HIGH)

def light_2_red():
    GPIO.output(LIGHT_2_RED_PIN, GPIO.HIGH)
    GPIO.output(LIGHT_2_GREEN_PIN, GPIO.LOW)
    GPIO.output(LIGHT_2_BLUE_PIN, GPIO.LOW)

def light_2_green():
    GPIO.output(LIGHT_2_RED_PIN, GPIO.LOW)
    GPIO.output(LIGHT_2_GREEN_PIN, GPIO.HIGH)
    GPIO.output(LIGHT_2_BLUE_PIN, GPIO.LOW)

def light_2_blue():
    GPIO.output(LIGHT_2_RED_PIN, GPIO.LOW)
    GPIO.output(LIGHT_2_GREEN_PIN, GPIO.LOW)
    GPIO.output(LIGHT_2_BLUE_PIN, GPIO.HIGH)

def one():
    GPIO.output(A_PIN, GPIO.LOW)
    GPIO.output(B_PIN, GPIO.HIGH)
    GPIO.output(C_PIN, GPIO.HIGH)
    GPIO.output(D_PIN, GPIO.LOW)
    GPIO.output(E_PIN, GPIO.LOW)
    GPIO.output(F_PIN, GPIO.LOW)
    GPIO.output(G_PIN, GPIO.LOW)
    
def two():
    GPIO.output(A_PIN, GPIO.HIGH)
    GPIO.output(B_PIN, GPIO.HIGH)
    GPIO.output(C_PIN, GPIO.LOW)
    GPIO.output(D_PIN, GPIO.HIGH)
    GPIO.output(E_PIN, GPIO.HIGH)
    GPIO.output(F_PIN, GPIO.LOW)
    GPIO.output(G_PIN, GPIO.HIGH)

def three():
    GPIO.output(A_PIN, GPIO.HIGH)
    GPIO.output(B_PIN, GPIO.HIGH)
    GPIO.output(C_PIN, GPIO.HIGH)
    GPIO.output(D_PIN, GPIO.HIGH)
    GPIO.output(E_PIN, GPIO.LOW)
    GPIO.output(F_PIN, GPIO.LOW)
    GPIO.output(G_PIN, GPIO.HIGH)

def four():
    GPIO.output(A_PIN, GPIO.LOW)
    GPIO.output(B_PIN, GPIO.HIGH)
    GPIO.output(C_PIN, GPIO.HIGH)
    GPIO.output(D_PIN, GPIO.LOW)
    GPIO.output(E_PIN, GPIO.LOW)
    GPIO.output(F_PIN, GPIO.HIGH)
    GPIO.output(G_PIN, GPIO.HIGH)

def five():
    GPIO.output(A_PIN, GPIO.HIGH)
    GPIO.output(B_PIN, GPIO.LOW)
    GPIO.output(C_PIN, GPIO.HIGH)
    GPIO.output(D_PIN, GPIO.HIGH)
    GPIO.output(E_PIN, GPIO.LOW)
    GPIO.output(F_PIN, GPIO.HIGH)
    GPIO.output(G_PIN, GPIO.HIGH)

def six():
    GPIO.output(A_PIN, GPIO.HIGH)
    GPIO.output(B_PIN, GPIO.LOW)
    GPIO.output(C_PIN, GPIO.HIGH)
    GPIO.output(D_PIN, GPIO.HIGH)
    GPIO.output(E_PIN, GPIO.HIGH)
    GPIO.output(F_PIN, GPIO.HIGH)
    GPIO.output(G_PIN, GPIO.HIGH)

def seven():
    GPIO.output(A_PIN, GPIO.HIGH)
    GPIO.output(B_PIN, GPIO.HIGH)
    GPIO.output(C_PIN, GPIO.HIGH)
    GPIO.output(D_PIN, GPIO.LOW)
    GPIO.output(E_PIN, GPIO.LOW)
    GPIO.output(F_PIN, GPIO.LOW)
    GPIO.output(G_PIN, GPIO.LOW)

def eight():
    GPIO.output(A_PIN, GPIO.HIGH)
    GPIO.output(B_PIN, GPIO.HIGH)
    GPIO.output(C_PIN, GPIO.HIGH)
    GPIO.output(D_PIN, GPIO.HIGH)
    GPIO.output(E_PIN, GPIO.HIGH)
    GPIO.output(F_PIN, GPIO.HIGH)
    GPIO.output(G_PIN, GPIO.HIGH)

def nine():
    GPIO.output(A_PIN, GPIO.HIGH)
    GPIO.output(B_PIN, GPIO.HIGH)
    GPIO.output(C_PIN, GPIO.HIGH)
    GPIO.output(D_PIN, GPIO.LOW)
    GPIO.output(E_PIN, GPIO.LOW)
    GPIO.output(F_PIN, GPIO.HIGH)
    GPIO.output(G_PIN, GPIO.HIGH)

def is_button_pressed():
    return GPIO.input(BUTTON_PIN) == GPIO.LOW

def lights_off():
    # turns off all
    GPIO.output(LIGHT_1_RED_PIN, GPIO.LOW)
    GPIO.output(LIGHT_1_GREEN_PIN, GPIO.LOW)
    GPIO.output(LIGHT_1_BLUE_PIN, GPIO.LOW)
    GPIO.output(LIGHT_2_RED_PIN, GPIO.LOW)
    GPIO.output(LIGHT_2_GREEN_PIN, GPIO.LOW)
    GPIO.output(LIGHT_2_BLUE_PIN, GPIO.LOW)

    GPIO.output(A_PIN, GPIO.LOW)
    GPIO.output(B_PIN, GPIO.LOW)
    GPIO.output(C_PIN, GPIO.LOW)
    GPIO.output(D_PIN, GPIO.LOW)
    GPIO.output(E_PIN, GPIO.LOW)
    GPIO.output(F_PIN, GPIO.LOW)
    GPIO.output(G_PIN, GPIO.LOW)
    

def display_number(num):
    """Display number on 7-segment display"""
    if num == 0:
        zero()
    elif num == 1:
        one()
    elif num == 2:
        two()
    elif num == 3:
        three()
    elif num == 4:
        four()
    elif num == 5:
        five()
    elif num == 6:
        six()
    elif num == 7:
        seven()
    elif num == 8:
        eight()
    elif num == 9:
        nine()

def zero():
    GPIO.output(A_PIN, GPIO.HIGH)
    GPIO.output(B_PIN, GPIO.HIGH)
    GPIO.output(C_PIN, GPIO.HIGH)
    GPIO.output(D_PIN, GPIO.HIGH)
    GPIO.output(E_PIN, GPIO.HIGH)
    GPIO.output(F_PIN, GPIO.HIGH)
    GPIO.output(G_PIN, GPIO.LOW)

def blink_light_2_blue():
    """Blink traffic light 2 blue 3 times"""
    for _ in range(3):
        light_2_blue()
        time.sleep(0.3)
        GPIO.output(LIGHT_2_BLUE_PIN, GPIO.LOW)
        time.sleep(0.3)

def cleanup():
    GPIO.cleanup()


def traffic_light_polling():
    setup()
    
    global last_button_press_time

    # State variables
    cooldown_period = 20  # 20 seconds cooldown
    
    try:
        lights_off()
        
        while True:
            current_time = time.time()

            # Check if cooldown period has passed
            cooldown_elapsed = (current_time - last_button_press_time) >= cooldown_period
            print(f"Cooldown elapsed: {cooldown_elapsed}, Time since last press: {current_time - last_button_press_time:.1f}s")
            
            # check if button is pressed and cooldown has expired
            if is_button_pressed() and cooldown_elapsed:
                print("Button pressed! Starting traffic light sequence...")
                last_button_press_time = current_time
                
                # b. traffic light 2 turns blue, blinks 3 times, then turns red
                blink_light_2_blue()
                light_2_red()
                
                # c. traffic light 1 becomes green and countdown begins from 9 to 0
                light_1_green()
                
                # countdown from 9 to 5 (normal green light)
                for countdown in range(9, 4, -1):
                    print(countdown)
                    display_number(countdown)
                    time.sleep(1)
                
                # d. When countdown reaches 4, traffic light 1 flashes blue until 0
                for countdown in range(4, -1, -1):
                    display_number(countdown)
                    
                    # flash blue light
                    start_flash_time = time.time()
                    while time.time() - start_flash_time < 1.0:
                        light_1_blue()
                        time.sleep(0.25)
                        light_1_green()
                        time.sleep(0.25)
                
                # e. When countdown reaches 0, light 1 red, light 2 green
                light_1_red()
                light_2_green()
                
                print("returning to normal state.")
            
            else:
                # a. When button not pressed, traffic light 2 stays green
                light_2_green()
                light_1_red()  # Default state for light 1
            
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        cleanup()

def demo():
    traffic_light_polling()

if __name__ == "__main__":
    demo()