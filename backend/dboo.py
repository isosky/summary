import datetime
import json
import os
import random
import sqlite3
import time
import calendar

if not os.path.exists("C:/Users/fengy/OneDrive/文档/tmss.db"):
    dbf = "C:/Users/isowang/OneDrive/文档/tmss.db"
else:
    dbf = "C:/Users/fengy/OneDrive/文档/tmss.db"

iswork = None
# TODO 要放到数据库里面
subject_work = {'游戏': 0, '自己': 0, '学习': 1, '项目': 1, '公司': 1}


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
# 定义step的函数
# #####################################


def step_add(time, step):
    global iswork
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    times = "','".join(time)
    # print("delete FROM my_steps where step_time in (%s) " % times)
    c.execute("delete FROM my_steps where step_time in ('%s') " % times)
    data = zip(time, step)
    c.executemany("insert into my_steps values(?,?)", data)
    conn.commit()
    conn.close()


def step_add_one(time, step):
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    c.execute("delete FROM my_steps where step_time = ?", [time])
    c.execute("insert into my_steps values(?,?)", [time, step])
    conn.commit()
    conn.close()


def getstep(forchart=True):
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    cursor = c.execute("select * from my_steps order by 1")
    result = []
    for row in cursor:
        result.append(row)
    conn.commit()
    conn.close()
    if not forchart:
        time = [x[0] for x in result]
        step = [x[1] for x in result]
        return {'time': time, 'value': step}
    return result


def weight_add_one(time, step):
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    c.execute("delete FROM my_weights where weight_time = ?", [time])
    c.execute("insert into my_weights values(?,?)", [time, step])
    conn.commit()
    conn.close()


def getweight(forchart=True):
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    cursor = c.execute("select * from my_weights order by 1")
    result = []
    for row in cursor:
        result.append(row)
    conn.commit()
    conn.close()
    if not forchart:
        time = [x[0] for x in result]
        step = [x[1] for x in result]
        return {'time': time, 'value': step}
    return result


# #####################################
# 定义task的函数
# #####################################


def initoption():
    global iswork
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    cursor = c.execute(
        "select subject,subsub,count(*) from task where isabandon=0 and iswork>=? group by subject,subsub order by 3 desc", [iswork])
    result = {}
    result_all = []
    # TODO 将所有的分类都加上
    for row in cursor:
        if row[0] not in result.keys():
            result[row[0]] = []
            result_all.append({'value': row[0], 'label': row[0]})
        result[row[0]].append(row[1])
    cursor = c.execute("select value from sys_cfg where id=1")
    lastchecktime = cursor.fetchone()[0]
    conn.close()
    return [result, result_all, lastchecktime]


def addtask(subject, subsub, title, etime):
    global subject_work
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    c.execute("insert into task (subject,subsub,title,etime,iswork) values (?,?,?,?,?)", [
              subject, subsub, title, etime, subject_work[subject]])
    conn.commit()
    conn.close()
    return gettasknow()


def gettasknow():
    global iswork
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    cursor = c.execute(
        "select task_id,subject,subsub,title,etime,stime,isfinish from task where isfinish=0 and isabandon=0 and iswork>=? order by etime,task_id", [iswork])
    result = []
    process = getallprocess()
    for row in cursor:
        temp = {'task_id': row[0], 'subject': row[1], 'subsub': row[2],
                'title': row[3], 'etime': row[4][5:], 'stime': row[5], 'tetime': row[4], 'isfinish': row[6]}
        if row[0] in process.keys():
            temp['num_process'] = process[row[0]]
        result.append(temp)
    # temp = cursor
    print(len(result))
    conn.close()
    return result


def getallprocess():
    conn = sqlite3.connect(dbf)
    c = conn.cursor()

    cursor = c.execute(
        "select task_id,count(*) from task_process group by task_id")
    pfa = dict(cursor)
    cursor = c.execute(
        "select task_id,count(*) from task_process where isfinish=1 group by task_id")
    pff = dict(cursor)
    result = {}
    for i in pfa.keys():
        if i in pff.keys():
            result[i] = str(pfa[i]) + '/'+str(pfa[i])
        else:
            result[i] = '0/'+str(pfa[i])
    conn.close()
    return result


def getprocess(task_id):
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    cursor = c.execute(
        "select stime,content,isfinish,process_id,task_id from task_process where task_id=? order by 1 desc", [task_id])
    result = []
    for row in cursor:
        result.append({'stime': row[0][0:10], 'content': row[1],
                       'isfinish': row[2], 'process_id': row[3], 'task_id': row[4]})
    conn.close()
    return result


