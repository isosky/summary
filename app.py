from flask import Flask, render_template, request
import json
import dboo as dboo


app = Flask(__name__)


@app.route('/')
def mainroute():
    return render_template("index.html")


@app.route('/data_add')
def data_add():
    return render_template("data_add.html")


@app.route('/step_add')
def step_add():
    arg_data = request.args.get('data')
    if arg_data:
        temp = arg_data.split(';')
        # result = []
        for i in temp:
            ttt = i.split(',')
            dboo.step_add_one(ttt[0], ttt[1])

    return json.dumps({"result": dboo.getstep()})


if __name__ == '__main__':
    app.run()
