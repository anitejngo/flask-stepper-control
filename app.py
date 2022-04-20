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
from src.stepper import STEPS_PER_MM_DEFAULT, DEFAULT_STEP_TYPE, is_set_type_valid, speed_to_delay, DEFAULT_STEP_DELAY

app = Flask(__name__)
CORS(app)

motor_control = MotorState(motor_position=0, is_motor_moving=False)


@app.route("/")
def main():
    response = {"message": "Motor controlling server is running"}
    return jsonify(response), 200


@app.route('/is-motor-at-start', methods=['GET'])
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


@app.route('/move', methods=['POST'])
def move():
    data = request.json
    steps_per_mm = data.get("stepsPerMm", STEPS_PER_MM_DEFAULT)
    distance_to_move = data.get("distanceToMove", 0)
    step_type = data.get("stepType", DEFAULT_STEP_TYPE)

    speed = data.get("speed", None)
    step_delay = data.get("stepDelay", DEFAULT_STEP_DELAY)

    if not is_set_type_valid(step_type):
        response = {"message": "Step type is not valid"}
        return jsonify(response), 400
    try:
        if distance_to_move:

            if step_delay and speed:
                response = {"message": "Cant send both speed and steps delay!"}
                return jsonify(response), 400
            elif speed:
                step_delay = speed_to_delay(speed)
            elif step_delay:
                step_delay = step_delay

            if motor_control.is_motor_moving:
                response = {"message": "Motor is already moving"}
                return jsonify(response), 409
            else:
                response = {"message": "Motor sent to %s with steps %s" % (distance_to_move, steps_per_mm)}
                motor_control.move_motor_to_distance(distance_to_move, steps_per_mm, step_type, step_delay)
                return jsonify(response), 200
        else:
            response = {"message", "Distance not provided"}
            return jsonify(response), 400
    except Exception as e:
        response = {"message": "Error: %s" % e}
        return jsonify(response), 400