def parsetime(timestring, timeformat):
    if timeformat == 'yyyymmdd':
        if type(timestring) == int:
            timestring = str(timestring)
        return '-'.join([timestring[0:4], timestring[4:6], timestring[6:8]])


def gettimedata():
    global iswork
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    cursor = c.execute(
        "select strftime('%Y-%m-%d',ftime),count(*) from task where isfinish =1 and isabandon=0 and iswork>=? group by strftime('%Y-%m-%d',ftime)", [iswork])
    result = []
    for row in cursor:
        result.append(row)
# 返回日历的时间
    cur_year = time.localtime()[0]
    cur_month = time.localtime()[1]
    if cur_month == 1:
        r = [str(cur_year-1)+'-12', str(cur_year)+'-01']
    elif cur_month == 12:
        r = [str(cur_year)+'-'+str(cur_month-1),
             str(cur_year+1)+'-01']
    else:
        r = [str(cur_year)+'-'+str(cur_month-1),
             str(cur_year)+'-'+str(cur_month+1)]
    conn.commit()
    conn.close()
    return {'result': result, 'range': r}


def finishtask(task_id, input_finish):
    conn = sqlite3.connect(dbf)
    # 格式化成2016-03-20 11:45:39形式
    etime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    c = conn.cursor()
    c.execute('''update task set ftime=? ,isfinish=1 where task_id =? ''', [
              etime, task_id])
    c.execute("insert into task_process (task_id,content,isfinish) values (?,?,1)", [
        task_id, input_finish])
    conn.commit()
    #   关闭所有进程
    c.execute('update task_process set isfinish=1 where task_id=?', [task_id])
    conn.commit()
    conn.close()


def deletetask(task_id):
    conn = sqlite3.connect(dbf)
    # 格式化成2016-03-20 11:45:39形式
    c = conn.cursor()
    c.execute('''update task set isabandon=1 where task_id =? ''', [task_id])
    conn.commit()
    conn.close()


def updatetask(task_id, subject, subsub, title, etime):
    conn = sqlite3.connect(dbf)
    # print(task_id, subsub, title, etime)
    c = conn.cursor()
    c.execute('''update task set subject=?, subsub=? , title=? , etime=? where task_id =? ''', [
              subject, subsub, title, etime, task_id])
    conn.commit()
    conn.close()


# 2020-07-05 星期日 放弃这部分展示
def gettasksummary():
    global iswork
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    etime = time.strftime("%Y-%m-%d", time.localtime())
    print(etime)
    today = c.execute(
        "select count(*) from task where etime=? and isfinish=0 and isabandon=0 and iswork>=?", [etime, iswork])
    for i in today:
        res_today = i[0]
    delay = c.execute(
        "select count(*) from task where etime<? and isfinish=0 and isabandon=0 and iswork>=?", [etime, iswork])
    for i in delay:
        res_delay = i[0]
    todo = c.execute(
        "select count(*) from task where isfinish=0 and isabandon=0 and iswork>=?", [iswork])
    for i in todo:
        res_todo = i[0]
    conn.close()
    return json.dumps({'res_delay': res_delay, 'res_today': res_today, 'res_todo': res_todo})


def querytask(query, subject, subsub, isqueryall):
    global iswork
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    query = '%'+query+'%'
    sql = "select task_id,subject,subsub,title,etime,stime,isfinish from task where isabandon=0 and title like ?"
    if not isqueryall:
        sql += " and isfinish = 0 "
    params_list = [query]
    if subject != '':
        sql += " and subject=? "
        params_list.append(subject)
    if subsub != '':
        sql += " and subsub=? "
        params_list.append(subsub)

    sql += " and iswork>=? order by etime,task_id"
    params_list.append(iswork)
    cursor = c.execute(sql, params_list)
    # 得到所有进展清单
    process = getallprocess()
    result = []
    for row in cursor:
        temp = {'task_id': row[0], 'subject': row[1], 'subsub': row[2],
                'title': row[3], 'etime': row[4][5:], 'stime': row[5], 'tetime': row[4], 'isfinish': row[6]}
        if row[0] in process.keys():
            temp['num_process'] = process[row[0]]
        result.append(temp)
    # temp = cursor
    conn.close()
    return result


def calday():
    today = datetime.date.today()
    return [(today - datetime.timedelta(days=today.weekday())).strftime('%Y%m%d'), (today - datetime.timedelta(days=today.weekday()-6)).strftime('%Y%m%d')]


