#!/usr/bin/env python

import line_sensor


def get_sensorval():
    while True:
        val = line_sensor.read_sensor()
        if val[0] <> -1:
            return val


print "WHITE LINE SETUP!!"
while True:
    print "Keep all the sensors over a white strip and press [Enter]"
    raw_input()
    print "--> Line sensor value: ",
    get_sensorval()
    print get_sensorval()
    print "If the reading look good, press 'y' and [Enter] to continue"
    inp = raw_input()
    if inp == 'y':
        line_sensor.set_white_line()
        break
print "White Line Values set: ",
print line_sensor.get_white_line()

print "BLACK LINE SETUP!!"
while True:
    print "Keep all the sensors over a black strip and press [Enter]",
    raw_input()
    print "--> Line sensor value: ",
    get_sensorval()
    print get_sensorval()
    print "If the reading look good, press 'y' and [Enter] to continue"
    inp = raw_input()
    if inp == 'y':
        line_sensor.set_black_line()
        break
print "White Line Values set: ",
print line_sensor.get_black_line()
