import pdf
import tbl_data
from models import *
# import pdf


from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import Paragraph, Table, TableStyle, Image, SimpleDocTemplate
from reportlab.lib import colors
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import ParagraphStyle as PS, getSampleStyleSheet
from reportlab.platypus import PageBreak
from reportlab.pdfbase.pdfmetrics import registerFontFamily

registerFontFamily('DejaVuSerif', normal='DejaVuSerif', bold='DejaVuSerif-Bold', italic='DejaVuSerif-Italic')
enc = 'UTF-8'


def func_zagolovok(canvas, doc):
    """создание заголовка страниц"""
    t = Title.select().order_by(Title.id.desc()).get()  # получение id последнего соревнования
    s = System.select().order_by(System.id).where(System.title_id == t).get()  # находит system id последнего
    p = s.page_vid
    if p == "альбомная":
        pv = landscape(A4)
    else:
        pv = A4
    (width, height) = pv
    title = Title.select().order_by(Title.id.desc()).get()
    nz = title.name
    ms = title.mesto
    sr = f"среди {title.sredi} {title.vozrast}"
    data_comp = pdf.data_title_string()
    # ds = str(title.data_start)

    canvas.saveState()

    canvas.setFont("DejaVuSerif-Italic", 14)
    canvas.drawCentredString(width / 2.0, height - 1.1 * cm, nz)  # центральный текст титула
    canvas.setFont("DejaVuSerif-Italic", 12)
    canvas.drawCentredString(width / 2.0, height - 1.5 * cm, sr)  # текста титула по основным
    canvas.drawRightString(width - 1 * cm, height - 1.6 * cm, f"г. {ms}")  # город
    canvas.drawString(0.8 * cm, height - 1.6 * cm, data_comp)  # дата начала
    canvas.setFont("DejaVuSerif-Italic", 11)
    if pv == landscape(A4):
        main_referee_collegia = f"Гл. судья: {title.referee} судья {title.kat_ref}______________  " \
                                f"Гл. секретарь: {title.secretary} судья {title.kat_sek} ______________"
        canvas.drawCentredString(width / 2.0, height - 20 * cm, main_referee_collegia)  # текста титула по основным
    else:
        main_referee = f"Гл. судья: {title.referee} судья {title.kat_ref} ______________"
        main_secretary = f"Гл. секретарь: {title.secretary} судья {title.kat_sek} ______________"
        canvas.drawString(2 * cm, 3 * cm, main_referee)  # подпись главного судьи
        canvas.drawString(2 * cm, 2 * cm, main_secretary)  # подпись главного секретаря
    canvas.restoreState()
    return func_zagolovok


def tbl(kg, ts, zagolovok, cW, rH):
    """данные таблицы и применение стиля и добавления заголовка столбцов"""
    dict_tbl = {}
    tdt = tbl_data.table_data(kg)  # данные результатов в группах
    for i in range(0, kg):
        tdt[i].insert(0, zagolovok)
        dict_tbl[i] = Table(tdt[i], colWidths=cW, rowHeights=rH)
        dict_tbl[i].setStyle(ts)
    return dict_tbl


