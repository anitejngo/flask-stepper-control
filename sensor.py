try:
    import RPi.GPIO
except (RuntimeError, ModuleNotFoundError):
    import fake_rpigpio.utils

    fake_rpigpio.utils.install()

sensor_pin = 25

# Declare a instance of class pass GPIO pins numbers
try:
    RPi.GPIO.setup(sensor_pin, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)  # set sensor pin as input
except Exception as error:
    print(error)
    pass


def get_limit_switch_state():
    return RPi.GPIO.input(sensor_pin)
