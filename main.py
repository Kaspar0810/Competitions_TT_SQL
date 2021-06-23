# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import comp_system
import tbl_data


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


import sys
import openpyxl as op
import pdf
import os


from PyQt6 import QtCore, QtGui, QtWidgets, QtPrintSupport, Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from datetime import *
from main_window import Ui_MainWindow  # импортируем из модуля (графического интерфейса main_window) класс Ui_MainWindow
# from models import *
from pdf import *

from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import Paragraph, Table, TableStyle, Image, SimpleDocTemplate
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.platypus import PageBreak
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER

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


# Создаем собственный класс MainWindow, унаследованный от класса графического интерфейса Mainwindow
# и класса QMainWindow

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None, *args, **kwargs) -> object:
        QMainWindow.__init__(self)
        self.setupUi(self)

        self._createAction()
        self._createMenuBar()
        self._connectActions()

        self.menuBar()

        self.Button_title_made.setEnabled(False)

        self.tabWidget.setCurrentIndex(0)
        self.toolBox.setCurrentIndex(0)

    # ======================
    # layout = QGridLayout()
    # layout.addWidget(self.toolBox, 0, 0, 10, 1)
    # layout.addWidget(self.frame_main, 11, 0, 5, 1)
    # layout.addWidget(self.tabWidget, 0, 1, 7, 1)
    # layout.addWidget(self.frame_table, 8, 1, 5, 1)
    # layout.addWidget(self.frame_score, 0, 2, 20, 1)
    #
    # widget = QWidget()
    # widget.setLayout(layout)
    # self.setCentralWidget(widget)
    # layout.setColumnStretch(0, 0)
    # layout.setColumnStretch(1, 6)

    # ====== создание строки меню ===========
    def _createMenuBar(self):
        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)  # разрешает показ менюбара
        # меню Соревнования
        fileMenu = QMenu("Соревнования", self)
        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.newAction)
        saveList = fileMenu.addMenu("Сохранить")
        fileMenu.addAction(self.exitAction)

        # меню Редактировать
        editMenu = menuBar.addMenu("Редактировать")
        #  создание подменю
        saveList.addAction(self.savelist_Action)
        ed_Menu = editMenu.addMenu("Редактор")
        ed_Menu.addAction(self.title_Action)
        ed_Menu.addAction(self.list_Action)
        find_Menu = editMenu.addMenu("Поиск")
        find_Menu.addAction(self.find_r_Action)
        find_Menu.addAction(self.find_r1_Action)

        # меню Рейтинг
        rankMenu = menuBar.addMenu("Рейтинг")
        rankMenu.addAction(self.rAction)
        rankMenu.addAction(self.r1Action)

    #  создание действий меню
    def _createAction(self):
        self.newAction = QAction(self)
        self.newAction.setText("Создать новые")
        self.exitAction = QAction("Выход")
        self.rAction = QAction("Текущий рейтинг")
        self.r1Action = QAction("Рейтинг за январь")
        self.title_Action = QAction("Титульный лист")  # подменю редактор
        self.list_Action = QAction("Список участников")
        self.find_r_Action = QAction("Поиск в текущем рейтинге")  # подменю поиск
        self.find_r1_Action = QAction("Поиск в январском рейтинге")
        self.savelist_Action = QAction("Список")  # подменю сохранить

    def _connectActions(self):
        # Connect File actions
        self.newAction.triggered.connect(self.newFile)
        self.exitAction.triggered.connect(self.exit)
        self.savelist_Action.triggered.connect(self.saveList)
        # Connect Рейтинг actions
        self.rAction.triggered.connect(self.r_File)
        self.r1Action.triggered.connect(self.r1_File)

    def newFile(self):
        # Logic for creating a new file goes here...
        my_win.textEdit.setText("Нажата кнопка меню соревнования")
        dbase()

    def r_File(self):
        # Logic for creating a new file goes here...
        self.statusbar.showMessage("Загружен рейтинг-лист на текущий месяц")
        load_tableWidget()

    def r1_File(self):
        # Logic for creating a new file goes here...
        self.statusbar.showMessage("Загружен рейтинг-лист на январь месяц")
        load_tableWidget()

    def exit(self):
        exit_comp()

    def saveList(self):
        my_win.tabWidget.setCurrentIndex(1)
        my_win.toolBox.setCurrentIndex(1)
        list_player_pdf()
        self.statusbar.showMessage("Список участников сохранен")


app = QApplication(sys.argv)
my_win = MainWindow()
my_win.setWindowTitle("Соревнования по настольному теннису")
my_win.show()



#  ==== наполнение комбобоксов ==========
page_orient = ("альбомная", "книжная")
kategoria_list = ("2-я кат.", "1-я кат.", " ССВК")
mylist = ('мальчиков и девочек', 'юношей и девушек', 'мужчин и женщин')
raz = ("б/р", "3-юн", "2-юн", "1-юн", "3-р", "2-р", "1-р", "КМС", "МС", "МСМК", "ЗМС")
stages1 = ("Основной", "Предварительный", "Полуфиналы", "Финальный", "Суперфинал")
stages2 = ("Полуфиналы", "Финальный", "Суперфинал")
months_list = ("января", "февраля", "марта", "апреля", "мая", "июня", "июля",
               "августа", "сентября", "октября", "ноября", "декабря")

my_win.comboBox_page_1.addItems(page_orient)
my_win.comboBox_page_2.addItems(page_orient)
my_win.comboBox_etap_1.addItems(stages1)
my_win.comboBox_etap_2.addItems(stages2)
my_win.comboBox_kategor_ref.addItems(kategoria_list)
my_win.comboBox_kategor_sek.addItems(kategoria_list)
my_win.comboBox_sredi.addItems(mylist)
my_win.comboBox_razryad.addItems(raz)