def table_made(pv):
    """создание таблиц kg - количество групп(таблиц), g2 - наибольшое кол-во участников в группе
     pv - ориентация страницы, е - если участников четно группам, т - их количество"""
    t = Title.select().order_by(Title.id.desc()).get()  # получение id последнего соревнования
    s = System.select().order_by(System.id).where(System.title_id == t).get()  # находит system id последнего
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
    if pv == "альбомная":  # альбомная ориентация стр
        pv = landscape(A4)
        if kg == 1 or t in [10, 11, 12, 13, 14, 15, 16]:
            wcells = 21.4 / t  # ширина столбцов таблицы в зависимости от кол-во чел (1 таблица)
        else:
            wcells = 7.4 / t  # ширина столбцов таблицы в зависимости от кол-во чел (2-ух в ряд)
    else:  # книжная ориентация стр
        pv = A4
        wcells = 12.8 / t  # ширина столбцов таблицы в зависимости от кол-во чел
    col = ((wcells * cm,) * t)

    elements = []

    cW = ((0.4 * cm, 3.2 * cm) + col + (1 * cm, 1 * cm, 1 * cm))  # кол-во столбцов в таблице и их ширина
    rH = (0.34 * cm)  # высота строки
    # rH = None  # высота строки
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
    h1 = PS("normal", fontSize=10, fontName="DejaVuSerif-Italic", leftIndent=150)  # стиль параграфа (номера таблиц)
    h2 = PS("normal", fontSize=10, fontName="DejaVuSerif-Italic", leftIndent=50)  # стиль параграфа (номера таблиц)
    dict_table = {}
    if kg == 1:
        dict_table = tbl(kg, ts, zagolovok, cW, rH)
        data = [[dict_table[0]]]
        shell_table = Table(data, colWidths=["*"])
        elements.append(shell_table)
    elif kg == 2:
        dict_table = tbl(kg, ts, zagolovok, cW, rH)
        if pv == landscape(A4) and t in [3, 4, 5, 6]:  # страница альбомная, то таблицы размещаются обе в ряд
            data = [[dict_table[0], dict_table[1]]]
            shell_table = Table(data, colWidths=["*"])
            elements.append(shell_table)
        else:  # страница книжная, то таблицы размещаются обе в столбец
            data = [[dict_table[0]]]
            data1 = [[dict_table[1]]]
            shell_table = Table(data, colWidths=["*"])
            shell_table1 = Table(data1, colWidths=["*"])
            elements.append(shell_table)
            elements.append(shell_table1)
    elif kg == 3:
        dict_table = tbl(kg, ts, zagolovok, cW, rH)
        if pv == landscape(A4):  # страница альбомная, то таблицы размещаются обе в ряд
            data = [[dict_table[0], dict_table[1]]]
            data1 = [[dict_table[2]]]
            shell_table = Table(data, colWidths=["*"])
            shell_table1 = Table(data1, colWidths=["*"])
            elements.append(shell_table)
            elements.append(shell_table1)
        else:  # страница книжная, то таблицы размещаются в столбец
            data = [[dict_table[0]]]
            data1 = [[dict_table[1]]]
            data2 = [[dict_table[2]]]
            shell_table = Table(data, colWidths=["*"])
            shell_table1 = Table(data1, colWidths=["*"])
            shell_table2 = Table(data2, colWidths=["*"])
            elements.append(shell_table)
            elements.append(shell_table1)
            elements.append(shell_table2)
    elif kg == 4:
        dict_table = tbl(kg, ts, zagolovok, cW, rH)
        if pv == landscape(A4):  # страница альбомная, то таблицы размещаются обе в ряд
            data = [[dict_table[0], dict_table[1]]]
            data1 = [[dict_table[2], dict_table[3]]]
            shell_table = Table(data, colWidths=["*"])
            shell_table1 = Table(data1, colWidths=["*"])
            elements.append(Paragraph('группа 1             группа 2', h2))
            elements.append(shell_table)
            elements.append(Paragraph('группа 3             группа 4', h2))
            elements.append(shell_table1)
        else:  # страница книжная, то таблицы размещаются обе в столбец
            data = [[dict_table[0]]]
            data1 = [[dict_table[1]]]
            data2 = [[dict_table[2]]]
            data3 = [[dict_table[3]]]
            shell_table = Table(data, colWidths=["*"])
            shell_table1 = Table(data1, colWidths=["*"])
            shell_table2 = Table(data2, colWidths=["*"])
            shell_table3 = Table(data3, colWidths=["*"])
            elements.append(shell_table)
            elements.append(shell_table1)
            elements.append(shell_table2)
            elements.append(shell_table3)
    elif kg == 5:
        dict_table = tbl(kg, ts, zagolovok, cW, rH)
        if pv == landscape(A4):  # страница альбомная, то таблицы размещаются обе в ряд
            data = [[dict_table[0], dict_table[1]]]
            data1 = [[dict_table[2], dict_table[3]]]
            data2 = [[dict_table[4]]]
            shell_table = Table(data, colWidths=["*"])
            shell_table1 = Table(data1, colWidths=["*"])
            shell_table2 = Table(data2, colWidths=["*"])
            elements.append(shell_table)
            elements.append(shell_table1)
            elements.append(shell_table2)
        else:  # страница книжная, то таблицы размещаются обе в столбец
            data = [[dict_table[0]]]
            data1 = [[dict_table[1]]]
            data2 = [[dict_table[2]]]
            data3 = [[dict_table[3]]]
            data4 = [[dict_table[4]]]
            shell_table = Table(data, colWidths=["*"])
            shell_table1 = Table(data1, colWidths=["*"])
            shell_table2 = Table(data2, colWidths=["*"])
            shell_table3 = Table(data3, colWidths=["*"])
            shell_table4 = Table(data4, colWidths=["*"])
            elements.append(shell_table)
            elements.append(shell_table1)
            elements.append(shell_table2)
            elements.append(shell_table3)
            elements.append(shell_table4)
    elif kg == 6:
        dict_table = tbl(kg, ts, zagolovok, cW, rH)
        if pv == landscape(A4):  # страница альбомная, то таблицы размещаются обе в ряд
            data = [[dict_table[0], dict_table[1]]]
            data1 = [[dict_table[2], dict_table[3]]]
            data2 = [[dict_table[4], dict_table[5]]]
            shell_table = Table(data, colWidths=["*"])
            shell_table1 = Table(data1, colWidths=["*"])
            shell_table2 = Table(data2, colWidths=["*"])
            elements.append(shell_table)
            elements.append(shell_table1)
            elements.append(shell_table2)
        else:  # страница книжная, то таблицы размещаются обе в столбец
            data = [[dict_table[0]]]
            data1 = [[dict_table[1]]]
            data2 = [[dict_table[2]]]
            data3 = [[dict_table[3]]]
            data4 = [[dict_table[4]]]
            data5 = [[dict_table[5]]]
            shell_table = Table(data, colWidths=["*"])
            shell_table1 = Table(data1, colWidths=["*"])
            shell_table2 = Table(data2, colWidths=["*"])
            shell_table3 = Table(data3, colWidths=["*"])
            shell_table4 = Table(data4, colWidths=["*"])
            shell_table5 = Table(data5, colWidths=["*"])
            elements.append(shell_table)
            elements.append(shell_table1)
            elements.append(shell_table2)
            elements.append(shell_table3)
            elements.append(shell_table4)
            elements.append(shell_table5)
    elif kg == 7:
        dict_table = tbl(kg, ts, zagolovok, cW, rH)
        if pv == landscape(A4):  # страница альбомная, то таблицы размещаются обе в ряд
            data = [[dict_table[0], dict_table[1]]]
            data1 = [[dict_table[2], dict_table[3]]]
            data2 = [[dict_table[4], dict_table[5]]]
            data3 = [[dict_table[6]]]
            shell_table = Table(data, colWidths=["*"])
            shell_table1 = Table(data1, colWidths=["*"])
            shell_table2 = Table(data2, colWidths=["*"])
            shell_table3 = Table(data3, colWidths=["*"])
            elements.append(shell_table)
            elements.append(shell_table1)
            elements.append(shell_table2)
            elements.append(shell_table3)
        else:  # страница книжная, то таблицы размещаются обе в столбец
            data = [[dict_table[0]]]
            data1 = [[dict_table[1]]]
            data2 = [[dict_table[2]]]
            data3 = [[dict_table[3]]]
            data4 = [[dict_table[4]]]
            data5 = [[dict_table[5]]]
            data6 = [[dict_table[6]]]
            shell_table = Table(data, colWidths=["*"])
            shell_table1 = Table(data1, colWidths=["*"])
            shell_table2 = Table(data2, colWidths=["*"])
            shell_table3 = Table(data3, colWidths=["*"])
            shell_table4 = Table(data4, colWidths=["*"])
            shell_table5 = Table(data5, colWidths=["*"])
            shell_table6 = Table(data6, colWidths=["*"])
            elements.append(shell_table)
            elements.append(shell_table1)
            elements.append(shell_table2)
            elements.append(shell_table3)
            elements.append(shell_table4)
            elements.append(shell_table5)
            elements.append(shell_table6)
    elif kg == 8:
        dict_table = tbl(kg, ts, zagolovok, cW, rH)
        if pv == landscape(A4):  # страница альбомная, то таблицы размещаются обе в ряд
            data = [[dict_table[0], dict_table[1]]]
            data1 = [[dict_table[2], dict_table[3]]]
            data2 = [[dict_table[4], dict_table[5]]]
            data3 = [[dict_table[6], dict_table[7]]]
            shell_table = Table(data, colWidths=["*"])
            shell_table1 = Table(data1, colWidths=["*"])
            shell_table2 = Table(data2, colWidths=["*"])
            shell_table3 = Table(data3, colWidths=["*"])
            elements.append(Paragraph('группа 1 группа 2', h2))  # заголовки групп (надо точно позиционировать)
            elements.append(shell_table)
            elements.append(Paragraph('группа 3 группа 4', h2))
            elements.append(shell_table1)
            elements.append(Paragraph('группа 5 группа 6', h2))
            elements.append(shell_table2)
            elements.append(Paragraph('группа 7 группа 8', h2))
            elements.append(shell_table3)
        else:  # страница книжная, то таблицы размещаются обе в столбец
            data = [[dict_table[0]]]
            data1 = [[dict_table[1]]]
            data2 = [[dict_table[2]]]
            data3 = [[dict_table[3]]]
            data4 = [[dict_table[4]]]
            data5 = [[dict_table[5]]]
            data6 = [[dict_table[6]]]
            data7 = [[dict_table[7]]]
            shell_table = Table(data, colWidths=["*"])
            shell_table1 = Table(data1, colWidths=["*"])
            shell_table2 = Table(data2, colWidths=["*"])
            shell_table3 = Table(data3, colWidths=["*"])
            shell_table4 = Table(data4, colWidths=["*"])
            shell_table5 = Table(data5, colWidths=["*"])
            shell_table6 = Table(data6, colWidths=["*"])
            shell_table7 = Table(data7, colWidths=["*"])
            elements.append(shell_table)
            elements.append(shell_table1)
            elements.append(shell_table2)
            elements.append(shell_table3)
            elements.append(shell_table4)
            elements.append(shell_table5)
            elements.append(shell_table6)
            elements.append(shell_table7)

    doc = SimpleDocTemplate("table_group.pdf", pagesize=pv)
    doc.build(elements, onFirstPage=func_zagolovok, onLaterPages=func_zagolovok)


