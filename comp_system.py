import tbl_data
from models import *
import pdf


from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import Paragraph, Table, TableStyle, Image, SimpleDocTemplate
from reportlab.lib import colors
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.platypus import PageBreak
from reportlab.pdfbase.pdfmetrics import registerFontFamily

registerFontFamily('DejaVuSerif', normal='DejaVuSerif', bold='DejaVuSerif-Bold', italic='DejaVuSerif-Italic')
enc = 'UTF-8'



def func_zagolovok(canvas, doc):
    """создание заголовка страниц"""
    s = System.select().order_by(System.id.desc()).get()
    p = s.page_vid
    if p == "альбомная":
        pv = landscape(A4)
    else:
        pv = A4
    (width, height) = pv
    title = Title.select().order_by(Title.id.desc()).get()
    nz = title.name
    ms = title.mesto
    sr = "среди " + title.sredi + " " + title.vozrast
    ds = str(title.data_start)
    if pv == landscape(A4):
        main_referee_collegia = "Гл. судья: " + title.referee + " судья " + title.kat_ref + "______________          " + \
                        "Гл. секретарь: " + title.secretary + " судья " + title.kat_sek + "______________"
    else:
        main_referee = "Гл. судья: " + title.referee + " судья " + title.kat_ref + "______________"
        main_secretary = "Гл. секретарь: " + title.secretary + " судья " + title.kat_sek + "______________"

    canvas.saveState()

    canvas.setFont("DejaVuSerif-Italic", 14)
    canvas.drawCentredString(width / 2.0, height - 1.1 * cm, nz)  # центральный текст титула
    canvas.setFont("DejaVuSerif-Italic", 12)
    canvas.drawCentredString(width / 2.0, height - 1.5 * cm, sr)  # текста титула по основным
    canvas.drawRightString(width - 1 * cm, height - 1.5 * cm, "г. " + ms)  # город
    canvas.drawString(0.8 * cm, height - 1.5 * cm, ds)  # дата начала
    canvas.setFont("DejaVuSerif-Italic", 11)
    if pv == landscape(A4):
        canvas.drawCentredString(width / 2.0, height - 20 * cm, main_referee_collegia)  # текста титула по основным
    else:
        canvas.drawString(2 * cm, 3 * cm, main_referee)  # подпись главного судьи
        canvas.drawString(2 * cm, 2 * cm, main_secretary)  # подпись главного секретаря
    canvas.restoreState()
    return func_zagolovok


def t_1(ts, zagolovok, cW, rH):
    """данные таблицы и применение стиля и добавления заголовка столбцов"""
    tbl_1 = tbl_data.table1_data()  # данные результатов в группах
    tbl_1.insert(0, zagolovok)
    t1 = Table(tbl_1, colWidths=cW, rowHeights=rH)
    t1.setStyle(ts)

    return t1


def t_2(ts, zagolovok, cW, rH):
    """данные таблицы и применение стиля и добавления заголовка столбцов"""
    tbl_2 = tbl_data.table2_data()  # данные результатов в группах
    tbl_2.insert(0, zagolovok)
    t2 = Table(tbl_2, colWidths=cW, rowHeights=rH)
    t2.setStyle(ts)

    return t2


def t_3(ts, zagolovok, cW, rH):
    """данные таблицы и применение стиля и добавления заголовка столбцов"""
    tbl_3 = tbl_data.table3_data()  # данные результатов в группах
    tbl_3.insert(0, zagolovok)
    t3 = Table(tbl_3, colWidths=cW, rowHeights=rH)
    t3.setStyle(ts)
    return t3


def t_4(ts, zagolovok, cW, rH):
    """данные таблицы и применение стиля и добавления заголовка столбцов"""
    tbl_4 = tbl_data.table4_data()  # данные результатов в группах
    tbl_4.insert(0, zagolovok)
    t4 = Table(tbl_4, colWidths=cW, rowHeights=rH)
    t4.setStyle(ts)
    return t4


def t_5(ts, zagolovok, cW, rH):
    """данные таблицы и применение стиля и добавления заголовка столбцов"""
    tbl_5 = tbl_data.table5_data()  # данные результатов в группах
    tbl_5.insert(0, zagolovok)
    t5 = Table(tbl_5, colWidths=cW, rowHeights=rH)
    t5.setStyle(ts)
    return t5


def t_6(ts, zagolovok, cW, rH):
    """данные таблицы и применение стиля и добавления заголовка столбцов"""
    tbl_6 = tbl_data.table6_data()  # данные результатов в группах
    tbl_6.insert(0, zagolovok)
    t6 = Table(tbl_6, colWidths=cW, rowHeights=rH)
    t6.setStyle(ts)
    return t6


