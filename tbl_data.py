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
    pl5 = Player.get(Player.id == 12)
    pl6 = Player.get(Player.id == 13)
    # занесение фамилии и города в таблицу
    table_1[0][1] = pl1.player
    table_1[1][1] = pl1.city
    table_1[2][1] = pl2.player
    table_1[3][1] = pl2.city
    table_1[4][1] = pl3.player
    table_1[5][1] = pl3.city
    table_1[6][1] = pl4.player
    table_1[7][1] = pl4.city
    table_1[8][1] = pl5.player
    table_1[9][1] = pl5.city
    table_1[10][1] = pl6.player
    table_1[11][1] = pl6.city
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
        if sc_game == "" and sc_game == "None":
            scg = 8
        else:
            scg = 9
        tours = str(list(result_list[i].values())[3])
        p1 = int(tours[0])
        p2 = int(tours[2])
        win = str(list(result_list[i].values())[6])
        player1 = str(list(result_list[i].values())[4])
        if win != "" and win != "None":
            if win == player1:
                td[p1 * 2 - 2][p2 + 1] = str(list(result_list[i].values())[7])  # очки 1-ого игрока
                td[p1 * 2 - 1][p2 + 1] = str(list(result_list[i].values())[scg])  # счет 1-ого игрока
                td[p2 * 2 - 2][p1 + 1] = str(list(result_list[i].values())[11])  # очки 2-ого игрока
                td[p2 * 2 - 1][p1 + 1] = str(list(result_list[i].values())[12])  # счет 2-ого игрока
                tp1 = str(list(result_list[i].values())[7])  # очки 1-ого игрока
                tp2 = str(list(result_list[i].values())[11])  # очки 2-ого игрока
                plr1 = total_score[p1]  # считывает из словаря 1-ого игрока всего очков
                plr2 = total_score[p2]  # считывает из словаря 2-ого игрока всего очков
                plr1 = plr1 + int(tp1)  # прибавляет очки 1-ого игрока
                plr2 = plr2 + int(tp2)  # прибавляет очки 2-ого игрока
                total_score[p1] = plr1  # записывает сумму очков 1-му игроку
                total_score[p2] = plr2  # записывает сумму очков 2-му игроку
            else:
                td[p1 * 2 - 2][p2 + 1] = str(list(result_list[i].values())[11])  # очки 1-ого игрока
                td[p1 * 2 - 1][p2 + 1] = str(list(result_list[i].values())[12])  # счет 1-ого игрока
                td[p2 * 2 - 2][p1 + 1] = str(list(result_list[i].values())[7])  # очки 2-ого игрока
                td[p2 * 2 - 1][p1 + 1] = str(list(result_list[i].values())[scg])  # счет 2-ого игрока
                tp1 = str(list(result_list[i].values())[11])  # очки 1-ого игрока
                tp2 = str(list(result_list[i].values())[7])  # очки 2-ого игрока
                plr1 = total_score[p1]  # считывает из словаря 1-ого игрока очки
                plr2 = total_score[p2]  # считывает из словаря 2-ого игрока очки
                plr1 = plr1 + int(tp1)  # прибавляет очки 1-ого игрока
                plr2 = plr2 + int(tp2)  # прибавляет очки 2-ого игрока
                total_score[p1] = plr1  # записывает сумму очков 1-му игроку
                total_score[p2] = plr2  # записывает сумму очков 2-му игроку
    for t in range(0, mp):
        td[t * 2][mp + 2] = total_score[t + 1]  # записывает каждому игроку сумму очков
    rank_in_group(total_score, mp, td, num_gr)


