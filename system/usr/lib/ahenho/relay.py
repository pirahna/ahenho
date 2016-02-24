#!/usr/bin/env python2

from time import sleep
import RPi.GPIO as GPIO
import argparse
import syslog

relay_pins = [ 21, 22, 10, 9, 11, 7 ]
task_value = { 'on' : GPIO.LOW, 'off' : GPIO.HIGH }


if __name__ == '__main__':
    syslog.openlog(logoption=syslog.LOG_PID, facility=syslog.LOG_LOCAL7)

    parser = argparse.ArgumentParser(description='Manage relays')
    parser.add_argument('relays', nargs='+', type=int, choices=range(0,6))
    parser.add_argument('task', choices=['on', 'off'])
    args = parser.parse_args()

    syslog.syslog(
        syslog.LOG_INFO, 
        'Start managing relays: [{0}] {1}'.format( str( args.relays ).strip('[]'), args.task))

    if ( args.task and args.relays ):
        try:
            GPIO.setmode( GPIO.BCM )
            GPIO.setwarnings( False )

            GPIO.setup( relay_pins, GPIO.OUT )
            GPIO.output( [ relay_pins[ relay ] for relay in args.relays ], task_value[ args.task ])

        except:
            syslog.syslog( syslog.LOG_ERR, 'exception on the set relay pins')

        finally:
            # GPIO.cleanup( relay_pins )
            syslog.syslog( syslog.LOG_INFO, 'switching relays complete')

