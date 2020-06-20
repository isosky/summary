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


role_list = ['scrapy', 'ploit', '吃糖了', '葛神棍']


def getroleequipsscore():
    global role_list
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    cursor = c.execute("select * from yys_role_yh_score order by 2,3")
    res = {}
    for i in cursor:
        # print(i)
        d = i[2].split(' ')[0]
        if d not in res.keys():
            res[d] = {}
        res[d][i[1]] = i[3]
        # print(d)
    axis = sorted(res.keys())
    temp_s = {}
    for i in axis:
        temp_s[i] = res[i]

    series = []
    for role in role_list:
        temp_data = [temp_s[x][role] if role in temp_s[x] else 0 for x in axis]
        for i in range(len(temp_data))[1:]:
            if temp_data[i] == 0 and temp_data[i-1] == 0:
                continue
            elif temp_data[i] == 0 and temp_data[i-1] != 0:
                temp_data[i] = temp_data[i-1]
        series.append({'name': role, 'type': "line", "data": temp_data})
    return {'legend': role_list, 'axis': axis, 'series': series}


if __name__ == "__main__":
    pass