def table_made(pv):
    """создание таблиц kg - количество групп(таблиц), g2 - наибольшое кол-во участников в группе
     pv - ориентация страницы, е - если участников четно группам, т - их количество"""

    s = System.select().order_by(System.id.desc()).get()
    kg = s.total_group
    ta = s.total_athletes
    t = int(ta) // int(kg)
    e = int(ta) % int(kg)  # если количество участников не равно делится на группы
    g2 = str(t + 1)

    g2 = int(g2)
    kg = int(kg)

    if e == 0:
        t = t
    else:
        t = g2

    if pv == landscape(A4):  # альбомная ориентация стр
        if kg == 1:
            wcells = 21.4 / t  # ширина столбцов таблицы в зависимости от кол-во чел (1 таблица)
        else:
            wcells = 7.4 / g2  # ширина столбцов таблицы в зависимости от кол-во чел (2-ух в ряд)
    else:  # книжная ориентация стр
        wcells = 12.8 / g2  # ширина столбцов таблицы в зависимости от кол-во чел
    col = ((wcells * cm,) * t)

    elements = []

    cW = ((0.4 * cm, 3.2 * cm) + col + (1 * cm, 1 * cm, 1 * cm))  # кол-во столбцов в таблице и их ширина
    rH = (0.4 * cm)  # высота строки
    num_columns = []  # заголовки столобцов и их нумерация в зависимости от кол-во участников
    for i in range(0, t):
        i += 1
        i = str(i)
        num_columns.append(i)
    zagolovok = (['№', 'Участники/ Город'] + num_columns + ['Очки', 'Соот', 'Место'])

    tblstyle = []
    # =========  цикл создания стиля таблицы ================
    for q in range(1, t + 1):  # город участника делает курсивом
        fn = ('FONTNAME', (1, q * 2), (1, q * 2), "DejaVuSerif-Italic")  # город участника делает курсивом
        tblstyle.append(fn)
        fn = ('FONTNAME', (1, q * 2 - 1), (1, q * 2 - 1), "DejaVuSerif-Bold")  # участника делает жирным шрифтом
        tblstyle.append(fn)
        fn = ('ALIGN', (1, q * 2 - 1), (1, q * 2 - 1), 'LEFT')  # центрирование текста в ячейках)
        tblstyle.append(fn)
        fn = ('SPAN', (0, q * 2 - 1), (0, q * 2))  # объединяет 1-2, 3-4, 5-6, 7-8 ячейки 1 столбца
        tblstyle.append(fn)
        fn = ('SPAN', (t + 2, q * 2 - 1), (t + 2, q * 2))  # объединяет клетки очки
        tblstyle.append(fn)
        fn = ('SPAN', (t + 3, q * 2 - 1), (t + 3, q * 2))  # объединяет клетки соот
        tblstyle.append(fn)
        fn = ('SPAN', (t + 4, q * 2 - 1), (t + 4, q * 2))  # объединяет клетки  место
        tblstyle.append(fn)
        fn = ('SPAN', (q + 1, q * 2 - 1), (q + 1, q * 2))  # объединяет диаганальные клетки
        tblstyle.append(fn)
        fn = ('BACKGROUND', (q + 1, q * 2 - 1), (q + 1, q * 2), colors.lightgreen)  # заливает диаганальные клетки
        tblstyle.append(fn)

    ts = []
    ts.append(tblstyle)
    # ============= полный стиль таблицы ======================
    ts = TableStyle([('FONTNAME', (0, 0), (-1, -1), "DejaVuSerif"),
                     ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                     ('FONTSIZE', (0, 0), (-1, -1), 7),
                     ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                     ('FONTNAME', (0, 0), (t + 5, 0), "DejaVuSerif-Bold"),
                     ('VALIGN', (0, 0), (t + 5, 0), 'MIDDLE')]  # центрирование текста в ячейках вертикальное
                    + tblstyle +
                    [('BACKGROUND', (0, 0), (t + 5, 0), colors.yellow),
                     ('TEXTCOLOR', (0, 0), (-1, -1), colors.darkblue),  # цвет шрифта в ячейках
                     ('LINEABOVE', (0, 0), (-1, 1), 1, colors.black),  # цвет линий нижней
                     ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),  # цвет и толщину внутренних линий
                     ('BOX', (0, 0), (-1, -1), 2, colors.black)  # внешние границы таблицы
                     ])