# ставит сегодняшнюю дату в виджете календарь
my_win.dateEdit_start.setDate(date.today())
my_win.dateEdit_end.setDate(date.today())


def dbase():
    """Создание DB и таблиц"""
    with db:
        db.create_tables([Title, R_list, Region, City, Player, R1_list, Coach, System, Result, Game_list])
    db_r()
    my_win.Button_title_made.setEnabled(True)


def db_insert_title():
    """Вставляем запись в таблицу титул"""
    nazv = Title(name=nm, sredi=sr, vozrast=vz, data_start=ds, data_end=de, mesto=ms, referee=rf,
                     kat_ref=kr, secretary=sk, kat_sek=ks).save()


def db_select_title():
    """извлекаем из таблицы данные и заполняем поля титула для редактирования или просмотра"""
    with db:
        titles = Title.select().order_by(Title.id.desc()).get()  # получение последней записи в таблице
        my_win.lineEdit_title_nazvanie.setText(titles.name)
        my_win.lineEdit_title_vozrast.setText(titles.vozrast)
        my_win.dateEdit_start.setDate(titles.data_start)
        my_win.dateEdit_end.setDate(titles.data_end)
        my_win.lineEdit_city_title.setText(titles.mesto)
        my_win.lineEdit_refery.setText(titles.referee)
        my_win.comboBox_kategor_ref.setCurrentText(titles.kat_ref)
        my_win.lineEdit_sekretar.setText(titles.secretary)
        my_win.comboBox_kategor_sek.setCurrentText(titles.kat_sek)


# t = Title.select().order_by(Title.id.desc()).get()  # получение последней записи в таблице
#
# if t.id > 0:
#     print("Соревнования уже есть")
#     db_select_title()  # при запуске заполняет титул данными из таблицы
# else:
#     # db_select_title()  # при запуске заполняет титул данными из таблицы
#     print("новые сореввнования")


def system_update(kg):
    """Обновляет таблицу система кол-во игроков, кол-во групп и прочее"""
    sender = my_win.sender()  # сигнал от кнопки
    ps = Player.select()
    ta = len(ps)
    e = int(ta) % int(kg)  # если количество участников не равно делится на группы
    t = int(ta) // int(kg)  # если количество участников равно делится на группы
    title = Title.select().order_by(Title.id.desc()).get()  # получение последней записи в таблице
    if sender == my_win.Button_1etap_made:
        system = System.get(System.id == title.id)  # находит в базе запись в таблице -system- по данным соревнованиям
        # etap_pred = system.get(System.stage == "Предварительный")  # делает выборку записи по этапу соревнований
        if e == 0:
            system.max_player = t
        else:
            system.max_player = t + 1
        system.total_athletes = ta
        system.total_group = kg
        system.stage = my_win.comboBox_etap_1.currentText()
        system.page_vid = my_win.comboBox_page_1.currentText()
    else:
        pass
    system.save()


def system_made():
    """Заполняет таблицу система кол-во игроков, кол-во групп и прочее"""
    t = Title.select().order_by(Title.id.desc()).get()  # последний id соревнований (текуших)
    ce = System.get(System.id == t.id)  # получаем id system текущих соревнований
    cs = System.select().where(System.id == ce)  # все строки, где title_id соревнований
    count_system = len(cs)  # полученкие количества записей (этапов) в системе
    sg = my_win.comboBox_etap_1.currentText()
    page_v = my_win.comboBox_page_1.currentText()
    total_group = ce.total_group
    total_athletes = ce.total_athletes
    max_player = ce.max_player
    if sg == "Основной":
        pass
    else:  # предварительный этап
        for i in range(1, count_system + 1):
            system = System(id=cs, title_id=t, total_athletes=total_athletes, total_group=total_group, max_player=max_player,
                            stage=sg, page_vid=page_v).save()

    player_in_table()
    my_win.checkBox_2.setChecked(False)
    my_win.checkBox_3.setChecked(False)
    my_win.Button_system_made.setEnabled(False)
    my_win.Button_1etap_made.setEnabled(False)
    my_win.Button_2etap_made.setEnabled(False)


def region():
    """добавляет из таблицы в комбобокс регионы"""
    if my_win.comboBox_region.currentIndex() > 0: # проверка на заполненость комбокса данными
        return
    else:
        with db:
            for r in range(1, 86):
                reg = Region.get(Region.id == r)
                my_win.comboBox_region.addItem(reg.region)


def load_tableWidget():
    """Заполняет таблицу списком или рейтингом в зависимости от выбора"""
    sender = my_win.menuWidget().sender()  # сигнал указывающий какой пункт меню нажат

    if sender == my_win.rAction:  # нажат пункт меню -текущий рейтинг-
        z = 5
        collumn_label = ["Место", "  Рейтинг", "Фамилия Имя", "Дата рождения", "Город"]
    elif sender == my_win.r1Action:  # нажат пункт меню -рейтинг за январь-
        z = 5
        collumn_label = ["Место", "  Рейтинг", "Фамилия Имя", "Дата рождения", "Город"]
    elif my_win.tabWidget.currentIndex() == 3:
        z = 7
        collumn_label = ["№ встречи", "Стадия", "Игрок_1", "Игрок_2", "Победитель", "Счет", "Счет в партии"]
    else:
        z = 9
        collumn_label = ["№", "Фамилия, Имя", "Дата рождения", "Рейтинг", "Город", "Регион", "Разряд", "Тренер(ы)", "Место"]


    my_win.tableWidget.setColumnCount(z)
    my_win.tableWidget.setRowCount(1)
    my_win.tableWidget.verticalHeader().hide()
    for i in range(0, z):  # закрашивает заголовки таблиц  рейтинга зеленым цветом
        item = QtWidgets.QTableWidgetItem()
        item.setBackground(QtGui.QColor(0, 255, 150))
        my_win.tableWidget.setHorizontalHeaderItem(i, item)
    my_win.tableWidget.setHorizontalHeaderLabels(collumn_label)
    my_win.tableWidget.isSortingEnabled()
    my_win.tableWidget.show()
    if sender == my_win.rAction:  # нажат пункт меню -текущий рейтинг- и загружет таблицу с рейтингом
        fill_table_R_list()
    elif sender == my_win.r1Action:  # нажат пункт меню -рейтинг за январь- и загружет таблицу с рейтингом
        fill_table_R1_list()
    elif my_win.tabWidget.currentIndex() == 3:
        fill_table_results()
    else:  # загружает таблицу со списком
        fill_table()


