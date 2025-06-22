import RPi.GPIO as GPIO
import time
import threading

# Define GPIO pins for each motor
motor1_pins = [18, 17, 27, 22]
motor2_pins = [23, 24, 25, 5]

# Define step sequence
seq = [
    [1,0,0,1],
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1]
]

# Speed presets (in seconds)
SPEEDS = {
    "fast": 0.0015,   # Fastest
    "medium": 0.003, # Moderate
    "slow": 0.006    # Slowest
}

GPIO.setmode(GPIO.BCM)

def setup(pins):
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

def move_motor(pins, steps, delay):
    for _ in range(steps):
        for step in seq:
            for pin, val in zip(pins, step):
                GPIO.output(pin, val)
            time.sleep(delay)

def run_both_motors(speed_label):
    delay = SPEEDS.get(speed_label, SPEEDS["medium"])
    t1 = threading.Thread(target=move_motor, args=(motor1_pins, 512, delay))    
    t2 = threading.Thread(target=move_motor, args=(motor2_pins, 512, delay))
    t1.start()
    t2.start()                                                                  
    t1.join()
    t2.join()

try:
    setup(motor1_pins)
    setup(motor2_pins)

    # Choose from "fast", "medium", or "slow"
    selected_speed = "fast"
    print(f"Running motors at {selected_speed} speed...")

    run_both_motors(selected_speed)

    print("Done.")

finally:
    GPIO.cleanup()