def removetask():
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    cursor = c.execute("select count(*) from task where isabandon=1")
    for i in cursor:
        result = i[0]
    # print(result)
    cursor = c.execute("delete from task where isabandon=1")
    conn.commit()
    return str(result)


# 统计的柱形图
def gettasksummary_bar():
    global iswork
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    cursor = c.execute(
        "select subsub,count(*) from task where isabandon=0 and iswork>=? group by subsub order by 2", [iswork])
    yAxisdata = []
    for i in cursor:
        yAxisdata.append(i[0])

    etime = time.strftime("%Y-%m-%d", time.localtime())
    # todo
    cursor = c.execute(
        "select subsub,count(*) from task where etime>=? and isabandon=0 and isfinish=0  and iswork>=? group by subsub", [etime, iswork])
    yAxistodo = {}
    for i in cursor:
        yAxistodo[i[0]] = i[1]

    # unfinish and delay
    cursor = c.execute(
        "select subsub,count(*) from task where etime<? and isfinish=0 and isabandon=0  and iswork>=? group by subsub", [etime, iswork])
    yAxistodooverdue = {}
    for i in cursor:
        yAxistodooverdue[i[0]] = i[1]

    # normal
    cursor = c.execute(
        "select subsub,count(*) from task where ftime<date(etime,'+1 day') and isfinish=1 and iswork>=? group by subsub", [iswork])
    yAxisnormal = {}
    for i in cursor:
        yAxisnormal[i[0]] = i[1]

    # overdue
    cursor = c.execute(
        "select subsub,count(*) from task where ftime>=date(etime,'+1 day')  and iswork>=? group by subsub", [iswork])
    yAxisoverdue = {}
    for i in cursor:
        yAxisoverdue[i[0]] = i[1]

    # step
    cursor = c.execute("select max(step_time),avg(steps) from my_steps")
    for i in cursor:
        step_date = i[0]
        step_avg = round(i[1], 2)

    step_date = parsetime(step_date, 'yyyymmdd')

    yAxistodo_list = []
    yAxisnormal_list = []
    yAxisoverdue_list = []
    yAxistodooverdue_list = []

    for subsub in yAxisdata:
        if subsub not in yAxistodo.keys():
            yAxistodo_list.append(0)
        else:
            yAxistodo_list.append(yAxistodo[subsub])

        if subsub not in yAxisnormal.keys():
            yAxisnormal_list.append(0)
        else:
            yAxisnormal_list.append(yAxisnormal[subsub])

        if subsub not in yAxisoverdue.keys():
            yAxisoverdue_list.append(0)
        else:
            yAxisoverdue_list.append(yAxisoverdue[subsub])

        if subsub not in yAxistodooverdue.keys():
            yAxistodooverdue_list.append(0)
        else:
            yAxistodooverdue_list.append(yAxistodooverdue[subsub])

    sum_todo = sum(yAxistodo_list)
    sum_normal = sum(yAxisnormal_list)
    sum_overdue = sum(yAxisoverdue_list)
    sum_todoovredue = sum(yAxistodooverdue_list)

    sum_task = sum_todo + sum_normal + sum_overdue + sum_todoovredue

    if sum_task != 0:
        overdue_percent = round(
            (sum_overdue+sum_todoovredue) / sum_task * 100, 2)
        finish_percent = round((sum_overdue+sum_normal)/sum_task*100, 2)
    else:
        overdue_percent = 0
        finish_percent = 0

    piedata = [{'value': sum_overdue, 'name': '逾期'}, {'value': sum_todoovredue, 'name': '待做逾期'}, {'value': sum_todo, 'name': '待做'}, {
        'value': sum_normal, 'name': '正常完成'}]

    result = {'sum_task': sum_task, 'percent': [finish_percent, overdue_percent], 'yAxisdata': yAxisdata, 'yAxistodo_list': yAxistodo_list,
              'yAxisnormal_list': yAxisnormal_list, 'yAxisoverdue_list': yAxisoverdue_list, 'yAxistodooverdue_list': yAxistodooverdue_list, 'piedata': piedata, 'step_avg': step_avg, 'step_date': step_date}
    # print('tongji')
    conn.close()
    return result


# #####################################
# 定义process的函数
# #####################################

def resetprocess(process_id):
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    c.execute("update task_process set isfinish=0 where process_id=?",
              [process_id])
    conn.commit()
    conn.close()
    return True


def finishprocess(process_id):
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    c.execute("update task_process set isfinish=1 where process_id=?",
              [process_id])
    conn.commit()
    conn.close()
    return True


