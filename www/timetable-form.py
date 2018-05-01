from flask import Flask, render_template,Response,request,jsonify
from datetime import datetime

from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
import sys
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


sensors_list = list()
speed_list = dict()

current_point = ''

@app.route("/api/timetable-config")
def timetable_config():
    args = dict(request.args)
    resp = dict()
    try:
        duration = args['duration'][0]
        station = args['station'][0]
        time_at_station = args['time_at_station'][0]

        resp['duration'] = int(duration)*60
        resp['station'] = int(station)
        resp['time_at_station'] = int(time_at_station)
        resp['status'] = 'OK'
    except:
        print("Wrong arguments")
        resp['status'] = 'ERR'

    return Response(json.dumps(resp), mimetype='application/json')

@app.route("/api/sensors-list-update",methods=['POST'])
def sensors_list_update():
    resp = dict()
    args = dict(request.form)['update'][0]
    # args = dict(request.args)

    resp['status'] = 'ERROR'

    try:
        sensors_list = args.split("\n")
        # duration = args['duration'][0]
        # station = args['station'][0]
        # time_at_station = args['time_at_station'][0]
        #
        # resp['duration'] = int(duration)*60
        # resp['station'] = int(station)
        # resp['time_at_station'] = int(time_at_station)
        resp['list'] = sensors_list
        resp['size'] = len(sensors_list)
        resp['status'] = 'OK'
    except:
        print("Wrong arguments")
        resp['status'] = 'ERR'
    return Response(json.dumps(resp), mimetype='application/json')

@app.route("/api/get-current-point",methods=['GET'])
def get_current_point():
    resp = dict()
    resp['point']=current_point
    return Response(json.dumps(resp), mimetype='application/json')

@app.route("/api/get-current-speed",methods=['GET'])
def get_current_speed():
    resp = dict()
    print(current_point)
    resp['speed']=speed_list[current_point]
    return Response(json.dumps(resp), mimetype='application/json')

@app.route("/api/get-all-speed",methods=['GET'])
def get_all_speed():
    resp = dict()
    resp['list']=speed_list
    return Response(json.dumps(resp), mimetype='application/json')



@app.route("/api/set-current-point",methods=['GET'])
def set_current_point():
    global current_point
    args = dict(request.args)
    resp = dict()
    try:
        current_point = args['point'][0]
        resp['status'] = 'OK'
        print(current_point)
    except:
        print("Wrong arguments")
        resp['status'] = 'ERR'

    return Response(json.dumps(resp), mimetype='application/json')

@app.route("/api/set-current-speed",methods=['GET'])
def set_current_speed():
    global speed_list
    global current_point
    args = dict(request.args)
    resp = dict()
    try:
        point = args['point'][0]
        speed = args['speed'][0]
        current_point = point
        speed_list[point] = float(speed)
        resp['status'] = 'OK'
    except:
        print("Wrong arguments")
        resp['status'] = 'ERR'

    return Response(json.dumps(resp), mimetype='application/json')



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7654)
