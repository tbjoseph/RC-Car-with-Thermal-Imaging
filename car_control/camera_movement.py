import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


class StepperMotor:
    """
    Class for controlling a stepper motor.
    """

    STEP_SEQUENCE = [
        [0, 0, 0, 1],
        [0, 0, 1, 1],
        [0, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 1, 0, 0],
        [1, 1, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 1],
    ]
    PROCESSING_DELAY = 0.001

    def __init__(self, in1, in2, in3, in4):
        """
        Initializes the stepper motor with the specified input pins.
        :param in1: First input pin
        :param in2: Second input pin
        :param in3: Third input pin
        :param in4: Fourth input pin
        """
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in3
        self.IN4 = in4
        self.direction = None

        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)

    def set_step(self, w1, w2, w3, w4):
        """
        Sets the state of the stepper motor's input pins.
        :param w1: State of the first input pin (0 or 1)
        :param w2: State of the second input pin (0 or 1)
        :param w3: State of the third input pin (0 or 1)
        :param w4: State of the fourth input pin (0 or 1)
        """
        GPIO.output(self.IN1, w1)
        GPIO.output(self.IN2, w2)
        GPIO.output(self.IN3, w3)
        GPIO.output(self.IN4, w4)

    def rotate(self, direction):
        """
        Rotates the stepper motor in the specified direction continuously.
        :param direction: Direction to rotate ('left' or 'right')
        :raises ValueError: If the direction is not 'left' or 'right'
        """
        if direction not in {"left", "right"}:
            raise ValueError("Invalid direction. Use 'left' or 'right'.")

        self.direction = direction

        steps = (
            StepperMotor.STEP_SEQUENCE[:]
            if self.direction == "right"
            else StepperMotor.STEP_SEQUENCE[::-1]
        )
        while self.direction == direction:
            for step in steps:
                self.set_step(*step)
                time.sleep(StepperMotor.PROCESSING_DELAY)

    def stop(self):
        """
        Stops the stepper motor's rotation.
        """
        self.set_step(0, 0, 0, 0)
        self.direction = None


panning_motor = StepperMotor(6, 13, 19, 26)


def pan_camera(direction):
    """
    Pans the camera using the stepper motor in the specified direction
    or stops panning.
    :param direction: Direction to pan or stop ('left', 'right', or 'stop')
    :raises ValueError: If the direction is not 'left', 'right', or 'stop'
    """
    if direction not in {"left", "right", "stop"}:
        raise ValueError("Invalid direction. Use 'left', 'right', or 'stop'.")

    if direction == "stop":
        panning_motor.stop()
    else:
        panning_motor.rotate(direction)
