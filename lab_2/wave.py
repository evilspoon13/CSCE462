import time
import board
import busio
import RPi.GPIO as GPIO
import adafruit_mcp4725
import math

BUTTON_PIN = 22

i2c = busio.I2C(board.SCL, board.SDA)
dac = adafruit_mcp4725.MCP4725(i2c)

def setup():
    """Setup GPIO pins"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN)

def wait_for_button():
    """Wait for button press"""
    while GPIO.input(BUTTON_PIN) == 1:
        time.sleep(0.1)
        time.sleep(0.2) # debounce

def get_inputs():
    """Get user input"""
    shape= input("Shape (square/triangle/sin): ").lower()
    freq = float(input("enter freq"))
    volt_ratio = float(input("ente rvolt ratio"))
    return shape, freq, volt_ratio

def generate_square(freq, volt_ratio):
    """Generate square wave"""
    period = 1.0 / freq
    half_period = period / 2
    high_val = int(float(4095 * volt_ratio) / 3.3)

    while GPIO.input(BUTTON_PIN) == 1:
        dac.raw_value = high_val
        time.sleep(half_period)
        dac.raw_value = 0
        time.sleep(half_period)

def generate_triangle(freq, volt_ratio):
    """Generate triangle wave"""
    period = 1.0 / freq
    steps = 50
    step_time = period / steps
    max_val = int(float(4095 * volt_ratio) / 3.3)

    while GPIO.input(BUTTON_PIN) == 1:
        # Up slope
        for i in range(steps//2):
            dac.raw_value = int((2 * i * max_val) / steps)
            time.sleep(step_time)
            if GPIO.input(BUTTON_PIN) == 0:
                return

        # Down slope
        for i in range(steps//2):
            dac.raw_value = int(max_val - (2 * i * max_val) / steps)
            time.sleep(step_time)
            if GPIO.input(BUTTON_PIN) == 0:
                return

def generate_sine(freq, volt_ratio):
    """Generate sine wave"""
    period = 1.0 / freq
    steps = 50
    step_time = period / steps
    max_val = int(float(4095 * volt_ratio) / 3.3)
    offset = max_val // 2
    amplitude = max_val // 2

    step = 0
    while GPIO.input(BUTTON_PIN) == 1:
        angle = (2 * math.pi * step) / steps
        value = int(offset + amplitude * math.sin(angle))
        dac.raw_value = max(0, min(4095, value))
        time.sleep(step_time)
        step = (step + 1) % steps

def main():

    setup()
    try:
        while True:
            wait_for_button()

            shape, freq, volt_ratio = get_inputs()

            print("GENERTING!!!!!")

            if shape == "square":
                generate_square(freq, volt_ratio)
            elif shape == "triangle":
                generate_triangle(freq, volt_ratio)
            elif shape == "sin":
                generate_sine(freq, volt_ratio)

            dac.raw_value = 0 # Stop output
            print("Stopped. Press button to continue...")

    except KeyboardInterrupt:
        dac.raw_value = 0
        GPIO.cleanup()
        print("\nProgram ended")

if __name__ == "__main__":
    main()