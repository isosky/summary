import sqlite3
import os
import random
import json
import time
import datetime


if not os.path.exists("C:/Users/fengy/OneDrive/文档/tmss.db"):
    conn = sqlite3.connect('C:/Users/fengy/OneDrive/文档/tmss.db')
    c = conn.cursor()
    # create table steps
    c.execute('''CREATE TABLE my_steps(step_time TEXT NOT NULL,steps INT );''')
    print("success create table steps")
    # create table task
    c.execute('''CREATE TABLE my_task(id  NOT NULL,steps INT );''')
    print("success create table steps")
    conn.commit()
    conn.close()


def init():
    conn = sqlite3.connect('C:/Users/fengy/OneDrive/文档/tmss.db')
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


def step_add(time, step):
    conn = sqlite3.connect('C:/Users/fengy/OneDrive/文档/tmss.db')
    c = conn.cursor()
    times = "','".join(time)
    # print("delete FROM my_steps where step_time in (%s) " % times)
    c.execute("delete FROM my_steps where step_time in ('%s') " % times)
    data = zip(time, step)
    c.executemany("insert into my_steps values(?,?)", data)
    conn.commit()
    conn.close()


def step_add_one(time, step):
    conn = sqlite3.connect('C:/Users/fengy/OneDrive/文档/tmss.db')
    c = conn.cursor()
    c.execute("delete FROM my_steps where step_time = ?", [time])
    c.execute("insert into my_steps values(?,?)", [time, step])
    conn.commit()
    conn.close()


def getstep(forchart=True):
    conn = sqlite3.connect('C:/Users/fengy/OneDrive/文档/tmss.db')
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
    conn = sqlite3.connect('C:/Users/fengy/OneDrive/文档/tmss.db')
    c = conn.cursor()
    c.execute("delete FROM my_weights where weight_time = ?", [time])
    c.execute("insert into my_weights values(?,?)", [time, step])
    conn.commit()
    conn.close()


def getweight(forchart=True):
    conn = sqlite3.connect('C:/Users/fengy/OneDrive/文档/tmss.db')
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
    conn = sqlite3.connect('C:/Users/fengy/OneDrive/文档/tmss.db')
    c = conn.cursor()
    c.execute("insert into task (subject,subsub,title,etime) values (?,?,?,?)", [
              subject, subsub, title, etime])
    conn.commit()
    conn.close()
    return gettasknow()


def gettasknow():
    conn = sqlite3.connect('C:/Users/fengy/OneDrive/文档/tmss.db')
    c = conn.cursor()
    cursor = c.execute(
        "select task_id,subject,subsub,title,etime,stime from task where isfinish=0 and isabandon=0 ")
    result = []
    for row in cursor:
        temp = {'task_id': row[0], 'subject': row[1], 'subsub': row[2],
                'title': row[3], 'etime': row[4][5:], 'stime': row[5], 'tetime': row[4]}
        result.append(temp)
    # temp = cursor
    conn.close()
    return result


def parsetime(timestring, timeformat):
    if timeformat == 'yyyymmdd':
        if type(timestring) == int:
            timestring = str(timestring)
        return '-'.join([timestring[0:4], timestring[4:6], timestring[6:8]])


def gettimedata():
    conn = sqlite3.connect('C:/Users/fengy/OneDrive/文档/tmss.db')
    c = conn.cursor()
    cursor = c.execute(
        "select ftime,sum(times) from task where isfinish =1 and isabandon=0 group by ftime")
    result = []
    for row in cursor:
        result.append(row)
    conn.commit()
    conn.close()
    return {'result': result}


def finishtask(task_id, task_numbers):
    conn = sqlite3.connect('C:/Users/fengy/OneDrive/文档/tmss.db')
    # 格式化成2016-03-20 11:45:39形式
    etime = time.strftime("%Y-%m-%d", time.localtime())
    c = conn.cursor()
    c.execute('''update task set ftime=? ,isfinish=1 ,times=? where task_id =? ''', [
              etime, task_numbers, task_id])
    conn.commit()
    conn.close()


def deletetask(task_id):
    conn = sqlite3.connect('C:/Users/fengy/OneDrive/文档/tmss.db')
    # 格式化成2016-03-20 11:45:39形式
    c = conn.cursor()
    c.execute('''update task set isabandon=1 where task_id =? ''', [task_id])
    conn.commit()
    conn.close()


def updatetask(task_id, subsub, title, etime):
    conn = sqlite3.connect('C:/Users/fengy/OneDrive/文档/tmss.db')
    # print(task_id, subsub, title, etime)
    c = conn.cursor()
    c.execute('''update task set subsub=? , title=? , etime=? where task_id =? ''', [
              subsub, title, etime, task_id])
    conn.commit()
    conn.close()


def gettasksummary():
    conn = sqlite3.connect('C:/Users/fengy/OneDrive/文档/tmss.db')
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


def querytask(query):
    conn = sqlite3.connect('C:/Users/fengy/OneDrive/文档/tmss.db')
    c = conn.cursor()
    query = '%'+query+'%'
    cursor = c.execute(
        "select task_id,subject,subsub,title,etime,stime from task where isfinish=0 and isabandon=0 and title like ?", [query])
    result = []
    for row in cursor:
        temp = {'task_id': row[0], 'subject': row[1], 'subsub': row[2],
                'title': row[3], 'etime': row[4][5:], 'stime': row[5], 'tetime': row[4]}
        result.append(temp)
    # temp = cursor
    conn.close()
    return result


def getcount():
    conn = sqlite3.connect("C:/Users/fengy/OneDrive/文档/tmss.db")
    c = conn.cursor()
    e, s = calday()


def calday():
    today = datetime.date.today()
    return [(today - datetime.timedelta(days=today.weekday())).strftime('%Y%m%d'), (today - datetime.timedelta(days=today.weekday()-6)).strftime('%Y%m%d')]


if __name__ == '__main__':
    s_time = [str(x) for x in range(20190701, 20190720)]
    step = [random.randint(7000, 10000) for x in range(len(s_time))]
    # querytask('规则')
    s, e = calday()
    print(s, e)

    # step_add_one('20190729', 4)
    # step_add(time, step)
    # getstep()
    # init()
    # addtask('工作', '规则引擎调优', '2019-09-09')
    # print(gettasknow())
    # print(parsetime('20190707', 'yyyymmdd'))
    # print(gettimedata())
