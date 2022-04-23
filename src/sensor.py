import RPi.GPIO as GPIO

sensor_pin = 25

# Declare a instance of class pass GPIO pins numbers
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # set sensor pin as input


def get_limit_switch_state():
    return GPIO.input(sensor_pin)
