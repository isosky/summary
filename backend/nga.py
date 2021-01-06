#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import random
import re
from multiprocessing.dummy import Pool
import csv
import json
import sys
from config import mysql_config
import pymysql
import time
from queue import Queue, LifoQueue


# 爬所有id，评论，图片放到mysql中
# 已经爬过的，记录时间和楼层
# 加入判断主题是否放空
# 按版统计
# 基于python的queue 来实现一下同步


# https://img.nga.178.com/attachments/./mon_202101/04/-7Q5-2wvK27T1kShs-134.jpg.medium.jpg
attach_url = 'https://img.nga.178.com/attachments'


def get_headers():
    # user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0',
    #                'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
    #                'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)',
    #                'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    #                'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
    #                'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)',
    #                'Opera/9.52 (Windows NT 5.0; U; en)',
    #                'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.2pre) Gecko/2008071405 GranParadiso/3.0.2pre',
    #                'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.458.0 Safari/534.3',
    #                'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.211.4 Safari/532.0',
    #                'Opera/9.80 (Windows NT 5.1; U; ru) Presto/2.7.39 Version/11.00']
    # user_agent = random.choice(user_agents)
    headers = {'host': "bbs.nga.cn",
               'connection': "keep-alive",
               'cache-control': "no-cache",
               'upgrade-insecure-requests': "1",
               'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
               'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               'referer': "http://bbs.ngacn.cc/misc/adpage_insert_2.html?http://bbs.ngacn.cc/read.php?tid=13427591&page=2",
               'accept-encoding': "gzip, deflate",
               'accept-language': "zh-CN,zh;q=0.9",
               'cookie': 'UM_distinctid=165d243d684e9-0111554226bb1c-3c604504-13edd4-165d243d68516f; taihe=aebe409faefff51e20f2dde377f1cea6; ngacn0comUserInfo=%25B0%25EB%25CF%25C4%25A8q%25A5%25A1%258EU%259B%25F6%09%25E5%258D%258A%25E5%25A4%258F%25E2%2595%25AD%25E3%2582%25A1%25E5%25B6%25B6%25E6%25B6%25BC%0939%0939%09%0910%090%090%090%090%09; ngaPassportUid=43320220; ngaPassportUrlencodedUname=%25B0%25EB%25CF%25C4%25A8q%25A5%25A1%258EU%259B%25F6; ngaPassportCid=Z8ltrcjgo616kor6sbbpgr0thdnbrsr96ge8kte5; ngacn0comUserInfoCheck=10d5d900ae3f241cd4bc9d2e144794f3; ngacn0comInfoCheckTime=1537976770; taihe_session=6444150154287a3254e70831f46a8868; CNZZDATA30043604=cnzz_eid%3D364786080-1536830942-%26ntime%3D1537976642; CNZZDATA30039253=cnzz_eid%3D943882560-1536826159-%26ntime%3D1537971608; Hm_lvt_5adc78329e14807f050ce131992ae69b=1536830988,1536839697,1537976774; lastvisit=1537976828; lastpath=/read.php?tid=12689996&page=2; bbsmisccookies=%7B%22insad_refreshid%22%3A%7B0%3A%22/153794231025962%22%2C1%3A1538581572%7D%2C%22pv_count_for_insad%22%3A%7B0%3A-46%2C1%3A1537981224%7D%2C%22insad_views%22%3A%7B0%3A1%2C1%3A1537981224%7D%7D; Hm_lpvt_5adc78329e14807f050ce131992ae69b=1537976834'
               }
    return headers


def strreplace(x):
    x = re.sub(re.compile('<.*?>', re.S), '', x)
    x = re.sub(re.compile('\n'), ' ', x)
    x = re.sub(re.compile('\r'), ' ', x)
    x = re.sub(re.compile('\r\n'), ' ', x)
    x = re.sub(re.compile('[\r\n]'), ' ', x)
    x = re.sub(re.compile('\s{2,}'), ' ', x)
    return x.strip()


class database(object):
    def __init__(self):
        self.db = pymysql.connect(
            host=mysql_config['host'], user=mysql_config['user'], password=mysql_config['passwd'], db=mysql_config['db'], port=mysql_config['port'])
        self.cursor = self.db.cursor()

    def add_nga_post(self, data):
        sql = 'insert into nga_post (post_id,replies,post_title,poster_id,sub) values (%s,%s,%s,%s,%s) on duplicate key update replies=VALUES(replies)'
        self.cursor.executemany(sql, data)
        self.db.commit()
        self.cursor.close()
        self.db.close()

    def update_nga_post(self, pid, ctime):
        sql = "update nga_post set collect_time = '%s' where post_id =%s" % (
            ctime, pid)
        # print(sql)
        self.cursor.execute(sql)
        self.db.commit()
        self.cursor.close()
        self.db.close()

    def add_nga_reply(self, data):
        sql = 'insert into nga_reply (post_id,poster_id,replys,reply_time,reply_content) values (%s,%s,%s,%s,%s) on duplicate key update replys=VALUES(replys)'
        try:
            self.cursor.executemany(sql, data)
        finally:
            pass
        self.db.commit()
        self.cursor.close()
        self.db.close()

    def add_nga_attach(self, data):
        sql = 'insert into nga_attach (post_id,poster_id,replys,attach_url) values (%s,%s,%s,%s) on duplicate key update replys=VALUES(replys)'
        self.cursor.executemany(sql, data)
        self.db.commit()
        self.cursor.close()
        self.db.close()

    def get_nga_post(self):
        temp = {}
        sql = 'select post_id from nga_post where is_finish!=1 or is_finish is null'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        for i in data:
            temp[i[0]] = 0
        sql = 'select post_id,max(replys) as lastnew from nga_reply group by post_id'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        for i in data:
            temp[i[0]] = i[1]
        self.cursor.close()
        self.db.close()
        # for i in temp.keys():
        #     print(i, temp[i])
        return temp


