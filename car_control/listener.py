from gevent import monkey

monkey.patch_all()

from flask import Flask
from flask_socketio import SocketIO
from parse_config_file import config
import car_movement as car
import camera_movement as camera
import camera_imagery as imagery

app = Flask(__name__)
app.config["SECRET_KEY"] = config.get("Server", "web_secret_key")
server_socket = SocketIO(app, cors_allowed_origins="*", async_mode="gevent")


@server_socket.on("car-movement")
def car_movement(direction):
    """
    Handles the "car-movement" event and moves the car in the specified direction.
    :param direction: Direction to move the car ('forward', 'backward', 'left',
    'right', or 'stop')
    """
    print(f"Received direction: {direction}")
    car.move_car(direction)


@server_socket.on("camera-movement")
def camera_movement(direction):
    """
    Handles the "camera-movement" event and moves the camera in the
    specified direction.
    :param direction: Direction to move the camera ('left', 'right', or 'stop')
    """
    print(f"Received direction: {direction}")
    camera.pan_camera(direction)


def camera_imagery(frame):
    """
    Emits the "camera-imagery" event with the given frame data.
    :param frame: The frame data to be sent
    """
    frame = frame.tolist()
    server_socket.emit("camera-imagery", frame)


imagery.start_stream(camera_imagery)

if __name__ == "__main__":
    server_socket.run(app, debug=True, host="0.0.0.0", port=5000)
