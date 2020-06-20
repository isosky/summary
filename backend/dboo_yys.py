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


SUIT_ID_TO_NAME = {300002: '雪幽魂', 300003: '地藏像', 300004: '蝠翼',
                   300006: '涅槃之火', 300007: '三味', 300008: '魍魉之匣',
                   300009: '被服', 300010: '招财猫', 300011: '反枕',
                   300012: '轮入道', 300013: '日女巳时', 300014: '镜姬',
                   300015: '钟灵', 300018: '狰', 300019: '火灵', 300020: '鸣屋',
                   300021: '薙魂', 300022: '心眼', 300023: '木魅', 300024: '树妖',
                   300026: '网切', 300027: '阴摩罗', 300029: '伤魂鸟',
                   300030: '破势', 300031: '镇墓兽', 300032: '珍珠',
                   300033: '骰子鬼', 300034: '蚌精', 300035: '魅妖',
                   300036: '针女', 300039: '返魂香', 300048: '狂骨',
                   300049: '幽谷响', 300050: '土蜘蛛', 300051: '胧车',
                   300052: '荒骷髅', 300053: '地震鲶', 300054: '蜃气楼',
                   300073: '飞缘魔', 300074: '兵主部', 300075: '青女房',
                   300076: '涂佛', 300077: '鬼灵歌伎'}


role_list = ['scrapy', 'ploit', '吃糖了', '葛神棍']


def getyhscore():
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


def getyhtypescore():
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    cursor = c.execute(
        "select role_id,suit_id,sum(score) as score,count(*) as nums from role_hero_equips where level=15 group by role_id,suit_id")
    axis = list(SUIT_ID_TO_NAME.values())
    series = {}
    # 得分
    temp_series_score = {}
    # 个数
    series_nums = {}
    temp_axis = list(SUIT_ID_TO_NAME.keys())
    for role in role_list:
        temp_series_score[role] = {}
        series_nums[role] = {}
        for i in temp_axis:
            temp_series_score[role][i] = 0
            series_nums[role][i] = 0
    for i in cursor:
        temp_series_score[i[0]][i[1]] = round(i[2], 2)
        series_nums[i[0]][SUIT_ID_TO_NAME[i[1]]] = i[3]

    series = {}
    for role in role_list:
        series[role] = {}
        for i in temp_axis:
            series[role] = list(temp_series_score[role].values())

    return {'axis': axis, 'series': series, 'yh_type_nums': series_nums}


def getyhtypenum():
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    cursor = c.execute(
        "select role_id,suit_id,pos,count(*) as count from role_hero_equips where level=15 group by role_id,suit_id,pos")
    temp_series = {}
    temp_axis = list(SUIT_ID_TO_NAME.keys())
    for role in role_list:
        temp_series[role] = {}
        for i in temp_axis:
            temp_series[role][i] = {}
            for j in range(6):
                temp_series[role][i][j] = 0
    for i in cursor:
        temp_series[i[0]][i[1]][i[2]] = i[3]

    series = {}
    for role in role_list:
        series[role] = {}
        for i in temp_axis:
            series[role][SUIT_ID_TO_NAME[i]] = list(
                temp_series[role][i].values())

    print('*')
    return {'series': series}


if __name__ == "__main__":
    print(getyhtypescore())
