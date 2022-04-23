# Replace libraries by fake ones
import platform

if platform.system() == 'Darwin':
    import sys
    import fake_rpi

    sys.modules['RPi'] = fake_rpi.RPi  # Fake RPi
    sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO  # Fake GPIO

from flask import Flask, jsonify, request
from flask_cors import CORS

from src.stepper import MotorState

app = Flask(__name__)
CORS(app)

motor_control = MotorState(is_motor_moving=False)


@app.route("/")
def main():
    response = {"message": "Motor controlling server is running"}
    return jsonify(response), 200


@app.route('/is-at-start', methods=['GET'])
def is_at_start():
    response = {"isMotorAtStart": motor_control.is_motor_at_start()}
    return jsonify(response), 200


@app.route('/is-moving', methods=['GET'])
def is_moving():
    if motor_control.is_motor_moving:
        response = {"message": "Motor is moving", "motorIsMoving": True}
        return jsonify(response), 200
    else:
        response = {"message": "Motor is idle", "motorIsMoving": False}
        return jsonify(response), 200


@app.route('/move-to-start', methods=['POST'])
def move_to_start():
    if motor_control.is_motor_moving:
        response = {"message": "Motor is already moving"}
        return jsonify(response), 409
    else:
        response = {"message": "Motor sent back to start"}
        motor_control.move_motor_to_start()
        return jsonify(response), 200


@app.route('/move-to-switch', methods=['POST'])
def move_to_switch():
    if motor_control.is_motor_moving:
        response = {"message": "Motor is already moving"}
        return jsonify(response), 409
    else:
        response = {"message": "Motor sent back to start"}
        motor_control.move_motor_to_switch()
        return jsonify(response), 200


@app.route('/move', methods=['POST'])
def move():
    data = request.json
    distance_to_move = data.get("distanceToMove", None)

    try:
        if distance_to_move:
            if motor_control.is_motor_moving:
                response = {"message": "Motor is already moving"}
                return jsonify(response), 409
            else:
                response = {"message": "Motor sent to %s" % distance_to_move}
                try:
                    motor_control.move_motor_to_distance(distance_to_move)
                    return jsonify(response), 200
                except Exception as e:
                    return jsonify(e), 200
        else:
            response = {"message", "Distance or speed not provided"}
            return jsonify(response), 400
    except Exception as e:
        response = {"message": "Error: %s" % e}
        return jsonify(response), 400
