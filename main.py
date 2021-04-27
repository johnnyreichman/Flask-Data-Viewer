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
    Templatehtml = render_template('interactive.html', hiVar= "johnny")
    return flask.jsonify({"html": Templatehtml, "elections": elections })

@app.route('/UpdateGraph', methods=["GET", "POST"])
def ChangeState():
    state = request.args['state']
    race = request.args['race']
    district = request.args['district']
    elections = StorageService.GetElectionsOverTime(state.upper(),race.upper(),district)
    Templatehtml = render_template('interactivegraph.html', hiVar= "johnny")
    return flask.jsonify({"html": Templatehtml, "elections": elections })

@app.route('/Dashboard', methods=["GET"])
def LoadDashboard():
    pieData = StorageService.GetPopularCandidateData()
    barData = StorageService.GetILTurnout()
    templateHtml = render_template('dashboard.html')
    return flask.jsonify({"html": templateHtml, "pieData": pieData, "barData": barData})

@app.route('/Home', methods=["GET"])
def GoHome():
    templateHtml = render_template('welcome.html')
    return flask.jsonify({"html": templateHtml})


if __name__ == '__main__':
    #start the local server
    app.run(host='localhost', port=3000, debug=True)
