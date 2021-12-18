try:
    import RPi.GPIO
except (RuntimeError, ModuleNotFoundError):
    import fake_rpigpio.utils

    fake_rpigpio.utils.install()

from RpiMotorLib import RpiMotorLib

direction = 22  # Direction (DIR) GPIO Pin
step = 23  # Step GPIO Pin
EN_pin = 24  # enable pin (LOW to enable)

STEPS_PER_MM_DEFAULT = 19.0375

DEFAULT_STEP_TYPE = 'Full'
STEP_TYPES = ['Full', 'Half', "1/4", '1/8', '1/16', '1/32']

DEFAULT_STEP_DELAY = .0005

# Declare a instance of class pass GPIO pins numbers and the motor type
try:
    motor = RpiMotorLib.A4988Nema(direction, step, (21, 21, 21), "DRV8825")
    RPi.GPIO.cleanup()  # clear GPIO allocat
    RPi.GPIO.setup(EN_pin, RPi.GPIO.OUT)  # set enable pin as output
except Exception as error:
    print(error)
    pass


def motor_move(cm, steps_per_mm, step_type, step_delay):
    try:
        steps = (float(cm) * 10) * int(steps_per_mm)
        steps = int(steps)
        print("Steps %f" % steps)
        # pull enable to low to enable motor
        RPi.GPIO.output(EN_pin, RPi.GPIO.LOW)

        motor.motor_go(steps > 0,  # True=Clockwise, False=Counter-Clockwise
                       step_type,  # Step type (Full,Half,1/4,1/8,1/16,1/32)
                       abs(steps),  # number of steps
                       step_delay,  # step delay [sec]
                       False,  # True = print verbose output
                       .05)  # initial delay [sec]
    except Exception as E:
        print("FAILED TO MOVE")
        print(E)
        pass


def is_set_type_valid(step_type):
    return step_type in STEP_TYPES
