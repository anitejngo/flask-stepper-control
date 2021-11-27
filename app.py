from flask import Flask, jsonify, request

try:
    import RPi.GPIO
except (RuntimeError, ModuleNotFoundError):
    import fake_rpigpio.utils
    fake_rpigpio.utils.install()

from RpiMotorLib import RpiMotorLib
import time


direction = 22  # Direction (DIR) GPIO Pin
step = 23  # Step GPIO Pin
EN_pin = 24  # enable pin (LOW to enable)
STEPS_IN_ONE_MM = 19.0375

# Declare a instance of class pass GPIO pins numbers and the motor type
try:
    motor = RpiMotorLib.A4988Nema(direction, step, (21, 21, 21), "DRV8825")
    RPi.GPIO.cleanup()  # clear GPIO allocat
    RPi.GPIO.setup(EN_pin, RPi.GPIO.OUT)  # set enable pin as output
except:
    pass


def motorMove(cm):
    try:

        steps = (float(cm) * 10) * STEPS_IN_ONE_MM
        steps = int(steps)
        print("Steps %f" % steps)
        # pull enable to low to enable motor
        RPi.GPIO.output(EN_pin, RPi.GPIO.LOW)

        motor.motor_go(steps > 0,  # True=Clockwise, False=Counter-Clockwise
                       "Full",  # Step type (Full,Half,1/4,1/8,1/16,1/32)
                       abs(steps),  # number of steps
                       .0005,  # step delay [sec]
                       False,  # True = print verbose output
                       .05)  # initial delay [sec]
    except Exception as E:
        print("FAILED TO MOVE")
        print(E)
        pass


app = Flask(__name__)


@app.route("/")
def main():
    response = {"message": "server is running"}
    return jsonify(response), 200


@app.route('/move', methods=['POST'])
def move():
    data = request.json
    response = {"message", "Error"}
    try:
        distance_to_move = data['cm']
        if distance_to_move:
            message = "Moving to %s" % distance_to_move
            response = {"message": message}
            motorMove(distance_to_move)
            return jsonify(response), 200
        else:
            response = {"message", "No cm parameter"}
            return jsonify(response), 400
    except Exception as e:
        message = "Error: %s" % e
        response = {"message": message}
        return jsonify(response), 400
