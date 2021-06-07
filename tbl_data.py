from models import *
import comp_system

def kol_player():

    ta = System.get(System.id == 1)
    a = ta.total_athletes
    g = ta.total_grupp
    e = a % g  # если количество участников не равно делится на группы
    t = a // g  # если количество участников равно делится на группы
    g2 = t + 1

    if e == 0:
        t = t
    else:
        t = g2
    return t


def table1_data():
    """данные результатов в таблице 1-й группы"""
    table_1 = []

    t = kol_player()

    for k in range(1, t * 2 + 1):
        st = ['']
        s = (st * (t + 4))
        s.insert(0, str((k + 1) // 2))  # получаем нумерацию строк по порядку
        table_1.append(s)

    pl1 = Player.get(Player.id == 1)
    table_1[1][1] = pl1.player
    c1 = pl1.city

    # s1[7] = '2'
    # s2[7] = '13,7,8'
    # s11[2] = '1'
    # s12[2] = '0-3'
    # s1[8] = '2'
    # s11[8] = '1'
    #

    table_1[2][7] = '5'

    return table_1

def table2_data():

    table_2 = []

    t = kol_player()

    for k in range(1, t * 2 + 1):
        st = ['']
        s = (st * (t + 4))
        s.insert(0, str((k + 1) // 2))  # получаем нумерацию строк по порядку
        table_2.append(s)

    pl1 = Player.get(Player.id == 2)
    p1 = pl1.player
    c1 = pl1.city

    return table_2