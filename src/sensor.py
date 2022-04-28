import RPi.GPIO as GPIO

SENSOR_PIN = 25

# Declare a instance of class pass GPIO pins numbers
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # set sensor pin as input


def get_limit_switch_state():
    return GPIO.input(SENSOR_PIN)
