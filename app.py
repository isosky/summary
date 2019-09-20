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


@app.route('/data_add_v', methods=['POST'])
def data_add_v():
    print(request.get_data())
    json_data = json.loads(request.get_data())
    arg_data = json_data['data']
    arg_type = json_data['type']
    print(arg_data, arg_type)
    if arg_type == 'step':
        if arg_data:
            temp = arg_data.split(';')
            # result = []
            for i in temp:
                ttt = i.split(',')
                print(ttt)
                if len(ttt) > 1:
                    dboo.step_add_one(ttt[0], ttt[1])
        return json.dumps({"result": dboo.getstep()})
    if arg_type == 'weight':
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


@app.route('/addtask', methods=['POST'])
def addtask():
    print(request.get_data())
    json_data = json.loads(request.get_data())
    arg_subject = json_data['subject']
    arg_subsub = json_data['subsub']
    arg_title = json_data['title']
    arg_edate = json_data['edate']
    print(arg_subject, arg_title, arg_edate)
    temp = dboo.addtask(arg_subject, arg_subsub, arg_title, arg_edate)
    return json.dumps({'arrays': temp})

@app.route('/initoption')
def initoption():
    return json.dumps({'task_sub_all_option':dboo.initoption()})


@app.route('/gettasknow')
def gettasknow():
    return json.dumps({'arrays': dboo.gettasknow()})


@app.route('/gettimedata')
def gettimedata():
    return json.dumps(dboo.gettimedata())


@app.route('/finishtask', methods=['POST'])
def finishtask():
    print(request.get_data())
    json_data = json.loads(request.get_data())
    task_id = json_data['task_id']
    input_numbers = json_data['input_numbers']
    dboo.finishtask(task_id, input_numbers)
    return json.dumps({'result': True})


@app.route('/deletetask', methods=['POST'])
def deletetask():
    print(request.get_data())
    json_data = json.loads(request.get_data())
    task_id = json_data['task_id']
    dboo.deletetask(task_id)
    return json.dumps({'result': True})


@app.route('/gettasksummary')
def gettasksummary():
    return dboo.gettasksummary()


@app.route('/querytask', methods=['POST'])
def querytask():
    json_data = json.loads(request.get_data())
    query = json_data['query']
    return json.dumps({'arrays': dboo.querytask(query)})


@app.route('/updatetask', methods=['POST'])
def updatetask():
    print(request.get_data())
    json_data = json.loads(request.get_data())
    task_id = json_data['task_id']
    subsub = json_data['subsub']
    title = json_data['title']
    etime = json_data['etime']
    dboo.updatetask(task_id, subsub, title, etime)
    return json.dumps({'result': True})


@app.route('/removetask')
def removetask():
    return json.dumps({'message':'已从任务中移除'+dboo.removetask()+'条删除的数据'})

if __name__ == '__main__':
    app.run()
