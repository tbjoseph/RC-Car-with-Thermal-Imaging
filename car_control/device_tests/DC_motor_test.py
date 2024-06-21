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


try:
    while True:
        # Get user input for motor and direction
        motor = input("Enter motor (A, B, C, or D): ").upper()
        direction = input("Enter direction (forward or backward): ").lower()

        if motor not in motor_pins.keys():
            print("Invalid motor. Please enter A, B, C, or D.")
            continue

        if direction not in ["forward", "backward"]:
            print("Invalid direction. Please enter 'forward' or 'backward'.")
            continue

        # Control the motor according to user input
        control_motor(
            motor, direction, 100
        )  # Change the speed value (0-100) as desired
        time.sleep(2)

        # Stop the motor
        control_motor(motor, "forward", 0)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    # Clean up GPIO and stop all motors
    for motor in motor_pwm.values():
        motor[0].stop()
        motor[1].stop()
    GPIO.cleanup()
