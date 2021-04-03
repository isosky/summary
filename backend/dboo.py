#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import json
import os
import random
import sqlite3
import time
import calendar

if os.path.exists("F:/OneDrive/文档/tmss.db"):
    dbf = "F:/OneDrive/文档/tmss.db"
elif os.path.exists("C:/Users/isowang/OneDrive/文档/tmss.db"):
    dbf = "C:/Users/isowang/OneDrive/文档/tmss.db"
else:
    dbf = "/data/wangtr/data/tmss.db"

type_work = {}
iswork = None


# #####################################
# 定义全局的函数
# #####################################


def getfirstpage():
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    temp = c.execute("select value from sys_cfg where id=4")
    i = temp.fetchone()[0]
    conn.commit()
    conn.close()
    return {'firstpage': i}


def setfirstpage(fp):
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    c.execute("update sys_cfg set value =? where id=4", [fp])
    conn.commit()
    conn.close()

# TODO 统一用datetime模块


# #####################################
# 定义全局的函数
# #####################################


def initoption():
    global iswork
    conn = sqlite3.connect(dbf)
    c = conn.cursor()

    # 获得所有
    result = {}
    result_all = []

    t = calbegin()
    cursor = c.execute(
        "select type,count(*) from task where isabandon=0 and iswork>=? and stime>=datetime(?,'-7 DAY') group by type order by 2 desc", [iswork, t])
    for i in cursor:
        result_all.append({'value': i[0], 'label': i[0]})
        result[i[0]] = []

    cursor = c.execute("select name from sys_cfg where type = 'type'")
    for i in cursor:
        if i[0] not in result.keys():
            result_all.append({'value': i[0], 'label': i[0]})
            result[i[0]] = []

    # 得到近7天高频的
    cursor = c.execute(
        "select type,sub_type,count(*) from task where isabandon=0 and iswork>=? and stime>=? group by type,sub_type order by 3 desc", [iswork, t])
    for row in cursor:
        result[row[0]].append(row[1])

    # 将多的加回来
    cursor = c.execute(
        "select type,sub_type,count(*) from task where isabandon=0 and iswork>=? group by type,sub_type order by 3 desc", [iswork])
    for row in cursor:
        if row[1] not in result[row[0]]:
            result[row[0]].append(row[1])

    cursor = c.execute("select value from sys_cfg where id=1")
    lastchecktime = cursor.fetchone()[0]

    conn.close()
    return [result, result_all, lastchecktime]


# #####################################
# 定义task的函数
# #####################################

def addtask(type, sub_type, task_name, etime, person_arrays):
    # TODO bug 添加任务的时候，如果过期了，status不应该使用默认值
    global type_work
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    c.execute("insert into task (type,sub_type,task_name,etime,iswork) values (?,?,?,?,?)", [
              type, sub_type, task_name, etime, type_work[type]])
    conn.commit()
    temp = c.execute("select max(task_id) from task")
    task_id = temp.fetchone()[0]
    if person_arrays:
        for i in person_arrays:
            c.execute("insert into task_person values (?,?)", [task_id, i])
    # if sub_type == '学习' and '-' not in task_name and '《' in task_name:
    #     # 添加总结
    #     new_etime = (datetime.datetime.strptime(etime, "%Y-%m-%d") +
    #                  datetime.timedelta(days=7)).strftime("%Y-%m-%d")
    #     c.execute("insert into task (type,sub_type,task_name,etime,iswork) values (?,?,?,?,?)", [
    #         type, sub_type, task_name + '-总结', new_etime, type_work[type]])
    #     # 添加复习
    #     new_etime = (datetime.datetime.strptime(new_etime, "%Y-%m-%d") +
    #                  datetime.timedelta(days=7)).strftime("%Y-%m-%d")
    #     c.execute("insert into task (type,sub_type,task_name,etime,iswork) values (?,?,?,?,?)", [
    #         type, sub_type, task_name + '-复习', new_etime, type_work[type]])
    conn.commit()
    conn.close()
    return gettasknow()


