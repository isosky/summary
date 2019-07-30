from flask import Flask, render_template, request
from flask_cors import CORS
import json
import dboo as dboo


app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/')
def mainroute():
    return render_template("index.html")


@app.route('/data_add')
def data_add():
    return render_template("data_add.html")


@app.route('/data_add_v')
def data_add_v():
    arg_data = request.args.get('data')
    arg_type = request.args.get('type')
    if arg_type == '1':
        if arg_data:
            temp = arg_data.split(';')
            # result = []
            for i in temp:
                ttt = i.split(',')
                print(ttt)
                if len(ttt) > 1:
                    dboo.step_add_one(ttt[0], ttt[1])
        return json.dumps({"result": dboo.getstep()})
    if arg_type == '2':
        if arg_data:
            temp = arg_data.split(';')
            # result = []
            for i in temp:
                ttt = i.split(',')
                print(ttt)
                if len(ttt) > 1:
                    dboo.weight_add_one(ttt[0], ttt[1])
        return json.dumps({"result": dboo.getweight()})


@app.route('/getstep')
def getstep():
    temp = dboo.getstep(False)
    return json.dumps(temp)


@app.route('/getweight')
def getweight():
    temp = dboo.getweight(False)
    return json.dumps(temp)


if __name__ == '__main__':
    app.run()
