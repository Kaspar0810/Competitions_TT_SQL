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

TTFSearchPath = (
    'c:/winnt/fonts',
    'c:/windows/fonts',
    '%(REPORTLAB_DIR)s/fonts',  # special
    '%(REPORTLAB_DIR)s/../fonts',  # special
    '%(REPORTLAB_DIR)s/../../fonts',  # special
    '%(CWD)s/fonts',  # special
    '~/fonts',
    '~/.fonts',
    '%(XDG_DATA_HOME)s/fonts',
    '~/.local/share/fonts',
    # mac os X - from
    '~/Library/Fonts',
    '/Library/Fonts',
    '/System/Library/Fonts',
)
pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf', enc))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf', enc))
pdfmetrics.registerFont(TTFont('DejaVuSerif', 'DejaVuSerif.ttf', enc))
pdfmetrics.registerFont(TTFont('DejaVuSerif-Bold', 'DejaVuSerif-Bold.ttf', enc))
pdfmetrics.registerFont(TTFont('DejaVuSerif-Italic', 'DejaVuSerif-Italic.ttf', enc))
from models import *


def table_pdf():
    """создание списка учстников в pdf файл"""
    pass
    # doc = SimpleDocTemplate("table_list.pdf", pagesize=A4)
    #
    # story = []  # Список данных таблицы участников
    # elements = []  # Список Заголовки столбцов таблицы
    # player_list = Player.select()
    # count = len(player_list)  # колличество записей в базе
    # kp = count + 1
    #
    # for k in range(0, count):  # цикл по списку по строкам
    #
    #     list = Player.get(Player.id == k + 1)
    #     n = list.num
    #     p = list.player
    #     b = list.bday
    #     c = list.rank
    #     g = list.city
    #     z = list.region
    #     t = list.razryad
    #     listC = Coach.get(Coach.id == list.coach_id)
    #     q = listC.coach
    #
    #     data = [n, p, b, c, g, z, t, q]
    #     elements.append(data)
    # elements.insert(0, ["№", "Фамилия, Имя", "Дата рождени ", "Рейтинг", "Город", "Регион", "Разряд", "Тренер(ы)"])
    # t = Table(elements, 8 * [2 * cm], kp * [0.8 * cm])  # количество столбцов и строк таблицы
    # t = Table(elements)  # количество столбцов и строк таблицы
    # # t = Table(elements, colWidths=(None, None, None, None, None, None, None, None))  #  ширина столбцов, если None-автомтическая
    # t.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), "DejaVuSerif"),  # Использую импортированный шрифт
    #                        ('FONTSIZE', (0, 0), (-1, -1), 8),  # Использую импортированный шрифта размер
    #                        ('BACKGROUND', (0, 0), (-1, (kp * -1)), colors.yellow),
    #                        ('TEXTCOLOR', (0, 0), (-1, (kp * -1)), colors.darkblue),
    #                        ('LINEABOVE', (0, 0), (-1, (kp * -1)), 1, colors.blue),
    #                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),  # цвет и толщину внутренних линий
    #                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black)  # внешние границы таблицы
    #                        ]))
    # h1 = PS("normal", fontSize=14, fontName="DejaVuSerif-Italic", leftIndent=0, firstLineIndent=-20)  # стиль параграфа
    # h1.spaceAfter = 10  # промежуток после заголовка
    # h1.spaceBefore = 0
    # h2 = PS("normal", fontSize=12, fontName="DejaVuSerif-Italic", leftIndent=50, firstLineIndent=-20)  # стиль параграфа
    # h2.spaceAfter = 20  # промежуток после заголовка
    #
    # story.append(Paragraph("Всероссийский турнир Будущее России", h1))
    # story.append(Paragraph('Список участников', h2))
    # story.append(t)
    # doc.multiBuild(story)


def title_pdf(string_data, nz, sr, vz, ct, filepatch):
    """сохранение в PDF формате титульной страницы"""
    canvas = Canvas("Title.pdf", pagesize=A4)
    if filepatch == None:
        canvas.setFont("DejaVuSerif-Italic", 14)
        canvas.drawString(5 * cm, 28 * cm, "Федерация настольного тенниса России")
        canvas.drawString(3 * cm, 27 * cm, "Федерация настольного тенниса Нижегородской области")
        canvas.setFont("DejaVuSerif-Italic", 20)
        canvas.drawString(2 * cm, 23 * cm, nz)
        canvas.setFont("DejaVuSerif-Italic", 16)
        canvas.drawString(2.5 * cm, 22 * cm, "среди " + sr + " " + vz)
        canvas.setFont("DejaVuSerif-Italic", 14)
        canvas.drawString(5.5 * cm, 5 * cm, "г. " + ct + " Нижегородская область")
        canvas.drawString(7.5 * cm, 4 * cm, string_data)
    else:
        canvas.drawImage(filepatch, 7 * cm, 12 * cm, 6.9 * cm, 4.9 * cm,
                         mask=[0, 2, 0, 2, 0, 2])  # делает фон прозрачным
        canvas.setFont("DejaVuSerif-Italic", 14)
        canvas.drawString(5 * cm, 28 * cm, "Федерация настольного тенниса России")
        canvas.drawString(3 * cm, 27 * cm, "Федерация настольного тенниса Нижегородской области")
        canvas.setFont("DejaVuSerif-Italic", 20)
        canvas.drawString(2 * cm, 23 * cm, nz)
        canvas.setFont("DejaVuSerif-Italic", 16)
        canvas.drawString(2.5 * cm, 22 * cm, "среди " + sr + " " + vz)
        canvas.setFont("DejaVuSerif-Italic", 14)
        canvas.drawString(5.5 * cm, 5 * cm, "г. " + ct + " Нижегородская область")
        canvas.drawString(7.5 * cm, 4 * cm, string_data)
    canvas.save()


def table_made():
    """создание 4-х таблиц по 4 участника на альбомном листе"""
    pass

