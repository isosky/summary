
# -*- coding: utf-8 -*-
import random


r = [{'SSR': 1}, {'SR': 39}, {'R': 60}]


def getrandowmitem(listrange):
    randomList = []
    for lr in listrange:
        for k, v in lr.items():
            randomList.extend([k]*v)
    random.shuffle(randomList)
    randomNum = random.randint(1, len(randomList))
    items = randomList[randomNum - 1]
    return items


if __name__ == "__main__":
    result = {}
    for i in range(10000):
        temp = getrandowmitem(r)
        if temp not in result.keys():
            result[temp] = 1
        else:
            result[temp] += 1
    print(result)