def load_listR_in_db(table_db, fname):
    """при отсутсвии выбора файла рейтинга, позволяет выбрать вторично или выйти из диалога
    если выбор был сделан загружает в базу данных"""
    filepatch = str(fname[0])
    if table_db == R_list:
        message = "Вы не выбрали файл с текущим рейтингом!" \
                  "если хотите выйти, нажмите <Ок>" \
                  "если хотите вернуться, нажмите <Отмена>"
    else:
        message = "Вы не выбрали файл с январским рейтингом!" \
                  "если хотите выйти, нажмите <Ок>" \
                  "если хотите вернуться, нажмите <Отмена>"

    if filepatch == "":
        reply = QtWidgets.QMessageBox.information(my_win, 'Уведомление', message,
                                                  QtWidgets.QMessageBox.StandardButtons.Ok,
                                                  QtWidgets.QMessageBox.StandardButtons.Cancel)
        if reply == QMessageBox.StandardButtons.Ok:
            return
        else:
            db_r(table_db=R1_list)
    else:
        rp = filepatch.rindex("/")
        RPath = filepatch[rp + 1: len(filepatch)]
        wb = op.load_workbook(RPath)
        s = wb.sheetnames[0]
        sheet = wb[s]
        for r in range(2, 4500):
            if sheet.cell(row=r, column=2).value is None:
                break
        data = []

        for i in range(2, r):
            A = sheet['A%s' % i].value
            B = sheet['B%s' % i].value
            C = sheet['C%s' % i].value
            D = sheet['D%s' % i].value
            E = sheet['E%s' % i].value
            data.append([A, B, C, D, E])

        with db:
            table_db.insert_many(data).execute()


def db_insert_results():
    """заполняет таблицу базу результаты"""
    pass
    with db:
        res = Result()


def db_r(table_db=R_list):  # table_db присваивает по умолчанию значение R_list
    """переходит на функцию выбора файла рейтинга в зависимости от текущего или январского,
     а потом загружает список регионов базу данных"""
    if table_db == R_list:
        fname = QFileDialog.getOpenFileName(my_win, "Выбрать файл R-листа", "", "Excels files (*.xlsx)")
        load_listR_in_db(table_db, fname)
        my_win.statusbar.showMessage("Текущий рейтинг загружен")
        table_db = R1_list
        fname = QFileDialog.getOpenFileName(my_win, "Выбрать файл R-листа", "", "Excels files (*_01*.xlsx)")
        load_listR_in_db(table_db, fname)
        my_win.statusbar.showMessage("Январский рейтинг загружен")
    else:
        table_db = R1_list
        fname = QFileDialog.getOpenFileName(my_win, "Выбрать файл R-листа", "", "Excels files (*_01*.xlsx)")
        load_listR_in_db(table_db, fname)
        my_win.statusbar.showMessage("Текущий рейтинг загружен")

    # добавляет в таблицу регионы
    wb = op.load_workbook("регионы.xlsx")
    s = wb.sheetnames[0]
    sheet = wb[s]
    reg = []
    for i in range(1, 86):
        A = sheet['B%s' % i].value
        reg.append([A])
    with db:
        Region.insert_many(reg).execute()
    region()
    my_win.statusbar.showMessage("Список регионов загружен")
    my_win.lineEdit_title_nazvanie.hasFocus()


def title_string():
    """ переменные строк титульного листа """
    global nm, vz, ds, de, ms, rf, kr, sk, ks, sr

    nm = my_win.lineEdit_title_nazvanie.text()
    sr = my_win.comboBox_sredi.currentText()
    vz = my_win.lineEdit_title_vozrast.text()
    ds = my_win.dateEdit_start.text()
    de = my_win.dateEdit_end.text()
    ms = my_win.lineEdit_city_title.text()
    rf = my_win.lineEdit_refery.text()
    sk = my_win.lineEdit_sekretar.text()
    kr = my_win.comboBox_kategor_ref.currentText()
    ks = my_win.comboBox_kategor_sek.currentText()
    # return nm, vz, ds, de, ms, rf, kr, sk, ks, sr


def data_title_string(months_list):
    """получение строки начало и конец соревнований для вставки в титульный лист"""
    datastart = my_win.dateEdit_start.text()
    dataend = my_win.dateEdit_end.text()
    ds = int(datastart[8:10])  # получаем число год из календаря
    ms = int(datastart[5:7])  # получаем число месяц из календаря
    ys = int(datastart[0:4])  # получаем число день из календаря
    # ye = int(dataend[0:4])
    me = int(dataend[5:7])
    de = int(dataend[8:10])
    month_st = months_list[ms - 1]
    if de > ds:  # получаем строку начало и конец соревнования в
        # одном месяце или два месяца если начало и конец в разных месяцах
        return str(ds) + " - " + str(de) + " " + month_st + " " + str(ys) + " г."
    else:
        month_end = months_list[me - 1]
        return str(ds) + " " + month_st + " - " + str(de) + " " + month_end + " " + str(ys) + " г."


