import os
from setuptools import setup
from nvpy import nvpy

setup(
    name = "flask-stepper-controll",
    version = "1.0",
    author = "Ognjen Lazic",
    author_email = "laogdo@gmail.com",
    description = "Control stepper over local network",
    license = "",
    packages=['app'],
    entry_points = {
        'console_scripts' : ['app = app.app:main']
    },
)
