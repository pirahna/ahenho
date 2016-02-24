#!/usr/bin/env python2

from time import sleep
from sys import exit
import RPi.GPIO as GPIO
import syslog


door_button = 24
motor_relays = [ 8, 25 ]

def stop_motor():
    GPIO.output(motor_relays, GPIO.HIGH)
    syslog.syslog(syslog.LOG_INFO, 'motor stoppeded')

def start_motor():
    GPIO.output(motor_relays, (GPIO.LOW, GPIO.HIGH))
    syslog.syslog(syslog.LOG_INFO, 'motor started')


def check_button(channel):

    GPIO.remove_event_detect( channel )

    cnt = 0;
    for i in range(0, 10):
        if GPIO.input( channel ):
            break
        else:
            cnt += 1
        sleep (0.05)

    if cnt >= 9:
        syslog.syslog(syslog.LOG_INFO, 'Got event from the power button, start the poweroff sequence')
        stop_motor()
        exit()
    else:
        GPIO.add_event_detect( channel,
            GPIO.FALLING, callback=check_button, bouncetime=200)


if __name__ == '__main__':
    try:
        syslog.openlog(logoption=syslog.LOG_PID, facility=syslog.LOG_LOCAL7)
        syslog.syslog(syslog.LOG_INFO, 'Start moving door DOWN')

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(motor_relays, GPIO.OUT)
        syslog.syslog(syslog.LOG_INFO, 'set motor relays mode to OUT')

        start_motor()

        GPIO.setup(door_button, GPIO.IN, pull_up_down=GPIO.PUD_UP )
        GPIO.add_event_detect( door_button,
            GPIO.FALLING, callback=check_button, bouncetime=200)

        # do motor 5 min or until sensor will be signalled
        sleep (300000)

        syslog.syslog(syslog.LOG_INFO, 'worked 5 mins without door sensor interruption')

    except KeyboardInterrupt:
        pass

    finally:
        stop_motor()
        GPIO.remove_event_detect(door_button)
        GPIO.cleanup(door_button)
