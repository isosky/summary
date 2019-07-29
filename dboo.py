import sqlite3
import os
import random
import json

if not os.path.exists("tmss.db"):
    conn = sqlite3.connect('tmss.db')
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
    conn = sqlite3.connect('tmss.db')
    c = conn.cursor()
    # create table steps
    c.execute('''CREATE TABLE my_weights(weight_time TEXT NOT NULL,weight INT );''')
    print("success create table my_weights")
    conn.commit()
    conn.close()


def step_add(time, step):
    conn = sqlite3.connect('tmss.db')
    c = conn.cursor()
    times = "','".join(time)
    # print("delete FROM my_steps where step_time in (%s) " % times)
    c.execute("delete FROM my_steps where step_time in ('%s') " % times)
    data = zip(time, step)
    c.executemany("insert into my_steps values(?,?)", data)
    conn.commit()
    conn.close()


def step_add_one(time, step):
    conn = sqlite3.connect('tmss.db')
    c = conn.cursor()
    c.execute("delete FROM my_steps where step_time = ?", [time])
    c.execute("insert into my_steps values(?,?)", [time, step])
    conn.commit()
    conn.close()


def getstep(forchart=True):
    conn = sqlite3.connect('tmss.db')
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
    conn = sqlite3.connect('tmss.db')
    c = conn.cursor()
    c.execute("delete FROM my_weights where weight_time = ?", [time])
    c.execute("insert into my_weights values(?,?)", [time, step])
    conn.commit()
    conn.close()


def getweight(forchart=True):
    conn = sqlite3.connect('tmss.db')
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


if __name__ == '__main__':
    time = [str(x) for x in range(20190701, 20190720)]
    step = [random.randint(7000, 10000) for x in range(len(time))]
    # step_add_one('20190729', 4)
    # step_add(time, step)
    # getstep()
    # init()
