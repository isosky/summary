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


def getroleequipsscore():
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    cursor = c.execute("select * from yys_role_yh_score")
    res = {}
    for i in cursor:
        if i[1] not in res.keys():
            res[i[1]] = []
        print(i)
    return


if __name__ == "__main__":
    getroleequipsscore()
