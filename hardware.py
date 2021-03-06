#!/usr/bin/python

import datetime

from crontab import CronTab
from datetime import time, datetime
from subprocess import call, check_output

class Temperature():
    """
    Temperature control for A-hen-ho management console. As far a temperature 
    can't be set from outside, there is only one method available
    """
    @staticmethod
    def get():
        res_text = ''
        try:
            res_text = check_output(['/usr/local/bin/get_temperature'], shell=True)
        except CalledProcessError as e:
            res_text = e.output

        return res_text

class HenTime():
    """
    Time control for A-hen-ho management console. teh time can be requested and set
    using this class functionality
    """
    @staticmethod
    def get():
        return datetime.now().isoformat()

    @staticmethod
    def set(time):
        res_text = 'was there'
        try:
            res_text = check_output('/usr/local/bin/set_time "%s"' % time, shell=True)
        except CalledProcessError as e:
            res_text = e.output

        return res_text


""" ========================================================================== """

"""
an associative map between the tasks descrition - a text visible to a user
and task command - the command to execute for a task
"""
hen_tasks = {
    'Lift door up' : '/usr/local/bin/door_up',
    'Put door down' : '/usr/local/bin/door_down',
    'Switch lamp 0 on' : '/usr/local/bin/relay 0 on',
    'Switch lamp 0 off' : '/usr/local/bin/relay 0 off',
    'Switch lamp 1 on' : '/usr/local/bin/relay 1 on',
    'Switch lamp 1 off' : '/usr/local/bin/relay 1 off',
    'Switch lamp 2 on' : '/usr/local/bin/relay 2 on',
    'Switch lamp 2 off' : '/usr/local/bin/relay 2 off',
    'Switch lamp 3 on' : '/usr/local/bin/relay 3 on',
    'Switch lamp 3 off' : '/usr/local/bin/relay 3 off',
    'Switch lamp 4 on' : '/usr/local/bin/relay 4 on',
    'Switch lamp 4 off' : '/usr/local/bin/relay 4 off',
    'Switch lamp 5 on' : '/usr/local/bin/relay 5 on',
    'Switch lamp 5 off' : '/usr/local/bin/relay 5 off'
}


def get_available_tasks():
    """ return a list of the possible tasks as their descriptions list """
    descriptions = hen_tasks.keys()
    descriptions.sort()
    return descriptions

def get_description_by_command(cmd):
    """ return a description by it's commmand text """
    return hen_tasks.keys()[ hen_tasks.values().index( cmd )]


def create_task( idx, cmd, hour, minute, enabled ):
    """ create the task object used for communication witha  frontend """
    return {
        'idx' : idx,
        'command' : cmd,
        'hour' : hour,
        'minute' : minute,
        'enabled' : enabled
    }


class HenTasks:
    """ this class is responsible for communication with a frontend.
    it executes all the frontend wiched and supplies it with necessary information
    """

    def __init__(self):
        self.__cron = HenCron()


    def get_all_tasks(self):
        """ return list of the all jobs created in the system """
        result = []
        for job in self.__cron.get_jobs():
            result.append({
                'idx' : job['idx'],
                'description' : get_description_by_command( job['command']),
                'hour' : job['hour'],
                'minute' : job['minute'],
                'enabled' : 'on' if job['enabled'] else 'off'
            })

        return result

    def add_new_task(self, description, hour, minute, enabled):
        """ add a new task. returns a created job object. this should be 
        valid job object to notify frontend about successfull creation
        """
        idx = self.__cron.new_job( create_task(
            0, hen_tasks[ description ], 
            hour, minute, ( enabled == 'on' )))

        return {
            'idx' : idx,
            'description' : description,
            'hour' : hour,
            'minute' : minute,
            'enabled' : enabled
        }


    def delete_task(self, idx):
        """ delete task by it's idx """
        self.__cron.delete_job( idx )

    def update_task(self, idx, description, hour, minute, enabled):
        """ update task configuration without changing it's idx.
        should return valid job object to notify frontend about 
        operation success
        """
        self.__cron.update_job( create_task(
            idx, hen_tasks[ description ], 
            hour, minute, ( enabled == 'on' )))

        return {
            'idx' : idx,
            'description' : description,
            'hour' : hour,
            'minute' : minute,
            'enabled' : enabled
        }

class HenCron:
    def __init__(self):
        self.__cron = CronTab(user=True)
        self.__cron.read()

        comments = [ int( idx ) for idx in self.__cron.comments ]
        if 0 == len( comments ):
            self.__next_idx = 0
        else:
            self.__next_idx = max( comments ) + 1


    def get_jobs(self):
        jobs = []
        for job in self.__cron:
            jobs.append({
                'command': job.command,
                'idx': job.comment,
                'hour': int( str( job.hour)),
                'minute' : int( str( job.minute)),
                'enabled' : job.is_enabled()
            })
        return jobs

    def new_job(self, job):
        idx = None
        if job['command'] and job['hour'] and job['minute']:
            idx = self.__next_idx
            self.__next_idx += 1

            jobc = self.__cron.new( command = job['command'], comment = str( idx ) )
            jobc.hours.on( job['hour'] )
            jobc.minute.on( job['minute'] )
            jobc.enable( job['enabled'] if job['enabled'] else False )

            self.__cron.write()

        return idx

    def update_job(self, job):
        if job['command'] and job['hour'] and job['minute']:
            jobc = list( self.__cron.find_comment( str( job['idx'] )))
            if len(jobc):
                jobc[0].hour.on( job['hour'] )
                jobc[0].minutes.on( job['minute'] )
                jobc[0].enable( job['enabled'] if job['enabled'] else False )
                self.__cron.write()


    def delete_job(self, idx):
        self.__cron.remove_all( comment = str(idx) )
        self.__cron.write()



"""

#=====================================================================
# crontab file can be only one per user. user must be in 'cron' group
# crontab module can make a list of the crons by filetring commands
# the comment of the command should contain ID
#
#

"""
