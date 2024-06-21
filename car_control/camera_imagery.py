import time
import threading
import board
import busio
import numpy as np
import adafruit_mlx90640


class ThermalCamera:
    """
    Class for interfacing with the MLX90640 thermal camera.
    """

    PROCESSING_DELAY = 0.1

    def __init__(self):
        """
        Initializes the thermal camera and sets the refresh rate.
        """
        self.i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
        self.mlx = adafruit_mlx90640.MLX90640(self.i2c)
        self.mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ
        self.mlx_shape = (24, 32)
        self.mlx_pixels = self.mlx_shape[0] * self.mlx_shape[1]

    def get_frame(self):
        """
        Captures a frame from the thermal camera and returns it as a numpy array.
        :return: 2D numpy array containing the temperature values of each pixel.
        """
        frame = np.zeros((self.mlx_pixels,))
        self.mlx.getFrame(frame)
        return np.reshape(frame, self.mlx_shape)

    def stream(self, callback):
        """
        Continuously captures frames from the thermal camera and calls the
        callback function with each frame.
        :param callback: Function to be called with each captured frame.
        """
        while True:
            try:
                callback(self.get_frame())
                time.sleep(ThermalCamera.PROCESSING_DELAY)
            except KeyboardInterrupt:
                return


thermal_camera = ThermalCamera()


def start_stream(callback):
    """
    Starts a separate thread to stream camera imagery and call the provided
    callback function with each frame.
    :param callback: Function to be called with each captured frame.
    """
    camera_imagery_thread = threading.Thread(
        target=thermal_camera.stream, args=(callback,)
    )
    camera_imagery_thread.start()