def gettasknow():
    global iswork
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    cursor = c.execute(
        "select task_id,type,sub_type,task_name,etime,stime,isfinish,status from task where isfinish=0 and isabandon=0 and iswork>=? order by etime,task_id", [iswork])
    result = []
    process = getallprocess()
    person = getallperson()
    for row in cursor:
        temp = {'task_id': row[0], 'type': row[1], 'sub_type': row[2],
                'task_name': row[3], 'etime': row[4][5:], 'stime': row[5], 'tetime': row[4], 'isfinish': row[6], 'status': row[7]}
        if row[0] in process.keys():
            temp['num_process'] = process[row[0]]
        if row[0] in person.keys():
            temp['num_person'] = person[row[0]]
        result.append(temp)
    # temp = cursor
    # print(len(result))
    conn.close()
    return result


def getallperson():
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    cursor = c.execute(
        "select task_id,count(*) from task_person group by task_id")
    result = dict(cursor)
    conn.close()
    return result


def getallprocess():
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    cursor = c.execute(
        "select task_id,count(*) from task_process where isfinish=1 group by task_id")
    pfa = dict(cursor)
    cursor = c.execute(
        "select task_id,count(*) from task_process group by task_id")
    pff = dict(cursor)
    result = {}
    for i in pff.keys():
        if i in pfa.keys():
            result[i] = str(pfa[i]) + '/'+str(pff[i])
        else:
            result[i] = '0/'+str(pff[i])
    conn.close()
    return result


def getprocess(task_id):
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    cursor = c.execute(
        "select stime,process_name,isfinish,process_id,task_id from task_process where task_id=? order by 1 desc", [task_id])
    result = []
    for row in cursor:
        result.append({'stime': row[0][0:10], 'process_name': row[1],
                       'isfinish': row[2], 'process_id': row[3], 'task_id': row[4]})
    conn.close()
    return result


def gettaskprocess(task_id):
    res = {}
    res['k'] = task_id
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    cursor = c.execute(
        "select '%s' ,count(*) as c from task_process where task_id='%s' and isfinish=1" % (task_id, task_id))
    f = dict(cursor)

    cursor = c.execute(
        "select '%s' , count(*) as c from task_process where task_id='%s' " % (task_id, task_id))
    a = dict(cursor)
    res['num_process'] = str(f[str(task_id)]) + '/' + str(a[str(task_id)])
    conn.close()
    return res


def parsetime(timestring, timeformat):
    if timeformat == 'yyyymmdd':
        if type(timestring) == int:
            timestring = str(timestring)
        return '-'.join([timestring[0:4], timestring[4:6], timestring[6:8]])


def gettimedata():
    global iswork
    conn = sqlite3.connect(dbf)
    start_time = datetime.datetime.strftime(
        datetime.date.today() - datetime.timedelta(days=13), "%Y-%m-%d")
    end_time = datetime.datetime.strftime(
        datetime.date.today(), "%Y-%m-%d")
    c = conn.cursor()
    cursor = c.execute(
        "select strftime('%Y-%m-%d',ftime),count(*) from task where isfinish =1 and isabandon=0 and iswork>=? and ftime>=? group by strftime('%Y-%m-%d',ftime)", [iswork, start_time])
    result = []
    for row in cursor:
        result.append(row)

    r = [start_time, end_time]

    conn.commit()
    conn.close()
    return {'result': result, 'range': r}


