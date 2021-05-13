import os
import sqlite3
import requests
import re
import json
import time
import datetime

if os.path.exists("F:/OneDrive/文档/tmss.db"):
    dbf = "F:/OneDrive/文档/tmss.db"
elif os.path.exists("C:/Users/isowang/OneDrive/文档/tmss.db"):
    dbf = "C:/Users/isowang/OneDrive/文档/tmss.db"
else:
    dbf = "/data/wangtr/data/tmss.db"

url = 'http://fund.eastmoney.com/pingzhongdata/{}.js'


def get_resonse(url):
    """
    :param url: 网页URL
    :return: 爬取的文本信息
    """
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except(Exception):
        print('Failed to get response to url!')
        return ''


def get_fund_info(code):
    data_list = {}
    print(url.format(code))
    response = get_resonse(url.format(code))
    # 爬取失败等待再次爬取
    if response == '':
        print(response)
        return ''
    else:
        strs = re.findall(r'var(.*?);', response)
        for i in range(0, len(strs)):
            tmp = strs[i].split('=')
            var_name = tmp[0].strip()
            data_list[var_name] = [tmp[1]]
        return data_list


def getmaxtime(code):
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    cursor = c.execute(
        "select max(fund_time) from fund_history where fund_code=?", [code])
    mt = cursor.fetchone()[0]
    conn.close()
    if mt is None:
        return ''
    return mt


def getfundall():
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    temp = c.execute("select fund_code from fund_total")
    sql = "insert into fund_history ('fund_code','fund_time','fund_prices','equity_return') values (?,?,?,?)"
    temp_list = []
    for i in temp:
        # print(i[0])
        jsvar = get_fund_info(i[0])
        mt = getmaxtime(i[0])
        Data_netWorthTrend = json.loads(jsvar['Data_netWorthTrend'][0])
        for dt in Data_netWorthTrend:
            # 转换成localtime
            time_local = time.localtime(dt['x']/1000)
            # 转换成新的时间格式(2016-05-05 20:28:54)
            ddt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            if ddt > mt:
                temp_list.append((i[0], ddt, dt['y'], dt['equityReturn']))
    c.executemany(sql, temp_list)
    conn.commit()
    conn.close()
    calfundtotal()


def calfundtotal(t=''):
    # fund_orders 中buy的share求和，sum求和，求平均为成本，减去sell的为实际的
    # 平均成本*sum（buy的share）-sum(sell的share)=现在的成本
    sql_a = "select fund_code,operation,round(sum(fund_shares),2),round(sum(order_sum),2) from fund_orders "
    sql_b = "group by fund_code,operation"
    if t != '':
        sql = sql_a + " where check_time<'"+t+"' " + sql_b
    else:
        t = datetime.datetime.now().strftime('%Y-%m-%d')
        sql = sql_a+sql_b
    # print(sql)
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    res = c.execute(sql)
    temp = {}
    for i in res:
        if i[0] not in temp.keys():
            temp[i[0]] = {'sell': [0, 0], 'buy': [0, 0]}
        temp[i[0]][i[1]][0] = i[2]
        temp[i[0]][i[1]][1] = i[3]
    for i in temp.keys():
        temp[i]['share'] = temp[i]['buy'][0]-temp[i]['sell'][0]
        temp[i]['sum'] = temp[i]['buy'][1]-temp[i]['sell'][1]
        temp[i]['cost'] = round(temp[i]['buy'][1]/temp[i]['share'], 4)
        temp[i]['earn_history'] = temp[i]['sell'][1] - \
            temp[i]['sell'][0]*temp[i]['cost']
        temp[i]['price_now'] = getpricesbydate(i, t)
        temp[i]['earn_sum'] = round(temp[i]['share'] *
                                    temp[i]['price_now'] - temp[i]['sum'], 2)
    # print(temp)
    # return

    sql = "select fund_code from fund_total"
    fund_exist = c.execute(sql)
    fund_exist = [x[0] for x in fund_exist]
    sql = "select max(fund_time) from fund_total_history"
    max_time = c.execute(sql)
    max_time = max_time.fetchone()[0]
    for i in temp.keys():
        if i not in fund_exist:
            c.execute(
                "insert into fund_total (fund_code,fund_shares,fund_sum,cost,earn_sum,earn_history) values (?,?,?,?,?,?)",
                [i, temp[i]['share'], temp[i]['cost'], temp[i]['sum'], temp[i]['earn_sum'], temp[i]['earn_history']])
        else:
            c.execute(
                "update fund_total set fund_shares=?,fund_sum=?,cost=?,earn_sum=?,earn_history=?,update_time=? where fund_code=?",
                [temp[i]['share'], temp[i]['cost'], temp[i]['sum'], temp[i]['earn_sum'], temp[i]['earn_history'], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), i])
        if t > max_time:
            c.execute(
                "insert into fund_total_history (fund_code,fund_time,earn_sum) values (?,?,?)", [i, t, temp[i]['earn_sum']])
        else:
            c.execute("update fund_total_history set earn_sum=? where fund_code = ? and fund_time =? ", [
                temp[i]['earn_sum'], i, t])
    conn.commit()
    conn.close()


def getpricesbydate(code, date):
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    res = c.execute(
        'select fund_prices from fund_history where fund_code=? and fund_time<=? order by fund_time desc limit 1', [code, date])
    temp = res.fetchone()[0]
    conn.close()
    return temp


if __name__ == '__main__':
    # print(url.format('123'))
    getfundall()
    # temp = '2021-04-07'
    # now = datetime.datetime.now().strftime('%Y-%m-%d')
    # while temp != now:
    #     temp = (datetime.datetime.strptime(
    #         temp, '%Y-%m-%d')+datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    #     # print(temp)
    #     calfundtotal(temp)
    #     # break
