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
    return hen_tasks.keys()


class HenTask:
    def __init__(self, command, description, idx, hour, minute, enabled):
        self.idx = idx
        self.hour = hour
        self.minute = minute
        self.enabled = enabled
        self.command = command
        self.description = description

    def to_crontab(self, cron):
        job = cron.new( command = self.command, comment = self.idx )
        job.hour.on( self.hour )
        job.minute.on( self.minute )
        job.enable( self.enable )


"""
class HenTaskFactory:
    def __init__(self, command, description):
        self.command = command
        self.description = description

    def create(self, idx, hour, minute, enabled):
        return HenTask( self.command, self.description, idx, hour, minute, enabled )
"""









"""
class Tasker:
    hen_tasks = [
        HenTask('Lift door up', '/usr/local/bin/door_up'),
        HenTask('Put door down', '/usr/local/bin/door_down'),
        HenTask('Switch lamp 0 on', '/usr/local/bin/relay 0 on'),
        HenTask('Switch lamp 0 off', '/usr/local/bin/relay 0 off'),
        HenTask('Switch lamp 1 on', '/usr/local/bin/relay 1 on'),
        HenTask('Switch lamp 1 off', '/usr/local/bin/relay 1 off'),
        HenTask('Switch lamp 2 on', '/usr/local/bin/relay 2 on'),
        HenTask('Switch lamp 2 off', '/usr/local/bin/relay 2 off'),
        HenTask('Switch lamp 3 on', '/usr/local/bin/relay 3 on'),
        HenTask('Switch lamp 3 off', '/usr/local/bin/relay 3 off'),
        HenTask('Switch lamp 4 on', '/usr/local/bin/relay 4 on'),
        HenTask('Switch lamp 4 off', '/usr/local/bin/relay 4 off'),
        HenTask('Switch lamp 5 on', '/usr/local/bin/relay 5 on'),
        HenTask('Switch lamp 5 off', '/usr/local/bin/relay 5 off'),
    ]

    def set_tasks(self, tasks):
        cron = CronTab(user=True)
        cron.remove_all()

        for task in tasks:
            pass

        cron.write()

    def get_tasks(self):
        return None

def get_available_tasks():
    tasks = []
    for tsk in Tasker.hen_tasks:
        tasks.append( tsk.description )
    return tasks


class Crons:
    # this class gives a control over the user's crontab file
    # this class can operate with a crons, related to the different
    # factories and with different id's

    # the job has follwing fields:
    # from - start time 
    # upto - end time
    # factory - command
    # idx - job index, original and always incremented
    def __job_to_dict(self, job):
        return {
            'idx'   : job.comment,
            'hour' : job.hour,
            'mint'  : job.minute,
            'cmd'   : job.command,
            'enable': job.is_enabled
        }

    def __init__(self):
        self.__crontab = CronTab( user = True )
        self.__crontab.read()
        self.__next_id = max( [ int( idx ) for idx in self.__crontab.comments ] ) + 1

    def get_jobs_list( self, factory ):
        return [ self.__job_to_dict( job ) for job in self.__crontab.find_command( factory ) ]

    def get_job( self, idx ):
        return self.__crontab.find_comment( str(idx.toString) )

    def delete_job( self, idx ):
        self.__crontab.remove_all( comment = str(idx.toString) )
        self.__crontab.write()

    def add_job( self, factory, params ):
        idx = None
        if params['cmd'] and params['hour'] and params['mint']:
            idx = self.__next_id
            ++self.__next_id
            job = self.__crontab.new( command = params['cmd'], comment = str( idx ) )
            job.hours.on( params['hour'] )
            job.minute.on( params['mint'] )
            if params['enable']:
                job.enable( params['enable'] )
            self.__crontab.write()

        return idx

    def change_job( self, params ):
        if params['cmd'] and params['hour'] and params['mint'] and params['idx']:
            job = self.__crontab.find_comment( params['idx'] )
            if job:
                job.hours.on( params['hour'] )
                job.minutes.on( params['mint'] )
                job.enable( params['enable'] )



#=====================================================================
# crontab file can be only one per user.
# crontab module can make a list of the crons by filetring commands
# the comment of the command should contain ID
#
#

"""