def finishtask(task_id, input_finish):
    conn = sqlite3.connect(dbf)
    # 格式化成2016-03-20 11:45:39形式
    ftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    c = conn.cursor()
    temp = c.execute("select etime from task where task_id=?", [task_id])
    etime = temp.fetchone()[0] + ' 23:59:59'
    etime_ts = time.mktime(time.strptime(etime, "%Y-%m-%d %H:%M:%S"))
    now_ts = time.time()
    if input_finish == '':
        input_finish = '已完成'
    if now_ts > etime_ts:
        status = 4
    else:
        status = 2
    c.execute("update task set ftime=? ,isfinish=1,status=? where task_id =? ", [
              ftime, status, task_id])
    c.execute("insert into task_process (task_id,process_name,isfinish) values (?,?,1)", [
        task_id, input_finish])
    conn.commit()
    #   关闭所有进程
    c.execute(
        "update task_process set isfinish=1,ftime=datetime('now','localtime') where task_id=?", [task_id])
    conn.commit()
    conn.close()


def deletetask(task_id):
    conn = sqlite3.connect(dbf)
    # 格式化成2016-03-20 11:45:39形式
    c = conn.cursor()
    c.execute(
        "update task set isabandon=1,status=5 where task_id =? ", [task_id])
    conn.commit()
    conn.close()


def updatetask(task_id, type, sub_type, task_name, etime, status):
    conn = sqlite3.connect(dbf)
    # print(task_id, sub_type, task_name, etime)
    c = conn.cursor()
    if status == 1 or status == 3:
        etime_ts = time.mktime(time.strptime(
            etime + ' 23:59:59', "%Y-%m-%d %H:%M:%S"))
        now_ts = time.time()
        if now_ts > etime_ts:
            status = 3
        else:
            status = 1
    c.execute(
        "insert into task_his  select *,datetime('now','localtime') from task where task_id=?", [task_id])
    c.execute("update task set type=?, sub_type=? , task_name=? , etime=?,status=? where task_id =? ", [
              type, sub_type, task_name, etime, status, task_id])
    conn.commit()
    conn.close()


def querytask(query, type, sub_type, ftime, query_duration, isstime, isqueryall, mode):
    # print(ftime, '|', query_duration, '|', isstime)
    global iswork
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    query = '%'+query+'%'
    sql = "select task_id,type,sub_type,task_name,etime,stime,isfinish,status from task where isabandon=0 and task_name like ?"
    if not isqueryall:
        sql += " and isfinish = 0 "
    params_list = [query]
    if type != '':
        sql += " and type=? "
        params_list.append(type)
    if sub_type != '':
        sql += " and sub_type=? "
        params_list.append(sub_type)
    # if ftime != '':
    #     sql += " and ftime like ?"
    #     ftime = '%'+ftime+'%'
    #     params_list.append(ftime)
    # if query_duration:
    if isstime and query_duration:
        sql += " and stime between ? and ?"
        params_list.extend(query_duration)
        if ftime != '' and ftime is not None:
            sql += " and ftime like ?"
            ftime = '%'+ftime+'%'
            params_list.append(ftime)
    if not isstime and ftime:
        sql += " and ftime like ?"
        ftime = '%'+ftime+'%'
        params_list.append(ftime)
    if not isstime and query_duration != []:
        sql += " and ftime between ? and ?"
        params_list.extend(query_duration)

    sql += " and iswork>=? "
    params_list.append(iswork)
    if mode == 'graph':
        t = calbegin()
        sql += " and (stime>=? or status in (1,3))"
        params_list.append(t)
    sql += " order by etime,task_id"
    # print('*'*10)
    # print(sql)
    # print(params_list)
    cursor = c.execute(sql, params_list)
    # 得到所有进展清单
    process = getallprocess()
    person = getallperson()
    result = []
    for row in cursor:
        temp = {'task_id': row[0], 'type': row[1], 'sub_type': row[2],
                'task_name': row[3], 'etime': row[4][5:], 'stime': row[5], 'tetime': row[4], 'isfinish': row[6], 'status': row[7]}
        if row[0] in process.keys():
            temp['num_process'] = process[row[0]]
        if row[0] in person.keys():
            temp['num_person'] = person[row[0]]
        # print(temp)
        result.append(temp)
    # temp = cursor
    conn.close()
    return result