def rank_in_group(total_score, mp, td, num_gr):
    """выставляет места в группах соответсвеноо очкам
    ls - кол-во человек в крутиловке"""
    rev_dict = {}  # словарь, где в качастве ключа номера групп, а значения - очки
    max_value = []

    game_max = Result.select().where(Result.number_group == num_gr)  # определение кол-во всего игр и сыгранных
    game_played = Result.select().where(Result.winner != "")
    kol_tours_played = len(game_played)
    kol_tours_in_group = len(game_max)  # кол-во всего игр в группе

    for y in range(0, mp):
        max_value.append(0)
    for key, value in total_score.items():
        rev_dict.setdefault(value, set()).add(key)
    result = [key for key, values in rev_dict.items() if len(values) > 1]

    key_list = list(total_score.keys())  # отдельно составляет список ключей (группы)
    val_list = list(total_score.values())  # отдельно составляет список значений (очки)
    sum_val = sum(val_list)
    if sum_val == 0:  # если пустая группа то не проставляет места
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
            ds = {index: value for index, value in enumerate(val_list)}  # получает словарь(ключ, очки)
            max_val = max(val_list)  # максимальное значение
            sorted_tuple = {k: ds[k] for k in sorted(ds, key=ds.get, reverse=True)}  # сортирует словарь по убываню соот
            m1 = val_list.count(max_val)  # сколько раз встречается значение
            ql = set(val_list)
            q_list = len(ql)  # кол-во повторяющихся значений(сколько групп участников с равным кол-во очков)
            mesto_points = {}
            valuesList = list(sorted_tuple.values())
            unique_numbers = list(set(valuesList))
            unique_numbers.sort(reverse=True)
            mesto = 1
            for r in range(0, q_list):  # создает словарь с уникальным кол-вом очков и соответсвиеим мест
                e = unique_numbers[r]  # из списка уникальных значений (очков)
                m_new = val_list.count(e)  # сколько раз встречается значение
                mesto_points[e] = mesto  # записывает в словарь пары (очки - мессто)
                mesto = mesto + m_new
            for t in range(0, mp):
                wr = val_list[t]  # очки игрока
                wk = key_list[t]  # номер группы
                w = mesto_points.setdefault(wr)  # находит ключ соответсвующий кол-во очков (место)
                td[wk * 2 - 2][mp + 4] = str(w)  # записывает место
            for a in range(0, m_new):
                key_max = max(total_score, key=total_score.get)  # ключ максимального значения (№ группы)
                max_val1 = total_score[key_max]  # максимальное значение
                ls = val_list.count(max_val1)  # кол-во человек в крутиловке
                tr = []
                # for s in range(key_max, key_max + ls):
                #     iv = val_list.index(max_val1, s - 1)
                #     ik = key_list[iv]  # находит ключ соответсвующий максимальному значению (№ участника в группе)
                #     ik = str(ik)
                #     tr.append(ik)  # создает список (встречи игроков)
                #     if ls > 1:
                #         if kol_tours_played == kol_tours_in_group:
                #             circle(ls, tr, num_gr, td, mp, mesto)
                #         return



