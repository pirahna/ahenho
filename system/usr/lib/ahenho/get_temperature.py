#!/usr/bin/env python2

from w1thermsensor import W1ThermSensor


if __name__ == '__main__':

    sensor = W1ThermSensor()
    print( sensor.get_temperature() )

