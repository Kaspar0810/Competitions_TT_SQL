from models import *
import comp_system

def kol_player():
    """выводит максимальное коичество человек в группе t если все группы равны, а g2 если разное количество"""
    ta = System.get(System.id == 1)
    a = ta.total_athletes
    g = ta.total_group
    e = a % g  # если количество участников равно делится на группы
    t = a // g  # если количество участников не равно делится на группы g2 наибольшое колво человек в группе
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
    pl2 = Player.get(Player.id == 2)
    pl3 = Player.get(Player.id == 5)
    table_1[0][1] = pl1.player
    table_1[1][1] = pl1.city
    table_1[2][1] = pl2.player
    table_1[3][1] = pl2.city
    table_1[4][1] = pl3.player
    table_1[5][1] = pl3.city
    return table_1


def table2_data():
    """данные результатов в таблице 2-й группы"""
    table_2 = []
    t = kol_player()
    for k in range(1, t * 2 + 1):
        st = ['']
        s = (st * (t + 4))
        s.insert(0, str((k + 1) // 2))  # получаем нумерацию строк по порядку
        table_2.append(s)

    pl1 = Player.get(Player.id == 3)
    pl2 = Player.get(Player.id == 4)
    pl3 = Player.get(Player.id == 6)
    table_2[0][1] = pl1.player
    table_2[1][1] = pl1.city
    table_2[2][1] = pl2.player
    table_2[3][1] = pl2.city
    table_2[4][1] = pl3.player
    table_2[5][1] = pl3.city
    return table_2


def table3_data():
    """данные результатов в таблице 3-й группы"""
    table_3 = []
    t = kol_player()
    for k in range(1, t * 2 + 1):
        st = ['']
        s = (st * (t + 4))
        s.insert(0, str((k + 1) // 2))  # получаем нумерацию строк по порядку
        table_3.append(s)
    return table_3


def table4_data():
    """данные результатов в таблице 4-й группы"""
    table_4 = []
    t = kol_player()
    for k in range(1, t * 2 + 1):
        st = ['']
        s = (st * (t + 4))
        s.insert(0, str((k + 1) // 2))  # получаем нумерацию строк по порядку
        table_4.append(s)
    return table_4


def table5_data():
    """данные результатов в таблице 5-й группы"""
    table_5 = []
    t = kol_player()
    for k in range(1, t * 2 + 1):
        st = ['']
        s = (st * (t + 4))
        s.insert(0, str((k + 1) // 2))  # получаем нумерацию строк по порядку
        table_5.append(s)
    return table_5


def table6_data():
    """данные результатов в таблице 6-й группы"""
    table_6 = []
    t = kol_player()
    for k in range(1, t * 2 + 1):
        st = ['']
        s = (st * (t + 4))
        s.insert(0, str((k + 1) // 2))  # получаем нумерацию строк по порядку
        table_6.append(s)

    return table_6


def total_data_table():
    """создает список списков данных групп"""
    tdt = []
    s = System.select().order_by(System.id.desc()).get()
    kg = s.total_group

    for m in range(1, 2):
        table_1 = table1_data()
        tdt.append(table_1)
        if kg == 1:
            break
        table_2 = table2_data()
        tdt.append(table_2)
        if kg == 2:
            break
        table_3 = table3_data()
        tdt.append(table_3)
        if kg == 3:
            break
        table_4 = table4_data()
        tdt.append(table_4)
        if kg == 4:
            break
    return tdt