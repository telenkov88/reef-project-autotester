from flask import Flask, redirect, url_for, request, render_template, jsonify, make_response
import subprocess
import datetime
import os
app = Flask(__name__)
from stepper import *

pump0 = StepperPumps(0)
pump1 = StepperPumps(1)
pump2 = StepperPumps(2)
pump3 = StepperPumps(3)

global last_steps


def execute(command, debug=True):
    # subprocess.Popen for python >= 3.6 or subprocess.run for python < 3.6
    if debug:
        print(datetime.datetime.now().strftime("%H:%M:%S"), command)

    result = subprocess.run([command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out = result.stdout.decode('utf-8', errors='ignore').split(os.linesep)
    err = result.stderr.decode('utf-8', errors='ignore').split(os.linesep)
    if debug:
        for line in out:
            print(line.rstrip())
        for line in err:
            print(line.rstrip())
    code = result.returncode
    return [code, out, err]  # return list [stdout, stderr, returncode]

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/start_pump0', methods=['POST'])
def start_pump0():
    print(request)
    data = request.get_json(force=True)
    print(data)
    if "Run" in data["command"]:
        pump0.start(1000, 1)
        resp = jsonify(success=True)
        return resp
    elif "Stop" in data["command"]:
        pump0.stop()
        resp = jsonify(success=True)
        return resp


@app.route('/start_pump1', methods=['POST'])
def start_pump1():
    print(request)
    data = request.get_json(force=True)
    print(data)
    if "Run" in data["command"]:
        pump1.start(1000, 1)
        resp = jsonify(success=True)
        return resp
    elif "Stop" in data["command"]:
        pump1.stop()
        resp = jsonify(success=True)
        return resp


@app.route('/start_pump2', methods=['POST'])
def start_pump2():
    print(request)
    data = request.get_json(force=True)
    print(data)
    if "Run" in data["command"]:
        pump2.start(10000, 1)
        resp = jsonify(success=True)
        return resp
    elif "Stop" in data["command"]:
        pump2.stop()
        resp = jsonify(success=True)
        return resp


@app.route('/start_pump3', methods=['POST'])
def start_pump3():
    print(request)
    data = request.get_json(force=True)
    print(data)
    if "Run" in data["command"]:
        pump3.start(1000, 1)
        resp = jsonify(success=True)
        return resp
    elif "Stop" in data["command"]:
        pump3.stop()
        resp = jsonify(success=True)
        return resp


@app.route('/get_count', methods=['POST'])
def get_count():
    print()
    print()
    print("get_count", request)
    data = request.get_json(force=True)
    print("get_count:", data)
    resp = jsonify(success=True)
    return resp

@app.route('/calibrate', methods=['POST'])
def calibrate():
    print()
    print()
    print("Cal_request", request)
    data = request.get_json(force=True)
    print("Calibrate", data)
    return 'OK'
    #resp = jsonify(success=True)
    #return resp


if __name__ == '__main__':
    init_gpio()
    last_steps = [0, 0, 0, 0]
    app.run(host="10.123.0.200")