def setka_16_made():
    elements = []
    data = []
    column = ['']
    # column = ['', '', '', '', '', '', '', '', '', '', '']
    column_count = column * 11

    # data = []
    # # column = ['']
    # column = ['', '', '', '', '', '', '', '', '', '', '']
    for i in range(0, 72):
        column_count[10] = i
        list_tmp = column_count.copy()
        data.append(list_tmp)

    # ==============
    cw = ((0.4 * cm, 4.5 * cm, 0.4 * cm, 3 * cm, 0.4 * cm, 3 * cm, 0.4 * cm, 3 * cm,
           0.4 * cm, 3 * cm, 0.6 * cm))
    t = Table(data, cw, 72 * [0.35 * cm])  # основа сетки на чем чертить таблицу (ширина столбцов и рядов, их кол-во)
    # отображениее сетки
    # tblstyle = [('INNERGRID', (0, 0), (-1, -1), 0.01, colors.grey),
    #             ('BOX', (0, 0), (-1, -1), 0.01, colors.grey)]
    # tblstyle = [('BOX', (0, 0), (-1, -1), 0.01, colors.grey)]
    # for i in range(0, 68):
    #     fn = ('FONTNAME', (9, i), (9, i), "DejaVuSerif-Italic")  # город участника делает курсивом
    #     tblstyle.append(fn)
    #     ('TEXTCOLOR', (9, i), (9, -i), colors.red)
    tblstyle = []
    style = []
    # =========  цикл создания стиля таблицы ================
    # ==== рисует основной столбец сетки (1-й тур)
    for q in range(1, 33, 2):  # рисует встречи 1-8
        fn = ('LINEABOVE', (0, q * 2 - q), (1, q * 2 - q), 1, colors.darkblue)  # окрашивает низ ячейки (от 0 до 2 ст)
        style.append(fn)
    for q in range(0, 16, 2):  # рисует встречи 9-12
        fn = ('LINEABOVE', (3, q * 2 + 2), (4, q * 2 + 2), 1, colors.darkblue)  # рисует 9-12 встречи
        style.append(fn)
        fn = ('LINEABOVE', (2, q + 41), (3, q + 41), 1, colors.darkblue)  # рисует 21-24 встречи
        style.append(fn)
    # ========== 3-й тур
    for q in range(1, 17, 4):
        fn = ('LINEABOVE', (5, q * 2 + 2), (5, q * 2 + 2), 1, colors.darkblue)  # рисует 13-14 встречи
        style.append(fn)
    for q in range(0, 7, 2):
        fn = ('LINEABOVE', (4, q + 32), (5, q + 32), 1, colors.darkblue)  # встречи (17, 18)
        style.append(fn)
        fn = ('LINEABOVE', (4, q + 58), (5, q + 58), 1, colors.darkblue)  # встречи (29, 30)
        style.append(fn)
    for q in range(0, 15, 4):
        fn = ('LINEABOVE', (5, q + 42), (5, q + 42), 1, colors.darkblue)  # рисует встречи 25-26
        style.append(fn)
    # ========== 4-й тур
    for q in range(1, 17, 8):
        fn = ('LINEABOVE', (7, q * 2 + 6), (8, q * 2 + 6), 1, colors.darkblue)  # встреча 15
        style.append(fn)
    for q in range(0, 3, 2):
        fn = ('LINEABOVE', (6, q + 29), (7, q + 29), 1, colors.darkblue)  # встреча 16
        style.append(fn)
        fn = ('LINEABOVE', (6, q + 39), (7, q + 39), 1, colors.darkblue)  # встреча 20
        style.append(fn)
        fn = ('LINEABOVE', (6, q + 55), (7, q + 55), 1, colors.darkblue)  # встреча 28
        style.append(fn)
        fn = ('LINEABOVE', (6, q + 65), (7, q + 65), 1, colors.darkblue)  # встреча 32
        style.append(fn)
    for q in range(0, 5, 4):
        fn = ('LINEABOVE', (7, q + 33), (7, q + 33), 1, colors.darkblue)  # встречи 19
        style.append(fn)
        fn = ('LINEABOVE', (7, q + 59), (7, q + 59), 1, colors.darkblue)  # встречи 31
        style.append(fn)
    for q in range(0, 16, 8):
        fn = ('LINEABOVE', (7, q + 44), (7, q + 44), 1, colors.darkblue)  # рисует 27 встречу
        style.append(fn)
    # ======= встречи за места =====
    for q in range(0, 11, 10):
        fn = ('LINEABOVE', (9, q + 16), (10, q + 16), 1, colors.darkblue)  # за 1-2 место
        style.append(fn)
    for q in range(0, 3, 2):
        fn = ('LINEABOVE', (9, q + 30), (10, q + 30), 1, colors.darkblue)  # за 3-4 место
        style.append(fn)
        fn = ('LINEABOVE', (9, q + 40), (10, q + 40), 1, colors.darkblue)  # за 7-8 место
        style.append(fn)
        fn = ('LINEABOVE', (9, q + 56), (10, q + 56), 1, colors.darkblue)  # за 11-12 место
        style.append(fn)
        fn = ('LINEABOVE', (9, q + 66), (10, q + 66), 1, colors.darkblue)  # за 15-16 место
        style.append(fn)
    for q in range(0, 4, 3):
        fn = ('LINEABOVE', (9, q + 35), (10, q + 35), 1, colors.darkblue)  # за 5-6 место
        style.append(fn)
        fn = ('LINEABOVE', (9, q + 61), (10, q + 61), 1, colors.darkblue)  # за 13-14 место
        style.append(fn)
    for q in range(0, 6, 5):
        fn = ('LINEABOVE', (9, q + 48), (10, q + 48), 1, colors.darkblue)  # за 9-10 место
        style.append(fn)
    # ============  объединяет ячейки между фамилии спортсменами номер встречи
    for q in range(1, 17, 2):  # объединяет ячейки между фамилии спортсменами номер встречи
        for i in range(0, 2):
            fn = ('SPAN', (i + 1, q * 2 - 1), (i + 1, q * 2))  # встречи 1-8
            style.append(fn)
    for q in range(0, 14, 4):
        for i in range(0, 2):
            fn = ('SPAN', (i + 3, q * 2 + 2), (i + 3, q * 2 + 5))  # встречи 9-12
            style.append(fn)
            fn = ('SPAN', (i + 3, q + 41), (i + 3, q + 42))  # встречи 21-24
            style.append(fn)
    for q in range(0, 17, 16):  # объединяет ячейки между фамилии спортсменами номер встречи
        for i in range(0, 2):
            fn = ('SPAN', (i + 5, q + 4), (i + 5, q + 11))  # встреча 13-14
            style.append(fn)
    for q in range(0, 5, 4):  # объединяет ячейки между фамилии спортсменами номер встречи
        for i in range(0, 2):
            fn = ('SPAN', (i + 5, q + 32), (i + 5, q + 33))  # встреча 17-18
            style.append(fn)
            fn = ('SPAN', (i + 5, q + 58), (i + 5, q + 59))  # встреча 29-30
            style.append(fn)
    for q in range(0, 16, 8):  # объединяет ячейки между фамилии спортсменами номер встречи
        for i in range(0, 2):
            fn = ('SPAN', (i + 5, q + 42), (i + 5, q + 45))  # встреча 25-26
            style.append(fn)
    for q in range(0, 2):  # объединяет ячейки между фамилии спортсменами номер встречи (за места)
        fn = ('SPAN', (q + 7, 8), (q + 7, 23))  # встреча 15
        style.append(fn)
        fn = ('SPAN', (q + 7, 29), (q + 7, 30))  # встреча 16
        style.append(fn)
        fn = ('SPAN', (q + 7, 33), (q + 7, 36))  # встречи 19
        style.append(fn)
        fn = ('SPAN', (q + 7, 39), (q + 7, 40))  # встреча 20
        style.append(fn)
        fn = ('SPAN', (q + 7, 44), (q + 7, 51))  # встреча 27
        style.append(fn)
        fn = ('SPAN', (q + 7, 55), (q + 7, 56))  # встреча 28
        style.append(fn)
        fn = ('SPAN', (q + 7, 59), (q + 7, 61))  # встречи 31
        style.append(fn)
        fn = ('SPAN', (q + 7, 65), (q + 7, 66))  # встреча 32
        style.append(fn)
    # ======= обводит ячейки где номера встреч
    for q in range(1, 33, 4):
        fn = ('BOX', (2, q), (2, q + 1), 1, colors.darkblue)  # рисует область 1 столбца, где номера встреч 1-8
        style.append(fn)
    for q in range(1, 14, 4):
        fn = ('BOX', (4, q * 2), (4, q * 2 + 3), 1, colors.darkblue)  # рисует область 2 столбца, где номера встреч 9-12
        style.append(fn)
        fn = ('BOX', (4, q + 40), (4, q + 41), 1, colors.darkblue)  # рисует область 2 столбца, где номера встреч 21-24
        style.append(fn)
    for q in range(1, 10, 8):
        fn = ('BOX', (6, q * 2 + 2), (6, q * 2 + 9), 1, colors.darkblue)  # рисует область 3 столбца, где встречи 13-14
        style.append(fn)
        fn = ('BOX', (6, q + 41), (6, q + 44), 1, colors.darkblue)  # рисует область 3 столбца, где номера встреч 25-26
        style.append(fn)
    for q in range(1, 6, 4):
        fn = ('BOX', (6, q + 31), (6, q + 32), 1, colors.darkblue)  # рисует область 3 столбца, где номера встреч 17-18
        style.append(fn)
        fn = ('BOX', (6, q + 57), (6, q + 58), 1, colors.darkblue)  # рисует область 3 столбца, где номера встреч 29-30
        style.append(fn)
    fn = ('BOX', (8, 8), (8, 23), 1, colors.darkblue)  # рисует область 4 столбца, где встреча 15
    style.append(fn)
    fn = ('BOX', (8, 29), (8, 30), 1, colors.darkblue)  # рисует область 4 столбца, где встреча 16
    style.append(fn)
    fn = ('BOX', (8, 33), (8, 36), 1, colors.darkblue)  # рисует область 4 столбца, где встреча 19
    style.append(fn)
    fn = ('BOX', (8, 39), (8, 40), 1, colors.darkblue)  # рисует область 4 столбца, где встреча 20
    style.append(fn)
    fn = ('BOX', (8, 44), (8, 51), 1, colors.darkblue)  # рисует область 4 столбца, где встреча 27
    style.append(fn)
    fn = ('BOX', (8, 55), (8, 56), 1, colors.darkblue)  # рисует область 4 столбца, где встреча 28
    style.append(fn)
    fn = ('BOX', (8, 59), (8, 62), 1, colors.darkblue)  # рисует область 4 столбца, где встреча 31
    style.append(fn)
    fn = ('BOX', (8, 65), (8, 66), 1, colors.darkblue)  # рисует область 4 столбца, где встреча 32
    style.append(fn)

    ts = []  # стиль таблицы (список оформления строк и шрифта)
    ts = style + tblstyle  # сложение стилей в один
    t.setStyle(TableStyle(ts))

    # ('SPAN', (1, 0), (1, 1))])  # объединяет 1-2, 3-4, 5-6, 7-8 ячейки 1 столбца))

    # t.setStyle(TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
    #                        ('TEXTCOLOR', (1, 1), (-2, -2), colors.red),
    #                        ('VALIGN', (0, 0), (0, -1), 'TOP'),
    #                        ('TEXTCOLOR', (0, 0), (0, -1), colors.blue),
    #                        ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
    #                        ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
    #                        ('TEXTCOLOR', (0, -1), (-1, -1), colors.green),
    #                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
    #                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    # ]))

    elements.append(t)
    doc = SimpleDocTemplate("setka_16.pdf", pagesize=A4)
    doc.build(elements)
    # doc.build(elements, onFirstPage=func_zagolovok, onLaterPages=func_zagolovok)
    # ============

    # cW = ((0.4 * cm, 3.2 * cm) + col + (1 * cm, 1 * cm, 1 * cm))  # кол-во столбцов в таблице и их ширина
    # rH = (0.34 * cm)  # высота строки
    # # rH = None  # высота строки
    # num_columns = []  # заголовки столобцов и их нумерация в зависимости от кол-во участников
    # # for i in range(0, t):
    # #     i += 1
    # #     i = str(i)
    # #     num_columns.append(i)
    # # zagolovok = (['№', 'Участники/ Город'] + num_columns + ['Очки', 'Соот', 'Место'])
    #
    # tblstyle = []
    # # =========  цикл создания стиля таблицы ================
    # for q in range(1, t + 1):  # город участника делает курсивом
    #     fn = ('FONTNAME', (1, q * 2), (1, q * 2), "DejaVuSerif-Italic")  # город участника делает курсивом
    #     tblstyle.append(fn)
    #     fn = ('FONTNAME', (1, q * 2 - 1), (1, q * 2 - 1), "DejaVuSerif-Bold")  # участника делает жирным шрифтом
    #     tblstyle.append(fn)
    #     fn = ('ALIGN', (1, q * 2 - 1), (1, q * 2 - 1), 'LEFT')  # центрирование текста в ячейках)
    #     tblstyle.append(fn)
    #     fn = ('SPAN', (0, q * 2 - 1), (0, q * 2))  # объединяет 1-2, 3-4, 5-6, 7-8 ячейки 1 столбца
    #     tblstyle.append(fn)
    #     fn = ('SPAN', (t + 2, q * 2 - 1), (t + 2, q * 2))  # объединяет клетки очки
    #     tblstyle.append(fn)
    #     fn = ('SPAN', (t + 3, q * 2 - 1), (t + 3, q * 2))  # объединяет клетки соот
    #     tblstyle.append(fn)
    #     fn = ('SPAN', (t + 4, q * 2 - 1), (t + 4, q * 2))  # объединяет клетки  место
    #     tblstyle.append(fn)
    #     fn = ('SPAN', (q + 1, q * 2 - 1), (q + 1, q * 2))  # объединяет диаганальные клетки
    #     tblstyle.append(fn)
    #     fn = ('BACKGROUND', (q + 1, q * 2 - 1), (q + 1, q * 2), colors.lightgreen)  # заливает диаганальные клетки
    #     tblstyle.append(fn)
    #
    # ts = []
    # ts.append(tblstyle)
    # # ============= полный стиль таблицы ======================
    # ts = TableStyle([('FONTNAME', (0, 0), (-1, -1), "DejaVuSerif"),
    #                  ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    #                  ('FONTSIZE', (0, 0), (-1, -1), 7),
    #                  ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    #                  ('FONTNAME', (0, 0), (t + 5, 0), "DejaVuSerif-Bold"),
    #                  ('VALIGN', (0, 0), (t + 5, 0), 'MIDDLE')]  # центрирование текста в ячейках вертикальное
    #                 + tblstyle +
    #                 [('BACKGROUND', (0, 0), (t + 5, 0), colors.yellow),
    #                  ('TEXTCOLOR', (0, 0), (-1, -1), colors.darkblue),  # цвет шрифта в ячейках
    #                  ('LINEABOVE', (0, 0), (-1, 1), 1, colors.black),  # цвет линий нижней
    #                  ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),  # цвет и толщину внутренних линий
    #                  ('BOX', (0, 0), (-1, -1), 2, colors.black)  # внешние границы таблицы
    #                  ])
    # #  ============ создание таблиц и вставка данных =================
    # h1 = PS("normal", fontSize=10, fontName="DejaVuSerif-Italic", leftIndent=150)  # стиль параграфа (номера таблиц)
    # h2 = PS("normal", fontSize=10, fontName="DejaVuSerif-Italic", leftIndent=50)  # стиль параграфа (номера таблиц)


