import time
import RPi.GPIO as GPIO

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motor control pins
motor_pins = {"A": (16, 12), "B": (18, 23), "C": (20, 21), "D": (25, 24)}

# Set up pins as output and set initial state
for pins in motor_pins.values():
    GPIO.setup(pins[0], GPIO.OUT)
    GPIO.setup(pins[1], GPIO.OUT)
    GPIO.output(pins[0], GPIO.LOW)
    GPIO.output(pins[1], GPIO.LOW)

# Set up PWM for each motor
pwm_frequency = 1000  # Change this to set the desired PWM frequency
motor_pwm = {}
for motor, pins in motor_pins.items():
    motor_pwm[motor] = (
        GPIO.PWM(pins[0], pwm_frequency),
        GPIO.PWM(pins[1], pwm_frequency),
    )


# Function to control motor direction and speed
def control_motor(motor, direction, speed):
    if direction == "forward":
        motor_pwm[motor][0].start(speed)
        motor_pwm[motor][1].stop()
    elif direction == "backward":
        motor_pwm[motor][0].stop()
        motor_pwm[motor][1].start(speed)
    else:
        raise ValueError("Invalid direction. Use 'forward' or 'backward'.")


# Function to control the car's movement
def control_car(direction):
    if direction == "f":  # Forward
        for motor in motor_pins.keys():
            control_motor(motor, "forward", 100)
    elif direction == "b":  # Backward
        for motor in motor_pins.keys():
            control_motor(motor, "backward", 100)
    elif direction == "l":  # Left
        control_motor("A", "forward", 50)
        control_motor("C", "forward", 50)
        control_motor("B", "forward", 100)
        control_motor("D", "forward", 100)
    elif direction == "r":  # Right
        control_motor("A", "forward", 100)
        control_motor("C", "forward", 100)
        control_motor("B", "forward", 50)
        control_motor("D", "forward", 50)
    else:
        raise ValueError("Invalid direction. Use 'f', 'b', 'l', or 'r'.")


try:
    while True:
        # Get user input for direction
        direction = input("Enter direction (f, b, l, or r): ").lower()

        if direction not in ["f", "b", "l", "r"]:
            print("Invalid direction. Please enter 'f', 'b', 'l', or 'r'.")
            continue

        # Control the car according to user input
        control_car(direction)
        time.sleep(2)

        # Stop the car
        for motor in motor_pins.keys():
            control_motor(motor, "forward", 0)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    # Clean up GPIO and stop all motors
    for motor in motor_pwm.values():
        motor[0].stop()
        motor[1].stop()
    GPIO.cleanup()
