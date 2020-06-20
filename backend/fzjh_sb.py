# -*- coding: utf-8 -*-
import math
import random

l_cz = [['changjian', 1.03, 1.03, 25, 30, 150, 120, 30, 150, 120],
        ['duanjian', 1.26, 1.28, 15, 25, 140, 115, 25, 120, 95],
        ['ruanjian', 1.3, 1.72, 15, 10, 30, 20, 10, 90, 80],
        ['zhongjian', 1.58, 1.13, 50, 40, 60, 20, 40, 200, 160],
        ['cijian', 1.38, 1.16, 15, 18, 65, 47, 40, 120, 80],
        ['changdao', 1.21, 1.11, 35, 35, 160, 125, 34, 140, 106],
        ['duandao', 1.25, 1.1, 15, 40, 150, 110, 30, 110, 80],
        ['wandao', 1.18, 1.08, 20, 20, 120, 100, 20, 120, 100],
        ['dahuandao', 1.1, 1.11, 45, 30, 170, 140, 45, 180, 135],
        ['shuangrenfu', 1.25, 1.11, 55, 40, 155, 115, 35, 160, 125],
        ['changgui', 1.18, 1.1, 50, 30, 100, 70, 30, 100, 70],
        ['changqiang', 0.91, 1.15, 45, 45, 130, 85, 30, 100, 70],
        ['sanjiegun', 1.11, 1.08, 25, 20, 90, 70, 20, 90, 70],
        ['langyabang', 1.1, 1.1, 60, 60, 200, 140, 20, 90, 70],
        ['zhanji', 1.03, 1.1, 50, 40, 135, 95, 45, 90, 45],
        ['changbian', 1.06, 1.11, 20, 20, 160, 140, 20, 160, 140],
        ['ruanbian', 0.86, 1.28, 12, 10, 40, 30, 40, 120, 80],
        ['jiujiebian', 1, 1.11, 40, 50, 160, 110, 25, 80, 55],
        ['ganzibian', 0.88, 1.3, 25, 20, 120, 100, 20, 100, 80],
        ['lianjia', 1.09, 1.1, 45, 30, 140, 110, 30, 90, 60],
        ['shuanghuan', 1.06, 1.01, 35, 30, 130, 100, 40, 120, 80],
        ['duijian', 1.18, 1.06, 40, 30, 100, 70, 30, 170, 140],
        ['shuanggou', 1.53, 1.03, 35, 30, 130, 100, 40, 130, 90]]


dict_cz = {}
for i in l_cz:
    dict_cz[i[0]] = i[1:]

dz = 550


def cz(sb_old, old_type, new_type):
    sb_new = {'sh': 0, 'zl': 0, 'yd': 0, 'rx': 0,
              'tx': 0, 'cl': 0, 'type': new_type}
    temp_old_cz = dict_cz[old_type]
    temp_new_cz = dict_cz[new_type]
    sb_new['rx'] = min(temp_new_cz[8] *
                       (sb_old['rx']-temp_old_cz[6])/temp_old_cz[8]+temp_new_cz[6], temp_new_cz[7])

    sb_new['yd'] = min(temp_new_cz[5] * (sb_old['yd']-temp_old_cz[3]) /
                       temp_old_cz[5]+temp_new_cz[3], temp_new_cz[4])

    sb_new['zl'] = temp_new_cz[2]*sb_old['zl']/temp_old_cz[2]

    sb_new['cl'] = sb_old['cl']

    if sb_old['sh'] < 460:
        sb_new['sh'] = sb_old['sh']+sb_old['cl'] * \
            (temp_new_cz[0]-temp_old_cz[0])
    # if sb_old['sh'] >= 460 and temp_old_cz[0] > temp_new_cz[0]:
    #     sb_new['sh'] = min()

    sb_new['tx'] = sb_old['tx']+sb_old['cl']*(temp_new_cz[1]-temp_old_cz[1])

    # print(sb_new)

    # for k, v in sb_new.items():
    #     sb_new[k] = math.floor(v)

    # print(sb_new)
    return sb_new


dict_cl = {'changjian': [{'sh': 1, 'zl': 0.033, 'yd': 0.4, 'rx': -0.4, 'tx': 1}, {'sh': 1, 'zl': 0.02,
                                                                                  'yd': -0.4, 'rx': 0.4, 'tx': 1}, {'sh': 1.1, 'zl': 0.01, 'yd': 0.15, 'rx': -0.15, 'tx': 1.2}],
           'duanjian': [{'sh': 1.2, 'zl': 0.033, 'yd': 0.38, 'rx': -0.38, 'tx': 1.1}, {'sh': 1.2, 'zl': 0.02,
                                                                                       'yd': -0.38, 'rx': 0.38, 'tx': 1.3}, {'sh': 1.4, 'zl': 0.01, 'yd': 0.35, 'rx': -0.25, 'tx': 1.45}],
           'ruanjian': [{'sh': 1.2, 'zl': 0.03, 'yd': 0.05, 'rx': -0.05, 'tx': 1.6}, {'sh': 1.3, 'zl': 0.02,
                                                                                      'yd': -0.25, 'rx': 0.25, 'tx': 1.7}, {'sh': 1.4, 'zl': 0.01, 'yd': 0.03, 'rx': -0.03, 'tx': 1.85}],
           'zhongjian': [{'sh': 1.6, 'zl': 0.033, 'yd': 0.25, 'rx': -0.2, 'tx': 1}, {'sh': 1.4, 'zl': 0.02,
                                                                                     'yd': -0.1, 'rx': 0.25, 'tx': 1.2}, {'sh': 1.75, 'zl': 0.01, 'yd': 0.15, 'rx': -0.05, 'tx': 1.2}],
           'cijian': [{'sh': 1.25, 'zl': 0.01, 'yd': 0.2, 'rx': -0.12, 'tx': 1.1}, {'sh': 1.4, 'zl': 0.015,
                                                                                    'yd': -0.15, 'rx': 0.25, 'tx': 1.15}, {'sh': 1.5, 'zl': 0.01, 'yd': 0.12, 'rx': -0.08, 'tx': 1.25}]}


