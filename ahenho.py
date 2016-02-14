#!/usr/bin/python

import sys
from datetime import datetime
from flask import Flask, render_template, request, g, redirect, url_for, json, jsonify, logging, make_response
from json import dumps


from hardware import Temperature, HenTime, get_available_tasks

import logging
from logging.handlers import RotatingFileHandler



app = Flask(__name__)


#==============================================================
# preliminary API wrappers
#
@app.route('/')
def root():
    return redirect(url_for('to_api'))

@app.route('/api/')
def to_api():
    return redirect(url_for('current_api'))

@app.route('/api/current/')
def current_api():
    return redirect(url_for('mainpage'))


@app.route('/api/1.0/', methods=['GET'])
def mainpage():
    return render_template('index.html', functions_available=get_available_tasks())

#==============================================================
# temperature API
#
@app.route('/api/1.0/temperature/', methods=['GET'])
def our_temperature():
    tmp = Temperature.get()
    app.logger.info("temperature is %s", tmp)
    return tmp

#==============================================================
# time API
#
@app.route('/api/1.0/time/', methods=['GET', 'POST'])
def our_time():
    if request.method == 'POST':
        app.logger.info("need to set time to %s", request.data)
        return HenTime.set(request.data)
    else:
        return HenTime.get()


#==============================================================
# door API
#
# GET - return JSON with all schedule items
# DELETE - delete one of the items
# POST - add new schedule item
# PUT - replace schedule item ( edit)
#
# every item have fields:
# id - original int code
# state - enabled/disabled
# from - begin time
# to - end time
#
@app.route('/api/1.0/jobs', methods=['GET', 'POST', 'DELETE'])
def all_jobs():
    if request.method == 'GET':
        return make_response(dumps( [
            { 'idx' : '1', 'enabled' : 'on', 'hour' : '08', 'minute' : '10', 'description' : 'door_up' },
            { 'idx' : '2', 'enabled' : 'on', 'hour' : '11', 'minute' : '11', 'description' : 'lamp 1 on' },
            { 'idx' : '3', 'enabled' : 'off', 'hour' : '21', 'minute' : '23', 'description' : 'door_down' }
        ] ))
    elif request.method == 'POST':
        app.logger.info('got a post request to add a new job')
        pass
    elif request.method == 'DELETE':
        app.logger.info('got a post request to delete a job with contents: %s', request.data)
        pass

    return ''


@app.route('/api/1.0/jobs/<int:idx>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def job_by_idx(idx):
    if request.method == 'GET':
        app.logger.info('got a get request to return a job data with idx: %s', idx)
        pass
    elif request.method == 'POST':
        app.logger.info('got a post request to add a new job with idx: %s', idx)
        pass
    elif request.method == 'DELETE':
        app.logger.info('got a post request to delete a job with idx: %s', idx)
        pass
    elif request.method == 'PUT':
        app.logger.info('got a put request to modify a job with idx: %s', idx)
        pass

    return ''



if __name__ == '__main__':
    """ 
    some logging support. all the logged messages will be collected in the file
    """
    handler=RotatingFileHandler('ahenho.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    """
    http://stackoverflow.com/questions/30362950/is-it-possible-to-use-angular-with-the-jinja2-template-engine

    jinia_options = app.jinia_options.copy()
    jinja_options.update(dict(
        block_start_string='<%',
        block_end_string='%>',
        variable_start_string='%%',
        variable_end_string='%%',
        comment_start_string='<#',
        comment_end_string='#>'
    ))
    app.jinja_options = jinja_options
    """


    app.run(debug=True, host='0.0.0.0', port=3080)