def title_pdf():
    """сохранение в PDF формате титульной страницы"""
    string_data = data_title_string(months_list)
    nz = my_win.lineEdit_title_nazvanie.text()
    sr = my_win.comboBox_sredi.currentText()
    vz = my_win.lineEdit_title_vozrast.text()
    ct = my_win.lineEdit_city_title.text()

    message = "Хотите добавить изображение в титульный лист?"
    reply = QtWidgets.QMessageBox.question(my_win, 'Уведомление', message,
                                           QtWidgets.QMessageBox.StandardButtons.Yes,
                                           QtWidgets.QMessageBox.StandardButtons.No)
    if reply == QtWidgets.QMessageBox.StandardButtons.Yes:
        fname = QFileDialog.getOpenFileName(my_win, "Выбрать изображение", "/desktop", "Image files (*.jpg, *.png)")
        filepatch = str(fname[0])
    else:
        filepatch = None
    pdf.title_pdf(string_data, nz, sr, vz, ct, filepatch)


def title_made():
    """создание тильного листа соревнования"""
    title_string()
    if my_win.Button_title_made.text() == "Редактировать":
        title_update()
        return
    else:
        db_insert_title()
    title_pdf()
    my_win.checkBox.setChecked(False)  # после заполнения титула выключает чекбокс
    my_win.Button_title_made.setText("Создать")
    region()
    # system_made()
    t = Title.select().order_by(Title.id.desc()).get()  # получение последней записи в таблице
    sg = my_win.comboBox_etap_1.currentText()
    page_v = my_win.comboBox_page_1.currentText()
    with db:
        System.create_table()
        sys = System(title_id=t, total_athletes=0, total_group=0, max_update=0, stage=sg, page_vid=page_v).save()


def title_update():
    """обновляет запись титула, если был он изменен"""
    title_string()
    nazv = Title.select().order_by(Title.id.desc()).get()
    nazv.name = nm
    nazv.vozrast = vz
    nazv.data_start = ds
    nazv.data_end = de
    nazv.mesto = ms
    nazv.referee = rf
    nazv.kat_ref = kr
    nazv.secretary = sk
    nazv.kat_sek = ks
    nazv.save()


def find_in_rlist():
    """при создании списка участников ищет спортсмена в текущем R-листе"""
    my_win.listWidget.clear()
    my_win.textEdit.clear()
    fp = my_win.lineEdit_Family_name.text()
    fp = fp.capitalize()  # Переводит первую букву в заглавную
    p = R_list.select()
    p = p.where(R_list.r_fname ** f'{fp}%')  # like
    if (len(p)) == 0:
        my_win.textEdit.setText("Нет спортсменов в рейтинг листе")
    else:
        for pl in p:
            full_stroka = pl.r_fname + ", " + str(pl.r_list) + ", " + pl.r_bithday + ", " + pl.r_city
            my_win.listWidget.addItem(full_stroka)


def fill_table():
    """заполняет таблицу со списком участников QtableWidget спортсменами из db"""
    player_list = Player.select()
    count = len(player_list)  # колличество записей в базе
    my_win.tableWidget.setRowCount(count)
    for k in range(0, count):  # цикл по списку по строкам

        list = Player.get(Player.id == k + 1)
        my_win.tableWidget.setItem(k, 0, QTableWidgetItem(list.num))
        my_win.tableWidget.setItem(k, 1, QTableWidgetItem(list.player))
        my_win.tableWidget.setItem(k, 2, QTableWidgetItem(list.bday))
        element = str(list.rank)
        padded = ('    ' + element)[-4:]  # make all elements the same length
        my_win.tableWidget.setItem(k, 3, QTableWidgetItem(padded))
        my_win.tableWidget.setItem(k, 4, QTableWidgetItem(list.city))
        my_win.tableWidget.setItem(k, 5, QTableWidgetItem(list.region))
        my_win.tableWidget.setItem(k, 6, QTableWidgetItem(list.razryad))
        listC = Coach.get(Coach.id == list.coach_id)
        my_win.tableWidget.setItem(k, 7, QTableWidgetItem(listC.coach))
        my_win.tableWidget.setItem(k, 8, QTableWidgetItem(list.mesto))
    my_win.tableWidget.resizeColumnsToContents()  # ставит размер столбцов согласно записям


def fill_table_R_list():
    """заполняет таблицу списком из текущего рейтинг листа"""
    player_rlist = R_list.select()
    count = len(player_rlist)  # колличество записей в базе
    my_win.tableWidget.setRowCount(count)
    for k in range(0, count):  # цикл по списку по строкам

        listR = R_list.get(R_list.id == k + 1)
        my_win.tableWidget.setItem(k, 0, QTableWidgetItem(str(listR.r_number)))
        et = str(listR.r_list)
        padded = ('    ' + et)[-4:]  # make all elements the same length
        my_win.tableWidget.setItem(k, 1, QTableWidgetItem(padded))
        my_win.tableWidget.setItem(k, 2, QTableWidgetItem(listR.r_fname))
        my_win.tableWidget.setItem(k, 3, QTableWidgetItem(listR.r_bithday))
        my_win.tableWidget.setItem(k, 4, QTableWidgetItem(listR.r_city))

    my_win.tableWidget.resizeColumnsToContents()  # ставит размер столбцов согласно записям


def fill_table_R1_list():
    """заполняет таблицу списком из январского рейтинг листа"""
    player_rlist = R1_list.select()
    count = len(player_rlist)  # колличество записей в базе
    my_win.tableWidget.setRowCount(count)
    for k in range(0, count):  # цикл по списку по строкам

        listR = R1_list.get(R1_list.id == k + 1)
        my_win.tableWidget.setItem(k, 0, QTableWidgetItem(str(listR.r1_number)))
        et = str(listR.r1_list)
        padded = ('    ' + et)[-4:]  # make all elements the same length
        my_win.tableWidget.setItem(k, 1, QTableWidgetItem(padded))
        my_win.tableWidget.setItem(k, 2, QTableWidgetItem(listR.r1_fname))
        my_win.tableWidget.setItem(k, 3, QTableWidgetItem(listR.r1_bithday))
        my_win.tableWidget.setItem(k, 4, QTableWidgetItem(listR.r1_city))
        # progressbar(count)
    my_win.tableWidget.resizeColumnsToContents()  # ставит размер столбцов согласно записям