#  ============ создание таблиц и вставка данных =================

    if kg == 1:
        t1 = t_1(ts, zagolovok, cW, rH)
        data = [[t1]]
        shell_table = Table(data, colWidths=["*"])
        elements.append(shell_table)
    elif kg == 2:
        t1 = t_1(ts, zagolovok, cW, rH)
        t2 = t_2(ts, zagolovok, cW, rH)
        if pv == landscape(A4):  # страница альбомная, то таблицы размещаются обе в ряд
            data = [[t1, t2]]
            shell_table = Table(data, colWidths=["*"])
            elements.append(shell_table)
        else:  # страница книжная, то таблицы размещаются обе в столбец
            data = [[t1]]
            data1 = [[t2]]
            shell_table = Table(data, colWidths=["*"])
            shell_table1 = Table(data1, colWidths=["*"])
            elements.append(shell_table)
            elements.append(shell_table1)
    elif kg == 3:
        t1 = t_1(ts, zagolovok, cW, rH)
        t2 = t_2(ts, zagolovok, cW, rH)
        t3 = t_3(ts, zagolovok, cW, rH)
        if pv == landscape(A4):  # страница альбомная, то таблицы размещаются обе в ряд
            data = [[t1, t2]]
            data1 = [[t3]]
            shell_table = Table(data, colWidths=["*"])
            shell_table1 = Table(data1, colWidths=["*"])
            elements.append(shell_table)
            elements.append(shell_table1)
        else:  # страница книжная, то таблицы размещаются обе в столбец
            data = [[t1]]
            data1 = [[t2]]
            data2 = [[t3]]
            shell_table = Table(data, colWidths=["*"])
            shell_table1 = Table(data1, colWidths=["*"])
            shell_table2 = Table(data2, colWidths=["*"])
            elements.append(shell_table)
            elements.append(shell_table1)
            elements.append(shell_table2)
    elif kg == 4:
        t1 = t_1(ts, zagolovok, cW, rH)
        t2 = t_2(ts, zagolovok, cW, rH)
        t3 = t_3(ts, zagolovok, cW, rH)
        t4 = t_4(ts, zagolovok, cW, rH)
        if pv == landscape(A4):  # страница альбомная, то таблицы размещаются обе в ряд
            data = [[t1, t2]]
            data1 = [[t3, t4]]
            shell_table = Table(data, colWidths=["*"])
            shell_table1 = Table(data1, colWidths=["*"])
            elements.append(shell_table)
            elements.append(shell_table1)
        else:  # страница книжная, то таблицы размещаются обе в столбец
            data = [[t1]]
            data1 = [[t2]]
            data2 = [[t3]]
            data3 = [[t4]]
            shell_table = Table(data, colWidths=["*"])
            shell_table1 = Table(data1, colWidths=["*"])
            shell_table2 = Table(data2, colWidths=["*"])
            shell_table3 = Table(data3, colWidths=["*"])
            elements.append(shell_table)
            elements.append(shell_table1)
            elements.append(shell_table2)
            elements.append(shell_table3)
    elif kg == 5:
        pass
    elif kg == 6:
        pass

    h3 = PS("normal", fontSize=12, fontName="DejaVuSerif-Italic", leftIndent=50)  # стиль параграфа
    # h3.spaceAfter = 10  # промежуток после заголовка
    h4 = PS("normal", fontSize=12, fontName="DejaVuSerif-Italic", leftIndent=550)  # стиль параграфа
    h4.spaceAfter = 10  # промежуток после заголовка
    # elements.append(Paragraph('группа', h3))
    # shell_table = Table(data, colWidths=["*"])
    # shell_table1 = Table(data1, colWidths=["*"])
    # elements.append(Paragraph('группа №1', h3))
    # elements.append(Paragraph('группа №2', h4))
    # elements.append(shell_table)
    # elements.append(Paragraph('группа №3', h3))
    # elements.append(Paragraph('группа №4', h4))
    # elements.append(shell_table1)

    doc = SimpleDocTemplate("table_grup.pdf", pagesize=pv)
    doc.build(elements, onFirstPage=func_zagolovok)


def tour(cp):
    """туры таблиц по кругу в зависимости от кол-во участников"""
    pass
    # tour_list = []
    # tr = [[['1-3'], ['1-2'], ['2-3']],
    #       [['1-3', '2-4'], ['1-2', '3-4'], ['2-3', '1-4']],
    #       [['2-4', '1-5'], ['1-4', '3-5'], ['1-3', '2-5'], ['1-2', '3-4']],
    #       [['2-4', '1-5', '3-6'], ['1-4', '2-6', '3-5'], ['1-3', '2-5', '4-6'], ['1-2', '3-4', '5-6']]]
    #
    # tour_list = tr[cp]
    # return tour_list