# 只查询本周
def querytask_week():
    global iswork
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    sql = "select task_id,type,sub_type,task_name,etime,stime,isfinish,status from task where isabandon=0 and iswork >= ? AND etime <= ? AND isfinish =0 order by etime"
    today = datetime.datetime.today()
    etime = datetime.datetime.strftime(
        today + datetime.timedelta(7 - today.weekday() - 1), "%Y-%m-%d")
    cursor = c.execute(sql, [iswork, etime])
    process = getallprocess()
    result = []
    for row in cursor:
        temp = {'task_id': row[0], 'type': row[1], 'sub_type': row[2],
                'task_name': row[3], 'etime': row[4][5:], 'stime': row[5], 'tetime': row[4], 'isfinish': row[6], 'status': row[7]}
        if row[0] in process.keys():
            temp['num_process'] = process[row[0]]
        result.append(temp)
    conn.close()
    return result


def calday():
    today = datetime.date.today()
    return [(today - datetime.timedelta(days=today.weekday())).strftime('%Y%m%d'), (today - datetime.timedelta(days=today.weekday()-6)).strftime('%Y%m%d')]


def calbegin():
    return datetime.date.today() - datetime.timedelta(days=13)

# 统计图


def gettasksummary_bar():
    global iswork
    t = calbegin()
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    cursor = c.execute(
        "select type,sub_type,count(*) from task where iswork>=? and (stime>=? or status in (1,3)) group by type,sub_type order by 3", [iswork, t])
    yAxisdata = []
    for i in cursor:
        yAxisdata.append(i[0]+'-'+i[1])
    # print(yAxisdata)

    yAxistodo = {}
    yAxistodooverdue = {}
    yAxisnormal = {}
    yAxisoverdue = {}
    yAxisabandon = {}

    cursor = c.execute(
        "select type,sub_type,status,count(*) from task where iswork>=? and (stime>=? or status in (1,3)) group by type,sub_type,status order by 1,2,3", [iswork, t])
    for i in cursor:
        if i[2] == 1:
            yAxistodo[i[0]+'-'+i[1]] = i[3]
        if i[2] == 2:
            yAxisnormal[i[0]+'-'+i[1]] = i[3]
        if i[2] == 3:
            yAxistodooverdue[i[0] + '-' + i[1]] = i[3]
        if i[2] == 4:
            yAxisoverdue[i[0]+'-'+i[1]] = i[3]
        if i[2] == 5:
            yAxisabandon[i[0] + '-' + i[1]] = i[3]

    yAxistodo_list = []
    yAxisnormal_list = []
    yAxisoverdue_list = []
    yAxistodooverdue_list = []
    yAxisabandon_list = []

    for sub_type in yAxisdata:
        if sub_type not in yAxistodo.keys():
            yAxistodo_list.append(0)
        else:
            yAxistodo_list.append(yAxistodo[sub_type])

        if sub_type not in yAxisnormal.keys():
            yAxisnormal_list.append(0)
        else:
            yAxisnormal_list.append(yAxisnormal[sub_type])

        if sub_type not in yAxisoverdue.keys():
            yAxisoverdue_list.append(0)
        else:
            yAxisoverdue_list.append(yAxisoverdue[sub_type])

        if sub_type not in yAxistodooverdue.keys():
            yAxistodooverdue_list.append(0)
        else:
            yAxistodooverdue_list.append(yAxistodooverdue[sub_type])

        if sub_type not in yAxisabandon.keys():
            yAxisabandon_list.append(0)
        else:
            yAxisabandon_list.append(yAxisabandon[sub_type])

    sum_todo = sum(yAxistodo_list)
    sum_normal = sum(yAxisnormal_list)
    sum_overdue = sum(yAxisoverdue_list)
    sum_todooverdue = sum(yAxistodooverdue_list)
    sum_abandon = sum(yAxisabandon_list)

    sum_task = sum_todo + sum_normal + sum_overdue + sum_todooverdue + sum_abandon

    if sum_task != 0:
        overdue_percent = round(
            (sum_overdue+sum_todooverdue) / sum_task * 100, 2)
        finish_percent = round((sum_overdue+sum_normal)/sum_task*100, 2)
    else:
        overdue_percent = 0
        finish_percent = 0

    cursor = c.execute(
        " select type, count(*) from task where iswork>=? and stime>=? group by type order by 2 desc", [iswork, t])
    pie_type_data = []
    for i in cursor:
        pie_type_data.append({'name': i[0], 'value': i[1]})

    cursor = c.execute(
        "select iswork,count(*) from task  where iswork>=? and stime>=? group by iswork order by 2 desc", [iswork, t])
    pie_type_data_c = []
    for i in cursor:
        if i[0]:
            pie_type_data_c.append({'name': '工作', 'value': i[1]})
        else:
            pie_type_data_c.append({'name': '非工作', 'value': i[1]})

    # 饼图数据
    pie_summary_data = [{'value': sum_overdue, 'name': '逾期完成'}, {'value': sum_todooverdue, 'name': '待做逾期'}, {'value': sum_todo, 'name': '待做'}, {
        'value': sum_normal, 'name': '正常'}, {'value': sum_abandon, 'name': '作废'}]

    # pie_summary_data = sorted(
    #     pie_summary_data, key=lambda e: e.__getitem__('value'), reverse=True)
    # print(pie_summary_data)

    # 柱形堆叠图数据
    result = {'sum_task': sum_task, 'percent': [finish_percent, overdue_percent], 'yAxisdata': yAxisdata, 'yAxistodo_list': yAxistodo_list,
              'yAxisnormal_list': yAxisnormal_list, 'yAxisoverdue_list': yAxisoverdue_list, 'yAxistodooverdue_list': yAxistodooverdue_list,
              'yAxisabandon_list': yAxisabandon_list, 'pie_summary_data': pie_summary_data, 'pie_type_data': pie_type_data, 'pie_type_data_c': pie_type_data_c}
    # print('tongji')
    conn.close()
    return result


