from threading import Thread
from flask import Flask, jsonify, request

from stepper import STEPS_PER_MM_DEFAULT, motor_move, motor_stop, DEFAULT_STEP_TYPE, is_set_type_valid, speed_to_delay

app = Flask(__name__)

global motor_thread


@app.route("/")
def main():
    response = {"message": "server is running"}
    return jsonify(response), 200


@app.route('/stop', methods=['POST'])
def stop():
    motor_stop()
    response = {"message": "Motor is stopped"}
    return jsonify(response), 200


@app.route('/moving', methods=['POST'])
def moving():
    motor_is_moving = motor_thread.is_alive()
    response = {"message": "Motor is %r" % motor_is_moving}
    return jsonify(response), 200


@app.route('/move', methods=['POST'])
def move():
    motor_stop()
    data = request.json
    steps_per_mm = data.get("stepsPerMm", STEPS_PER_MM_DEFAULT)
    distance_to_move = data.get("distanceToMove", 0)
    step_type = data.get("stepType", DEFAULT_STEP_TYPE)

    speed = data.get("speed", None)
    step_delay = data.get("stepDelay", None)

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

            response = {"message": "Motor sent to %s with steps %s" % (distance_to_move, steps_per_mm)}
            global motor_thread
            motor_thread = Thread(
                target=lambda: motor_move(distance_to_move, steps_per_mm, step_type, step_delay))
            motor_thread.start()
            return jsonify(response), 200
        else:
            response = {"message", "Distance not provided"}
            return jsonify(response), 400
    except Exception as e:
        response = {"message": "Error: %s" % e}
        return jsonify(response), 400
