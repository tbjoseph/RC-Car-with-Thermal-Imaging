import time
import RPi.GPIO as GPIO

# Configure the GPIO mode
GPIO.setwarnings(GPIO.LOW)
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins connected to the stepper motor driver
IN1 = 6
IN2 = 13
IN3 = 19
IN4 = 26

# Set up the GPIO pins as outputs
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)


# Function to set the GPIO pins according to the step sequence
def set_step(w1, w2, w3, w4):
    GPIO.output(IN1, w1)
    GPIO.output(IN2, w2)
    GPIO.output(IN3, w3)
    GPIO.output(IN4, w4)


# Rotate the stepper motor in the desired direction
def rotate_motor(direction):
    step_sequence = [
        [0, 0, 0, 1],
        [0, 0, 1, 1],
        [0, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 1, 0, 0],
        [1, 1, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 1],
    ]

    if direction == "counter":
        step_sequence.reverse()

    try:
        while True:
            for step in step_sequence:
                set_step(*step)
                time.sleep(0.001)  # Adjust this value to control the motor speed
    except KeyboardInterrupt:
        set_step(0, 0, 0, 0)  # Release the motor


# Main program
try:
    while True:
        direction = input("Enter the rotation direction (clockwise/counter): ")
        rotate_motor(direction)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    GPIO.cleanup()
