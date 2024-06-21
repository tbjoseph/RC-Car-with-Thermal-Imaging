import time
import board
import busio
import numpy as np
import cv2
import matplotlib.pyplot as plt
import adafruit_mlx90640

### Initialize I2C bus ###
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

### Initialize MLX90640 thermal camera ###
mlx = adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_16_HZ
mlx_shape = (24, 32)
mlx_pixels = mlx_shape[0] * mlx_shape[1]

### Set up Matplotlib ###
# Enable interactive mode
plt.ion()
# Create a new figure and axis
fig, ax = plt.subplots()
# Set up the image with a color map and temperature limits
thermal_image = ax.imshow(
    np.zeros((mlx_shape[0], mlx_shape[1])),
    cmap="inferno",
    interpolation="nearest",
    vmin=0,
    vmax=60,
)
# Add a colorbar
cbar = fig.colorbar(thermal_image)
# Set colorbar label
cbar.ax.set_ylabel("Temperature (°C)")
# Draw the figure
fig.canvas.draw()

try:
    while True:
        frame = np.zeros((mlx_pixels,))
        mlx.getFrame(frame)
        frame = np.reshape(frame, mlx_shape)
        print(f"Got frame: {str(frame[0][:3])[1:-1]}, ...")

        # Update the displayed data
        thermal_image.set_data(frame)
        fig.canvas.draw()
        plt.pause(0.2)  # Small delay to allow the plot to update
except KeyboardInterrupt:
    plt.close()  # Close the plot if the user presses Ctrl+C
