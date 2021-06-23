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


def player_list_pdf():
    pass
    """создание списка учстников в pdf файл"""
    # doc = SimpleDocTemplate("table_list.pdf", pagesize=A4)
    # title = Title.select().order_by(Title.id.desc()).get()  # получение последней записи в таблице
    # nz = title.name
    # sr = f"среди {title.sredi} {title.vozrast}"
    #
    # story = []  # Список данных таблицы участников
    # elements = []  # Список Заголовки столбцов таблицы
    # player_list = Player.select()
    # count = len(player_list)  # колличество записей в базе
    # kp = count + 1
    # my_win.tableWidget.setRowCount(count)
    #
    # for k in range(0, count):  # цикл по списку по строкам
    #     n = my_win.tableWidget.item(k, 0).text()
    #     p = my_win.tableWidget.item(k, 1).text()
    #     b = my_win.tableWidget.item(k, 2).text()
    #     c = my_win.tableWidget.item(k, 3).text()
    #     g = my_win.tableWidget.item(k, 4).text()
    #     z = my_win.tableWidget.item(k, 5).text()
    #     t = my_win.tableWidget.item(k, 6).text()
    #     q = my_win.tableWidget.item(k, 7).text()
    #     m = my_win.tableWidget.item(k, 8).text()
    #
    #     data = [n, p, b, c, g, z, t, q, m]
    #     elements.append(data)
    # elements.insert(0, ["№", "Фамилия, Имя", "Дата рождени ", "Рейтинг", "Город", "Регион", "Разряд", "Тренер(ы)",
    #                     "Место"])
    # t = Table(elements,
    #           colWidths=(
    #           None, None, None, None, None, None, None, None, None))  # ширина столбцов, если None-автомтическая
    # t.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), "DejaVuSerif"),  # Использую импортированный шрифт
    #                        ('FONTSIZE', (0, 0), (-1, -1), 8),  # Использую импортированный шрифта размер
    #                        ('BACKGROUND', (0, 0), (-1, kp * -1), colors.yellow),
    #                        ('TEXTCOLOR', (0, 0), (-1, kp * -1), colors.darkblue),
    #                        ('LINEABOVE', (0, 0), (-1, kp * -1), 1, colors.blue),
    #                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),  # цвет и толщину внутренних линий
    #                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black)  # внешние границы таблицы
    #                        ]))
    # h1 = PS("normal", fontSize=14, fontName="DejaVuSerif-Italic", leftIndent=0, firstLineIndent=-20)  # стиль параграфа
    # h1.spaceAfter = 10  # промежуток после заголовка
    # h1.spaceBefore = 0
    # h2 = PS("normal", fontSize=12, fontName="DejaVuSerif-Italic", leftIndent=50, firstLineIndent=-20)  # стиль параграфа
    # h2.spaceAfter = 20  # промежуток после заголовка
    # h3 = PS("normal", fontSize=12, fontName="DejaVuSerif-Italic", leftIndent=50, firstLineIndent=-20)  # стиль параграфа
    # h3.spaceAfter = 10  # промежуток после заголовка
    #
    # story.append(Paragraph(nz, h1))
    # story.append(Paragraph(sr, h2))
    # story.append(Paragraph('Список участников', h3))
    # story.append(t)
    # doc.multiBuild(story)


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


def table7_data():
    """данные результатов в таблице 5-й группы"""
    table_7 = []
    t = kol_player()
    for k in range(1, t * 2 + 1):
        st = ['']
        s = (st * (t + 4))
        s.insert(0, str((k + 1) // 2))  # получаем нумерацию строк по порядку
        table_7.append(s)
    return table_7


def table8_data():
    """данные результатов в таблице 6-й группы"""
    table_8 = []
    t = kol_player()
    for k in range(1, t * 2 + 1):
        st = ['']
        s = (st * (t + 4))
        s.insert(0, str((k + 1) // 2))  # получаем нумерацию строк по порядку
        table_8.append(s)

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