import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


class DCMotor:
    """
    Class for controlling a DC motor.
    """

    def __init__(self, forward_pin, backward_pin, pwm_frequency=1000):
        """
        Initialize a DCMotor instance.
        :param forward_pin: GPIO pin for forward movement
        :param backward_pin: GPIO pin for backward movement
        :param pwm_frequency: PWM frequency for motor control (default: 1000)
        """
        GPIO.setup(forward_pin, GPIO.OUT)
        GPIO.setup(backward_pin, GPIO.OUT)

        self.forward_pwm = GPIO.PWM(forward_pin, pwm_frequency)
        self.backward_pwm = GPIO.PWM(backward_pin, pwm_frequency)

    def rotate(self, direction, speed):
        """
        Rotates the DC motor in the specified direction at the specified speed.
        :param direction: Direction to rotate ('forward' or 'backward')
        :param speed: Speed of rotation (0-100)
        :raises ValueError: If the direction is not 'forward' or 'backward'
        """
        if direction == "forward":
            self.forward_pwm.start(speed)
            self.backward_pwm.stop()
        elif direction == "backward":
            self.forward_pwm.stop()
            self.backward_pwm.start(speed)
        else:
            raise ValueError("Invalid direction. Use 'forward' or 'backward'.")

    def stop(self):
        """
        Stops the DC motor.
        """
        self.forward_pwm.stop()
        self.backward_pwm.stop()


class MotorGroup:
    """
    Class for controlling a group of four DC motors.
    """

    def __init__(self):
        """
        Initialize a MotorGroup instance.
        """
        self.motorA = DCMotor(16, 12)
        self.motorB = DCMotor(18, 23)
        self.motorC = DCMotor(21, 20)
        self.motorD = DCMotor(24, 25)
        self.motors = [self.motorA, self.motorB, self.motorC, self.motorD]

    def move(self, direction):
        """
        Moves the group of motors in the specified direction.
        :param direction: Direction to move ('forward', 'backward',
        'left', or 'right')
        :raises ValueError: If the direction is not 'forward',
        'backward', 'left', or 'right'
        """
        if direction == "forward":
            for motor in self.motors:
                motor.rotate("forward", 100)
        elif direction == "backward":
            for motor in self.motors:
                motor.rotate("backward", 100)
        elif direction == "left":
            self.motorA.rotate("forward", 5)
            self.motorB.rotate("forward", 100)
            self.motorC.rotate("forward", 5)
            self.motorD.rotate("forward", 100)
        elif direction == "right":
            self.motorA.rotate("forward", 100)
            self.motorB.rotate("forward", 5)
            self.motorC.rotate("forward", 100)
            self.motorD.rotate("forward", 5)
        else:
            raise ValueError(
                "Invalid direction. Use 'forward', 'backward', 'left', or 'right'."
            )

    def stop(self):
        """
        Stops all motors in the group.
        """
        for motor in self.motors:
            motor.stop()


motors = MotorGroup()


def move_car(direction):
    """
    Moves the car in the specified direction or stops it.
    :param direction: Direction to move or stop ('forward', 'backward',
    'left', 'right', or 'stop')
    :raises ValueError: If the direction is not 'forward', 'backward',
    'left', 'right', or 'stop'
    """
    if direction not in {"forward", "backward", "left", "right", "stop"}:
        raise ValueError(
            "Invalid direction. Use 'forward', 'backward', 'left', 'right', or 'stop'."
        )

    if direction == "stop":
        motors.stop()
    else:
        motors.move(direction)