# #####################################
# 定义process的函数
# #####################################

def resetprocess(process_id):
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    c.execute("update task_process set isfinish=0,ftime=datetime('now','localtime') where process_id=?",
              [process_id])
    conn.commit()
    conn.close()
    return True


def finishprocess(process_id):
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    c.execute("update task_process set isfinish=1,ftime=datetime('now','localtime') where process_id=?",
              [process_id])
    conn.commit()
    conn.close()
    return True


def addprocess(task_id, process_name):
    conn = sqlite3.connect(dbf)
    # etime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    c = conn.cursor()
    c.execute("insert into task_process (task_id,process_name) values (?,?)", [
              task_id, process_name])
    conn.commit()
    conn.close()
    return True


def updateprocess(process_id, process_name):
    conn = sqlite3.connect(dbf)
    # etime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    c = conn.cursor()
    c.execute("update task_process set process_name=? where process_id=?", [
        process_name, process_id])
    conn.commit()
    conn.close()
    return True


# #####################################
# 定义schedule的函数
# #####################################
def initschedule(force=False):
    global type_work
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    c.execute("select value from sys_cfg where id=1")
    lastcheck = c.fetchone()[0]
    print('last check time is : '+lastcheck)
    d = datetime.date.today().strftime("%Y-%m-%d")
    if d != lastcheck or force:
        cursor = c.execute(
            "select * from schedule where isabandon=0 and (lasttime is null or nexttime<date(date('now','localtime') ,'+10 day'))")
        res = []
        for i in cursor:
            temp = {'schedule_id': i[0], 'type': i[1], 'sub_type': i[2], 'task_name': i[3],
                    'schedule_type': i[4], 'schedule_frequence': i[5], 'nexttime': i[8]}
            res.append(temp)
        # 添加定时任务
        for i in res:
            # print(i['subject'],i['subsub'],i['content'],i['nexttime']+' 00:00:00')
            c.execute("insert into task (type,sub_type,task_name,etime,iswork) values (?,?,?,?,?)", [
                      i['type'], i['sub_type'], i['task_name'], i['nexttime'], type_work[i['type']]])
            newtaskid = c.lastrowid
            c.execute("insert into schedule_task (schedule_id,task_id,etime) values (?,?,?)", [
                      i['schedule_id'], newtaskid, i['nexttime']])
            nexttime = i['nexttime'].split('-')
            nexttime = datetime.date(year=int(nexttime[0]), month=int(
                nexttime[1]), day=int(nexttime[2]))
            newnexttime = schedulecalnexttime(
                i['schedule_type'], i['schedule_frequence'], nexttime)
            c.execute("update schedule set nexttime =?,lasttime = ? where schedule_id=?", [
                      newnexttime, d, i['schedule_id']])
            conn.commit()
        c.execute("update sys_cfg set value =? where id=1", [d])
        c.execute(
            "update task set status=3 where etime<date('now','localtime') and isfinish=0 and isabandon=0")
        conn.commit()

        c.execute(
            "insert into log (checktime) values (datetime('now','localtime'))")
        conn.commit()
        # 删除无效的task
        # TODO 带验证删除
        # deleterows = removetask()
        conn.close()
        return {'status': 1, 'message': '新增了：'+str(len(res)) + '条计划任务，可查看详情。lastchecktime:' + lastcheck}
    else:
        return {'status': 0, 'message': '今日已检查', 'lastchecktime': lastcheck}


