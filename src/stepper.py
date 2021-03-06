import time
from threading import Thread

import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib

from src.sensor import get_limit_switch_state

DIRECTION_PIN = 22  # Direction (DIR) GPIO Pin
STEP_PIN = 23  # Step GPIO Pin
ENABLE_PIN = 24  # enable pin (LOW to enable)

# Calculated by doing this simple formula
# (VALUE_TO_GO / VALUE IT WENT) + STEPS_PER_MM_DEFAULT (get new more accurate step per mm)
# STEPS_PER_MM_DEFAULT = 19.05482
STEPS_PER_MM_DEFAULT = 19.0375
DEFAULT_STEP_TYPE = 'Full'  # ['Full', 'Half', "1/4", '1/8', '1/16', '1/32']

# FAST_STEP_DELAY = 0.00001
DEFAULT_STEP_DELAY = 0.00006
SLOW_STEP_DELAY = 0.00016

# Declare a instance of class pass GPIO pins numbers and the motor type
GPIO.setmode(GPIO.BCM)
GPIO.setup(ENABLE_PIN, GPIO.OUT)  # set enable pin as output
motor = RpiMotorLib.A4988Nema(DIRECTION_PIN, STEP_PIN, (21, 21, 21), "DRV8825")


def move_motor_to_steps(steps, movement_done, go_slow=False):
    try:
        # pull enable to low to enable motor
        GPIO.output(ENABLE_PIN, GPIO.LOW)
        motor.motor_go(steps > 0,  # True=Clockwise, False=Counter-Clockwise
                       DEFAULT_STEP_TYPE,  # Step type (Full,Half,1/4,1/8,1/16,1/32)
                       abs(steps),  # number of steps
                       SLOW_STEP_DELAY if go_slow else DEFAULT_STEP_DELAY,  # step delay [sec]
                       False,  # True = print verbose output
                       .05)  # initial delay [sec]
        movement_done()
    except Exception as E:
        print("MOTOR FAILED TO MOVE")
        print(E)
        movement_done()
        pass


def stop_motor():
    try:
        # RPi.GPIO.output(ENABLE_PIN, RPi.GPIO.HIGH)
        motor.motor_stop()
    except Exception as E:
        print("MOTOR FAILED TO STOP")
        print(E)
        pass


def is_motor_at_start():
    return bool(get_limit_switch_state())


def check_start_sensor_to_stop_motor(movement_done):
    while True:
        if is_motor_at_start():
            stop_motor()
            movement_done()
            break
        else:
            time.sleep(0.1)


class MotorState:
    def __init__(self, is_motor_moving):
        self.motor_position = float(0)
        self.is_motor_moving = is_motor_moving

    def mark_motor_movement_as_complete(self, moved_steps):
        self.motor_position = moved_steps
        self.is_motor_moving = False

    def move_motor_to_distance(self, distance_to_move):
        # move  motor to distance in cm sent from frontend by calculating it in steps and going left or right
        self.is_motor_moving = True

        steps_to_move = int((float(distance_to_move) * 10) * STEPS_PER_MM_DEFAULT)

        steps_to_move_from_current_position = int(steps_to_move - float(self.motor_position))

        if steps_to_move < 0:
            self.is_motor_moving = False
            raise Exception('Motor cant got below 0')
        motor_thread = Thread(
            target=lambda: move_motor_to_steps(steps_to_move_from_current_position,
                                               lambda: self.mark_motor_movement_as_complete(
                                                   steps_to_move)))
        motor_thread.start()

    def move_motor_to_start(self):
        # move motor  back to zero
        self.is_motor_moving = True
        motor_thread = Thread(
            target=lambda: move_motor_to_steps(-self.motor_position, lambda: self.mark_motor_movement_as_complete(0)))
        motor_thread.start()

    def move_motor_to_switch(self):
        # send motor back 4 meters and stop when it gets to limit switch
        self.is_motor_moving = True
        steps_to_move = int(4000 * STEPS_PER_MM_DEFAULT)
        motor_thread = Thread(
            target=lambda: move_motor_to_steps(-steps_to_move, lambda: print('MOTOR STOP BY SWITCH'), True))
        motor_thread.start()
        motor_stop_thread = Thread(
            target=lambda: check_start_sensor_to_stop_motor(lambda: self.mark_motor_movement_as_complete(0))
        )
        motor_stop_thread.start()
