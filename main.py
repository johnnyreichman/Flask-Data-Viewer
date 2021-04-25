import flask
from flask import Flask, render_template, request
import StorageService


app = flask.Flask(__name__)

@app.route('/')
def hello():
    return render_template('dashboard.html')

@app.route('/ChangeOverTime', methods=["GET", "POST"])
def ChangeOverTime():
    state = request.args['state']
    elections = StorageService.GetSenateOverTime(state.upper())
    Templatehtml = render_template('overtime.html', hiVar= "johnny")
    return flask.jsonify({"html": Templatehtml, "elections": elections })

@app.route('/ChangeState', methods=["GET", "POST"])
def ChangeState():
    state = request.args['state']
    elections = StorageService.GetSenateOverTime(state.upper())
    Templatehtml = render_template('overtimegraph.html', hiVar= "johnny")
    return flask.jsonify({"html": Templatehtml, "elections": elections })


def hello():
    return render_template('dashboard.html')

@app.route('/Dashboard', methods=["GET"])
def LoadDashboard():
    StorageService.LoadDashboard(id,name,age,state,othernum)
    return flask.jsonify("hi")


if __name__ == '__main__':
    #start all of out thingies
    app.run(host='localhost', port=3000, debug=True)