def fill_table_results():
    pass
    """заполняет таблицу результатов QtableWidget из db"""
    result_list = Result.select()
    count = len(result_list)  # колличество записей в базе
    my_win.tableWidget.setRowCount(count)
    # for k in range(0, count):  # цикл по списку по строкам

        # list = Player.get(Player.id == k + 1)
        # my_win.tableWidget.setItem(k, 0, QTableWidgetItem(list.num))
        # my_win.tableWidget.setItem(k, 1, QTableWidgetItem(list.player))
        # my_win.tableWidget.setItem(k, 2, QTableWidgetItem(list.bday))
        # element = str(list.rank)
        # padded = ('    ' + element)[-4:]  # make all elements the same length
        # my_win.tableWidget.setItem(k, 3, QTableWidgetItem(padded))
        # my_win.tableWidget.setItem(k, 4, QTableWidgetItem(list.city))
        # my_win.tableWidget.setItem(k, 5, QTableWidgetItem(list.region))
        # my_win.tableWidget.setItem(k, 6, QTableWidgetItem(list.razryad))
        # listC = Coach.get(Coach.id == list.coach_id)
        # my_win.tableWidget.setItem(k, 7, QTableWidgetItem(listC.coach))
    my_win.tableWidget.resizeColumnsToContents()  # ставит размер столбцов согласно записям


def progressbar(count):
    pass
    # progress = QtWidgets.QProgressBar()
    # progress.setValue(100)
    # progress.setMinimum(0)
    # progress.setMaximum(100)
    # m = int(count / 100)
    # for i in range(m, count, m):
    #     progress.setValue(100)


def add_player():
    """добавляет игрока в список и базу данных"""
    fill_table()
    player_list = Player.select()
    count = len(player_list)
    my_win.tableWidget.setRowCount(count + 1)
    pl = my_win.lineEdit_Family_name.text()
    bd = my_win.lineEdit_bday.text()
    rn = my_win.lineEdit_R.text()
    ct = my_win.lineEdit_city_list.text()
    rg = my_win.comboBox_region.currentText()
    rz = my_win.comboBox_razryad.currentText()
    ch = my_win.lineEdit_coach.text()
    ms = ""

    num = count + 1
    add_coach(ch, num)

    with db:
        idc = Coach.get(Coach.coach == ch)
        plr = Player(num=num, player=pl, bday=bd, rank=rn, city=ct, region=rg,
                     razryad=rz, coach_id=idc, mesto=ms).save()

    add_city()
    element = str(rn)
    rn = ('    ' + element)[-4:]  # make all elements the same length
    spisok = (str(num), pl, bd, rn, ct, rg, rz, ch, ms)

    for i in range(0, 9):  # добавляет в tablewidget
        my_win.tableWidget.setItem(count, i, QTableWidgetItem(spisok[i]))

    my_win.lineEdit_Family_name.clear()
    my_win.lineEdit_bday.clear()
    my_win.lineEdit_R.clear()
    my_win.lineEdit_city_list.clear()
    my_win.lineEdit_coach.clear()

    my_win.tableWidget.resizeColumnsToContents()
    list_player_pdf()


def dclick_in_listwidget():
    """Находит фамилию спортсмена в рейтинге или фамилию тренера и заполняет соответсвующие поля списка"""
    text = my_win.listWidget.currentItem().text()
    tc = my_win.lineEdit_coach.text()  # если строка "тренер" пустая значит заполняются поля игрока
    if tc == "":
        ds = len(text)
        sz = text.index(",")
        sz1 = text.index(",", sz + 1)
        sz2 = text.index(",", sz1 + 1)
        fam = text[0:sz]
        r = text[sz + 2:sz1]
        dr = text[sz1 + 2:sz2]
        ci = text[sz2 + 2:ds]
        my_win.lineEdit_Family_name.setText(fam)
        my_win.lineEdit_bday.setText(dr)
        my_win.lineEdit_R.setText(r)
        my_win.lineEdit_city_list.setText(ci)
        c = City.select()  # находит город и соответсвующий ему регион
        c = c.where(City.city ** f'{ci}')  # like
        if (len(c)) == 0:
            my_win.textEdit.setText("Нет такого города в базе")
            my_win.comboBox_region.setCurrentText("")
        else:  # вставляет регион соответсвующий городу
            cr = City.get(City.city == ci)
            rg = Region.get(Region.id == cr.region_id)
            my_win.comboBox_region.setCurrentText(rg.region)
            my_win.listWidget.clear()
    else:  # идет заполнение поля "тренер" из listWidget
        my_win.lineEdit_coach.setText(text)
        my_win.listWidget.clear()


def filter():
    """заполняет комбобокс фильтр групп для таблицы результаты"""
    my_win.comboBox_group.clear()
    gr_txt = []
    kg = my_win.spinBox_kol_group.text()  # количество групп
    kg = int(kg)
    for i in range(1, kg + 1):
        txt = str(i) + " группа"
        gr_txt.append(txt)
    my_win.comboBox_group.addItems(gr_txt)


