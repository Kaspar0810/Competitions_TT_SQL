from models import *

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


def kol_game(kg, count):
    """подсчет кол-во групп и человек в группах"""
    pass
    # e = int(count) % int(kg)
    # t = int(count) // int(kg)
    # g1 = (int(kg) - e)
    # g2 = str(t + 1)
    # if e == 0:
    #     stroka_kol_grupp = (kg + " группы по " + str(t) + " чел.")
    # else:
    #     stroka_kol_grupp = (str(g1) + " групп(а) по " + str(t) + " чел. и "
    #                         + str(e) + " групп(а) по " + str(g2) + " чел.")
    # return stroka_kol_grupp


def func(canvas, psize):
    """создание заголовка страниц"""
    tit = Title.get(Title.id == 1)
    nz = tit.name
    ms = tit.mesto
    ds = str(tit.data_start)
    canvas.saveState()

    canvas.setFont("DejaVuSerif-Italic", 12)
    (width, height) = A4
    canvas.drawCentredString(width / 2.0, height - 1.2 * cm, nz)
    canvas.drawRightString(width - 1 * cm, height - 1.2 * cm, ms)
    canvas.drawString(width - 20 * cm, height - 1.2 * cm, ds)
    # if psize == landscape(A4):
    #     canvas.drawCentredString(width / 2.0, height - 1.2 * cm, nz)
    #     canvas.drawRightString(width - 1 * cm, height - 1.2 * cm, ms)
    #     canvas.drawString(width - 28 * cm, height - 1.2 * cm, ds)
    # else:
    #     canvas.drawCentredString(width / 2.0, height - 1.2 * cm, nz)
    #     canvas.drawRightString(width - 1 * cm, height - 1.2 * cm, ms)
    #     canvas.drawString(width - 20 * cm, height - 1.2 * cm, ds)

    canvas.restoreState()
    return func


def table_made(kg, e, g2, t):
    """создание таблиц по g2 участника
    kg - количество групп(таблиц), g2 - наибольшое кол-во участников в группе
     g1 - если везде одинаковое кол-во участников"""
    g2 = int(g2)
    kg = int(kg)


    if e == 0:
        t = t
    else:
        t = g2

    if kg == 1 and g2 <= 16:
        psize = A4
        wcells = 13.4 / g2  # ширина столбцов таблицы в зависимости от колво чел (книжная ореинтация стр)
        col = ((wcells * cm,) * t)
    elif kg == 1 and g2 <= 16 or g2 >= 10:
        psize = landscape(A4)
        wcells = 7.4 / g2  # ширина столбцов таблицы в зависимости от колво чел (альбомная ореинтация стр)
        col = ((wcells * cm,) * t)
    elif kg >= 2 and g2 <= 6:
        psize = landscape(A4)
        wcells = 7.4 / g2  # ширина столбцов таблицы в зависимости от колво чел (альбомная ореинтация стр)
        col = ((wcells * cm,) * t)

    doc = SimpleDocTemplate("table_grup.pdf", pagesize=psize)
    elements = []

    cW = ((0.4 * cm, 3.2 * cm) + col + (1 * cm, 1 * cm, 1 * cm))  # кол-во столбцов в таблице и их ширина
    rH = (0.6 * cm)  # высота строки
    num_columns = []  # заголовки столобцов и их нумерация в зависимости от кол-во участников
    for i in range(0, t):
        i += 1
        i = str(i)
        num_columns.append(i)
    zagolovok = (['№', 'Участники/ Город'] + num_columns + ['Очки', 'Соот', 'Место'])
    stroki_table = []

    for k in range(1, t * 2 + 1):
        st = ['']
        s = (st * (t + 4))
        s.insert(0, str((k + 1) // 2))  # получаем нумерацию строк по порядку
        stroki_table.append(s)
    stroki_table.insert(0, zagolovok)
    data1 = stroki_table
    t1 = Table(data1, colWidths=cW, rowHeights=rH)
    tblstyle = []
    # ========= стиль таблицы ================
    for q in range(1, t + 1):  # город участника делает курсивом
        fn = ('FONTNAME', (1, q * 2), (1, q * 2), "DejaVuSerif-Italic")  # город участника делает курсивом
        tblstyle.append(fn)
        fn = ('FONTNAME', (1, q * 2 - 1), (1, q * 2 - 1), "DejaVuSerif-Bold")  # участника делает жирным шрифтом
        tblstyle.append(fn)
        fn = ('ALIGN', (1, q * 2 - 1), (1, q * 2 - 1), 'LEFT')  # цетнрирование текста в ячейках])
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
    ts = TableStyle([('FONTNAME', (0, 0), (-1, -1), "DejaVuSerif"),
                     ('FONTSIZE', (0, 0), (-1, -1), 7),
                     ('ALIGN', (0, 0), (-1, -1), 'CENTER')]
                    + tblstyle +
                    [('BACKGROUND', (0, 0), (t * 2, 0), colors.yellow),
                     ('TEXTCOLOR', (0, 0), (-1, -1), colors.darkblue),  # цвет шрифта в ячейках
                     ('LINEABOVE', (0, 0), (-1, 1), 1, colors.black),  # цвет линий нижней
                     ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),  # цвет и толщину внутренних линий
                     ('BOX', (0, 0), (-1, -1), 2, colors.black)  # внешние границы таблицы
                     ])

    if kg == 1:
        data = [[t1]]
        t1.setStyle(ts)
    elif kg == 2:
        t1.setStyle(ts)
        data2 = stroki_table
        t2 = Table(data2, colWidths=cW, rowHeights=rH)
        t2.setStyle(ts)
        data = [[t1, t2]]
    elif kg == 3 or kg == 4:
        data2 = stroki_table
        t2 = Table(data2, colWidths=cW, rowHeights=rH)
        t2.setStyle(ts)
        data = [[t1, t2]]
        data3 = stroki_table
        t3 = Table(data3, colWidths=cW, rowHeights=rH)
        t3.setStyle(ts)
        data4 = stroki_table
        t4 = Table(data4, colWidths=cW, rowHeights=rH)
        t4.setStyle(ts)
        data1 = [[t3, t4]]


    h3 = PS("normal", fontSize=12, fontName="DejaVuSerif-Italic", leftIndent=50)  # стиль параграфа
    # h3.spaceAfter = 10  # промежуток после заголовка
    h4 = PS("normal", fontSize=12, fontName="DejaVuSerif-Italic", leftIndent=550)  # стиль параграфа
    h4.spaceAfter = 10  # промежуток после заголовка
    # elements.append(Paragraph('группа', h3))
    shell_table = Table(data, colWidths=["*"])
    # shell_table1 = Table(data1, colWidths=["*"])
    # elements.append(Paragraph('группа №1', h3))
    # elements.append(Paragraph('группа №2', h4))
    elements.append(shell_table)
    # elements.append(Paragraph('группа №3', h3))
    # elements.append(Paragraph('группа №4', h4))
    # elements.append(shell_table1)
    doc.build(elements, onFirstPage=func)
