import jieba
import sqlite3
import os


if not os.path.exists("C:/Users/fengy/OneDrive/文档/tmss.db"):
    dbf = "C:/Users/isowang/OneDrive/文档/tmss.db"
else:
    dbf = "C:/Users/fengy/OneDrive/文档/tmss.db"



def getdata():
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    cursor = c.execute("select title from task where isfinish=1 order by 1")
    temp_title =[]
    for row in cursor:
        seg_list = jieba.cut(row[0])
        print(list(seg_list))
        temp_title.append(seg_list)
    conn.close()
    return 


if __name__=='__main__':
    getdata()