import sqlite3
import os


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


def step_add(data):
    pass


def step_add_one(time, step):
    conn = sqlite3.connect('tmss.db')
    c = conn.cursor()
    c.execute("delete FROM my_steps where step_time = ?", [time])
    c.execute("insert into my_steps values(?,?)", [time, step])
    conn.commit()
    conn.close()


if __name__ == '__main__':
    step_add_one('20190729', 4)