def tab():
    """Изменяет вкладку tabWidget в зависимости от вкладки toolBox"""
    tw = my_win.tabWidget.currentIndex()
    if tw == 0:
        my_win.tableWidget.show()
        db_select_title()
    elif tw == 1:
        region()
        load_tableWidget()
        my_win.tableWidget.show()
    elif tw == 2:
        my_win.Button_system_made.setEnabled(False)
        my_win.Button_1etap_made.setEnabled(False)
        my_win.Button_2etap_made.setEnabled(False)
        s = System.select().order_by(System.id.desc()).get()
        st = s.total_athletes
        se = s.stage
        if st > 0:
           my_win.comboBox_etap_1.setCurrentText(se)
        else:
            my_win.tableWidget.hide()
            my_win.label_11.hide()
            my_win.label_12.hide()
            my_win.spinBox_kol_group.hide()
            player_list = Player.select()
            count = len(player_list)
            my_win.label_8.setText("Всего участников: " + str(count) + " чел.")
    elif tw == 3:  # вкладка группы
        my_win.tableWidget.show()
        load_tableWidget()
    elif tw == 4:
        my_win.tableWidget.hide()
    elif tw == 5:
        my_win.tableWidget.hide()
    my_win.toolBox.setCurrentIndex(tw)


def page():
    """Изменяет вкладку toolBox в зависимости от вкладки tabWidget"""
    tb = my_win.toolBox.currentIndex()
    if tb == 0:
        db_select_title()
        my_win.tableWidget.show()
    elif tb == 1:
        region()
        load_tableWidget()
        my_win.tableWidget.show()
    elif tb == 2:
        my_win.Button_system_made.setEnabled(False)
        my_win.Button_1etap_made.setEnabled(False)
        my_win.Button_2etap_made.setEnabled(False)
        my_win.tableWidget.hide()
        my_win.label_11.hide()
        my_win.label_12.hide()
        my_win.spinBox_kol_group.hide()
        player_list = Player.select()
        count = len(player_list)
        my_win.label_8.setText("Всего участников: " + str(count) + " чел.")
        s = System.select().order_by(System.id.desc()).get()
        se = s.stage
        my_win.comboBox_etap_1.setCurrentText(se)
        # my_win.label_12.setText()
        my_win.label_12.show()
    elif tb == 3:
        my_win.tableWidget.show()
        load_tableWidget()
    elif tb == 4:
        my_win.tableWidget.hide()
    elif tb == 5:
        my_win.tableWidget.hide()
    my_win.tabWidget.setCurrentIndex(tb)


def add_city():
    """добавляет в таблицу город и соответсвующий ему регион"""
    ci = my_win.lineEdit_city_list.text()
    c = City.select()  # находит город и соответсвующий ему регион
    c = c.where(City.city ** f'{ci}')  # like
    if (len(c)) == 0:  # Если связки город-регион нет в базе то дабавляет
        ir = my_win.comboBox_region.currentIndex()
        ir = ir + 1
        ct = my_win.lineEdit_city_list.text()
        with db:
            city = City(city=ct, region_id=ir).save()


def find_coach():
    """поиск тренера в базе"""
    my_win.listWidget.clear()
    my_win.textEdit.clear()
    cp = my_win.lineEdit_coach.text()
    cp = cp.capitalize()  # Переводит первую букву в заглавную
    c = Coach.select()
    c = c.where(Coach.coach ** f'{cp}%')  # like
    if (len(c)) == 0:
        my_win.textEdit.setText("Нет тренера в базе")
    else:
        for chp in c:
            full_stroka = chp.coach
            my_win.listWidget.addItem(full_stroka)


def add_coach(ch, num):
    """Проверяет наличие тренера в базе и если нет, то добавляет"""
    coach = Coach.select()
    count_coach = len(coach)
    if count_coach == 0:  # если первая запись то добавляет без проверки
        with db:
            cch = Coach(coach=ch, player_id=num).save()
        return
    for c in coach:
        coa = Coach.select().where(Coach.coach == ch)

        if bool(coa):
            my_win.textEdit.setText("Такой тренер(ы) существует")
        else:
            cch = Coach(coach=ch, player_id=num).save()


def find_player_in_R():
    """если есть необходимость в поиске игрок в рейтинг листах январском или текущем"""
    pass


def sort(self):
    """сортировка таблицы QtableWidget (по рейтингу или по алфавиту)"""
    sender = my_win.sender()  # сигнал от кнопки
    player_list = Player.select()
    count = len(player_list)  # колличество записей в базе
    if sender == my_win.Button_sort_R:  # в зависимости от сигала кнопки идет сортировка
        my_win.tableWidget.sortItems(3, QtCore.Qt.SortOrder.DescendingOrder)  # сортировка  Я-А 3-ого столбца
    else:
        my_win.tableWidget.sortItems(1, QtCore.Qt.SortOrder.AscendingOrder)  # сортировка  А-Я 1-ого столбца
    for i in range(0, count):  # отсортировывает номера строк по порядку
        my_win.tableWidget.setItem(i, 0, QTableWidgetItem(str(i + 1)))


def button_etap_made_enabled(state):
    """включает кнопку - создание таблиц - если отмечен чекбокс, защита от случайного нажатия"""
    if state == 2:
        my_win.Button_1etap_made.setEnabled(True)
        my_win.Button_2etap_made.setEnabled(True)


def button_title_made_enable(state):
    """включает кнопку - создание титула - если отмечен чекбокс, защита от случайного нажатия"""
    if state == 2:  # если флажок установлен
        title_string()
        t = Title.select().order_by(Title.id.desc()).get()  # получение последней записи в таблице
        if t.name == nm and str(t.data_start) == ds and str(t.data_end) == de:
            my_win.Button_title_made.setText("Редактировать")
        else:
             my_win.Button_title_made.setText("Создать")
        my_win.Button_title_made.setEnabled(True)
    else:
        my_win.Button_title_made.setEnabled(False)


def button_sytem_made_enable(state):
    """включает кнопку - создание системы - если отмечен чекбокс, защита от случайного нажатия"""
    if state == 2:
        my_win.Button_system_made.setEnabled(True)


