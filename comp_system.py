
import pdf
import tbl_data
from models import *



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
    title = Title.select().order_by(Title.id.desc()).get()  # получение id последнего соревнования

    # s = System.select().order_by(System.id).where(System.title_id == title).get()  # находит system id последнего
    # p = s.page_vid  # рабочий вариант
    # p = A4  # временно пока идет наладки таблицы (сетка 16)
    # if p == "альбомная":
    #     pv = landscape(A4)
    # else:
    pv = A4
    (width, height) = pv

    nz = title.name
    ms = title.mesto
    sr = f"среди {title.sredi} {title.vozrast}"
    data_comp = pdf.data_title_string()

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
        canvas.drawString(2 * cm, 2 * cm, main_referee)  # подпись главного судьи
        canvas.drawString(2 * cm, 1 * cm, main_secretary)  # подпись главного секретаря
    canvas.restoreState()
    return func_zagolovok


def tbl(kg, ts, zagolovok, cW, rH):
    """данные таблицы и применение стиля и добавления заголовка столбцов"""
    dict_tbl = {}
    t = Title.select().order_by(Title.id.desc()).get()  # получение id последнего соревнования
    tdt = tbl_data.table_data(kg, title_id=t)  # данные результатов в группах
    for i in range(0, kg):
        tdt[i].insert(0, zagolovok)
        dict_tbl[i] = Table(tdt[i], colWidths=cW, rowHeights=rH)
        dict_tbl[i].setStyle(ts)
    return dict_tbl


def table_made(pv, title_id):
    """создание таблиц kg - количество групп(таблиц), g2 - наибольшое кол-во участников в группе
     pv - ориентация страницы, е - если участников четно группам, т - их количество"""
    s = System.select().order_by(System.id).where(System.title_id == title_id).get()  # находит system id последнего
    stage = s.stage
    ta = s.total_athletes
    if stage != "Круговая система":
        kg = s.total_group
        t = int(ta) // int(kg)
        e = int(ta) % int(kg)  # если количество участников не равно делится на группы
        g2 = t + 1
        kg = int(kg)
        if e == 0:
            t = t
        else:
            t = g2
    else:
        kg = 1
        t = ta
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
    # dict_table = {}
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

#=============
# def made_pdf():
#     def header(canvas, doc, content):
#         canvas.saveState()
#         w, h = content.wrap(doc.width, doc.topMargin)
#         content.drawOn(canvas, doc.leftMargin, doc.height + doc.bottomMargin + doc.topMargin - h)
#         canvas.restoreState()
#
#     def footer(canvas, doc, content):
#         canvas.saveState()
#         w, h = content.wrap(doc.width, doc.bottomMargin)
#         content.drawOn(canvas, doc.leftMargin, h)
#         canvas.restoreState()
#
#     def header_and_footer(canvas, doc, header_content, footer_content):
#         header(canvas, doc, header_content)
#         footer(canvas, doc, footer_content)
#
#     styles = getSampleStyleSheet()
#
#     filename = "out.pdf"
#
#     PAGESIZE = A4
#
#     pdf = SimpleDocTemplate(filename, pagesize=PAGESIZE,
#             leftMargin = 2.2 * cm,
#             rightMargin = 2.2 * cm,
#             topMargin = 1.5 * cm,
#             bottomMargin = 2.5 * cm)
#
#     frame = Frame(pdf.leftMargin, pdf.bottomMargin, pdf.width, pdf.height, id='normal')
#
#     header_content = Paragraph("This is a header. testing testing testing  ", styles['Normal'])
#     footer_content = Paragraph("This is a footer. It goes on every page.  ", styles['Normal'])
#
#     template = PageTemplate(id='test', frames=frame, onPage=partial(header_and_footer, header_content=header_content,
#                                                                     footer_content=footer_content))
#
#     pdf.addPageTemplates([template])
#
#     pdf.build([Paragraph("This is content")])

