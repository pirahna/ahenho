#!/usr/bin/python

from crontab import CronTab

from datetime import time
from subprocess import call, check_output

class Temperature():
    @staticmethod
    def get():
        res_text = ''
        try:
#            res_text = check_output(['sudo', 'get_temperature'])
            res_text = check_output(['/usr/local/bin/get_temperature'], shell=True)
        except CalledProcessError as e:
            res_text = e.output

        return res_text



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

class Door():
    def _get_job_by_id(id):
        return cronobj.find_comment( id )

    def __init__(self):
        self.state = 0
        self.cron = CronTab(user = True)
        self.read()

    def get(self, id=None):
        return []

    def put(self, item):
        return []

    def delete(self, id):
        return []

    def post(self, item):
        return []




class Lamp():
    def __init__(self):
        pass


class Lamps():
    def __init__(self):
        self.lamps = [ Lamp, Lamp, Lamp, Lamp ]