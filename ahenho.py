#!/usr/bin/python

import sys
from datetime import datetime
from flask import Flask, render_template, request, g, redirect, url_for, json, jsonify
from hardware import Temperature, Door, Lamps


app = Flask(__name__)
door = Door
lamps = Lamps

#==============================================================
# preliminary API wrappers
#
@app.route('/')
def to_api():
    return redirect(url_for('to_api_version'))

@app.route('/api/')
def to_api_version():
    return redirect(url_for('mainpage'))

@app.route('/api/1.0/', methods=['GET'])
def mainpage():
    return render_template('template.html')

#==============================================================
# temperature API
#
@app.route('/api/1.0/temperature/', methods=['GET'])
def our_temperature():
    return Temperature.get()

#==============================================================
# time API
#
@app.route('/api/1.0/time/', methods=['GET', 'POST'])
def our_time():
    if request.method == 'POST':
        pass
    else:
        return datetime.now().isoformat()

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
@app.route('/api/1.0/schedule/door/', methods=['GET', 'POST', 'DELETE', 'PUT'])
def door_schedule():
    if request.method == 'POST':
        pass
    elif request.method == 'PUT':
        pass
    elif request.method == 'GET':
        pass
    elif request.method == 'DELETE':
        pass
    return ''

#==============================================================
# lamps API
#
@app.route('/api/1.0/schedule/lamp/<number>/', methods=['GET', 'POST'])
def lamp_schedule(number=None):
    if request.method == 'POST':
        pass
    else:
        return datetime.now().isoformat()




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
#    app.run(debug=True)