def addschedule(type, sub_type, schedule_type, schedule_frequence, task_name):
    # sql = 'insert into schedule (type,sub_type,task_name) values (?,?,?)'
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    c.execute("insert into schedule (type,sub_type,task_name,schedule_type,schedule_frequence) values (?,?,?,?,?)", [
              type, sub_type, task_name, schedule_type, schedule_frequence])
    s_id = c.lastrowid
    nexttime = schedulecalnexttime(schedule_type, schedule_frequence, None)
    # if schedule_type == 'month':
    c.execute("update schedule set nexttime=? where schedule_id=?", [
        nexttime, s_id])
    conn.commit()
    initschedule(force=True)
    conn.close()
    return True


def schedulecalnexttime(schedule_type, schedule_frequence, nexttime):
    # 月任务的写法应该是
    # 1;3 每月1号，3号
    # 1:1;2:2 第一个周一，第二个周二
    # print(schedule_type, schedule_frequence, nexttime)
    day31s = [1, 3, 5, 7, 8, 10, 12]
    # 判断计算哪个时间
    if nexttime:
        n = max(datetime.date.today(), nexttime)
    else:
        n = datetime.date.today()
    # 得到下个月
    if n.month == 12:
        nn = n.replace(year=n.year+1)
        nn = nn.replace(month=1)
    else:
        if n.month == 1 and n.day > 28:
            nn = n.replace(day=28)
            nn = nn.replace(month=2)
        elif n.day >= 30 and (n.month+1 not in day31s):
            nn = n.replace(day=30)
            nn = nn.replace(month=n.month+1)
        else:
            nn = n.replace(month=n.month+1)
    if schedule_type == 'week':
        t_sf = schedule_frequence.split(',')
        t_sf = [int(x) for x in t_sf]
        temp = []
        for wd in t_sf:
            temp.extend(getdate(n.year, n.month, wd))
            temp.extend(getdate(nn.year, nn.month, wd))
    if schedule_type == 'month':
        t_sf = schedule_frequence.split(';')
        temp = []
        for wd in t_sf:
            if ':' not in wd:
                td = n.replace(day=int(wd))
                temp.append(td)
                td = nn.replace(day=int(wd))
                temp.append(td)
            else:
                weeks, days = wd.split(':')
                weeks = int(weeks)
                days = [int(x) for x in days.split(',')]
                for i in days:
                    alldd = getdate(n.year, n.month, i)
                    allddnn = getdate(nn.year, nn.month, i)
                    if weeks > 0:
                        temp.append(alldd[weeks-1])
                        temp.append(allddnn[weeks-1])
                    else:
                        temp.append(alldd[weeks])
                        temp.append(allddnn[weeks])
        # print(temp)
    temp = [x for x in temp if x > n]
    # print(td.strftime("%Y-%m-%d"))
    return min(temp)


