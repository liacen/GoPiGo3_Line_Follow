#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
from builtins import input

import line_sensor
import time
import easygopigo3 as easy
import atexit

egpg3 = easy.EasyGoPiGo3()

atexit.register(egpg3.stop)  # When you ctrl-c out of the code, it stops the gopigo motors.

# Calibrate speed at first run
# 100 is good with fresh batteries
# 125 for batteries with half capacity

fwd_speed = 1000  # Forward speed at which the GoPiGo should run.
# If you're swinging too hard around your line
# reduce this speed.
poll_time = 0.01  # Time between polling the sensor, seconds.

slight_turn_speed = int(.7 * fwd_speed)
turn_speed = int(.7 * fwd_speed)

last_val = [0] * 5  # An array to keep track of the previous values.
curr = [0] * 5  # An array to keep track of the current values.

egpg3.set_speed(fwd_speed)

gpg_en = 1  # Enable/disable gopigo
msg_en = 1  # Enable messages on screen.  Turn this off if you don't want messages.

# Get line parameters
line_pos = [0] * 5
white_line = line_sensor.get_white_line()
black_line = line_sensor.get_black_line()
range_sensor = line_sensor.get_range()
threshold = [a + b / 2 for a, b in
             zip(white_line, range_sensor)]  # Make an iterator that aggregates elements from each of the iterables.

# Position to take action on
mid = [0, 0, 1, 0, 0]  # Middle Position.
mid1 = [0, 1, 1, 1, 0]  # Middle Position.
small_l = [0, 1, 1, 0, 0]  # Slightly to the left.
small_l1 = [0, 1, 0, 0, 0]  # Slightly to the left.
small_r = [0, 0, 1, 1, 0]  # Slightly to the right.
small_r1 = [0, 0, 0, 1, 0]  # Slightly to the right.
left = [1, 1, 0, 0, 0]  # Slightly to the left.
left1 = [1, 0, 0, 0, 0]  # Slightly to the left.
right = [0, 0, 0, 1, 1]  # Sensor reads strongly to the right.
right1 = [0, 0, 0, 0, 1]  # Sensor reads strongly to the right.
stop = [1, 1, 1, 1, 1]  # Sensor reads stop.
stop1 = [0, 0, 0, 0, 0]  # Sensor reads stop.


# Converts the raw values to absolute 0 and 1 depending on the threshold set
def absolute_line_pos():
    raw_vals = line_sensor.get_sensorval()
    for i in range(5):
        if raw_vals[i] > threshold[i]:
            line_pos[i] = 1
        else:
            line_pos[i] = 0
    return line_pos


# GoPiGo actions
def go_straight():
    if msg_en:
        print("Going straight")
    if gpg_en:
        egpg3.set_speed(fwd_speed)
        egpg3.forward()


def turn_slight_left():
    if msg_en:
        print("Turn slight left")
    if gpg_en:
        # egpg3.set_right_speed(slight_turn_speed)
        # egpg3.set_left_speed(fwd_speed)
        # egpg3.fwd()
        egpg3.left()


def turn_left():
    if msg_en:
        print("Turn left")
    if gpg_en:
        egpg3.set_speed(turn_speed)
        egpg3.left()


def turn_slight_right():
    if msg_en:
        print("Turn slight right")
    if gpg_en:
        # egpg3.set_right_speed(fwd_speed)
        # egpg3.set_left_speed(slight_turn_speed)
        # egpg3.fwd()
        egpg3.right()


def turn_right():
    if msg_en:
        print("Turn right")
    if gpg_en:
        egpg3.set_speed(turn_speed)
        egpg3.right()


def stop_now():
    if msg_en:
        print("Stop")
    if gpg_en:
        egpg3.stop()


def go_back():
    if msg_en:
        print("Go Back")
    if gpg_en:
        egpg3.set_speed(turn_speed)
        egpg3.backward()


# Action to run when a line is detected
def run_gpg(curr):
    # if the line is in the middle, keep moving straight
    # if the line is slightly left of right, keep moving straight
    if curr == small_r or curr == small_l or curr == mid or curr == mid1:
        go_straight()

    # If the line is towards the sligh left, turn slight right
    elif curr == small_l1:
        turn_slight_right()
    elif curr == left or curr == left1:
        turn_right()

    # If the line is towards the sligh right, turn slight left
    elif curr == small_r1:
        turn_slight_left()
    elif curr == right or curr == right1:
        turn_left()
    elif curr == stop:
        stop_now()
    time.sleep(poll_time)


try:
    while True:
        last_val = curr
        curr = absolute_line_pos()
        print(curr)

        # white line reached
        if curr == stop1:
            if msg_en:
                print("White found, last cmd running")
            for i in range(5):
                run_gpg(last_val)
        else:
            run_gpg(curr)
except KeyboardInterrupt:
    print("--> Input Ctrl + C")
    egpg3.stop()
    egpg3.reset_all()
