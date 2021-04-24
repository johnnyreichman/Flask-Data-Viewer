import flask
from flask import Flask, render_template, request
import StorageService


app = flask.Flask(__name__)

class OverTimeData:
  def __init__(self, html, dates):
    self.html = html
    self.dates = dates

@app.route('/')
def hello():
    return render_template('dashboard.html')

@app.route('/ChangeOverTime', methods=["GET", "POST"])
def ChangeOverTime():
    state = request.args['state']
    elections = StorageService.GetSenateOverTime(state.upper())
    print(elections[5])
    data = OverTimeData("", [])
    Templatehtml = render_template('overtime.html', hiVar= "johnny")
    return flask.jsonify({"html": Templatehtml, "elections": elections })


def hello():
    return render_template('dashboard.html')

@app.route('/AddRow', methods=["POST"])
def AddRowToDb():
    id = request.form['id']
    name = request.form['name']
    age = request.form['age']
    state = request.form['state']
    othernum = request.form['othernum']
    print(id)
    print(name)
    print(state)
    print(othernum)
    StorageService.AddRow(id,name,age,state,othernum)
    return flask.jsonify("hi")


if __name__ == '__main__':
    #start all of out thingies
    app.run(host='localhost', port=3000, debug=True)
