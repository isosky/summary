#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import time
import random
import re
from multiprocessing.dummy import Pool
import csv
import json
import sys


# 爬所有id，评论，图片放到mysql中
# 已经爬过的，记录时间和楼层
# 加入判断主题是否放空
# 按版统计


base_url = 'https://bbs.nga.cn/thread.php?fid=-7'

# url = 'http://bbs.nga.cn/read.php?tid=%s&page=%d' % (game_id, page)

test_url = 'http://bbs.nga.cn/read.php?tid=%s&page=%d' % (24972648, 1)

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


def getonepage(tid, page):
    t_url = 'http://bbs.nga.cn/read.php?tid=%s&page=%d' % (
        tid, page)
    print(t_url)
    text = requests.get(t_url, headers=get_headers()
                        ).content.decode('gbk', 'ignore')
    # with open('ad.html', 'wb') as f:
    #     f.write(text)
    # print("*"*10)
    # with open('ac.html', 'rb') as f:
    imgs = []
    # text = f.read().decode("utf8")
    # print(text)
    p0 = re.compile(
        r"<a href='nuke\.php\?func=ucp&uid=(\d+?)' id='postauthor(\d+).*?title='reply time'>(.*?)</span>.*?<span id='postcontent\d+?' class='postcontent ubbcode'>(.*?)</span>", re.S)
    p1 = re.compile(
        r"<a href='nuke\.php\?func=ucp&uid=(\d+?)' id='postauthor(\d+).*?title='reply time'>(.*?)</span>.*?<p id='postcontent\d+?' class='postcontent ubbcode'>(.*?)</p>", re.S)
    items = re.findall(p0, text)
    items.extend(re.findall(p1, text))
    print(len(items))
    print("*"*10)
    for i in items:
        time = str(i[2])+':00'
        comments = strreplace(i[3])
        img0 = re.compile(r"\[img\]([^\[]*)\[\/img\]")
        pimgs = re.findall(img0, comments)
        if pimgs:
            print(i[1], pimgs)
            if len(pimgs) > 1:
                for pi in pimgs:
                    if 'attachments' not in pi:
                        temp = attach_url + str(pi[1:])
                    else:
                        temp = pi
                    imgs.append((i[1], temp))
            else:
                if 'attachments' not in pimgs[0]:
                    temp = attach_url + str(pimgs[0][1:])
                else:
                    temp = pimgs[0]
                imgs.append((i[1], temp))

    print("*" * 10)
    for i in imgs:
        print(i)


def getlist():
    page_url = 'https://bbs.nga.cn/thread.php?fid=-7&page=%d' % (1)
    text = requests.get(page_url, headers=get_headers()
                        ).content.decode('gbk', 'ignore')
    # with open('lad.html', 'wb') as f:
    #     f.write(text)
    # print("*" * 10)
    pl = re.compile(r"<td class='c1'><a id='t_rc1_\d*' title='打开新窗口' href='\/read.php\?tid=(\d*)'.*?(\d*)<\/a><\/td>.*?class='topic'>(.*?)</a>.*?a href='\/nuke.php\?func=ucp&uid=(\d*)", re.S)
    temp_items = re.findall(pl, text)
    if temp_items:
        items = [list(x) for x in temp_items]
        for i in items:
            i.append(int(int(i[1]) / 20) + 1)
            print(i)


if __name__ == "__main__":
    # getonepage(24972648, 1)
    getlist()
