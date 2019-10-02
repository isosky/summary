import datetime
import json
import os
import random
import sqlite3
import time

if not os.path.exists("C:/Users/fengy/OneDrive/文档/tmss.db"):
    dbf = "C:/Users/isowang/OneDrive/文档/tmss.db"
else:
    dbf = "C:/Users/fengy/OneDrive/文档/tmss.db"


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


def initoption():
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    cursor = c.execute(
        "select subject,subsub,count(*) from task where isabandon=0 group by subject,subsub order by 3 desc")
    result = {}
    for row in cursor:
        if row[0] not in result.keys():
            result[row[0]] = []
        result[row[0]].append(row[1])
    return result


def step_add(time, step):
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


def addtask(subject, subsub, title, etime):
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    c.execute("insert into task (subject,subsub,title,etime) values (?,?,?,?)", [
              subject, subsub, title, etime])
    conn.commit()
    conn.close()
    return gettasknow()


def gettasknow():
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    cursor = c.execute(
        "select task_id,subject,subsub,title,etime,stime,isfinish from task where isfinish=0 and isabandon=0 order by etime,task_id")
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
        "select task_id,count(*) from task_process where isfinish=0 group by task_id")
    result = {}
    for row in cursor:
        result[row[0]] = row[1]
    return result


def getprocess(task_id):
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    cursor = c.execute(
        "select stime,content from task_process where task_id=? order by 1 desc", [task_id])
    result = []
    for row in cursor:
        result.append({'stime': row[0][0:10], 'content': row[1]})
    conn.close()
    return result


def parsetime(timestring, timeformat):
    if timeformat == 'yyyymmdd':
        if type(timestring) == int:
            timestring = str(timestring)
        return '-'.join([timestring[0:4], timestring[4:6], timestring[6:8]])


def gettimedata():
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    cursor = c.execute(
        "select strftime('%Y-%m-%d',ftime),sum(times) from task where isfinish =1 and isabandon=0 group by strftime('%Y-%m-%d',ftime)")
    result = []
    for row in cursor:
        result.append(row)
    conn.commit()
    conn.close()
    return {'result': result}


def finishtask(task_id, input_finish):
    conn = sqlite3.connect(dbf)
    # 格式化成2016-03-20 11:45:39形式
    etime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    c = conn.cursor()
    c.execute('''update task set ftime=? ,isfinish=1 where task_id =? ''', [
              etime, task_id])
    c.execute("insert into task_process (task_id,content) values (?,?)", [
        task_id, input_finish])
    conn.commit()
    #   关闭所有进程
    c.execute('update task_process set isfinish=1 where task_id=?', [task_id])
    conn.commit()
    conn.close()


def updateprocess(task_id, content):
    conn = sqlite3.connect(dbf)
    # etime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    c = conn.cursor()
    c.execute("insert into task_process (task_id,content) values (?,?)", [
              task_id, content])
    conn.commit()
    conn.close()
    return True


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


def gettasksummary():
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    etime = time.strftime("%Y-%m-%d", time.localtime())
    print(etime)
    today = c.execute(
        "select count(*) from task where etime=? and isfinish=0 and isabandon=0", [etime])
    for i in today:
        res_today = i[0]
    delay = c.execute(
        "select count(*) from task where etime<? and isfinish=0 and isabandon=0", [etime])
    for i in delay:
        res_delay = i[0]
    todo = c.execute(
        "select count(*) from task where isfinish=0 and isabandon=0")
    for i in todo:
        res_todo = i[0]

    return json.dumps({'res_delay': res_delay, 'res_today': res_today, 'res_todo': res_todo})


def querytask(query, subject, subsub, isqueryall):
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    query = '%'+query+'%'
    sql = "select task_id,subject,subsub,title,etime,stime,isfinish from task where isabandon=0 and title like ?"
    if not isqueryall:
        sql += " and isfinish = 0 "

    params_list = [query]

    print(subject)

    if subject != '':
        sql += " and subject=? "
        params_list.append(subject)
    if subsub != '':
        sql += " and subsub=? "
        params_list.append(subsub)

    sql += " order by etime,task_id"
    print(sql)
    # print("select task_id,subject,subsub,title,etime,stime,isfinish from task where isabandon=0 and title like ? and subject=? and subsub=? and isfinish=? order by etime,task_id", [
    #       query, subject, subsub, isfinish])
    cursor = c.execute(sql, params_list)
    result = []
    for row in cursor:
        temp = {'task_id': row[0], 'subject': row[1], 'subsub': row[2],
                'title': row[3], 'etime': row[4][5:], 'stime': row[5], 'tetime': row[4], 'isfinish': row[6]}
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
    print(result)
    cursor = c.execute("delete from task where isabandon=1")
    conn.close()
    return str(result)


# 统计的柱形图
def gettasksummary_bar():
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    cursor = c.execute(
        "select subsub,count(*) from task where isabandon=0 group by subsub order by 2")
    yAxisdata = []
    for i in cursor:
        yAxisdata.append(i[0])

    etime = time.strftime("%Y-%m-%d", time.localtime())
    # todo
    cursor = c.execute(
        "select subsub,count(*) from task where etime>=? and isabandon=0 and isfinish=0 group by subsub", [etime])
    yAxistodo = {}
    for i in cursor:
        yAxistodo[i[0]] = i[1]

    # unfinish and delay
    cursor = c.execute(
        "select subsub,count(*) from task where etime<? and isfinish=0 and isabandon=0 group by subsub", [etime])
    yAxistodooverdue = {}
    for i in cursor:
        yAxistodooverdue[i[0]] = i[1]

    # normal
    cursor = c.execute(
        "select subsub,count(*) from task where ftime<date(etime,'+1 day') group by subsub")
    yAxisnormal = {}
    for i in cursor:
        yAxisnormal[i[0]] = i[1]

    # overdue
    cursor = c.execute(
        "select subsub,count(*) from task where ftime>=date(etime,'+1 day') group by subsub")
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

    overdue_percent = round((sum_overdue+sum_todoovredue) / sum_task * 100, 2)
    finish_percent = round((sum_overdue+sum_normal)/sum_task*100, 2)

    piedata = [{'value': sum_overdue, 'name': '逾期'}, {'value': sum_todoovredue, 'name': '待做逾期'}, {'value': sum_todo, 'name': '待做'}, {
        'value': sum_normal, 'name': '正常完成'}]

    result = {'sum_task': sum_task, 'percent': [finish_percent, overdue_percent], 'yAxisdata': yAxisdata, 'yAxistodo_list': yAxistodo_list,
              'yAxisnormal_list': yAxisnormal_list, 'yAxisoverdue_list': yAxisoverdue_list, 'yAxistodooverdue_list': yAxistodooverdue_list, 'piedata': piedata, 'step_avg': step_avg, 'step_date': step_date}
    # print('tongji')
    return result


if __name__ == '__main__':
    gettasksummary_bar()
    # s_time = [str(x) for x in range(20190701, 20190720)]
    # step = [random.randint(7000, 10000) for x in range(len(s_time))]
    # querytask('规则')
    # s, e = calday()
    # removetask()
    # step_add_one('20190729', 4)
    # step_add(time, step)
    # getstep()
    # init()
    # addtask('工作', '规则引擎调优', '2019-09-09')
    # print(gettasknow())
    # print(parsetime('20190707', 'yyyymmdd'))
    # print(gettimedata())