def circle(ls, tr, num_gr, td, mp, mesto):
    """выставляет места в крутиловке
    -tour- встречи игроков, p1, p2 фамилии, num_gr номер группы
    ls кол-во игроков с одинаковым кол-вом очков, mp общее кол-во ироков в группе"""
    if ls == 2:  # кол-во человек в крутиловке (одинаковое кол-во очков)
        tour = "-".join(tr)  # делает строку встреча в туре
        p1 = int(tour[0])
        p2 = int(tour[2])
        c = Result.select().where((Result.number_group == num_gr) & (Result.tours == tour)).get()  # ищет в базе
        # строчку номер группы в туре
        if c.winner == c.player1:
            points_p1 = c.points_win  # очки во встрече победителя
            points_p2 = c.points_loser  # очки во встрече проигравшего
            td[p1 * 2 - 2][mp + 4] = mesto  # записывает место победителю
            td[p2 * 2 - 2][mp + 4] = mesto + 1  # записывает место проигравшему
        else:
            points_p1 = c.points_loser
            points_p2 = c.points_win
            td[p1 * 2 - 2][mp + 4] = mesto + 1  # очки во встрече победителя
            td[p2 * 2 - 2][mp + 4] = mesto  # очки во встрече проигравшего
        td[p1 * 2 - 2][mp + 3] = points_p1  # записывает место победителю
        td[p2 * 2 - 2][mp + 3] = points_p2  # записывает место проигравшему
    elif ls == 3:
        tr_all = []
        game_p1 = []
        game_p2 = []
        pp = {1: [], 2: [], 3: []}  # словарь со списками очков каждого игрока в крутиловке
        pg_win = {1: [], 2: [], 3: []}
        pg_los = {1: [], 2: [], 3: []}
        tr3 = []  # 3-я пара игроков в крутиловке
        tr1 = tr[:2]  # 1-я пара игроков в крутиловке
        tr2 = tr[1:]  # 2-я пара игроков в крутиловке
        tr3.append(tr[0])
        tr3.append(tr[2])
        tr_all.append(tr1)  # получение списка списков всех туров крутиловки
        tr_all.append(tr2)
        tr_all.append(tr3)

        for n in range(0, ls):
            tour = "-".join(tr_all[n])  # получает строку встреча в туре
            k1 = tr_all[n][0]  # 1-й игрок в туре
            k2 = tr_all[n][1]  # 2-й игрок в туре
            ki1 = tr.index(k1)  # получение индекса 1-й игрока
            ki2 = tr.index(k2)

            c = Result.select().where((Result.number_group == num_gr) & (Result.tours == tour)).get()  # ищет в базе
            # данную встречу
            if c.winner == c.player1:  # победил 1-й игрок
                points_p1 = c.points_win  # очки победителя
                points_p2 = c.points_loser  # очки проигравшего
                game_p1 = c.score_in_game  # счет во встречи (выиграные и проигранные партии) победителя
                game_p2 = c.score_loser  # счет во встречи (выиграные и проигранные партии) проигравшего
                p1_game_win = int(game_p1[0])
                p1_game_los = int(game_p1[4])
                p2_game_win = int(game_p2[0])
                p2_game_los = int(game_p2[4])
            else:
                points_p1 = c.points_loser
                points_p2 = c.points_win
                game_p1 = c.score_loser
                game_p2 = c.score_in_game
                p1_game_win = int(game_p1[0])
                p1_game_los = int(game_p1[4])
                p2_game_win = int(game_p2[0])
                p2_game_los = int(game_p2[4])

            pp[ki1 + 1].append(points_p1)  # добавляет очки 1-ому игроку встречи
            pp[ki2 + 1].append(points_p2)  # добавляет очки 2-ому игроку встречи
            pg_win[ki1 + 1].append(p1_game_win)
            pg_los[ki1 + 1].append(p1_game_los)
            pg_win[ki2 + 1].append(p2_game_win)
            pg_los[ki2 + 1].append(p2_game_los)
            ps = []
        for i in range(1, ls + 1):  # суммирует очки каждого игрока
            pp[i] = sum(pp[i])
            pg_win[i] = sum(pg_win[i])
            pg_los[i] = sum(pg_los[i])
            x = pg_win[i] / pg_los[i]
            x = float('{:.3f}'.format(x))
            ps.append(x)

        if pp[1] == pp[2] == pp[3]:  # сравнивает их между собой, если они у всех они равны
            d = {index: value for index, value in enumerate(tr)}  # получает словарь(ключ, номер группы)
            ds = {index: value for index, value in enumerate(ps)}  # получает словарь(ключ, соотношение)
            sorted_tuple = {k: ds[k] for k in sorted(ds, key=ds.get, reverse=True)}  # сортирует словарь по убываню соот

            for i in range(0, ls):
                w = int(d.setdefault(i))  # получает ключ словаря с номером группы
                wq = sorted_tuple.setdefault(i)  # получает соотношение
                td[w * 2 - 2][mp + 3] = wq  # записывает соотношения игроку
                td[w * 2 - 2][mp + 4] = i + mesto  # записывает место
