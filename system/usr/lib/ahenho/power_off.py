#!/usr/bin/env python3


from time import sleep
from subprocess import call
import RPi.GPIO as GPIO
import syslog


door_button     = 24
power_button    = 23
power_led       = 18

motor_relays    = [ 8, 25 ]
light_relays    = [ 21, 22, 10, 9, 11, 7 ]


def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings( False )
    # initialize inputs. set to output mode, assign low value, set as 
    # inputs afterwards
    GPIO.setup( [ door_button, power_button ], GPIO.OUT, initial=GPIO.LOW )
    GPIO.output( [ door_button, power_button ], GPIO.LOW )
    GPIO.setup( [ door_button, power_button ], GPIO.IN, pull_up_down=GPIO.PUD_UP )
    # initialize as outputs
    GPIO.setup( motor_relays + light_relays + [ power_led ], GPIO.OUT, initial=GPIO.HIGH )
    # switch LED on
    GPIO.output( power_led, GPIO.LOW )


def check_button(channel):

    GPIO.remove_event_detect( power_button )

    cnt = 0;
    for i in range(0, 10):
        if GPIO.input( power_button ):
            break
        else:
            cnt += 1
        sleep (0.05)

    if cnt >= 9:
        syslog.syslog(syslog.LOG_INFO, 'Got event from the power button, start the poweroff sequence')
        call(["sudo", "poweroff"])
    else:
        GPIO.add_event_detect(power_button,
            GPIO.FALLING, callback=check_button, bouncetime=200)


if __name__ == '__main__':

    try:
        syslog.openlog(logoption=syslog.LOG_PID, facility=syslog.LOG_DAEMON)
        syslog.syslog(syslog.LOG_INFO, 'Power-off daemon started')

        init()

        GPIO.add_event_detect(
            power_button,
            GPIO.FALLING, callback=check_button, bouncetime=1200)

        while True:
            sleep(100000)

    finally:
        GPIO.cleanup( [ power_button, power_led ] )

