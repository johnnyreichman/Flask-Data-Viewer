import flask
from flask import Flask, render_template, request
import StorageService


app = flask.Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/ChangeOverTime', methods=["GET", "POST"])
def ChangeOverTime():
    state = request.args['state']
    race = request.args['race']
    district = request.args['district']
    elections = StorageService.GetElectionsOverTime(state.upper(),race.upper(),district)
    Templatehtml = render_template('overtime.html', hiVar= "johnny")
    return flask.jsonify({"html": Templatehtml, "elections": elections })

@app.route('/ChangeState', methods=["GET", "POST"])
def ChangeState():
    state = request.args['state']
    race = request.args['race']
    district = request.args['district']
    elections = StorageService.GetElectionsOverTime(state.upper(),race.upper(),district)
    Templatehtml = render_template('overtimegraph.html', hiVar= "johnny")
    return flask.jsonify({"html": Templatehtml, "elections": elections })


def hello():
    return render_template('dashboard.html')

@app.route('/Dashboard', methods=["GET"])
def LoadDashboard():
    templateHtml = render_template('dashboard.html')
    return flask.jsonify({"html": templateHtml})

@app.route('/Home', methods=["GET"])
def GoHome():
    templateHtml = render_template('welcome.html')
    return flask.jsonify({"html": templateHtml})


if __name__ == '__main__':
    #start all of out thingies
    app.run(host='localhost', port=3000, debug=True)
