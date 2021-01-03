#!/usr/bin/python
# -*- coding: utf-8 -*-

# import getlockscreen as ls
import json

from flask import Flask, render_template, request
from flask_cors import CORS

import dboo as dboo
import dboo_yys as dboo_yys

app = Flask(__name__)
CORS(app, supports_credentials=True)

# TODO 将所有的json格式化放到app.py里面


@app.route('/')
def mainroute():
    return render_template("index.html")


@app.route('/data_add')
def data_add():
    return render_template("data_add.html")


@app.route('/addtask', methods=['POST'])
def addtask():
    # print(request.get_data())
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
    temp = dboo.initoption()
    return json.dumps({'task_sub_all_option': temp[0], 'task_select_option': temp[1], 'lastchecktime': temp[2]})


@app.route('/gettasknow')
def gettasknow():
    return json.dumps({'arrays': dboo.gettasknow()})


@app.route('/gettimedata')
def gettimedata():
    return json.dumps(dboo.gettimedata())


@app.route('/finishtask', methods=['POST'])
def finishtask():
    # print(request.get_data())
    json_data = json.loads(request.get_data())
    task_id = json_data['task_id']
    input_finish = json_data['input_finish']
    dboo.finishtask(task_id, input_finish)
    return json.dumps({'result': True})


@app.route('/deletetask', methods=['POST'])
def deletetask():
    # print(request.get_data())
    json_data = json.loads(request.get_data())
    task_id = json_data['task_id']
    dboo.deletetask(task_id)
    return json.dumps({'result': True})


@app.route('/querytask', methods=['POST'])
def querytask():
    json_data = json.loads(request.get_data())
    query = json_data['query']
    subject = json_data['subject']
    subsub = json_data['subsub']
    isqueryall = json_data['isqueryall']
    return json.dumps({'arrays': dboo.querytask(query, subject, subsub, isqueryall)})


@app.route('/updatetask', methods=['POST'])
def updatetask():
    json_data = json.loads(request.get_data())
    # print(json_data)
    task_id = json_data['task_id']
    subject = json_data['subject']
    subsub = json_data['subsub']
    title = json_data['title']
    etime = json_data['etime']
    dboo.updatetask(task_id, subject, subsub, title, etime)
    return json.dumps({'result': True})


@app.route('/removetask')
def removetask():
    return json.dumps({'message': '已从任务中移除'+dboo.removetask()+'条删除的数据'})


@app.route('/gettasksummary_bar')
def gettasksummary_bar():
    return json.dumps(dboo.gettasksummary_bar())


# 更新
@app.route('/addprocess', methods=['POST'])
def addprocess():
    json_data = json.loads(request.get_data())
    task_id = json_data['task_id']
    content = json_data['content']
    if dboo.addprocess(task_id, content):
        return json.dumps({'result': True})


# 更新
# TODO 把这个任务的最新状态反馈一下
@app.route('/getprocess', methods=['POST'])
def getprocess():
    json_data = json.loads(request.get_data())
    task_id = json_data['task_id']
    return json.dumps({'arrays': dboo.getprocess(task_id)})


# #####################################
# 定义process的函数
# #####################################
@app.route('/resetprocess', methods=['POST'])
def resetprocess():
    json_data = json.loads(request.get_data())
    process_id = json_data['process_id']
    # print(process_id)
    return json.dumps({'status': dboo.resetprocess(process_id)})


@app.route('/finishprocess', methods=['POST'])
def finishprocess():
    json_data = json.loads(request.get_data())
    process_id = json_data['process_id']
    # print(process_id)
    return json.dumps({'status': dboo.finishprocess(process_id)})


@app.route('/updateprocess', methods=['POST'])
def updateprocess():
    json_data = json.loads(request.get_data())
    process_id = json_data['process_id']
    content = json_data['content']
    # print(process_id)
    return json.dumps({'status': dboo.updateprocess(process_id, content)})

# #####################################
# 定义schedule的函数
# #####################################


@app.route('/initschedule')
def initschedule():
    return json.dumps(dboo.initschedule())


@app.route('/addschedule', methods=['POST'])
def addschedule():
    json_data = json.loads(request.get_data())
    subject = json_data['task_select']
    subsub = json_data['task_sub_select']
    schedule_type = json_data['schedule_type']
    schedule_frequence = json_data['schedule_frequence']
    content = json_data['schedule_content']
    temp = dboo.addschedule(subject, subsub, schedule_type,
                            schedule_frequence, content)
    return json.dumps({'result': temp})


@app.route('/getscheduledata')
def getscheduledata():
    return json.dumps({'data': dboo.getscheduledata()})


@app.route('/getscheduletaskdata', methods=['POST'])
def getscheduletaskdata():
    json_data = json.loads(request.get_data())
    schedule_id = json_data['schedule_id']
    # print(schedule_id)
    return json.dumps({'data': dboo.getscheduletaskdata(schedule_id)})


@app.route('/forbidschedule', methods=['POST'])
def forbidschedule():
    json_data = json.loads(request.get_data())
    schedule_id = json_data['schedule_id']
    # print(schedule_id)
    return json.dumps({'status': dboo.forbidschedule(schedule_id)})


@app.route('/startschedule', methods=['POST'])
def startschedule():
    json_data = json.loads(request.get_data())
    schedule_id = json_data['schedule_id']
    # print(schedule_id)
    return json.dumps({'status': dboo.startschedule(schedule_id)})


@app.route('/modifyschedule', methods=['POST'])
def modifyschedule():
    json_data = json.loads(request.get_data())
    schedule_id = json_data['schedule_id']
    subject = json_data['subject']
    subsub = json_data['subsub']
    schedule_type = json_data['schedule_type']
    schedule_frequence = json_data['schedule_frequence']
    content = json_data['schedule_content']
    # print(schedule_id)
    return json.dumps({'status': dboo.modifyschedule(schedule_id, subject, subsub, schedule_type, schedule_frequence, content)})


# #####################################
# 定义schedule的函数
# #####################################
@app.route('/setiswork', methods=['POST'])
def setiswork():
    json_data = json.loads(request.get_data())
    iswork = json_data['iswork']
    dboo.setiswork(iswork)
    return json.dumps({'result': True})


@app.route('/getiswork')
def getiswork():
    res = dboo.getiswork()
    return json.dumps({'iswork': res})


# #####################################
# 定义yys的函数
# #####################################
@app.route('/yys_getyhscore')
def yys_getyhscore():
    res = dboo_yys.getyhscore()
    return json.dumps(res)


@app.route('/yys_getyhtypescore')
def yys_getyhtypescore():
    res = dboo_yys.getyhtypescore()
    return json.dumps(res)


@app.route('/yys_getyhtypenum')
def yys_getyhtypenum():
    res = dboo_yys.getyhtypenum()
    return json.dumps(res)


@app.route('/yys_getyhtypesunburst')
def yys_getyhtypesunburst():
    res = dboo_yys.getyhtypesunburst()
    return json.dumps(res)


@app.route('/yys_getyysrole')
def yys_getyysrole():
    res = dboo_yys.getyysrole()
    return json.dumps(res)


# #####################################
# 定义全局的函数
# #####################################
@app.route('/getfirstpage')
def getfirstpage():
    res = dboo.getfirstpage()
    return json.dumps(res)


@app.route('/setfirstpage', methods=['POST'])
def setfirstpage():
    json_data = json.loads(request.get_data())
    firstpage = json_data['firstpage']
    dboo.setfirstpage(firstpage)
    return json.dumps({'result': True})


if __name__ == '__main__':
    # ls.getlocksreen()
    app.run(host='0.0.0.0', port=5000, debug=True)
