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
    tit = Title.get(Title.id == 1)
    nz = tit.name
    ms = tit.mesto
    sr = "среди " + tit.sredi + " " + tit.vozrast
    ds = str(tit.data_start)
    main_referee_collegia = "Гл. судья: " + tit.referee + " судья " + tit.kat_ref + "______________          " + \
                        "Гл. секретарь: " + tit.secretary + " судья " + tit.kat_sek + "______________"
    (width, height) = landscape(A4)
    canvas.saveState()

    canvas.setFont("DejaVuSerif-Italic", 14)
    canvas.drawCentredString(width / 2.0, height - 1.1 * cm, nz)  # центральный текст титула
    canvas.setFont("DejaVuSerif-Italic", 12)
    canvas.drawCentredString(width / 2.0, height - 1.5 * cm, sr)  # текста титула по основным
    canvas.drawRightString(width - 1 * cm, height - 1.5 * cm, "г. " + ms)  # город
    canvas.drawString(0.8 * cm, height - 1.5 * cm, ds)  # дата начала
    canvas.setFont("DejaVuSerif-Italic", 11)
    canvas.drawCentredString(width / 2.0, height - 20 * cm, main_referee_collegia)  # текста титула по основным
    canvas.restoreState()
    return func_zagolovok


def table_made(kg, e, g2, t, pv):
    """создание таблиц по g2 участника
    kg - количество групп(таблиц), g2 - наибольшое кол-во участников в группе """
    g2 = int(g2)
    kg = int(kg)

    if e == 0:
        t = t
    else:
        t = g2

    if kg == 1 and t <= 16:
        wcells = 13.4 / g2  # ширина столбцов таблицы в зависимости от колво чел (книжная ориентация стр)
        col = ((wcells * cm,) * t)
    elif kg == 1 and t <= 16 or g2 >= 10 or (kg >= 2 and t <= 6):
        wcells = 8.4 / g2  # ширина столбцов таблицы в зависимости от колво чел (альбомная ориентация стр)
        col = ((wcells * cm,) * t)
    # elif kg >= 2 and t <= 6:
    #     wcells = 8.4 / g2  # ширина столбцов таблицы в зависимости от колво чел (альбомная ориентация стр)
    #     col = ((wcells * cm,) * t)

    doc = SimpleDocTemplate("table_grup.pdf", pagesize=pv)
    elements = []

    cW = ((0.4 * cm, 3.2 * cm) + col + (1 * cm, 1 * cm, 1 * cm))  # кол-во столбцов в таблице и их ширина
    rH = (0.4 * cm)  # высота строки
    num_columns = []  # заголовки столобцов и их нумерация в зависимости от кол-во участников
    for i in range(0, t):
        i += 1
        i = str(i)
        num_columns.append(i)
    zagolovok = (['№', 'Участники/ Город'] + num_columns + ['Очки', 'Соот', 'Место'])
#  ================= данные таблиц =============
    tbl_1 = tbl_data.table1_data()  # если будут занаситься данные результатов
    tbl_2 = tbl_data.table2_data()

    #  =========================================
    tbl_1.insert(0, zagolovok)
    t1 = Table(tbl_1, colWidths=cW, rowHeights=rH)
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
        data = [[t1]]
        t1.setStyle(ts)
    elif kg == 2:
        t1.setStyle(ts)
        tbl_2.insert(0, zagolovok)
        t2 = Table(tbl_2, colWidths=cW, rowHeights=rH)
        t2.setStyle(ts)
        data = [[t1, t2]]
        shell_table = Table(data, colWidths=["*"])
        elements.append(shell_table)
    elif kg == 3 or kg == 4:
        t1 = Table(tbl_1, colWidths=cW, rowHeights=rH)
        t1.setStyle(ts)
        t2 = Table(tbl_2, colWidths=cW, rowHeights=rH)
        t2.setStyle(ts)
        # # tbl_3 = stroki_table
        # t3 = Table(tbl_3, colWidths=cW, rowHeights=rH)
        # t3.setStyle(ts)
        # # tbl_4 = stroki_table
        # t4 = Table(tbl_4, colWidths=cW, rowHeights=rH)
        # t4.setStyle(ts)
        # создание таблиц на листе
        data = [[t1, t2]]
        # data1 = [[t3, t4]]
        shell_table = Table(data, colWidths=["*"])
        # shell_table1 = Table(data1, colWidths=["*"])
        elements.append(shell_table)
        # elements.append(shell_table1)

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
    doc.build(elements, onFirstPage=func_zagolovok)