def addprocess(task_id, content):
    conn = sqlite3.connect(dbf)
    # etime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    c = conn.cursor()
    c.execute("insert into task_process (task_id,content) values (?,?)", [
              task_id, content])
    conn.commit()
    conn.close()
    return True


def updateprocess(process_id, content):
    conn = sqlite3.connect(dbf)
    # etime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    c = conn.cursor()
    c.execute("update task_process set content=? where process_id=?", [
        content, process_id])
    conn.commit()
    conn.close()
    return True


# #####################################
# 定义schedule的函数
# #####################################
def initschedule(force=False):
    global subject_work
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    c.execute("select value from sys_cfg where id=1")
    lastcheck = c.fetchone()[0]
    print('last check time is : '+lastcheck)
    d = datetime.date.today().strftime("%Y-%m-%d")
    if d != lastcheck or force:
        cursor = c.execute(
            "select * from schedule where isabandon=0 and (lasttime is null or nexttime<date(date(),'+10 day'))")
        res = []
        for i in cursor:
            temp = {'schedule_id': i[0], 'subject': i[1], 'subsub': i[2], 'content': i[3],
                    'schedule_type': i[4], 'schedule_frequence': i[5], 'nexttime': i[8]}
            res.append(temp)
        # 添加定时任务
        for i in res:
            # print(i['subject'],i['subsub'],i['content'],i['nexttime']+' 00:00:00')
            c.execute("insert into task (subject,subsub,title,etime,iswork) values (?,?,?,?,?)", [
                      i['subject'], i['subsub'], i['content'], i['nexttime'], subject_work[i['subject']]])
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
        conn.commit()
        # 删除无效的task
        deleterows = removetask()
        conn.close()
        return {'status': 1, 'message': '新增了：'+str(len(res))+'条计划任务，可查看详情。删除了：'+str(len(deleterows))+'条无效任务', 'lastchecktime': lastcheck}
    else:
        return {'status': 0, 'message': '今日已检查', 'lastchecktime': lastcheck}


def addschedule(subject, subsub, schedule_type, schedule_frequence, content):
    # sql = 'insert into schedule (subject,subsub,content) values (?,?,?)'
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    c.execute("insert into schedule (subject,subsub,content,schedule_type,schedule_frequence) values (?,?,?,?,?)", [
              subject, subsub, content, schedule_type, schedule_frequence])
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
        temp = {'schedule_id': i[0], 'subject': i[1], 'subsub': i[2], 'content': i[3],
                'schedule_type': i[4], 'schedule_frequence': i[5], 'lasttime': lasttime, 'nexttime': i[8], 'isabandon': i[9]}
        res.append(temp)
    conn.close()
    return res


def getscheduletaskdata(schedule_id):
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    params_list = []
    sql = "select a.schedule_id,b.content,a.task_id,a.addtime,a.etime from schedule_task a,schedule b where a.schedule_id =b.schedule_id "
    if schedule_id != '':
        sql += ' and a.schedule_id=?'
        params_list.append(schedule_id)
    sql += " order by a.addtime desc"
    cursor = c.execute(sql, params_list)
    res = []
    for i in cursor:
        temp = {'schedule_id': i[0], 'content': i[1],
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


def modifyschedule(schedule_id, subject, subsub, schedule_type, schedule_frequence, content):
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    netxtime = schedulecalnexttime(schedule_type, schedule_frequence, None)
    c.execute("update schedule set subject=?,subsub=?,schedule_type=?,schedule_frequence=?,nexttime=? where schedule_id=?", [
              subject, subsub, schedule_type, schedule_frequence, netxtime, schedule_id])
    conn.commit()
    conn.close()
    return True


# #####################################
# 定义全局的函数
# #####################################
def getiswork():
    global iswork
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    cursor = c.execute("select value from sys_cfg where id=2")
    iswork = cursor.fetchone()[0]
    # print(iswork)
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


def init():
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    # create table steps
    # c.execute('''CREATE TABLE my_weights(weight_time TEXT NOT NULL,weight INT );''')
    # print("success create table my_weights")
    c.execute('''create table task (
    task_id            integer PRIMARY KEY autoincrement,                -- 设置主键
    subject       varchar(20),
    title         varchar (100),
    content      varchar(400),
    stime   datetime default (datetime('now', 'localtime')),
    etime   datetime ,
    ftime  datetime,
    times int default 1,
    isfinish int default 0,
    isabandon int default 0
    );''')
    conn.commit()
    conn.close()


if __name__ == '__main__':
    print(gettimedata())
else:
    getiswork()