def list_player_pdf():
    """создание списка учстников в pdf файл"""
    title = Title.select().order_by(Title.id.desc()).get()  # получение последней записи в таблице

    story = []  # Список данных таблицы участников
    elements = []  # Список Заголовки столбцов таблицы
    player_list = Player.select()
    count = len(player_list)  # колличество записей в базе
    kp = count + 1
    my_win.tableWidget.setRowCount(count)

    for k in range(0, count):  # цикл по списку по строкам
        n = my_win.tableWidget.item(k, 0).text()
        p = my_win.tableWidget.item(k, 1).text()
        b = my_win.tableWidget.item(k, 2).text()
        c = my_win.tableWidget.item(k, 3).text()
        g = my_win.tableWidget.item(k, 4).text()
        z = my_win.tableWidget.item(k, 5).text()
        t = my_win.tableWidget.item(k, 6).text()
        q = my_win.tableWidget.item(k, 7).text()
        m = my_win.tableWidget.item(k, 8).text()
        q = chop_line(q)
        data = [n, p, b, c, g, z, t, q, m]
        elements.append(data)
    elements.insert(0, ["№", "Фамилия, Имя", "Дата рожд.", "Рейтинг", "Город", "Регион", "Разряд", "Тренер(ы)",
                        "Место"])
    t = Table(elements,
              colWidths=(0.6 * cm, 3.7 * cm, 1.9 * cm, 1.2 * cm, 2.5 * cm, 3.1 * cm, 1.2 * cm, 4.7 * cm, 1.1 * cm),
              rowHeights=0.7 * cm)  # ширина столбцов, если None-автомтическая
    t.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), "DejaVuSerif"),  # Использую импортированный шрифт
                           ('FONTSIZE', (0, 0), (-1, -1), 7),  # Использую импортированный шрифта размер
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # вериткальное выравнивание в ячейке заголовка
                           ('ALIGN', (0, 0), (-1, kp * -1), 'CENTER'),  # горизонтальное выравнивание в ячейке
                           ('BACKGROUND', (0, 0), (-1, kp * -1), colors.yellow),
                           ('TEXTCOLOR', (0, 0), (-1, kp * -1), colors.darkblue),
                           ('LINEABOVE', (0, 0), (-1, kp * -1), 1, colors.blue),
                           ('INNERGRID', (0, 0), (-1, -1), 0.05, colors.black),  # цвет и толщину внутренних линий
                           ('BOX', (0, 0), (-1, -1), 0.25, colors.black)  # внешние границы таблицы
                           ]))

    h3 = PS("normal", fontSize=12, fontName="DejaVuSerif-Italic", leftIndent=150, firstLineIndent=-20)  # стиль параграфа
    h3.spaceAfter = 10  # промежуток после заголовка
    story.append(Paragraph('Список участников', h3))
    story.append(t)

    doc = SimpleDocTemplate("table_list.pdf", pagesize=A4)
    doc.build(story, onFirstPage=comp_system.func_zagolovok)


def exit_comp():
    pass
    print("хотите выйти")


def system():
    """выбор системы проведения"""
    ct = my_win.comboBox_etap_1.currentText()
    if ct == "Основной":
        my_win.spinBox_kol_group.hide()
        my_win.label_11.hide()
    elif ct == "Предварительный":
        my_win.spinBox_kol_group.show()
        my_win.spinBox_kol_group.setValue(2)
        my_win.label_11.show()


def kol_player_in_group(self):
    """подсчет кол-во групп и человек в группах"""
    sender = my_win.sender()  # сигнал от кнопки
    kg = my_win.spinBox_kol_group.text()  # количество групп
    player_list = Player.select()
    count = len(player_list)  # колличество записей в базе
    e = int(count) % int(kg)  # если количество участников не равно делится на группы
    t = int(count) // int(kg)  # если количество участников равно делится на группы
    g1 = (int(kg) - e)
    g2 = str(t + 1)
    if e == 0:  # то в группах равное количесто человек -t-
        stroka_kol_group = (kg + " группы по " + str(t) + " чел.")
    else:
        stroka_kol_group = (str(g1) + " групп(а) по " + str(t) + " чел. и "
                            + str(e) + " групп(а) по " + str(g2) + " чел.")
    my_win.label_12.setText(stroka_kol_group)
    my_win.label_12.show()
    filter()
    if sender == my_win.Button_1etap_made:
        system_update(kg)


def page_vid():
    """присваивает переменной значение выборат вида страницы"""
    if my_win.comboBox_page_1.currentText() == "альбомная":
        pv = landscape(A4)
    else:
        pv = A4
    return pv


def view():
    """просмотр PDF файлов средствами OS"""
    tw = my_win.tabWidget.currentIndex()
    view_file = ""
    if tw == 0:
        view_file = "Title.pdf"
    elif tw == 1:
        view_file = "table_list.pdf"
    elif tw == 2:
        pass
    elif tw == 3:  # вкладка группы
        view_file = "table_grup.pdf"
    elif tw == 4:
        pass
    elif tw == 5:
        pass
    os.system(f"open {view_file}")


def player_in_table():
    """заполняет таблицу Game_list данными спортсменами из группы tdt - список списков данных из групп"""
    si = System.get(System.id)
    kg = si.total_group
    ct = si.max_player
    comp_system.table_made(page_vid())
    tdt = tbl_data.total_data_table()
    for p in range(0, kg):
        gr = tdt[p]
        number_group = str(p + 1) + ' группа'
        k = 0
        for i in range(0, ct * 2 - 1, 2):
            family_player = gr[i][1]  # фамилия игрока
            k += 1
            with db:
                game_list = Game_list(number_group=number_group, rank_num_player=k, player_group=family_player,
                                        system_id=si).save()


def chop_line(q, maxline=30):
    """перевод строки если слишком длинный список тренеров"""
    if len(q) > maxline:
        s1 = q.find(",", 0, maxline)
        s2 = q.find(",", s1 + 1, maxline)

        cant = len(q) // maxline
        cant += 1
        strline = ""
        for k in range(1, cant):
            index = maxline * k
            strline += "%s\n" % (q[(index - maxline):s2 + 1])
        strline += "%s" % (q[s2 + 1:])
        q = strline
        return q
    else:
        return q


