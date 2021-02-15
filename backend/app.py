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
    arg_type = json_data['type']
    arg_sub_type = json_data['sub_type']
    arg_task_name = json_data['task_name']
    arg_edate = json_data['edate']
    arg_person = json_data['person']
    print(arg_type, arg_task_name, arg_edate)
    temp = dboo.addtask(arg_type, arg_sub_type,
                        arg_task_name, arg_edate, arg_person)
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
    type = json_data['type']
    ftime = json_data['ftime']
    sub_type = json_data['sub_type']
    query_duration = json_data['query_duration']
    isstime = json_data['isstime']
    isqueryall = json_data['isqueryall']
    mode = json_data['mode']
    return json.dumps({'arrays': dboo.querytask(query, type, sub_type, ftime, query_duration, isstime, isqueryall, mode)})


@app.route('/querytask_week')
def querytask_week():
    return json.dumps({'arrays': dboo.querytask_week()})


@app.route('/updatetask', methods=['POST'])
def updatetask():
    json_data = json.loads(request.get_data())
    print(json_data)
    task_id = json_data['task_id']
    type = json_data['type']
    sub_type = json_data['sub_type']
    task_name = json_data['task_name']
    etime = json_data['etime']
    status = json_data['dustatus']
    dboo.updatetask(task_id, type, sub_type, task_name, etime, status)
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
    process_name = json_data['process_name']
    if dboo.addprocess(task_id, process_name):
        return json.dumps({'result': True})


# 更新
# TODO 把这个任务的最新状态反馈一下
@app.route('/getprocess', methods=['POST'])
def getprocess():
    json_data = json.loads(request.get_data())
    task_id = json_data['task_id']
    temp = dboo.getprocess(task_id)
    temp_s = dboo.gettaskprocess(task_id)
    return json.dumps({'arrays': temp, 'status': temp_s})


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
    process_name = json_data['process_name']
    # print(process_id)
    return json.dumps({'status': dboo.updateprocess(process_id, process_name)})

# #####################################
# 定义schedule的函数
# #####################################


@app.route('/initschedule')
def initschedule():
    return json.dumps(dboo.initschedule())


@app.route('/addschedule', methods=['POST'])
def addschedule():
    json_data = json.loads(request.get_data())
    type = json_data['type']
    sub_type = json_data['sub_type']
    schedule_type = json_data['schedule_type']
    schedule_frequence = json_data['schedule_frequence']
    task_name = json_data['task_name']
    temp = dboo.addschedule(type, sub_type, schedule_type,
                            schedule_frequence, task_name)
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
    type = json_data['type']
    sub_type = json_data['sub_type']
    schedule_type = json_data['schedule_type']
    schedule_frequence = json_data['schedule_frequence']
    task_name = json_data['schedule_content']
    # print(schedule_id)
    return json.dumps({'status': dboo.modifyschedule(schedule_id, type, sub_type, schedule_type, schedule_frequence, task_name)})


# #####################################
# 定义sys的函数
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


@app.route('/gettype')
def gettype():
    res = dboo.gettype()
    return json.dumps(res)


@app.route('/addtype', methods=['POST'])
def addtype():
    json_data = json.loads(request.get_data())
    typename = json_data['typename']
    typevalue = json_data['typevalue']
    dboo.addtype(typename, typevalue)
    return json.dumps({'result': True})


@app.route('/deletetype', methods=['POST'])
def deletetype():
    json_data = json.loads(request.get_data())
    typeid = json_data['typeid']
    dboo.deletetype(typeid)
    return json.dumps({'result': True})


@app.route('/getcompany')
def getcompany():
    res = dboo.getcompany()
    return json.dumps(res)


@app.route('/getperson')
def getperson():
    res = dboo.getperson()
    return json.dumps(res)


@app.route('/getperson_option')
def getperson_option():
    res = dboo.getperson_option()
    return json.dumps(res)


@app.route('/addperson', methods=['POST'])
def addperson():
    json_data = json.loads(request.get_data())
    company = json_data['company']
    person_name = json_data['person_name']
    dboo.addperson(company, person_name)
    return json.dumps({'result': True})


@app.route('/deleteperson', methods=['POST'])
def deleteperson():
    json_data = json.loads(request.get_data())
    personid = json_data['personid']
    dboo.deleteperson(personid)
    return json.dumps({'result': True})


@app.route('/getperson_data', methods=['POST'])
def getperson_data():
    json_data = json.loads(request.get_data())
    task_id = json_data['task_id']
    res = dboo.getperson_data(task_id)
    return json.dumps(res)


@app.route('/appendtaskperson', methods=['POST'])
def appendtaskperson():
    json_data = json.loads(request.get_data())
    print(json_data)
    task_id = json_data['task_id']
    person_id = json_data['person_id']
    res = dboo.appendtaskperson(task_id, person_id)
    return json.dumps(res)


@app.route('/deletetaskperson', methods=['POST'])
def deletetaskperson():
    json_data = json.loads(request.get_data())
    task_id = json_data['task_id']
    person_id = json_data['person_id']
    res = dboo.deletetaskperson(task_id, person_id)
    return json.dumps(res)

# #####################################
# 定义count的函数
# #####################################


@app.route('/gettotalmonth')
def gettotalmonth():
    res = dboo.gettotalmonth()
    return json.dumps(res)


if __name__ == '__main__':
    # ls.getlocksreen()
    app.run(host='0.0.0.0', port=5000, debug=True)
