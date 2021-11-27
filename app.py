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

# Declare a instance of class pass GPIO pins numbers and the motor type
try:
    motor = RpiMotorLib.A4988Nema(direction, step, (21, 21, 21), "DRV8825")
    GPIO.setup(EN_pin, GPIO.OUT)  # set enable pin as output
except:
    pass



def motorMove():
    try:
        GPIO.output(EN_pin, GPIO.LOW)  # pull enable to low to enable motor
        motor.motor_go(False,  # True=Clockwise, False=Counter-Clockwise
                       "Full",  # Step type (Full,Half,1/4,1/8,1/16,1/32)
                       200,  # number of steps
                       .0005,  # step delay [sec]
                       False,  # True = print verbose output
                       .05)  # initial delay [sec]

        GPIO.cleanup()  # clear GPIO allocat
    except Exception:
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
            motorMove()
            return jsonify(response), 200
        else:
            response = {"message", "No cm parameter"}
            return jsonify(response), 400
    except Exception as e:
        message = "Error: %s" % e
        response = {"message": message}
        return jsonify(response), 400
