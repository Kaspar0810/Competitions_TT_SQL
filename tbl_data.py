from models import *
import comp_system


def kol_player():
    """выводит максимальное коичество человек в группе t если все группы равны, а g2 если разное количество"""
    ta = System.select().order_by(System.id.desc()).get()
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
    td = table_1
    num_gr = "1 группа"
    t = kol_player()
    for k in range(1, t * 2 + 1):
        st = ['']
        s = (st * (t + 4))
        s.insert(0, str((k + 1) // 2))  # получаем нумерацию строк по порядку
        table_1.append(s)
    #  id игроков 1-й таблицы
    pl1 = Player.get(Player.id == 1)
    pl2 = Player.get(Player.id == 2)
    pl3 = Player.get(Player.id == 5)
    pl4 = Player.get(Player.id == 8)
    # занесение фамилии и города в таблицу
    table_1[0][1] = pl1.player
    table_1[1][1] = pl1.city
    table_1[2][1] = pl2.player
    table_1[3][1] = pl2.city
    table_1[4][1] = pl3.player
    table_1[5][1] = pl3.city
    table_1[6][1] = pl4.player
    table_1[7][1] = pl4.city
    score_in_table(td, num_gr)
    return table_1


def table2_data():
    """данные результатов в таблице 2-й группы"""
    table_2 = []
    td = table_2
    num_gr = "2 группа"
    t = kol_player()
    for k in range(1, t * 2 + 1):
        st = ['']
        s = (st * (t + 4))
        s.insert(0, str((k + 1) // 2))  # получаем нумерацию строк по порядку
        table_2.append(s)

    pl1 = Player.get(Player.id == 3)
    pl2 = Player.get(Player.id == 4)
    pl3 = Player.get(Player.id == 6)
    pl4 = Player.get(Player.id == 11)
    table_2[0][1] = pl1.player
    table_2[1][1] = pl1.city
    table_2[2][1] = pl2.player
    table_2[3][1] = pl2.city
    table_2[4][1] = pl3.player
    table_2[5][1] = pl3.city
    table_2[6][1] = pl4.player
    table_2[7][1] = pl4.city
    score_in_table(td, num_gr)  # вызывает функцию, где заносит счет в таблицу pdf
    return table_2


def table3_data():
    """данные результатов в таблице 3-й группы"""
    table_3 = []
    td = table_3
    num_gr = "3 группа"
    t = kol_player()
    for k in range(1, t * 2 + 1):
        st = ['']
        s = (st * (t + 4))
        s.insert(0, str((k + 1) // 2))  # получаем нумерацию строк по порядку
        table_3.append(s)
    score_in_table(td, num_gr)
    return table_3


def table4_data():
    """данные результатов в таблице 4-й группы"""
    table_4 = []
    td = table_4
    num_gr = "4 группа"
    t = kol_player()
    for k in range(1, t * 2 + 1):
        st = ['']
        s = (st * (t + 4))
        s.insert(0, str((k + 1) // 2))  # получаем нумерацию строк по порядку
        table_4.append(s)
    score_in_table(td, num_gr)
    return table_4


def table5_data():
    """данные результатов в таблице 5-й группы"""
    table_5 = []
    td = table_5
    num_gr = "5 группа"
    t = kol_player()
    for k in range(1, t * 2 + 1):
        st = ['']
        s = (st * (t + 4))
        s.insert(0, str((k + 1) // 2))  # получаем нумерацию строк по порядку
        table_5.append(s)
    score_in_table(td, num_gr)
    return table_5


def table6_data():
    """данные результатов в таблице 6-й группы"""
    table_6 = []
    td = table_6
    num_gr = "6 группа"
    t = kol_player()
    for k in range(1, t * 2 + 1):
        st = ['']
        s = (st * (t + 4))
        s.insert(0, str((k + 1) // 2))  # получаем нумерацию строк по порядку
        table_6.append(s)
    score_in_table(td, num_gr)
    return table_6


def table7_data():
    """данные результатов в таблице 5-й группы"""
    table_7 = []
    td = table_7
    num_gr = "7 группа"
    t = kol_player()
    for k in range(1, t * 2 + 1):
        st = ['']
        s = (st * (t + 4))
        s.insert(0, str((k + 1) // 2))  # получаем нумерацию строк по порядку
        table_7.append(s)
        score_in_table(td, num_gr)
    return table_7


def table8_data():
    """данные результатов в таблице 6-й группы"""
    table_8 = []
    td = table_8
    num_gr = "8 группа"
    t = kol_player()
    for k in range(1, t * 2 + 1):
        st = ['']
        s = (st * (t + 4))
        s.insert(0, str((k + 1) // 2))  # получаем нумерацию строк по порядку
        table_8.append(s)
    score_in_table(td,num_gr)
    return table_8


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
        table_5 = table5_data()
        tdt.append(table_5)
        if kg == 5:
            break
        table_6 = table6_data()
        tdt.append(table_6)
        if kg == 6:
            break
        table_7 = table7_data()
        tdt.append(table_7)
        if kg == 7:
            break
        table_8 = table8_data()
        tdt.append(table_8)
        if kg == 8:
            break
    return tdt


def score_in_table(td, num_gr):
    """заносит счет в таблицу группы pdf"""
    total_score = {}

    ta = System.select().order_by(System.id.desc()).get()
    mp = ta.max_player
    for s in range(1, mp + 1):
        total_score[s] = 0
    r = Result.select().where(Result.title_id == ta and Result.number_group == num_gr)
    count = len(r)
    result_list = r.dicts().execute()
    for i in range(0, count):
        sc_game = str(list(result_list[i].values())[9])
        if sc_game == "":
            scg = 8
        else:
            scg = 9
        tours = str(list(result_list[i].values())[3])
        p1 = int(tours[0])
        p2 = int(tours[2])
        win = str(list(result_list[i].values())[6])
        player1 = str(list(result_list[i].values())[4])
        if win != "":
            if win == player1:
                td[p1 * 2 - 2][p2 + 1] = str(list(result_list[i].values())[7])  # очки 1-ого игрока
                td[p1 * 2 - 1][p2 + 1] = str(list(result_list[i].values())[scg])  # счет 1-ого игрока
                td[p2 * 2 - 2][p1 + 1] = str(list(result_list[i].values())[11])  # очки 2-ого игрока
                td[p2 * 2 - 1][p1 + 1] = str(list(result_list[i].values())[12])  # счет 2-ого игрока
                tp1 = int(list(result_list[i].values())[7])  # очки 1-ого игрока
                tp2 = int(list(result_list[i].values())[11])  # очки 2-ого игрока
                plr1 = total_score[p1]  # считывает из словаря 1-ого игрока очки
                plr2 = total_score[p2]  # считывает из словаря 2-ого игрока очки
                plr1 = plr1 + tp1  # прибавляет очки 1-ого игрока
                plr2 = plr2 + tp2  # прибавляет очки 2-ого игрока
                total_score[p1] = plr1  # записывает сумму очков 1-му игроку
                total_score[p2] = plr2  # записывает сумму очков 2-му игроку
            else:
                td[p1 * 2 - 2][p2 + 1] = str(list(result_list[i].values())[11])  # очки 1-ого игрока
                td[p1 * 2 - 1][p2 + 1] = str(list(result_list[i].values())[12])  # счет 1-ого игрока
                td[p2 * 2 - 2][p1 + 1] = str(list(result_list[i].values())[7])  # очки 2-ого игрока
                td[p2 * 2 - 1][p1 + 1] = str(list(result_list[i].values())[scg])  # счет 2-ого игрока
                tp1 = int(list(result_list[i].values())[11])  # очки 1-ого игрока
                tp2 = int(list(result_list[i].values())[7])  # очки 2-ого игрока
                plr1 = total_score[p1]  # считывает из словаря 1-ого игрока очки
                plr2 = total_score[p2]  # считывает из словаря 2-ого игрока очки
                plr1 = plr1 + tp1  # прибавляет очки 1-ого игрока
                plr2 = plr2 + tp2  # прибавляет очки 2-ого игрока
                total_score[p1] = plr1  # записывает сумму очков 1-му игроку
                total_score[p2] = plr2  # записывает сумму очков 2-му игроку
        else:
            break
    for t in range(0, mp):
        td[t * 2][mp + 2] = total_score[t + 1]  # записывает каждому игроку сумму очков
    rank_in_group(total_score, mp, td)


def rank_in_group(total_score, mp, td):
    """выставляет места в группах соответсвеноо очкам. пока без крутиловок"""
    rev_dict = {}  # словарь, где в качастве ключа номера групп, а значения - очки
    max_value = []
    for y in range(0, mp):
        max_value.append(0)
    for key, value in total_score.items():
        rev_dict.setdefault(value, set()).add(key)
    result = [key for key, values in rev_dict.items() if len(values) > 1]

    key_list = list(total_score.keys())  # отдельно составляет список ключей
    val_list = list(total_score.values())  # отдельно составляет список значений
    sum_val = sum(val_list)
    if sum_val == 0:
        return
    else:
        if len(result) == 0:  # =========== если нет одинакового кол-во очков
            Keymax = max(total_score, key=total_score.get)  # ключ максимального значения
            mv1 = total_score[Keymax]  # максимальное значение
            td[Keymax * 2 - 2][mp + 4] = 1  # записывает 1 место игроку
            for s in range(0, mp - 1):
                mv = mv1
                mv1 = max_value[s + 1]
                for v in total_score.values():  # следующее значние по максимуму
                    if mv1 < v < mv:  # находит наибольшое из оставшихся
                        mv1 = v
                i = key_list[val_list.index(mv1)]  # находит ключ соответсвующий максимальному значению
                td[i * 2 - 2][mp + 4] = s + 2  # записывает место игроку
        else:  # =========== если одинаковое кол-во очков
            ql = set(val_list)
            q_list = len(ql)  # кол-во повторяющихся значений(сколько групп участников с равным кол-во очков)
            for a in range(0, q_list):
                key_max = max(total_score, key=total_score.get)  # ключ максимального значения (№ группы)
                max_val1 = total_score[key_max]  # максимальное значение
                ls = val_list.count(max_val1)
                for s in range(key_max, key_max + ls):
                    iv = val_list.index(max_val1, s - 1)
                    ik = key_list[iv]  # находит ключ соответсвующий максимальному значению
                    td[ik * 2 - 2][mp + 4] = 1  # записывает 1 место игроку
                mv = max_val1
                max_val1 = 0
                im = 0
                for v in val_list:  # следующее значние по максимуму
                    if max_val1 < v < mv:  # находит наибольшое из оставшихся
                        ls1 = val_list.count(v)  # кол-во этих значений (очков)
                        for x in range(0, ls1):
                            iv = val_list.index(v, im)
                            im = iv + 1
                            ik = key_list[iv]  # находит ключ соответсвующий максимальному значению
                            td[ik * 2 - 2][mp + 4] = 1 + ls  # записывает 1 место игроку
                        return