def tour(cp):
    """туры таблиц по кругу в зависимости от кол-во участников -cp- кол-во участников"""
    tour_list = []
    tr = [['1-3', '1-2', '2-3'],
          [['1-3', '2-4'], ['1-2', '3-4'], ['2-3', '1-4']],
          [['2-4', '1-5'], ['1-4', '3-5'], ['1-3', '2-5'], ['2-3', '4-5'], ['1-2', '3-4']],
          [['2-4', '1-5', '3-6'], ['1-4', '2-6', '3-5'], ['1-3', '2-5', '4-6'], ['2-3', '1-6', '4-5'],
           ['1-2', '3-4', '5-6']],
          [['2-6', '3-5', '1-7'], ['2-5', '1-6', '4-7'], ['1-5', '4-6', '3-7'], ['4-5', '2-7', '3-6'],
           ['1-3', '2-4', '5-7'], ['1-4', '2-3', '6-7'], ['1-2', '3-4', '5-6']],
          [['2-6', '3-5', '1-7', '4-8'], ['2-5', '1-6', '3-8', '4-7'], ['1-5', '2-8', '4-6', '3-7'],
           ['1-8', '4-5', '2-7', '3-6'], ['1-3', '2-4', '5-7', '6-8'], ['1-4', '2-3', '6-7', '5-8'],
           ['1-2', '3-4', '5-6', '7-8']]]

    tour_list = tr[cp]
    return tour_list
