import board
import busio
import adafruit_mpu6050
# perf_counter is more precise than time() for dt calculation
from time import sleep, perf_counter
i2c = busio.I2C(board.SCL, board.SDA)
mpu = adafruit_mpu6050.MPU6050(i2c)


ACCEL_THRESHOLD_HIGH = 2.0
ACCEL_THRESHOLD_LOW = -2.0
DEBOUNCE_TIME = 0.2 # min time between steps


num_steps = 0
last_step_time = 0
step_state = "WAITING_FOR_PEAK"

while True:
    current_time = perf_counter()
    acceleration = mpu.acceleration[2] - 9.8
    
    time_since_last_step = current_time - last_step_time
    
    if step_state == "WAITING_FOR_PEAK":
        if acceleration > ACCEL_THRESHOLD_HIGH and time_since_last_step > DEBOUNCE_TIME:
            step_state = "WAITING_FOR_MIN"
            
    elif step_state == "WAITING_FOR_MIN":
        if acceleration < ACCEL_THRESHOLD_LOW:
            num_steps += 1
            last_step_time = current_time
            step_state = "WAITING_FOR_PEAK"
    
    print("Steps: ", num_steps)
    
    sleep(0.1)