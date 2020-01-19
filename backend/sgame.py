
# -*- coding: utf-8 -*-
import random


r = [{'items': 'SSR', 'value': 1}, {'items': 'SR',
                                        'value': 39}, {'items': 'R', 'value': 60}]


def getrandowmitem(listrange):
    randomList = []
    for k in listrange:
        for h in range(k.get('value')):
            randomList.append(k.get('items'))
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
