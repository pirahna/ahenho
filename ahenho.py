#!/usr/bin/python

import sys
from datetime import datetime
from flask import Flask, render_template, request, g, redirect, url_for, json, jsonify, logging, make_response
from json import dumps


from hardware import Temperature, HenTime, get_available_tasks, HenTasks

import logging
from logging.handlers import RotatingFileHandler



app = Flask(__name__)
tasks = HenTasks()


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
        return make_response( dumps( tasks.get_all_tasks() ))

    elif request.method == 'POST':
        params = request.get_json( force=True )
        return jsonify( tasks.add_new_task(
            params['description'], 
            params['hour'],
            params['minute'],
            params['enabled'] 
        ))

    elif request.method == 'DELETE':
        app.logger.info('got a post request to delete a job with contents: %s', request.data)
        pass

    return ''


@app.route('/api/1.0/jobs/<int:idx>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def job_by_idx(idx):
    if request.method == 'GET':
        app.logger.info('got a get request to return a job data with idx: %s', idx)
        pass

    elif request.method == 'DELETE':
        tasks.delete_task( idx )
        return ''

    elif request.method == 'PUT' or request.method == 'POST':
        params = request.get_json( force=True )
        return jsonify( tasks.update_task(
            idx,
            params['description'],
            params['hour'],
            params['minute'],
            params['enabled'] 
        ))

    return ''



if __name__ == '__main__':
    """ 
    some logging support. all the logged messages will be collected in the file
    """
    """
    handler=RotatingFileHandler('ahenho.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    """

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