def proba():
    elements = []
    player_list = Player.select()
    count = len(player_list)  # колличество записей в базе
    # kp = count + 1
    width, height = A4
    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    styleN.alignment = TA_LEFT
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER

    def coord(x, y, unit=1):
        x, y = x * unit, height - y * unit
        return x, y

    # Headers
    num = Paragraph('''<b>№</b>''', styleBH)
    family = Paragraph('''<b>Фамилия, Имя</b>''', styleBH)
    bday = Paragraph('''<b>Дата рождения</b>''', styleBH)
    rank = Paragraph('''<b>Рейтинг</b>''', styleBH)
    city = Paragraph('''<b>Город</b>''', styleBH)
    region = Paragraph('''<b>Регион</b>''', styleBH)
    razryad = Paragraph('''<b>Разряд</b>''', styleBH)
    coach = Paragraph('''<b>Тренер(ы)</b>''', styleBH)
    mesto = Paragraph('''<b>Место</b>''', styleBH)

    #==========================
    for k in range(0, count):  # цикл по списку по строкам
        n = my_win.tableWidget.item(k, 0).text()
        p = my_win.tableWidget.item(k, 1).text()
        b = my_win.tableWidget.item(k, 2).text()
        c = my_win.tableWidget.item(k, 3).text()
        g = my_win.tableWidget.item(k, 4).text()
        z = my_win.tableWidget.item(k, 5).text()
        t = my_win.tableWidget.item(k, 6).text()
        q = my_win.tableWidget.item(k, 7).text()
        m = my_win.tableWidget.item(k, 8).text()

        n = Paragraph(n, styleN)
        p = Paragraph(p, styleN)
        b = Paragraph(b, styleN)
        c = Paragraph(c, styleN)
        g = Paragraph(g, styleN)
        z = Paragraph(z, styleN)
        t = Paragraph(t, styleN)
        q = Paragraph(q, styleN)

        data = [n, p, b, c, g, z, t, q, m]
        # elements.append(data)
    #==========================
    # Texts
    #     n = Paragraph(n, styleN)
    #     p = Paragraph(p, styleN)
    #     b = Paragraph(b, styleN)
    #     c = Paragraph(c, styleN)
    #     g = Paragraph(g, styleN)
    #     z = Paragraph(z, styleN)
    #     t = Paragraph(t, styleN)
    #     q = Paragraph(q, styleN)
    #     m = Paragraph(m, styleN)
    #     elements.append(data)
    data = [[num, family, bday, rank, city, region, razryad, coach, mesto], [n, p, b, c, g, z, t, q, m]]

    t = Table(data, colWidths=(0.6 * cm, 3.7 * cm, 1.9 * cm, 1.2 * cm, 2.5 * cm, 3.1 * cm, 1.2 * cm,
                                4.7 * cm, 1.1 * cm))

    t.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), "DejaVuSerif"),  # Использую импортированный шрифт
                           ('FONTSIZE', (0, 0), (-1, -1), 7),  # Использую импортированный шрифта размер
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # вериткальное выравнивание в ячейке заголовка
                           ('ALIGN', (0, 0), (8, 0), 'CENTER'),  # горизонтальное выравнивание в ячейке
                           ('BACKGROUND', (0, 0), (8, 0), colors.yellow),
                           ('TEXTCOLOR', (0, 0), (8, 0), colors.darkblue),
                           ('LINEABOVE', (0, 0), (8, 0), 1, colors.blue),
                           ('INNERGRID', (0, 0), (-1, -1), 0.05, colors.black),  # цвет и толщину внутренних линий
                           ('BOX', (0, 0), (-1, -1), 0.25, colors.black)  # внешние границы таблицы
                           ]))

    c = canvas.Canvas("a.pdf", pagesize=A4)
    t.wrapOn(c, width, height)
    t.drawOn(c, *coord(0.5, 20, cm))
    c.save()

# ====== отслеживание изменения текста в полях ============

my_win.lineEdit_Family_name.textChanged.connect(find_in_rlist)  # в поле поиска и вызов функции
my_win.lineEdit_coach.textChanged.connect(find_coach)

my_win.listWidget.itemDoubleClicked.connect(dclick_in_listwidget)

my_win.tabWidget.currentChanged.connect(tab)
my_win.toolBox.currentChanged.connect(page)
# ==================================
my_win.spinBox_kol_group.textChanged.connect(kol_player_in_group)
# ======== изменение индекса комбобоксов ===========
my_win.comboBox_etap_1.currentTextChanged.connect(system)
my_win.comboBox_page_1.currentTextChanged.connect(page_vid)

# =======  отслеживание переключение чекбоксов =========
my_win.checkBox.stateChanged.connect(button_title_made_enable)  # при изменении чекбокса активирует кнопку создать
my_win.checkBox_2.stateChanged.connect(button_etap_made_enabled)  # при изменении чекбокса активирует кнопку создать
my_win.checkBox_3.stateChanged.connect(button_sytem_made_enable)  # при изменении чекбокса активирует кнопку создать
# =======  нажатие кнопок =========
my_win.Button_1etap_made.clicked.connect(kol_player_in_group)  # рисует таблицы группового этапа и заполняет game_list
my_win.Button_system_made.clicked.connect(system_made)  # создание системы соревнований
my_win.Button_proba.clicked.connect(proba)
my_win.Button_add_player.clicked.connect(add_player)  # добавляет игроков в список и базу
my_win.Button_group.clicked.connect(player_in_table)  # вносит спортсменов в группы
my_win.Button_title_made.clicked.connect(title_made)  # записывает в базу или редактирует титул

my_win.Button_sort_R.clicked.connect(sort)
my_win.Button_sort_Name.clicked.connect(sort)
my_win.Button_view.clicked.connect(view)
sys.exit(app.exec())
