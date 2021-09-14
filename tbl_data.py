
from models import *


def kol_player():
    """выводит максимальное количество человек в группе t если все группы равны, а g2 если разное количество"""
    t = Title.select().order_by(Title.id.desc()).get()  # получение id последнего соревнования
    ta = System.select().order_by(System.id).where(System.title_id == t).get()  # находит system id последнего
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


def table_data(kg):
    """циклом создаем список участников каждой группы"""
    t = Title.select().order_by(Title.id.desc()).get()  # получение id последнего соревнования
    ta = Result.select().where(Result.title_id == t)  # находит system id последнего
    tr = len(ta)  # проверяет заполнена ли таблица (если строк 0, то еще нет записей)
    tbl_tmp = []  # временный список группы tbl
    tdt = []
    t = kol_player()
    for p in range(0, kg):
        num_gr = f"{p + 1} группа"
        posev_data = player_choice_in_group(num_gr)
        for k in range(1, t * 2 + 1):  # цикл нумерации строк (2-е строки на каждого участника
            st = ['']
            s = (st * (t + 4))  # получаем пустой список номер, фамилия или регион, клетки (колво участников)
            s.insert(0, str((k + 1) // 2))  # получаем нумерацию строк по порядку
            tbl_tmp.append(s)
        for i in range(1, t * 2 + 1, 2):
            posev = posev_data[((i + 1) // 2) - 1]
            tbl_tmp[i - 1][1] = posev["фамилия"]
            tbl_tmp[i][1] = posev["регион"]
        td = tbl_tmp.copy()
        tbl_tmp.clear()
        tdt.append(td)
        if tr != 0:  # если еще не была жеребъевка, то пропуск счета в группе
            score_in_table(td, num_gr)
    return tdt


def setka_data_16(fin):
    """данные сетки на 16"""
    t = Title.select().order_by(Title.id.desc()).get()  # получение id последнего соревнования
    system = System.select().where(System.title_id == t)  # находит system id последнего
    for sys in system.select():  # проходит циклом по всем отобранным записям
        if sys.stage == fin:
            mp = sys.max_player
    tds = []
    posev_data = player_choice_in_setka(fin)
    for i in range(1, mp * 2 + 1, 2):
        posev = posev_data[((i + 1) // 2) - 1]
        family = posev['фамилия']
        space = family.find(" ")  # находит пробел отделяющий имя от фамилии
        line = family.find("/")  # находит черту отделяющий имя от города
        city_slice = family[line:]  # получает отдельно город
        family_slice = family[:space + 2]   # получает отдельно фамилия и первую букву имени
        family_city = f'{family_slice}.{city_slice}'   # все это соединяет
        tds.append(family_city)
    return tds


def score_in_table(td, num_gr):
    """заносит счет в таблицу группы pdf
    -td- список строки таблицы, куда пишут счет"""
    total_score = {}  # словарь, где ключ - номер группы, а значение - очки
    t = Title.select().order_by(Title.id.desc()).get()  # получение id последнего соревнования
    ta = System.select().order_by(System.id).where(System.title_id == t).get()  # находит system id последнего
    mp = ta.max_player
    for s in range(1, mp + 1):
        total_score[s] = 0
    r = Result.select().where(Result.title_id == ta and Result.number_group == num_gr)
    count = len(r)
    result_list = r.dicts().execute()
    for i in range(0, count):
        sc_game = str(list(result_list[i].values())[9])
        if sc_game == "" and sc_game == "None":  # номер столбца
            scg = 8
        else:
            scg = 9
        tours = str(list(result_list[i].values())[3])  # номера игроков в туре
        p1 = int(tours[0])
        p2 = int(tours[2])
        win = str(list(result_list[i].values())[6])
        player1 = str(list(result_list[i].values())[4])
        if win != "" and win != "None":  # если нет сыгранной встречи данного тура
            if win == player1:  # если победитель игрок под первым номером в туре
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
            else:  # если победитель игрок под вторым номером в туре
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
    gl = Game_list.select().where(Game_list.id == 1)
    a = len(gl)
    if a >= 1:
        rank_in_group(total_score, mp, td, num_gr)
    else:
        return


def numer_game(num_game):
    """определяет куда записывать победителя и проигравшего по сноске в сетке, номера встреч"""
    snoska = []
    num_game = int(num_game)
    # решить игры за места===================
    dict_winner = {1: 9, 2: 9, 3: 10, 4: 10, 5: 11, 6: 11, 7: 12, 8: 12, 9: 13, 10: 13, 11: 14, 12: 14, 13: 15, 14: 15,
                   17: 19, 18: 19, 21: 25, 22: 25, 23: 26, 24: 26, 25: 27, 26: 27, 29: 31, 30: 31}
    dict_loser = {1: 21, 2: 21, 3: 22, 4: 22, 5: 23, 6: 23, 7: 24, 8: 24, 9: 17, 10: 17, 11: 18, 12: 18, 13: 16, 14: 16,
                  17: 20, 18: 20, 21: 29, 22: 29, 23: 30, 24: 30, 25: 28, 26: 28, 29: 32, 30: 32}
    dict_loser_pdf = {1: -1, 2: -2, 3: -3, 4: -4, 5: -5, 6: -6, 7: -7, 8: -8, 9: -9, 10: -10, 11: -11, 12: -12, 13: -13,
                      14: -14, 17: -17, 18: -18, 21: -21, 22: -22, 23: -23, 24: -24, 25: -25, 26: -26, 29: -29, 30: -30}
    dict_mesta = [15, 16, 19, 20, 27, 28, 31, 32]

    if num_game in dict_mesta:
        index = dict_mesta.index(num_game)
        snoska = [0, 0]
        game_loser = dict_mesta[index] * -1  # для отбражения в pdf (встречи с минусом)
        snoska.append(game_loser)
    else:
        game_winner = dict_winner[num_game]  # номер игры победителя
        snoska.append(game_winner)
        game_loser = dict_loser[num_game]  # номер игры проигравшего
        snoska.append(game_loser)
        game_loser = dict_loser_pdf[num_game]  # для отбражения в pdf (встречи с минусом)
        snoska.append(game_loser)
    return snoska


def score_in_setka(fin):
    """ выставляет счет победителя и сносит на свои места в сетке"""
    dict_setka = {}
    match = []
    tmp_match = []
    t = Title.select().order_by(Title.id.desc()).get()  # получение id последнего соревнования
    result = Result.select().where(Result.title_id == t and Result.number_group == fin)  # находит system id последнего

    for res in result:
        num_game = int(res.tours)
        family_win = res.winner
        if res.winner is not None and res.winner != "":
            snoska = numer_game(num_game)
            tmp_match.append(snoska[0])
            tmp_match.append(res.winner)
            tmp_match.append(f'{res.score_in_game} {res.score_win}')
            tmp_match.append(snoska[2])
            tmp_match.append(res.loser)
            match = tmp_match.copy()
            tmp_match.clear()
            dict_setka[num_game] = match
    return dict_setka


def rank_in_group(total_score, max_person, td, num_gr):
    """выставляет места в группах соответсвенно очкам
    men_of_circle - кол-во человек в крутиловке"""
    rev_dict = {}  # словарь, где в качастве ключа очки, а значения - номера групп

    game_max = Result.select().where(Result.number_group == num_gr)  # сколько всего игр в группе
    played = Result.select().where(Result.number_group == num_gr)  # 1-й запрос на выборку с группой
    game_played = played.select().where(Result.winner is None or Result.winner != "")  # 2-й запрос на выборку
    # с победителями из 1-ого запроса
    kol_tours_played = len(game_played)  # сколько игр сыгранных
    kol_tours_in_group = len(game_max)  # кол-во всего игр в группе

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
            Keymax = max(total_score, key=total_score.get)  # ключ максимального значения (группа)
            m_val_1 = total_score[Keymax]  # максимальное значение (очки)
            td[Keymax * 2 - 2][max_person + 4] = 1  # записывает 1 место игроку
            new_list = val_list.copy()  # создает копию списка
            for s in range(0, max_person - 1):  # цикл по игрокам группы
                m_val = m_val_1
                new_list.remove(m_val)  # удаляет из копии списка макс значение
                m_val_1 = max(new_list)  # находит макс значение из оставшихся
                i = key_list[val_list.index(m_val_1)]  # находит ключ соответсвующий максимальному значению
                td[i * 2 - 2][max_person + 4] = s + 2  # записывает место игроку
        else:  # =========== если одинаковое кол-во очков
            ds = {index: value for index, value in enumerate(val_list)}  # получает словарь(ключ, очки)
            sorted_tuple = {k: ds[k] for k in sorted(ds, key=ds.get, reverse=True)}  # сортирует словарь по убываню соот
            mesto_points = {}  # словарь (ключ-очки, а значения места без учета соотношений)
            valuesList = list(sorted_tuple.values())
            unique_numbers = list(set(valuesList))
            unique_numbers.sort(reverse=True)
            q_list = len(unique_numbers)  # кол-во повторяющихся значений(сколько групп участников с равным кол-во очков)
            mesto = 1
            for r in range(0, q_list):  # создает словарь с уникальным кол-вом очков и соответствием мест (очки-место)
                e = unique_numbers[r]  # из списка уникальных значений (очков)
                m_new = val_list.count(e)  # сколько раз встречается значение
                mesto_points[e] = mesto  # записывает в словарь пары (очки - место)
                mesto = mesto + m_new  #
            for t in range(0, max_person):  # цикл записи группа место (без уточнения мест в крутиловке)
                wr = val_list[t]  # очки игрока
                wk = key_list[t]  # номер группы
                w = mesto_points.setdefault(wr)  # находит ключ соответсвующий кол-во очков (место)
                men_of_circle = val_list.count(wr)  # кол-во человек в крутиловке
                mesto = 1
                if men_of_circle > 1:
                    mesto = int(w)
                td[wk * 2 - 2][max_person + 4] = str(w)  # записывает место
                tr = []
                if men_of_circle > 1 and kol_tours_played == kol_tours_in_group:  # когда все встречи сыграны
                    # и есть крутиловки
                    num_player = rev_dict.get(wr)
                    for x in num_player:
                        tr.append(str(x))  # создает список (встречи игроков)
                    circle(men_of_circle, tr, num_gr, td, max_person, mesto)


def circle(men_of_circle, tr, num_gr, td, max_person, mesto):
    """выставляет места в крутиловке
    -tour- встречи игроков, p1, p2 фамилии, num_gr номер группы
    men_of_circle кол-во игроков с одинаковым кол-вом очков,
    max_person общее кол-во ироков в группе"""
    if men_of_circle == 2:  # кол-во человек в крутиловке (одинаковое кол-во очков)
        tour = "-".join(tr)  # делает строку встреча в туре
        p1 = int(tour[0])
        p2 = int(tour[2])
        c = Result.select().where((Result.number_group == num_gr) & (Result.tours == tour)).get()  # ищет в базе
        # строчку номер группы и тур по двум столбцам
        if c.winner == c.player1:
            points_p1 = c.points_win  # очки во встрече победителя
            points_p2 = c.points_loser  # очки во встрече проигравшего
            td[p1 * 2 - 2][max_person + 4] = mesto  # записывает место победителю
            td[p2 * 2 - 2][max_person + 4] = mesto + 1  # записывает место проигравшему
        else:
            points_p1 = c.points_loser
            points_p2 = c.points_win
            td[p1 * 2 - 2][max_person + 4] = mesto + 1  # очки во встрече победителя
            td[p2 * 2 - 2][max_person + 4] = mesto  # очки во встрече проигравшего
        td[p1 * 2 - 2][max_person + 3] = points_p1  # записывает место победителю
        td[p2 * 2 - 2][max_person + 3] = points_p2  # записывает место проигравшему
    elif men_of_circle == 3:
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
        # tours_in_circle(tr, pp)

        for n in range(0, men_of_circle):
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
            pps = []
        for i in range(1, men_of_circle + 1):  # суммирует очки каждого игрока
            pp[i] = sum(pp[i])  # сумма очков

        if pp[1] == pp[2] == pp[3]:  # сравнивает очки между собой, если они у всех равны
            for i in range(1, men_of_circle + 1):  # суммирует выйгранные и проигранные партии каждого игрока
                pg_win[i] = sum(pg_win[i])  # сумма выйгранных партий
                pg_los[i] = sum(pg_los[i])  # сумма проигранных партий
                x = pg_win[i] / pg_los[i]
                x = float('{:.3f}'.format(x))
                ps.append(x)
                pps.append(pp[i])

            d = {index: value for index, value in enumerate(tr)}  # получает словарь(ключ, номер участника)
            ds = {index: value for index, value in enumerate(ps)}  # получает словарь(ключ, соотношение)
            sorted_tuple = {k: ds[k] for k in sorted(ds, key=ds.get, reverse=True)}  # сортирует словарь по убываню соот
            key_l = list(sorted_tuple.keys())
            val_l = list(sorted_tuple.values())
            vls = set(val_l)  # группирует разные значения
            vl = len(vls)  # подсчитывает их колличество
            m = 0
            if vl == 1:  # посчитывает соотношений выйгранных и проигранных мячей в партиях
                plr_ratio = score_in_circle(tr_all, men_of_circle, num_gr, tr)
                sorted_ratio = {k: plr_ratio[k] for k in sorted(plr_ratio, key=plr_ratio.get, reverse=True)}  # сортирует словарь по убываню соот
                key_ratio = list(sorted_ratio.keys())  # получает список ключей отсортированного словаря
                r = 0
                for i in key_ratio:
                    ratio = sorted_ratio[i]  # соотношение в крутиловке
                    person = int(d[i])  # номер игрока
                    td[person * 2 - 2][max_person + 3] = str(ratio)  # записывает место
                    td[person * 2 - 2][max_person + 4] = str(mesto + r)  # записывает место
                    r += 1
            else:
                for i in val_l:
                    w = key_l[val_l.index(i)]  # получает ключ, по которому в списке ищет игрока
                    wq = int(d.setdefault(w))  # получает номер группы, соответсвующий
                    td[wq * 2 - 2][max_person + 3] = str(i)  # записывает соотношения игроку
                    td[wq * 2 - 2][max_person + 4] = str(m + mesto)  # записывает место
                    m += 1

        else:  # если очки равны, но внутри крутиловки у всех очки разные (без подсчета соотношений)
            d = {index: value for index, value in enumerate(tr)}  # получает словарь(ключ, номер группы)
            sorted_tuple = {k: pp[k] for k in sorted(pp, key=pp.get, reverse=True)}  # сортирует словарь по убываню соот
            key_l = list(sorted_tuple.keys())
            val_l = list(sorted_tuple.values())
            m = 0
            for i in val_l:
                w = key_l[val_l.index(i)]  # получает ключ, по которому в списке ищет групп
                wq = int(d.setdefault(w - 1))  # получает номер группы, соответсвующий
                td[wq * 2 - 2][max_person + 3] = str(i)  # записывает соотношения игроку
                td[wq * 2 - 2][max_person + 4] = str(m + mesto)  # записывает место
                m += 1
    elif men_of_circle == 4:
        pass


def score_in_circle(tr_all, men_of_circle, num_gr, tr):
    """подсчитывает счет по партиям в крутиловке"""
    plr_win = {0: [], 1: [], 2: []}
    plr_los = {0: [], 1: [], 2: []}
    plr_ratio = {0: [], 1: [], 2: []}
    for n in range(0, men_of_circle):
        tour = "-".join(tr_all[n])  # получает строку встреча в туре
        c = Result.select().where((Result.number_group == num_gr) & (Result.tours == tour)).get()  # ищет в базе
        k1 = tr_all[n][0]  # 1-й игрок в туре
        k2 = tr_all[n][1]  # 2-й игрок в туре
        ki1 = tr.index(k1)  # получение индекса 1-й игрока
        ki2 = tr.index(k2)
        g = c.score_win
        g_len = len(g)
        g = g[1:g_len - 1]
        sc_game = g.split(",")

        if c.winner == c.player1:  # победил 1-й игрок
            for i in sc_game:
                i = int(i)
                if i < 0:
                    plr_win[ki1].append(abs(i))
                    plr_los[ki2].append(abs(i))
                    if abs(i) < 10:
                        plr_los[ki1].append(11)
                        plr_win[ki2].append(11)
                    else:
                        plr_los[ki1].append(abs(i) + 2)
                        plr_win[ki2].append(abs(i) + 2)
                elif 0 <= i < 10:
                    plr_win[ki1].append(11)
                    plr_los[ki1].append(i)
                    plr_win[ki2].append(i)
                    plr_los[ki2].append(11)
                elif i >= 10:
                    plr_win[ki1].append(i + 2)
                    plr_los[ki1].append(i)
                    plr_win[ki2].append(i)
                    plr_los[ki2].append(i + 2)
        else:  # если победил 2-й игрок
            for i in sc_game:
                i = int(i)
                if i < 0:  # партию проиграл
                    plr_win[ki2].append(abs(i))
                    plr_los[ki1].append(abs(i))
                    if abs(i) < 10:
                        plr_los[ki2].append(11)
                        plr_win[ki1].append(11)
                    else:
                        plr_los[ki2].append(abs(i) + 2)
                        plr_win[ki1].append(abs(i) + 2)
                elif 0 <= i < 10:  # выйграл партию
                    plr_win[ki2].append(11)
                    plr_los[ki2].append(i)
                    plr_win[ki1].append(i)
                    plr_los[ki1].append(11)
                elif i >= 10:  # выйграл партию на больше меньше
                    plr_win[ki2].append(i + 2)
                    plr_los[ki2].append(i)
                    plr_win[ki1].append(i)
                    plr_los[ki1].append(i + 2)
    for n in range(0, men_of_circle):
        plr_win[n] = sum(plr_win[n])
        plr_los[n] = sum(plr_los[n])
        x = plr_win[n] / plr_los[n]
        x = float('{:.3f}'.format(x))
        plr_ratio[n] = x
    return plr_ratio


def player_choice_in_group(num_gr):
    """распределяет спортсменов по группам согласно жеребъевке"""
    posev_data = []
    choice = Choice.select().order_by(Choice.posev_group).where(Choice.group == num_gr)
    for posev in choice:
        posev_data.append({
            'фамилия': posev.family,
            'регион': posev.region,
        })
    return posev_data


def player_choice_in_setka(fin):
    """распределяет спортсменов в сетке согласно жеребъевке"""
    posev_data = []
    choice = Choice.select().order_by(Choice.posev_final).where(Choice.final == fin)
    for posev in choice:
        player = Player.get(Player.player == posev.family)
        city = player.city
        posev_data.append({
            'посев': posev.posev_final,
            'фамилия': f'{posev.family}/ {city}'
        })
    return posev_data