def cl(sb_old, sbtype, m1, m2, m3):
    sb_new = {'sh': 0, 'zl': 0, 'yd': 0, 'rx': 0,
              'tx': 0, 'cl': 0, 'type': sb_old['type']}
    temp = dict_cl[sbtype]
    sb_new['sh'] = sb_old['sh']+m1*temp[0]['sh'] + \
        m2*temp[1]['sh']+m3*temp[2]['sh']
    sb_new['zl'] = sb_old['zl']+m1*temp[0]['zl'] + \
        m2*temp[1]['zl']+m3*temp[2]['zl']
    sb_new['yd'] = sb_old['yd']+m1*temp[0]['yd'] + \
        m2*temp[1]['yd']+m3*temp[2]['yd']
    sb_new['rx'] = sb_old['rx']+m1*temp[0]['rx'] + \
        m2*temp[1]['rx']+m3*temp[2]['rx']
    sb_new['tx'] = sb_old['tx']+m1*temp[0]['tx'] + \
        m2*temp[1]['tx']+m3*temp[2]['tx']
    sb_new['cl'] = sb_old['cl']+m1+m2+m3
    return sb_new


npc = {'tj': 500.0, 'xs': 600.0, 'ht': 750.0,
       'wjc': 700.0, 'tps': 800.0, 'oyz': 1200.0}


def cl_cost():
    global npc
    i = 0
    ai = 0
    res_cost = 0
    while i < 300:
        # print(i, ai, res_cost)
        if i <= 50:
            res_cost += m_cost(npc['tj'], i)
            i += 1
        # if i > 50 and i <= 100:
        #     if random.random() <= m_cgl(npc['ht'], i):
        #         i += 1
        #     res_cost += m_cost(npc['ht'], i)
        if i > 50 and i <= 300:
            if random.random() <= m_cgl(npc['tps'], i):
                i += 1
            res_cost += m_cost(npc['tps'], i)
        # if i > 250:
        #     if random.random() <= m_cgl(npc['oyz'], i):
        #         i += 1
        #     res_cost += m_cost(npc['oyz'], i)
        ai += 1
    return [i, ai, res_cost]


def m_cost(dz, cs):
    return math.floor(dz/12+math.pow(cs+1, 1.2))


def m_cgl(dz, cs):
    if cs > 50 and cs <= 100:
        return min(20.0/cs+dz/1000.0, 0.85)
    if cs > 100 and cs <= 200:
        return min(20.0/cs+dz/1500.0, 0.75)
    if cs > 200 and cs <= 300:
        return min(10.0/cs+dz/2400.0, 0.40)


if __name__ == "__main__":
    print('*'*20)
    sb = 0
    sc = 0
    for i in range(10000):
        a, b, c = cl_cost()
        sb += b
        sc += c
        # print(cl_cost())
    print(sb/10000, sc/10000, sb/10000*5/100, sb/10000*5/100+sc/10000)

    # q = [51.0, 100.0, 101.0, 200.0, 201.0, 300.0]

    # for k, v in npc.items():
    #     for i in q:
    #         print(k, i, m_cgl(v, i), m_cost(v, i))

    # sb_old = {'sh': 129, 'zl': 42, 'yd': 72, 'rx': 82,
    #           'tx': 20, 'cl': 0, 'type': 'zhongjian'}
    # temp1 = cz(sb_old, 'zhongjian', 'cijian')
    # print('dddd cijian:', temp1)

    # sb_old = cl(sb_old, 'zhongjian', m1=25, m2=200, m3=0)
    # print('1 cijian   :', cz(sb_old, 'zhongjian', 'cijian'))

    # # temp2 = cl(temp1, 'cijian', m1=9, m2=136, m3=155)
    # temp2 = cl(temp1, 'cijian', m1=0, m2=200, m3=100)
    # print('222 cijian :', temp2)

    # print('*'*20)
    # sb_old = {'sh': 125, 'zl': 42, 'yd': 72, 'rx': 82,
    #           'tx': 20, 'cl': 0, 'type': 'zhongjian'}

    # print('*'*20)
    # t_dj = cz(sb_old, 'zhongjian', 'duanjian')
    # print('t_dj :', t_dj)
    # print('*'*20)

    # t_dj1 = cl(t_dj, 'duanjian', m1=0, m2=160, m3=0)
    # print('t_dj1 :', t_dj1)
    # print('t_cj1 :', cz(t_dj1, 'duanjian', 'cijian'))

    # t_cj1 = cz(t_dj1, 'duanjian', 'cijian')
    # t_cj1 = cl(t_cj1, 'cijian', 90, 50, 0)
    # print('t_cj1 :', t_cj1)

    # print('*'*20)
    # t_dj2 = cl(t_dj, 'duanjian', m1=0, m2=180, m3=0)
    # print('t_dj2 :', t_dj2)
    # print('t_cj2 :', cz(t_dj2, 'duanjian', 'cijian'))

    # t_cj2 = cz(t_dj2, 'duanjian', 'cijian')
    # t_cj2 = cl(t_cj2, 'cijian', 90, 30, 0)

    # print('t_jc2 :', t_cj2)

    # sb_old = {'sh': 125, 'zl': 40, 'yd': 65, 'rx': 84,
    #           'tx': 20, 'cl': 0, 'type': 'zhongjian'}

    # t_dj = cz(sb_old, 'zhongjian', 'duanjian')
    # print(t_dj)