def getonepage(tid, page, rp):
    t_url = 'http://bbs.nga.cn/read.php?tid=%s&page=%d' % (
        tid, page)
    print('*' * 10)
    print('开始抓取：', t_url)
    # print(t_url)
    text = requests.get(t_url, headers=get_headers()
                        ).content.decode('gbk', 'ignore')
    with open('ae.html', 'wb') as f:
        f.write(text.encode('utf8'))
    # print("*"*10)
    # with open('ac.html', 'rb') as f:
    # text = f.read().decode("utf8")
    # print(text)
    p0 = re.compile(
        r"<span id='posterinfo[^0]\d*' class='posterinfo'>.*?<a href='nuke\.php\?func=ucp&uid=(\d+?)' id='postauthor(\d+).*?title='reply time'>(.*?)</span>.*?<span id='postcontent\d+?' class='postcontent ubbcode'>(.*?)</span>", re.S)
    p1 = re.compile(
        r"<a href='nuke\.php\?func=ucp&uid=(\d+?)' id='postauthor(\d+).*?title='reply time'>(.*?)</span>.*?<p id='postcontent\d+?' class='postcontent ubbcode'>(.*?)</p>", re.S)
    items = re.findall(p0, text)
    if page == 1:
        items.extend(re.findall(p1, text))
    print("帖子id:", tid, ',第', page, '页,共有:', len(items), '条')
    print("*" * 10)
    temp_data = []
    imgs = []
    for i in items:
        # time = str(i[2])+':00'
        comments = strreplace(i[3])
        img0 = re.compile(r"\[img\]([^\[]*)\[\/img\]")
        pimgs = re.findall(img0, comments)
        # 增加主题id
        temp = list(i)
        temp.insert(0, tid)
        if int(i[1]) >= rp:
            temp_data.append(temp)
        print("经过计算，追加：", len(temp_data))
        # 结束增加
        if pimgs:
            # print(i[1], pimgs)
            if len(pimgs) > 1:
                for pi in pimgs:
                    if 'attachments' not in pi:
                        temp = attach_url + str(pi[1:])
                    else:
                        temp = pi
                    imgs.append([tid, i[0], i[1], temp])
            else:
                if 'attachments' not in pimgs[0]:
                    temp = attach_url + str(pimgs[0][1:])
                else:
                    temp = pimgs[0]
                imgs.append([tid, i[0], i[1], temp])

    print("*" * 10)

    if imgs:
        print("*" * 10)
        print("增加 %s 附件，总计 %s " % (tid, str(len(imgs))))
        db = database()
        db.add_nga_attach(imgs)

    print("*" * 10)
    print("增加 %s 回复" % (tid))
    db = database()
    db.add_nga_reply(temp_data)

    print("*" * 10)
    print("更新 %s 日期" % (tid))
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    db = database()
    db.update_nga_post(tid, now)

    print("*" * 10)
    print("抓取结束")


def getlist(page_dict):
    page_url = 'https://bbs.nga.cn/thread.php?fid=-7&page=%d' % (1)
    text = requests.get(page_url, headers=get_headers()
                        ).content.decode('gbk', 'ignore')
    # with open('lad.html', 'wb') as f:
    #     f.write(text)
    # print("*" * 10)
    pl = re.compile(r"<td class='c1'><a id='t_rc1_\d*' title='打开新窗口' href='\/read.php\?tid=(\d*)'.*?(\d*)<\/a><\/td>.*?class='topic'>(.*?)</a>(.*?)a href='\/nuke.php\?func=ucp&uid=(\d*)", re.S)
    ps = re.compile(r"class='silver'>(.*?)</a>", re.S)
    # ['24936998', '99', '[单机向]挂机/放置游戏整理和推荐(更新各游戏图片预览)', '60061086', '游戏综合讨论']
    temp_items = re.findall(pl, text)
    if temp_items:
        items = [list(x) for x in temp_items]
        for i in items:
            temp_ps = re.findall(ps, i[3])
            if temp_ps:
                i.append(temp_ps[0][1:-1])
            else:
                i.append('')
            del (i[3])
            page_dict[i[0]] = int(i[1])
        db = database()
        db.add_nga_post(items)

        # TODO 移除无效的page

        # # TODO 增量抓取
        # for i in items:
        #     if i[0] == '18809689':
        #         continue
        #     if int(i[1]) > 2000:
        #         continue
        #     pages = int(int(i[1]) / 20) + 1
        #     print('*' * 10)
        #     print('开始抓取：', i[0], '共有：', pages, '页')
        #     for p in range(pages)[1:]:
        #         getonepage(i[0], p)
        #         time.sleep(5)


def caltask(pd, tq):
    db = database()
    temp = db.get_nga_post()
    for i in pd.keys():
        if i in temp.keys():
            page_min = int(temp[i] / 20) + 1
            page_max = int(int(pd[i]) / 20) + 1
            if page_min != page_max:
                for p in range(page_min, page_max):
                    tq.put([i, p, temp[i]])
            else:
                tq.put([i, page_max, temp[i]])
        else:
            page_max = int(int(pd[i]) / 20) + 1
            for p in range(1, page_max):
                tq.put([i, p, 0])


if __name__ == "__main__":
    task_queue = Queue()
    page_dict = {}
    getlist(page_dict)
    caltask(page_dict, task_queue)
    while not task_queue.empty():
        print('=' * 10)
        t = task_queue.get()
        getonepage(t[0], t[1], t[2])
        print('=' * 10)
        print('休息5秒')
        time.sleep(5)