def getnextmonthsameday(date):
    if date.month == 12:
        date = date.replace(year=date.year+1)
        date = date.replace(month=1)
    else:
        date = date.replace(month=date.month+1)
    # print(date)
    return date


# 早知道有calendar这个包就不用写的那么辛苦了
def getdate(year, month, weekday):
    c = calendar.Calendar()
    monthcal = c.monthdatescalendar(year, month)
    result = [day for week in monthcal for day in week if day.weekday(
    ) == weekday-1 and day.month == month]
    # result = [day for week in monthcal for day in week if day.weekday(
    # ) == weekday-1 and day.month == month][weeks]
    return result


def getscheduledata():
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    cursor = c.execute("select * from schedule order by schedule_id desc")
    res = []
    for i in cursor:
        if i[7]:
            lasttime = i[7][0:10]
        else:
            lasttime = i[7]
        temp = {'schedule_id': i[0], 'type': i[1], 'sub_type': i[2], 'task_name': i[3],
                'schedule_type': i[4], 'schedule_frequence': i[5], 'lasttime': lasttime, 'nexttime': i[8], 'isabandon': i[9]}
        res.append(temp)
    conn.close()
    return res


def getscheduletaskdata(schedule_id):
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    params_list = []
    sql = "select a.schedule_id,b.task_name,a.task_id,a.addtime,a.etime from schedule_task a,schedule b where a.schedule_id =b.schedule_id "
    if schedule_id != '':
        sql += ' and a.schedule_id=?'
        params_list.append(schedule_id)
    sql += " order by a.addtime desc"
    cursor = c.execute(sql, params_list)
    res = []
    for i in cursor:
        temp = {'schedule_id': i[0], 'task_name': i[1],
                'task_id': i[2], 'addtime': i[3], 'etime': i[4]}
        res.append(temp)
    # print(res)
    conn.close()
    return res


def forbidschedule(schedule_id):
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    c.execute("update schedule set isabandon=1 where schedule_id=?",
              [schedule_id])
    conn.commit()
    conn.close()
    return True


def startschedule(schedule_id):
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    c.execute("update schedule set isabandon=0 where schedule_id=?",
              [schedule_id])
    conn.commit()
    conn.close()
    return True


def modifyschedule(schedule_id, type, sub_type, schedule_type, schedule_frequence, task_name):
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    netxtime = schedulecalnexttime(schedule_type, schedule_frequence, None)
    c.execute("update schedule set type=?,sub_type=?,schedule_type=?,schedule_frequence=?,nexttime=?,task_name=? where schedule_id=?", [
              type, sub_type, schedule_type, schedule_frequence, netxtime, task_name, schedule_id])
    c.execute(
        "update task set task_name=? where task_id in (select task_id from schedule_task where schedule_id=?)", [task_name, schedule_id])
    conn.commit()
    conn.close()
    return True


# #####################################
# 定义全局的函数
# #####################################
def getiswork():
    global iswork, type_work
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    cursor = c.execute("select value from sys_cfg where id=2")
    iswork = cursor.fetchone()[0]

    cursor = c.execute("select name,value from sys_cfg where type='type'")
    for i in cursor:
        type_work[i[0]] = int(i[1])
    conn.close()
    return iswork


def setiswork(isw):
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    if isw == True:
        isw = 1
    else:
        isw = 0
    c.execute("update sys_cfg set value = ? where id=2", [isw])
    conn.commit()
    conn.close()


def gettype():
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    temp = []
    cursor = c.execute(
        "select id, name,value from sys_cfg where type = 'type'")
    for i in cursor:
        temp.append({'type_id': i[0], 'name': i[1], 'value': i[2]})
    conn.commit()
    conn.close()
    return temp


