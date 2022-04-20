import time
from threading import Thread

import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib

from src.sensor import get_limit_switch_state

direction = 22  # Direction (DIR) GPIO Pin
step = 23  # Step GPIO Pin
EN_pin = 24  # enable pin (LOW to enable)

STEPS_PER_MM_DEFAULT = 19.0375

DEFAULT_STEP_TYPE = 'Full'
STEP_TYPES = ['Full', 'Half', "1/4", '1/8', '1/16', '1/32']

DEFAULT_STEP_DELAY = .0005
FAST_STEP_DELAY = 0.00001
DEFAULT_SPEED = 99
SEED_TO_DELAY_DIFFERENCE = 100000

MIN_DELAY = 0.00099
MAX_DELAY = 0.00001


def speed_to_delay(speed):
    if 1 <= speed <= 99:
        return speed / SEED_TO_DELAY_DIFFERENCE
    else:
        raise Exception('Speed needs to be in limits from 1 to 99')


# Declare a instance of class pass GPIO pins numbers and the motor type
GPIO.setmode(GPIO.BCM)
GPIO.setup(EN_pin, GPIO.OUT)  # set enable pin as output
motor = RpiMotorLib.A4988Nema(direction, step, (21, 21, 21), "DRV8825")


def is_set_type_valid(step_type):
    return step_type in STEP_TYPES


def move_motor_to_steps(steps, step_type, step_delay, movement_done):
    try:
        # pull enable to low to enable motor
        GPIO.output(EN_pin, GPIO.LOW)

        motor.motor_go(steps > 0,  # True=Clockwise, False=Counter-Clockwise
                       step_type,  # Step type (Full,Half,1/4,1/8,1/16,1/32)
                       abs(steps),  # number of steps
                       step_delay,  # step delay [sec]
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
        # RPi.GPIO.output(EN_pin, RPi.GPIO.HIGH)
        motor.motor_stop()
    except Exception as E:
        print("MOTOR FAILED TO STOP")
        print(E)
        pass


def check_start_sensor_to_stop_motor(movement_done):
    while True:
        if bool(get_limit_switch_state()):
            stop_motor()
            movement_done()
            break
        else:
            time.sleep(0.1)


class MotorState:
    def __init__(self, motor_position, is_motor_moving):
        self.motor_position = motor_position
        self.is_motor_moving = is_motor_moving

    def motor_movement_complete(self, moved_steps):
        self.motor_position = moved_steps
        self.is_motor_moving = False

    def is_motor_at_start(self):
        return self.motor_position is 0 and bool(get_limit_switch_state())

    def move_motor_to_distance(self, distance_to_move, steps_per_mm, step_type, step_delay):
        self.is_motor_moving = True
        steps_to_move = int((float(distance_to_move) * 10) * int(steps_per_mm))
        steps_to_move_from_current_position = self.motor_position - steps_to_move
        motor_thread = Thread(
            target=lambda: move_motor_to_steps(steps_to_move_from_current_position, step_type, step_delay,
                                               lambda: self.motor_movement_complete(steps_to_move)))
        motor_thread.start()

    def move_motor_to_start(self):
        self.is_motor_moving = True
        # 4 meters
        steps_to_move = int((400 * 10) * int(STEPS_PER_MM_DEFAULT))
        motor_thread = Thread(
            target=lambda: move_motor_to_steps(-steps_to_move, DEFAULT_STEP_TYPE, FAST_STEP_DELAY,
                                               lambda: print('MOTOR STOP BY SWITCH')))
        motor_thread.start()
        motor_stop_thread = Thread(
            target=lambda: check_start_sensor_to_stop_motor(lambda: self.motor_movement_complete(0))
        )
        motor_stop_thread.start()
