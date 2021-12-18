from flask import Flask, jsonify, request

from stepper import STEPS_PER_MM_DEFAULT, motor_move, DEFAULT_STEP_TYPE, is_set_type_valid, DEFAULT_STEP_DELAY

app = Flask(__name__)


@app.route("/")
def main():
    response = {"message": "server is running"}
    return jsonify(response), 200


@app.route('/move', methods=['POST'])
def move():
    data = request.json
    steps_per_mm = data.get("stepsPerMm", STEPS_PER_MM_DEFAULT)
    distance_to_move = data.get("distanceToMove", STEPS_PER_MM_DEFAULT)
    step_delay = data.get("stepDelay", DEFAULT_STEP_DELAY)
    step_type = data.get("stepType", DEFAULT_STEP_TYPE)
    if not is_set_type_valid(step_type):
        response = {"message": "Step type is not valid"}
        return jsonify(response), 400
    try:
        if distance_to_move:
            response = {"message": "Moved to %s with steps %s" % (distance_to_move, steps_per_mm)}
            motor_move(distance_to_move, steps_per_mm, step_type, step_delay)
            return jsonify(response), 200
        else:
            response = {"message", "Distance not provided"}
            return jsonify(response), 400
    except Exception as e:
        response = {"message": "Error: %s" % e}
        return jsonify(response), 400