#==========
def setka_16_made(fin):
    """сетка на 16 в pdf"""
    elements = []
    data = []
    column = ['']
    column_count = column * 11
    # добавить в аргументы функции
    final = fin
    first_mesto = mesto_in_final(fin)
    for i in range(0, 69):
        # column_count[10] = i  # нумерация 10 столбца для удобного просмотра таблицы
        list_tmp = column_count.copy()
        data.append(list_tmp)

    # ========= места ==========
    n = 1
    x = 0
    for i in range(0, 20, 2):
        n += 1
        i = i + x
        data[i + 29][10] = str(first_mesto + n) + "Место"
        if n == 3:
            x = n = 4
        elif n == 7:
            n = 9
            x = 16
        elif n == 11:
            n = 12
            x = 20
    for i in range(1, 4, 2):
        data[i * 5 + 10][10] = str(first_mesto + i // 2) + "Место"
        data[i // 2 + i * 2 + 45][10] = str(first_mesto + i // 2 + 8) + "Место"

    data[34][10] = str(first_mesto + 4) + "Место"
    data[60][10] = str(first_mesto + 12) + "Место"
    p = 0
    # ========= нумерация встреч сетки ==========
    for i in range(1, 33, 2):  # создание номеров игроков сетки (1-16)
        data[i - 1][0] = str(p + 1)
        p += 1
    p = 0
    for i in range(0, 29, 4):  # создание номеров встреч (1-8)
        data[i + 1][2] = str(p + 1)
        data[i // 2 + 40][2] = str((p + 1) * -1)  # номера проигравших 1-8
        p += 1
    for i in range(2, 27, 8):
        data[i][4] = str(p + 1)  # создание номеров встреч (9-12)
        data[i // 4 + 31][4] = str((p + 1) * -1)  # номера проигравших 9-12
        data[i // 2 + 40][4] = str(p + 13)  # создание номеров встреч (21-24)
        data[i // 4 + 57][4] = str((p + 13) * -1)  # номера проигравших 21-24
        p += 1
    for i in range(4, 21, 16):
        data[i][6] = str(p + 1)  # создание номеров встреч (13-14)
        data[i // 8 + 28][6] = str((p + 1) * -1)  # номера проигравших 13-14
        data[i // 2 + 40][6] = str(p + 13)  # создание номеров встреч (25-26)
        data[i // 8 + 54][6] = str((p + 13) * -1)  # номера проигравших 25-26
        p += 1
    for i in range(32, 37, 4):
        data[i][6] = str(p + 3)  # создание номеров встреч (17-18)
        data[i // 2 + 22][6] = str((p + 3) * -1)  # номера проигравших 17-18
        data[i + 26][6] = str(p + 15)  # создание номеров встреч (29-30)
        data[i // 2 + 48][6] = str((p + 15) * -1)  # номера проигравших 29-30
        p += 1
    for i in range(33, 40, 6):
        data[i][8] = str(p + 3)  # создание номеров встреч (19-20)
        data[i + 26][8] = str(p + 15)  # создание номеров встреч (31-32)
        p += 1
    data[8][8] = str(15)  # создание номеров встреч 15
    data[25][8] = str(-15)
    data[29][8] = str(16)  # создание номеров встреч 16
    data[31][8] = str(-16)
    data[37][8] = str(-19)
    data[41][8] = str(-20)
    data[44][8] = str(27)  # создание номеров встреч 27
    data[52][8] = str(-27)
    data[55][8] = str(28)  # создание номеров встреч 28
    data[57][8] = str(-28)
    data[63][8] = str(-31)
    data[67][8] = str(-32)

    # ============= данные игроков и встреч и размещение по сетке =============
    # ======= создать словарь  ключ - номер встречи, значение - номер ряда
    dict_num_game = {}
    for d in range(2, 11, 2):
        for r in range(0, 69):
            key = data[r][d]
            if key != "":
                dict_num_game[key] = r
    # ===== добавить данные игроков и счета в data ==================
    all_list = tbl_data.setka_data_16(fin)  # список фамилия/ город 1-ого посева
    tds = all_list[0]
    id_name_city = all_list[1]
    id_sh_name = all_list[2]
    for i in range(0, 31, 2):  # цикл расстановки игроков по своим номерам в 1-ом посеве
        n = i - (i // 2)
        data[i][1] = tds[n]
    # ===== вставить результаты встреч необходим цикл по всей таблице -Result-
    dict_setka = tbl_data.score_in_setka(fin)  # функция расстановки счетов и сносок игроков
    key_list = []
    val_list = []
    for k in dict_setka.keys():
        key_list.append(k)
    for v in key_list:
        val = dict_setka[v]
        val_list.append(val)
    column = [[9, 10, 11, 12, 21, 22, 23, 24], [13, 14, 17, 18, 25, 26, 29, 30], [15, 16, 19, 20, 27, 28, 31, 32]]
    row_plus = [[13, 14, 27], [15]]
    #======= list mest
    mesta_list = [15, -15, 16, -16, 19, -19,  20, -20, 27, -27, 28, -28, 31, -31, 32, -32]
    #============
    count = len(column)
    # записать в базу данных в списки места финальные
    for i in key_list:
        match = dict_setka[i]
        pl_win = match[1]
        pl_los = match[4]
        if pl_win != "bye":
            id_win = id_sh_name[f"{pl_win}"]
        if pl_los != "bye":
            id_los = id_sh_name[f"{pl_los}"]
        i = str(i)
        r = str(match[3])
        row_rank = match[3]
        #===== определение мест и запись в db
        if row_rank in mesta_list:
            index = mesta_list.index(row_rank)
            mesto = first_mesto + index
            pl1 = match[1]
            pl1_mesto = mesto - 1
            pl2 = match[4]
            pl2_mesto = mesto
            player = Player.get(Player.id == id_win)  # записывает места в таблицу -Player-
            player.mesto = pl1_mesto
            player.save()
            player = Player.get(Player.id == id_los)
            player.mesto = pl2_mesto
            player.save()
        c = match[0]
        row_win = dict_num_game[i]  # строка победителя
        if c != 0:
            for u in range(0, count):  # в зависимости от встречи делает сдвиг по столбцам
                if c in column[u]:
                    col = u * 2 + 3
                    break
            for n in range(0, 2):  # корректировка значения строки
                if c in row_plus[n]:
                    if n == 0:
                        row_win += 1
                    else:
                        row_win += 3
                    break
        else:  # встречи за места сдвиг на 9-й ряд
            col = 9
        if row_rank == -15:
            row_win += 7
        elif row_rank == -19 or row_rank == -31:
            row_win += 1
        elif row_rank == -27:
            row_win += 3

        win = match[1]  # победитель
        score = match[2]  # счет во встречи
        row_los = dict_num_game[r]  # строка проигравшего
        los = match[4]  # проигравший
        data[row_win][col] = win
        data[row_win + 1][col] = score
        data[row_los][col] = los

    # ==============
    cw = ((0.3 * cm, 4.6 * cm, 0.4 * cm, 3 * cm, 0.4 * cm, 3 * cm, 0.4 * cm, 3 * cm,
           0.4 * cm, 3.2 * cm, 1.2 * cm))
    t = Table(data, cw, 69 * [0.35 * cm])  # основа сетки на чем чертить таблицу (ширина столбцов и рядов, их кол-во)
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
    # ============  объединяет ячейки номер встречи
    for q in range(1, 17, 2):  # объединяет ячейки номер встречи
        fn = ('SPAN', (2, q * 2 - 1), (2, q * 2))  # встречи 1-8
        style.append(fn)
        fn = ('BACKGROUND', (2, q * 2 - 1), (2, q * 2), colors.lightyellow)  # встречи 1-8
        style.append(fn)
    for q in range(0, 14, 4):
        fn = ('SPAN', (4, q * 2 + 2), (4, q * 2 + 5))  # встречи 9-12
        style.append(fn)
        fn = ('BACKGROUND', (4, q * 2 + 2), (4, q * 2 + 5), colors.lightyellow)  # встречи 1-8
        style.append(fn)
        fn = ('SPAN', (4, q + 41), (4, q + 42))  # встречи 21-24
        style.append(fn)
        fn = ('BACKGROUND', (4, q + 41), (4, q + 42), colors.lightyellow)  # встречи 1-8
        style.append(fn)
    for q in range(0, 17, 16):  # объединяет ячейки между фамилии спортсменами номер встречи
        fn = ('SPAN', (6, q + 4), (6, q + 11))  # встреча 13-14
        style.append(fn)
        fn = ('BACKGROUND', (6, q + 4), (6, q + 11), colors.lightyellow)  # встречи 1-8
        style.append(fn)
    for q in range(0, 5, 4):  # объединяет ячейки между фамилии спортсменами номер встречи
        fn = ('SPAN', (6, q + 32), (6, q + 33))  # встреча 17-18
        style.append(fn)
        fn = ('BACKGROUND', (6, q + 32), (6, q + 33), colors.lightyellow)  # встречи 1-8
        style.append(fn)
        fn = ('SPAN', (6, q + 58), (6, q + 59))  # встреча 29-30
        style.append(fn)
        fn = ('BACKGROUND', (6, q + 58), (6, q + 59), colors.lightyellow)  # встречи 1-8
        style.append(fn)
    for q in range(0, 16, 8):  # объединяет ячейки между фамилии спортсменами номер встречи
        fn = ('SPAN', (6, q + 42), (6, q + 45))  # встреча 25-26
        style.append(fn)
        fn = ('BACKGROUND', (6, q + 42), (6, q + 45), colors.lightyellow)  # встречи 1-8
        style.append(fn)
 # объединяет ячейки между фамилии спортсменами номер встречи (за места)
    fn = ('SPAN', (8, 8), (8, 23))  # встреча 15
    style.append(fn)
    fn = ('BACKGROUND', (8, 8), (8, 23), colors.lightyellow)  # встречи 15
    style.append(fn)
    fn = ('SPAN', (8, 29), (8, 30))  # встреча 16
    style.append(fn)
    fn = ('BACKGROUND', (8, 29), (8, 30), colors.lightyellow)  # встречи 16
    style.append(fn)
    fn = ('SPAN', (8, 33), (8, 36))  # встречи 19
    style.append(fn)
    fn = ('BACKGROUND', (8, 33), (8, 36), colors.lightyellow)  # встречи 19
    style.append(fn)
    fn = ('SPAN', (8, 39), (8, 40))  # встреча 20
    style.append(fn)
    fn = ('BACKGROUND', (8, 39), (8, 40), colors.lightyellow)  # встречи 20
    style.append(fn)
    fn = ('SPAN', (8, 44), (8, 51))  # встреча 27
    style.append(fn)
    fn = ('BACKGROUND', (8, 44), (8, 51), colors.lightyellow)  # встречи 27
    style.append(fn)
    fn = ('SPAN', (8, 55), (8, 56))  # встреча 28
    style.append(fn)
    fn = ('BACKGROUND', (8, 55), (8, 56), colors.lightyellow)  # встречи 28
    style.append(fn)
    fn = ('SPAN', (8, 59), (8, 61))  # встречи 31
    style.append(fn)
    fn = ('BACKGROUND', (8, 59), (8, 61), colors.lightyellow)  # встречи 31
    style.append(fn)
    fn = ('SPAN', (8, 65), (8, 66))  # встреча 32
    style.append(fn)
    fn = ('BACKGROUND', (8, 65), (8, 66), colors.lightyellow)  # встречи 32
    style.append(fn)
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
    for i in range(1, 8, 2):
        fn = ('TEXTCOLOR', (i, 0), (i, 68), colors.black)  # цвет шрифта игроков
        style.append(fn)
        fn = ('TEXTCOLOR', (i + 1, 0), (i + 1, 68), colors.green)  # цвет шрифта номеров встреч
        style.append(fn)
        fn = ('ALIGN', (i, 0), (i, 68), 'LEFT')  # выравнивание фамилий игроков по левому краю
        style.append(fn)
        fn = ('ALIGN', (i + 1, 0), (i + 1, 68), 'CENTER')  # центрирование номеров встреч
        style.append(fn)
    # fn = ('INNERGRID', (0, 0), (-1, -1), 0.01, colors.grey)  # временное отображение сетки
    # style.append(fn)

    ts = style   # стиль таблицы (список оформления строк и шрифта)

    t.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                           ('FONTNAME', (0, 0), (-1, -1), "DejaVuSerif"),
                           ('FONTSIZE', (0, 0), (-1, -1), 7),
                           ('FONTNAME', (1, 0), (1, 32), "DejaVuSerif-Bold"),
                           ('FONTSIZE', (1, 0), (1, 32), 7),
                           ('TEXTCOLOR', (10, 0), (10, 68), colors.red),  # 10 столбец с 0 по 68 ряд (цвет места)
                           # ('VALIGN', (0, 0), (0, -1), 'TOP'),
                           ('TEXTCOLOR', (0, 0), (0, 68), colors.blue),  # цвет шрифта игроков 1 ого тура
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
                           ] + ts))

    elements.append(t)
    pv = A4
    znak = final.rfind("-")
    f = final[:znak]
    name_table_final = f"setka_16_{f}_финал.pdf"
    doc = SimpleDocTemplate(name_table_final, pagesize=pv)
    doc.build(elements, onFirstPage=func_zagolovok, onLaterPages=func_zagolovok)
    return tds


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
          ['1-2', '3-4', '5-6', '7-8']],
         [['1-9', '2-8', '3-7', '4-6'], ['5-9', '1-8', '2-7', '3-6'], ['4-9', '5-8', '1-7', '2-6'],
          ['3-9', '4-8', '5-7', '1-6'], ['2-4', '1-5', '3-8', '7-9'], ['4-1', '5-3', '9-2', '8-6'],
          ['1-3', '2-5', '4-7', '6-9'], ['3-2', '5-4', '8-9', '7-6'], ['1-2', '3-4', '5-6', '7-8']],
         [['1-9', '2-8', '3-7', '4-6', '5-10'], ['5-9', '1-8', '2-7', '3-6', '4-10'], ['4-9', '5-8', '1-7', '2-6', '3-10'],
          ['3-9', '4-8', '5-7', '1-6', '2-10'], ['2-4', '1-5', '3-8', '7-9', '6-10'], ['4-1', '5-3', '9-2', '8-6', '7-10'],
          ['1-3', '2-5', '4-7', '6-9', '8-10'], ['3-2', '5-4', '8-9', '7-6', '1-10'], ['1-2', '3-4', '5-6', '7-8', '9-10']],
         [['1-11', '2-10', '3-9','4-8', '5-7'], ['6-11', '1-10', '2-9', '3-8', '4-7'], ['5-11', '6-10', '1-9', '2-8', '3-7'],
          ['4-11', '5-10', '6-9', '1-8', '2-7'], ['3-11', '4-10', '5-9', '6-8', '1-7'], ['2-11', '3-10', '4-9', '5-8', '6-7'],
          ['2-4', '1-5', '3-6', '7-10', '9-11'], ['1-4','2-6','3-5','8-10','7-11'], ['1-3', '2-5', '4-6', '7-9', '8-11'],
          ['2-3', '1-6', '4-5', '8-9', '10-11'], ['1-2', '3-4', '5-6', '7-8', '9-10']],
         [['1-11', '2-10', '3-9', '4-8', '5-7', '6-12'], ['6-11', '1-10', '2-9', '3-8', '4-7', '5-12'],
          ['5-11', '6-10', '1-9', '2-8', '3-7', '4-12'], ['4-11', '5-10', '6-9', '1-8', '2-7', '3-12'],
          ['3-11', '4-10', '5-9', '6-8', '1-7', '2-12'], ['2-11', '3-10', '4-9', '5-8', '6-7', '1-12'],
          ['2-4', '1-5', '3-6', '7-10', '9-11', '8-12'], ['1-4', '2-6', '3-5', '8-10', '7-11', '9-12'],
          ['1-3', '2-5', '4-6', '7-9', '8-11', '10-12'], ['2-3', '1-6', '4-5', '8-9', '10-11', '7-12'],
          ['1-2', '3-4', '5-6', '7-8', '9-10', '11-12']],
         [['1-13', '2-12', '3-11', '4-10', '5-9', '6-8'], ['7-13', '1-12', '2-11', '3-10', '4-9', '5-8'],
          ['6-13', '7-12', '1-11', '2-10', '3-9', '4-8'], ['5-13', '6-12', '7-11', '1-10', '2-9', '3-8'],
          ['4-13', '5-12', '6-11', '7-10', '1-9', '2-8'], ['3-13', '4-12', '5-11', '6-10', '7-9', '1-8'],
          ['1-7', '2-6', '3-5', '4-11', '9-13', '10-12'], ['1-6', '2-5', '4-7', '3-12', '8-11', '10-13'],
          ['1-4', '2-7', '3-6', '5-10', '8-13', '9-12'], ['1-5', '3-7', '4-6', '2-13', '8-12', '9-11'],
          ['1-3', '2-4', '5-7', '6-9', '8-10', '11-13'], ['2-3', '4-5', '6-7', '8-9', '10-11', '12-13'],
          ['1-2', '3-4', '5-6', '7-8', '9-10', '11-12']],
         [['1-13', '2-12', '3-11', '4-10', '5-9', '6-8', '7-14'], ['7-13', '1-12', '2-11', '3-10', '4-9', '5-8', '6-14'],
          ['6-13', '7-12', '1-11', '2-10', '3-9', '4-8', '5-14'], ['5-13', '6-12', '7-11', '1-10', '2-9', '3-8', '4-14'],
          ['4-13', '5-12', '6-11', '7-10', '1-9', '2-8', '3-14'], ['3-13', '4-12', '5-11', '6-10', '7-9', '1-8', '2-14'],
          ['1-7', '2-6', '3-5', '4-11', '9-13', '10-12', '8-14'], ['1-6', '2-5', '4-7', '3-12', '8-11', '10-13', '9-14'],
          ['1-4', '2-7', '3-6', '5-10', '8-13', '9-12', '11-14'], ['1-5', '3-7', '4-6', '2-13', '8-12', '9-11', '10-14'],
          ['1-3', '2-4', '5-7', '6-9', '8-10', '11-13', '12-14'], ['2-3', '4-5', '6-7', '8-9', '10-11', '12-13', '1-14'],
          ['1-2', '3-4', '5-6', '7-8', '9-10', '11-12', '13-14']],
         [['1-15', '2-14', '3-13', '4-12', '5-11', '6-10', '7-9'], ['8-15', '1-14', '2-13', '3-12', '4-11', '5-10', '6-9'],
          ['8-15', '1-14', '2-13', '3-12', '4-11', '5-10', '6-9'], ['7-15', '8-14', '1-13', '2-12', '3-11', '4-10', '5-9'],
          ['6-15', '7-14', '8-13', '1-12', '2-11', '3-10', '4-9'], ['5-15', '6-14', '7-13', '8-12', '1-11', '2-10', '3-9'],
          ['4-15', '5-14', '6-13', '7-12', '8-11', '1-10', '2-9'], ['3-15', '4-14', '5-13', '6-12', '7-11', '8-10', '1-9'],
          ['2-15', '3-14', '4-13', '5-12', '6-11', '7-10', '8-9'], ['1-7', '2-6', '3-5', '4-8', '9-13', '12-14', '11-15'],
          ['1-6', '2-5', '3-8', '4-7', '9-14', '10-13', '12-15'], ['1-5', '2-8', '3-7', '4-6', '9-15', '10-14', '11-13'],
          ['1-4', '2-7', '3-6', '5-8', '9-12', '10-15', '11-14'], ['1-3', '2-4', '5-7', '6-8', '9-11', '10-12', '13-15'],
          ['1-8', '2-3', '4-5', '6-7', '10-11', '12-13', '14-15'], ['1-2', '3-4', '5-6', '7-8', '9-10', '11-12', '13-14']],
         [['1-15', '2-14', '3-13', '4-12', '5-11', '6-10', '7-9', '8-16'],
          ['8-15', '1-14', '2-13', '3-12', '4-11', '5-10', '6-9', '7-16'],
          ['7-15', '8-14', '1-13', '2-12', '3-11', '4-10', '5-9', '6-16'],
          ['6-15', '7-14', '8-13', '1-12', '2-11', '3-10', '4-9', '5-16'],
          ['5-15', '6-14', '7-13', '8-12', '1-11', '2-10', '3-9', '4-16'],
          ['4-15', '5-14', '6-13', '7-12', '8-11', '1-10', '2-9', '3-16'],
          ['3-15', '4-14', '5-13', '6-12', '7-11', '8-10', '1-9', '2-16'],
          ['2-15', '3-14', '4-13', '5-12', '6-11', '7-10', '8-9', '1-16'],
          ['1-7', '2-6', '3-5', '4-8', '9-13', '12-14', '11-15', '10-16'],
          ['1-6', '2-5', '3-8', '4-7', '9-14', '10-13', '12-15', '11-16'],
          ['1-5', '2-8', '3-7', '4-6', '9-15', '10-14', '11-13', '12-16'],
          ['1-4', '2-7', '3-6', '5-8', '9-12', '10-15', '11-14', '13-16'],
          ['1-3', '2-4', '5-7', '6-8', '9-11', '10-12', '13-15', '14-16'],
          ['1-8', '2-3', '4-5', '6-7', '10-11', '12-13', '14-15', '9-16'],
          ['1-2', '3-4', '5-6', '7-8', '9-10', '11-12', '13-14', '15-16']]]


    tour_list = tr[cp]
    return tour_list


def mesto_in_final(fin):
    """с какого номера расставляются места в финале, в зависимости от его номера и кол-во участников
    fin - финал"""
    final = []
    mesto = {}
    tmp = []

    system = System.select().order_by(System.id).where(System.title_id == title_id())  # находит system id последнего

    first = 1
    k = 0
    for sys in system:
        f = sys.stage
        if f != "Предварительный":
            if f != "Полуфиналы":
                tmp.append(f)
                if k >= 1:
                    tmp.append(first + final[k - 1][2])
                else:
                    tmp.append(first)
                tmp.append(sys.max_player)
                k += 1
            final.append(tmp.copy())
            tmp.clear()
            mesto[f] = final[k - 1][1]
    first_mesto = mesto[fin]
    return first_mesto


def title_id():
    """возвращает title id в зависимости от соревнования"""
    name = my_win.lineEdit_title_nazvanie.text()  # определяет название соревнований из титула
    if name != "":
        data = my_win.dateEdit_start.text()
        gamer = my_win.lineEdit_title_gamer.text()
        t = Title.select().where(Title.name == name and Title.data_start == data)  # получает эту строку в db
        count = len(t)
        title = t.select().where(Title.gamer == gamer).get()
        title_id = title.id  # получает его id
    else:
        t_id = Title.select().order_by(Title.id.desc()).get()  # получение последней записи в таблице
        title_id = t_id
    return title_id