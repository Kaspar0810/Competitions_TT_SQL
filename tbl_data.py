
from models import *
from itertools import *
from collections import Counter


def kol_player():
    """выводит максимальное количество человек в группе t если все группы равны, а g2 если разное количество"""
    title = Title.select().order_by(Title.id.desc()).get()  # получение id последнего соревнования
    ta = System.select().order_by(System.id).where(System.title_id == title).get()  # находит system id последнего
    a = ta.total_athletes
    g = ta.total_group
    e = a % g  # если количество участников равно делится на группы
    t = a // g  # если количество участников не равно делится на группы, g2 наибольшое кол-во человек в группе
    g2 = t + 1
    if e == 0:
        t = t
    else:
        t = g2
    return t


def table_data(kg, title_id):
    """циклом создаем список участников каждой группы"""
    ta = Result.select().where(Result.title_id == title_id)  # находит system id последнего
    tr = len(ta)  # проверяет заполнена ли таблица (если строк 0, то еще нет записей)
    tbl_tmp = []  # временный список группы tbl
    tdt = []
    y = kol_player()
    for p in range(0, kg):
        num_gr = f"{p + 1} группа"
        posev_data = player_choice_in_group(num_gr)
        count_player_group = len(posev_data)
        # for k in range(1, count_player_group * 2 + 1):  # цикл нумерации строк (2-е строки на каждого участника
        for k in range(1, y * 2 + 1):  # цикл нумерации строк (по 2-е строки на каждого участника)
            st = ['']
            s = (st * (y + 4))  # получаем пустой список (номер, фамилия и регион, клетки (кол-во уч), оч, соот, место)
            s.insert(0, str((k + 1) // 2))  # получаем нумерацию строк по порядку
            tbl_tmp.append(s)
        for i in range(1, count_player_group * 2 + 1, 2):
            posev = posev_data[((i + 1) // 2) - 1]
            tbl_tmp[i - 1][1] = posev["фамилия"]
            tbl_tmp[i][1] = posev["регион"]
        td = tbl_tmp.copy()
        tbl_tmp.clear()
        tdt.append(td)
        if tr != 0:  # если еще не была жеребьевка, то пропуск счета в группе
            score_in_table(td, num_gr)
    return tdt


def setka_data_16(fin):
    """данные сетки на 16"""
    t = Title.select().order_by(Title.id.desc()).get()  # получение id последнего соревнования
    system = System.select().where(System.title_id == t)  # находит system id последнего
    for sys in system:  # проходит циклом по всем отобранным записям
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
    total_score = {}  # словарь, где ключ - номер участника группы, а значение - очки
    t = Title.select().order_by(Title.id.desc()).get()  # получение id последнего соревнования
    ta = System.select().order_by(System.id).where(System.title_id == t).get()  # находит system id последнего
    mp = ta.max_player

    # for s in range(1, mp + 1):
    #     total_score[s] = 0
    r = Result.select().where(Result.title_id == ta and Result.number_group == num_gr)
    choice = Choice.select().where(Choice.group == num_gr)  # фильтрует по группе
    count = len(r)
    count_player = len(choice)  # определяет сколько игроков в группе
    result_list = r.dicts().execute()
 # новый вариант
    for s in range(1, count_player + 1):
        total_score[s] = 0

    for i in range(0, count):
        sc_game = str(list(result_list[i].values())[9])  # счет в партиях
        if sc_game != "" or sc_game != "None":
            scg = 9
        else:  # номер столбца
            scg = 8
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
    # for t in range(0, mp):  # записывает очки не зависимо от кол-во игроков в группе
    #     td[t * 2][mp + 2] = total_score[t + 1]  # записывает каждому игроку сумму очков
    for t in range(0, count_player):  # записывает очки в зависимости от кол-во игроков в группе
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


def result_rank_group(num_gr, player_rank_group):
    """записывает места из группы в таблицу -Choice-"""
    if len(player_rank_group) > 0:
        t = Title.select().order_by(Title.id.desc()).get()  # получение последней записи в таблице
        system = System.select().order_by(System.id).where(System.title_id == t)  # находит system id последнего
        choice = Choice.select().where(Choice.group == num_gr)
        count = len(choice)
        for ch in choice:
            for i in range(0, count):
                if ch.posev_group == player_rank_group[i][0]:
                    with db:
                        ch.mesto_group = player_rank_group[i][1]
                        ch.save()


def rank_in_group(total_score, max_person, td, num_gr):
    """выставляет места в группах соответсвенно очкам
    men_of_circle - кол-во человек в крутиловке
    player_rank_group - список списков номер игрока - место
    num_player -
    player_group - кол-во участников в группе"""
    pl_group = Choice.select().where(Choice.group == num_gr)
    player_group = len(pl_group)
    rev_dict = {}  # словарь, где в качастве ключа очки, а значения - номера групп
    player_rank_group = []
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
            player_rank_group.append([td[Keymax * 2 - 2][max_person + 4], 1])  # список номер игрока в группе и 1
                # место для занесения в таблицу -Choice-
            new_list = val_list.copy()  # создает копию списка
            for s in range(0, player_group - 1):  # цикл по игрокам группы
                m_val = m_val_1
                new_list.remove(m_val)  # удаляет из копии списка макс значение
                m_val_1 = max(new_list)  # находит макс значение из оставшихся
                i = key_list[val_list.index(m_val_1)]  # находит ключ соответсвующий максимальному значению
                td[i * 2 - 2][max_person + 4] = s + 2  # записывает место игроку
                # место для занесения в таблицу -Choice-
                player_rank_group.append([int(td[i * 2 - 2][0]), s + 2])
        else:  # =========== если одинаковое кол-во очков
            ds = {index: value for index, value in enumerate(val_list)}  # получает словарь(ключ - номер участника,
            # значение - очки)
            sorted_tuple = {k: ds[k] for k in sorted(ds, key=ds.get, reverse=True)}  # сортирует словарь по убываню соот
            mesto_points = {}  # словарь (ключ-очки, а значения места без учета соотношений)
            valuesList = list(sorted_tuple.values())
            unique_numbers = list(set(valuesList))
            unique_numbers.sort(reverse=True)
            q_list = len(unique_numbers)  # кол-во повторяющ значений(сколько групп участников с равным кол-во очков)
            mesto = 1
            for r in range(0, q_list):  # создает словарь с уникальным кол-вом очков и соответствием мест (очки-место)
                e = unique_numbers[r]  # из списка уникальных значений (очков)
                m_new = val_list.count(e)  # сколько раз встречается значение
                mesto_points[e] = mesto  # записывает в словарь пары (очки - место)
                mesto = mesto + m_new  #
            for t in unique_numbers:  # цикл записи группа место (без уточнения мест в крутиловке)
                wr = val_list.index(t)  # очки игрока
                wk = key_list[wr]  # номер игрока группы
                w = mesto_points.setdefault(t)  # находит ключ соответсвующий кол-во очков (место)
                men_of_circle = val_list.count(t)  # кол-во человек в крутиловке
                mesto = 1
                # если есть игроки с одинаковыми очками, то создает список (номера игроков)
                if men_of_circle > 1:
                    number_player = []
                    for key, value in ds.items():
                        if value == t:
                            number_player.append(key)
                    mesto = w
                    for q in number_player:
                        td[q * 2][max_person + 4] = str(w)  # записывает место
                        player_rank_group.append([int(td[q * 2][0]), str(w)])
                else:
                    td[wk * 2 - 2][max_person + 4] = str(w)  # записывает место
                    player_rank_group.append([int(td[wk * 2 - 2][0]), str(w)])
                tr = []
                if men_of_circle > 1 and kol_tours_played == kol_tours_in_group:  # встречи сыграныи и есть крутиловки
                    num_player = rev_dict.get(t)
                    for x in num_player:
                        tr.append(str(x))  # создает список (встречи игроков)
                    player_rank = circle(men_of_circle, tr, num_gr, td, max_person, mesto)
                    player_rank.sort()  # сортирует список по возрастанию группы
                    pc = len(player_rank)  # кол-во
                    for i in range(0, pc):  # заменяет список (места еще не праставлены) на новый с правильными местами
                        a = 0
                        pl = player_rank[i]
                        for p in player_rank_group:
                            if p[0] == pl[0]:
                                player_rank_group[a] = pl
                                break
                            a += 1
    if kol_tours_played == kol_tours_in_group:  # когда все встречи сыграны
        result_rank_group(num_gr, player_rank_group)  # функция простановки мест из группы в -Choice-


def circle(men_of_circle, tr, num_gr, td, max_person, mesto):
    """выставляет места в крутиловке
    -tour- встречи игроков, p1, p2 фамилии, num_gr номер группы
    men_of_circle кол-во игроков с одинаковым кол-вом очков,
    max_person общее кол-во игроков в группе
    player_rank - список (номер игроков и их места)"""

    player_rank = []
    tr_all = []
    ps = []
    pps = []
    pp = {}
    pg_win = {}
    pg_los = {}
    pp_all = []

    for r in range(1, men_of_circle + 1):
        pp[r] = []
        pg_win[r] = []
        pg_los[r] = []
    for i in combinations(tr, 2):  # получает список с парами игроков в туре
        i = list(i)
        tr_all.append(i)

    count_game_circle = len(tr_all)

    if men_of_circle == 2:  # у двоих человек одинаковое кол-во очков, определяем по личной победе
        circle_2_player(tr, td, max_person, mesto, player_rank, num_gr)
    elif men_of_circle > 2:  # 3 или больше спортсмена в крутиловке
        for n in range(0, count_game_circle):
            tour = "-".join(tr_all[n])  # получает строку встреча в туре
            k1 = tr_all[n][0]  # 1-й игрок в туре
            k2 = tr_all[n][1]  # 2-й игрок в туре
            ki1 = tr.index(k1)  # получение индекса 1-й игрока
            ki2 = tr.index(k2)
            sum_points_circle(num_gr, tour, ki1, ki2, pg_win, pg_los, pp)

        for i in range(1, men_of_circle + 1):  # суммирует очки каждого игрока
            pp[i] = sum(pp[i])  # сумма очков
            pp_all.append(pp[i])

        lst = Counter(pp_all).keys()  # ищет уникальные значения (очки игроков в крутиловке)
        uniq = len(lst)

        if men_of_circle == 3:
            circle_3_player(uniq, tr, td, max_person, mesto, player_rank, num_gr, ps, tr_all, men_of_circle,
                            pg_win, pg_los, pp, pps)
        elif men_of_circle == 4:  # ищет вариант крутиловки (2 + 2) или (1 + 3)
            tmp = []  # временный список
            count_list = []  # список списков (кол-во очков, их повторяемость)
            count_l = []
            group_dict = {}
            for z in lst:
                n = pp_all.count(z)  # определяет кол-во вс
                count_l.clear()
                count_l.append(z)
                count_l.append(n)
                tmp = count_l.copy()
                count_list.append(tmp)
            count_list.sort(reverse=True)
            for x in range(0, men_of_circle):
                group_dict[tr[x]] = pp_all[x]
            ret = count_list[0][1]
            k_list = list(group_dict.keys())  # отдельно составляет список ключей (группы)
            v_list = list(group_dict.values())  # отдельно составляет список значений (очки)

            if ret == 2:
                tur = []
                for y in range(0, ret):
                    for x in group_dict.keys():
                        max_zn = count_list[y][0]  # максимальное значение (очков игрока в крутиловке)
                        if group_dict[x] == max_zn:  # если у игрока кол-во очков равно max_zn, то дабавляет в тур
                            tur.append(x)
                            tr = tur.copy()
                    circle_2_player(tr, td, max_person, mesto, player_rank, num_gr)
                    tur.clear()
                    mesto = mesto + ret  # меняет место на новое
            elif ret == 3:
                circle_3_player()
    return player_rank


def circle_2_player(tr, td, max_person, mesto, player_rank, num_gr):
    """крутиловка из 2-ух человек"""
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
        player_rank.append([p1, mesto])
        player_rank.append([p2, mesto + 1])
    else:
        points_p1 = c.points_loser
        points_p2 = c.points_win
        td[p1 * 2 - 2][max_person + 4] = mesto + 1  # записывает место победителю
        td[p2 * 2 - 2][max_person + 4] = mesto  # записывает место проигравшему
        player_rank.append([p1, mesto + 1])
        player_rank.append([p2, mesto])
    td[p1 * 2 - 2][max_person + 3] = points_p1  # очки во встрече победителя
    td[p2 * 2 - 2][max_person + 3] = points_p2  # очки во встрече проигравшего


def circle_3_player(uniq, tr, td, max_person, mesto, player_rank, num_gr, ps, tr_all, men_of_circle,
                    pg_win, pg_los, pp, pps):
    """в крутиловке 3-и спортсмена"""
    if uniq == 1:  # у всех трех участников равное кол-во очков
        for k in range(1, men_of_circle + 1):  # суммирует выйгранные и проигранные партии каждого игрока
                pg_win[k] = sum(pg_win[k])  # сумма выйгранных партий
                pg_los[k] = sum(pg_los[k])  # сумма проигранных партий
                x = pg_win[k] / pg_los[k]
                x = float('{:.3f}'.format(x))
                ps.append(x)
                pps.append(pp[k])
        d = {index: value for index, value in enumerate(tr)}  # получает словарь(ключ, номер участника)
        ds = {index: value for index, value in enumerate(ps)}  # получает словарь(ключ, соотношение)
        sorted_tuple = {k: ds[k] for k in sorted(ds, key=ds.get, reverse=True)}  # сортирует словарь по убываню соот
        key_l = list(sorted_tuple.keys())
        val_l = list(sorted_tuple.values())
        vls = set(val_l)  # группирует разные значения
        vl = len(vls)  # подсчитывает их колличество
        m = 0
        if vl == 1:  # подсчитывает соотношения выйгранных и проигранных мячей в партиях
            plr_ratio = score_in_circle(tr_all, men_of_circle, num_gr, tr)
            sorted_ratio = {k: plr_ratio[k] for k in
                            sorted(plr_ratio, key=plr_ratio.get, reverse=True)}  # сортирует словарь по убываню соот
            key_ratio = list(sorted_ratio.keys())  # получает список ключей отсортированного словаря
            r = 0
            for i in key_ratio:
                ratio = sorted_ratio[i]  # соотношение в крутиловке
                person = int(d[i])  # номер игрока
                td[person * 2 - 2][max_person + 3] = str(ratio)  # записывает соотношение
                td[person * 2 - 2][max_person + 4] = str(mesto + r)  # записывает место
                player_rank.append([person, mesto + r])  # добавляет в список группа, место, чтоб занести в таблицу Choice
                r += 1
        else:
            for i in val_l:
                w = key_l[val_l.index(i)]  # получает ключ, по которому в списке ищет игрока
                wq = int(d.setdefault(w))  # получает номер группы, соответсвующий
                td[wq * 2 - 2][max_person + 3] = str(i)  # записывает соотношения игроку
                td[wq * 2 - 2][max_person + 4] = str(m + mesto)  # записывает место
                player_rank.append([wq, m + mesto])  # добавляет в список группа, место, чтоб занести в таблицу Choice
                m += 1
    else:
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
            player_rank.append([wq, m + mesto])  # добавляет в список группа, место, чтоб занести в таблицу Choice
            m += 1


def sum_points_circle(num_gr, tour, ki1, ki2, pg_win, pg_los, pp):
    """сумма очков кажого игрока в крутиловке"""
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
    """распределяет спортсменов в сетке согласно жеребьевке"""
    posev_data = []
    first_posev = []
    second_posev = []
    choice_first = Choice.select().order_by(Choice.group).where(Choice.mesto_group == 1)
    choice_second = Choice.select().order_by(Choice.group).where(Choice.mesto_group == 2)
    first_number = [1, 16, 8, 9, 4, 5, 12, 13]
    second_number = [10, 3, 11, 7, 14, 15, 2, 6]
    n = 0
    k = 0
    for posev in choice_first:
        player = Player.get(Player.player == posev.family)
        city = player.city
        for i in range(n, n + 1):
            first_posev.append({'посев': first_number[i], 'фамилия': f'{posev.family}/ {city}'})
            n += 1
    for posev in choice_second:
        player = Player.get(Player.player == posev.family)
        city = player.city
        for k in range(k, k + 1):
            second_posev.append({'посев': second_number[k], 'фамилия': f'{posev.family}/ {city}'})
            k += 1
    posev_data = first_posev + second_posev
    posev_data = sorted(posev_data, key=lambda i: i['посев'])  # сортировка (списка словарей) по ключу словаря -посев-
    return posev_data



# def title_id_last():
#     """возвращает title id в зависимости от соревнования"""
#
#     name = my.lineEdit_title_nazvanie.text()  # определяет название соревнований из титула
#     data = my_win.dateEdit_start.text()
#     gamer = my_win.lineEdit_title_gamer.text()
#     t = Title.select().where(Title.name == name and Title.data_start == data)  # получает эту строку в db
#     count = len(t)
#     title = t.select().where(Title.gamer == gamer).get()
#     title_id = title.id  # получает его id
#     return title_id
# def result_rank_group(num_group, max_player):
#     """записывает места из группы в таблицу -Result-"""
#     pass