def addtype(typename, typevalue):
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    c.execute("insert into  sys_cfg ('type','name','value') values ('type',?,?)", [
              typename, typevalue])
    conn.commit()
    conn.close()


def deletetype(typeid):
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    c.execute("delete from sys_cfg where id=?", [typeid])
    conn.commit()
    conn.close()


def getcompany():
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    company_selector = []
    cursor = c.execute(
        "select company,count(*) from person group by company order by 2 desc")
    for i in cursor:
        company_selector.append({'value': i[0], 'label': i[0]})

    person_post_selector = []
    cursor = c.execute(
        "select person_post,count(*) from person group by person_post order by 2 desc")
    for i in cursor:
        person_post_selector.append({'value': i[0], 'label': i[0]})
    conn.close()
    return {"person_post_selector": person_post_selector, "company_selector": company_selector}


def getperson():
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    temp = []
    cursor = c.execute(
        "select a.person_id,company,person_name,person_post,count(*) from person a left join task_person b  on a.person_id=b.person_id group by a.person_id,a.company,a.person_name order by 4 desc")
    for i in cursor:
        temp.append({'person_id': i[0], 'company': i[1],
                     'person_name': i[2], 'person_post': i[3]})
    conn.commit()
    conn.close()
    return temp


def getperson_option():
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    temp = []
    cursor = c.execute(
        "select a.person_id,company,person_name,count(*) from person a left join task_person b  on a.person_id=b.person_id group by a.person_id,a.company,a.person_name order by 4 desc")
    for i in cursor:
        temp.append({'value': i[0], 'label': i[1]+'-' + i[2]})
    conn.commit()
    conn.close()
    return temp


# TODO 去重
def addperson(company, person_name, person_post, force):
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    temp = c.execute(
        "select count(*) from person where company=? and person_name=?", [company, person_name])
    temp = temp.fetchone()[0]

    print(temp > 0 and not force)
    if temp > 0 and not force:
        conn.close()
        return {"msg": False}

    c.execute("insert into  person ('company','person_name','person_post') values (?,?,?)", [
              company, person_name, person_post])
    conn.commit()
    conn.close()
    return {"msg": True}


def deleteperson(personid):
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    c.execute("delete from person where person_id=?", [personid])
    conn.commit()
    conn.close()


def getperson_data(task_id):
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    temp = c.execute(
        "select person_id,company,person_name from person where person_id in (select person_id from task_person where task_id =?)", [task_id])
    res = []
    for row in temp:
        res.append(
            {"person_id": row[0], "company": row[1], "person_name": row[2]})
    conn.commit()
    conn.close()
    return res


def appendtaskperson(task_id, person_id):
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    temp = c.execute(
        "select person_id from task_person where task_id=? ", [task_id])
    temp = list(temp)
    temp = [x[0] for x in temp]
    newperson = [x for x in person_id if x not in temp]
    if newperson:
        for i in newperson:
            c.execute(
                "insert into task_person (task_id,person_id) values (?,?)", [task_id, i])
    conn.commit()
    conn.close()
    res = getperson_data(task_id)
    return res


def deletetaskperson(task_id, person_id):
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    c.execute(
        "delete from task_person where task_id=? and  person_id=? ", [task_id, person_id])
    conn.commit()
    conn.close()
    res = getperson_data(task_id)
    return res


# #####################################
# 定义count的函数
# #####################################
def gettotalmonth():
    res = {}
    for i in range(12):
        res[i] = {'k': i * 12, 'v': str(i+1) * 6}
    return res


# querytask(query, type, sub_type, qt, isqueryall)
if __name__ == '__main__':
    getiswork()
    initschedule(force=True)
    # print(type_work)
    print(initoption())
    # temp = querytask('', '自己', '投资', '', True)
    # temp = gettasksummary_bar()
    # print(temp)
    # print(temp.keys())
else:
    getiswork()
