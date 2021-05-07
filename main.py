# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


import sys
import openpyxl as op


from PyQt6 import QtCore, QtGui, QtWidgets, QtPrintSupport, Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from datetime import *
from main_window import Ui_MainWindow  # импортируем из модуля (графического интерфейса main_window) класс Ui_MainWindow
from models import *

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch, cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, Table, TableStyle, Image
enc = 'UTF-8'

TTFSearchPath = (
            'c:/winnt/fonts',
            'c:/windows/fonts',
            '%(REPORTLAB_DIR)s/fonts',      #special
            '%(REPORTLAB_DIR)s/../fonts',   #special
            '%(REPORTLAB_DIR)s/../../fonts',#special
            '%(CWD)s/fonts',                #special
            '~/fonts',
            '~/.fonts',
            '%(XDG_DATA_HOME)s/fonts',
            '~/.local/share/fonts',
            #mac os X - from
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

    def __init__(self, parent=None, *args, **kwargs):
        QMainWindow.__init__(self)
        self.setupUi(self)
        # self.setMinimumSize(1440, 800)
        self._createAction()
        self._createMenuBar()
        self._connectActions()
        self.statusbar.showMessage("Ready")
        # установка таблицы списка спортсменов QtableWidget
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(1)
        self.tableWidget.verticalHeader().hide()
        for i in range(0, 8):  # закрашивает заголовки таблиц зеленым цветом
            item = QtWidgets.QTableWidgetItem()
            item.setBackground(QtGui.QColor(0, 255, 150))
            self.tableWidget.setHorizontalHeaderItem(i, item)
        collumn_label = ["№", "Фамилия, Имя", "Дата рождения", "Рейтинг", "Город", "Регион", "Разряд", "Тренер(ы)"]
        self.tableWidget.setHorizontalHeaderLabels(collumn_label)
        self.tableWidget.isSortingEnabled()
        # установка таблицы списка R спортсменов QtableWidget_R_list
        self.tableWidget_R_list.setColumnCount(5)
        self.tableWidget_R_list.setRowCount(1)
        self.tableWidget_R_list.verticalHeader().hide()
        for i in range(0, 6):  # закрашивает заголовки таблиц  рейтинга зеленым цветом
            item = QtWidgets.QTableWidgetItem()
            item.setBackground(QtGui.QColor(0, 255, 150))
            self.tableWidget_R_list.setHorizontalHeaderItem(i, item)
        collumn_label = ["Место", "  Рейтинг", "Фамилия Имя", "Дата рождения", "Город"]
        self.tableWidget_R_list.setHorizontalHeaderLabels(collumn_label)
        self.tableWidget_R_list.isSortingEnabled()
        self.tableWidget_R_list.hide()
        self.menuBar()

        self.Button_title_made.setEnabled(False)
        self.Button_title_edit.setEnabled(False)
    #  размещение виджета в правой стороне
    #     self.centralwidget = QWidget()
    #     self.setCentralWidget(self.centralwidget)
    #     self.grid = QGridLayout(self.centralwidget)
    #
    #     # self.grid.setSpacing(10)
    #     self.grid.addWidget(self.toolBox, 0, 0, 20, 1)
    #     self.grid.addWidget(self.frame_main, 21, 0, 6, 1)
    #     self.grid.addWidget(self.tabWidget, 0, 2, 10, 3)
    #     self.grid.addWidget(self.frame_table, 11, 2, 16, 3)
    #     self.grid.addWidget(self.frame_score, 0, 6, 28, 3)


    # ====== создание строки меню ===========
    def _createMenuBar(self):
        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)  # разрешает показ менюбара
        # меню Соревнования
        fileMenu = QMenu("Соревнования", self)
        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.newAction)
        # меню Рейтинг
        rank_Menu = menuBar.addMenu("Рейтинг")
        rank_Menu.addAction(self.rAction)
        rank_Menu.addAction(self.r1Action)

    #  создание действий меню
    def _createAction(self):
        self.newAction = QAction(self)
        self.newAction.setText("Создать")
        self.rAction = QAction("Текущий рейтинг")
        self.r1Action = QAction("Рейтинг за январь")

    def _connectActions(self):
        # Connect File actions
        self.newAction.triggered.connect(self.newFile)
        # Connect Рейтинг actions
        self.rAction.triggered.connect(self.r_File)
        self.r1Action.triggered.connect(self.r1_File)

    def newFile(self):
        # Logic for creating a new file goes here...
        my_win.textEdit.setText("Нажата кнопка меню соревнования")

    def r_File(self):
        # Logic for creating a new file goes here...
        self.statusbar.showMessage("Загружен рейтинг-лист на текущий месяц")
        fill_table_R_list()

    def r1_File(self):
        # Logic for creating a new file goes here...
        self.statusbar.showMessage("Загружен рейтинг-лист на январь месяц")
        fill_table_R1_list()



app = QApplication(sys.argv)
my_win = MainWindow()
my_win.setWindowTitle("Соревнования по настольному теннису")
my_win.show()



with db:  # добавляет из таблицы в комбобокс регионы
    for r in range(1, 86):
        reg = Region.get(Region.id == r)
        my_win.comboBox_region.addItem(reg.region)

#  ==== наполнение комбобоксов ==========
kategoria_list = ("2-я кат.", "1-я кат.", " ССВК")
mylist = ('мальчиков и девочек', 'юношей и девушек', 'мужчин и женщин')
raz = ("б/р", "3-юн", "2-юн", "1-юн", "3-р", "2-р", "1-р", "КМС", "МС", "МСМК", "ЗМС")

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
        db.create_tables([Title, R_list, Region, City, Player, R1_list, Coach])

    db_r()


def db_insert_title():
    """Вставляем запись в таблицу титул"""
    with db:
        nazv = Title(name=nm, vozrast=vz, data_start=ds, data_end=de, mesto=ms, referee=rf,
                     kat_ref=kr, secretary=sk, kat_sek=ks).save()


def db_select_title():
    """извлекаем из таблицы данные и заполняем поля титула для редактирования или просмотра"""
    with db:
        titles = Title.get(Title.id == 1)
        my_win.lineEdit_title_nazvanie.setText(titles.name)
        my_win.lineEdit_title_vozrast.setText(titles.vozrast)
        my_win.dateEdit_start.setDate(titles.data_start)
        my_win.dateEdit_end.setDate(titles.data_end)
        my_win.lineEdit_city_title.setText(titles.mesto)
        my_win.lineEdit_refery.setText(titles.referee)
        my_win.comboBox_kategor_ref.setCurrentText(titles.kat_ref)
        my_win.lineEdit_sekretar.setText(titles.secretary)
        my_win.comboBox_kategor_sek.setCurrentText(titles.kat_sek)


def load_listR_in_db(table_db, fname):
    """при отсутсвии выбора файла рейтинга, позволяет выбрать вторично или выйти из диалога
    если выбор был сделан загружает в базу данных"""
    filepatch = str(fname[0])
    if table_db == R_list:
        message = "Вы не выбрали файл с текущим рейтингом!" \
                  "если хотите выйти, нажмите <Ок>"    \
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
        my_win.statusbar.showMessage("Текущий рейтинг загружен")
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


def title_string():  # переменные строк титульного листа
    global nm, vz, ds, de, ms, rf, kr, sk, ks

    nm = my_win.lineEdit_title_nazvanie.text()
    vz = my_win.lineEdit_title_vozrast.text()
    ds = my_win.dateEdit_start.text()
    de = my_win.dateEdit_end.text()
    ms = my_win.lineEdit_city_title.text()
    rf = my_win.lineEdit_refery.text()
    sk = my_win.lineEdit_sekretar.text()
    kr = my_win.comboBox_kategor_ref.currentText()
    ks = my_win.comboBox_kategor_sek.currentText()


def title_made():
    """создание тильного листа соревнования"""
    age = my_win.lineEdit_title_vozrast.text()
    p = age.count(" ")
    if p == 2:
        god = int(age[3:5])
        age = date.today().year - (god - 1)  # год рождения и младше могут играть
    elif p == 4:
        age = int(age[0:5])  # год рождения и младше могут играть
    data_title_string()
    # dbase()
    # db_insert_title()
    title_pdf()
    my_win.Button_title_made.setEnabled(False)  # после заполнения титула выключает кнопку
    my_win.Button_title_edit.setEnabled(1)


def title_update():
    """обновляет запись титула, если был он изменен"""

    title_string()
    nazv = Title.get(Title.id == 1)
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


def data_title_string(string_data):
    """получение строки начало и конец соревнований для вставки в титульный лист"""
    months_list = ("января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа",
                   "сентября", "октября", "ноября", "декабря")
    datastart = my_win.dateEdit_start.text()
    dataend = my_win.dateEdit_end.text()
    ys = int(datastart[0:4])  # получаем число год из календаря
    ms = int(datastart[5:7])  # получаем число месяц из календаря
    ds = int(datastart[8:10])  # получаем число день из календаря
    ye = int(dataend[0:4])
    me = int(dataend[5:7])
    de = int(dataend[8:10])
    month_st = months_list[ms - 1]
    month_end = months_list[me - 1]
    if de > ds:  # получаем строку начало и конец соревнования в
        # одном месяце или два месяца если начало и конец в разных месяцах
        string_data = str(ds) + " - " + str(de) + " " + month_st + " " + str(ys) + " г."
    else:
        month_end = months_list[me - 1]
        string_data = str(ds) + " " + month_st + " - " + str(de) + " " + month_end + " " + str(ys) + " г."
    return string_data

def title_pdf(string_data):
    """сохранение в PDF формате титульной страницы"""
    canvas = Canvas("Title.pdf", pagesize=A4)
    message = "Хотите добавить изображение в титульный лист?"
    reply = QtWidgets.QMessageBox.question(my_win, 'Уведомление', message,
                                           QtWidgets.QMessageBox.StandardButtons.Yes,
                                           QtWidgets.QMessageBox.StandardButtons.No)
    if reply == QtWidgets.QMessageBox.StandardButtons.Yes:
        fname = QFileDialog.getOpenFileName(my_win, "Выбрать изображение", "/desktop", "Image files (*.jpg, *.png)")
        filepatch = str(fname[0])
        canvas.drawImage(filepatch, 7 * cm, 12 * cm, 6.9 * cm, 4.9 * cm, mask=[0, 2, 0, 2, 0, 2])  # делает фон прозрачным
        canvas.setFont("DejaVuSerif-Italic", 14)
        canvas.drawString(5 * cm, 28 * cm, "Федерация настольного тенниса России")
        canvas.drawString(3 * cm, 27 * cm, "Федерация настольного тенниса Нижегородской области")
        canvas.setFont("DejaVuSerif-Italic", 20)
        canvas.drawString(2 * cm, 23 * cm, my_win.lineEdit_title_nazvanie.text())
        canvas.setFont("DejaVuSerif-Italic", 16)
        canvas.drawString(2.5 * cm, 22 * cm,
                          "среди " + my_win.comboBox_sredi.currentText() + " " + my_win.lineEdit_title_vozrast.text())
        canvas.setFont("DejaVuSerif-Italic", 14)
        canvas.drawString(5.5 * cm, 5 * cm, "г. " + my_win.lineEdit_city_title.text() + " Нижегородская область")
        canvas.drawString(7.5 * cm, 4 * cm, data_title_string(string_data))
    else:
        canvas.setFont("DejaVuSerif-Italic", 14)
        canvas.drawString(5 * cm, 28 * cm, "Федерация настольного тенниса России")
        canvas.drawString(3 * cm, 27 * cm, "Федерация настольного тенниса Нижегородской области")
        canvas.setFont("DejaVuSerif-Italic", 20)
        canvas.drawString(2 * cm, 23 * cm, my_win.lineEdit_title_nazvanie.text())
        canvas.setFont("DejaVuSerif-Italic", 16)
        canvas.drawString(2.5 * cm, 22 * cm,
                          "среди " + my_win.comboBox_sredi.currentText() + " " + my_win.lineEdit_title_vozrast.text())
        canvas.setFont("DejaVuSerif-Italic", 14)
        canvas.drawString(5.5 * cm, 5 * cm, "г. " + my_win.lineEdit_city_title.text() + " Нижегородская область")
        canvas.drawString(7.5 * cm, 4 * cm, data_title_string(string_data))
    canvas.save()


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
    my_win.tableWidget.resizeColumnsToContents()  # ставит размер столбцов согласно записям


def fill_table_R_list():
    """заполняет таблицу списком из текущего рейтинг листа"""
    my_win.tableWidget.hide()
    my_win.tableWidget_R_list.show()
    player_rlist = R_list.select()
    count = len(player_rlist)  # колличество записей в базе
    my_win.tableWidget_R_list.setRowCount(count)
    for k in range(0, count):  # цикл по списку по строкам

        listR = R_list.get(R_list.id == k + 1)
        my_win.tableWidget_R_list.setItem(k, 0, QTableWidgetItem(str(listR.r_number)))
        et = str(listR.r_list)
        padded = ('    ' + et)[-4:]  # make all elements the same length
        my_win.tableWidget_R_list.setItem(k, 1, QTableWidgetItem(padded))
        my_win.tableWidget_R_list.setItem(k, 2, QTableWidgetItem(listR.r_fname))
        my_win.tableWidget_R_list.setItem(k, 3, QTableWidgetItem(listR.r_bithday))
        my_win.tableWidget_R_list.setItem(k, 4, QTableWidgetItem(listR.r_city))

    my_win.tableWidget_R_list.resizeColumnsToContents()  # ставит размер столбцов согласно записям


def fill_table_R1_list():
    """заполняет таблицу списком из январского рейтинг листа"""
    my_win.tableWidget.hide()
    my_win.tableWidget_R_list.show()
    player_rlist = R1_list.select()
    count = len(player_rlist)  # колличество записей в базе
    my_win.tableWidget_R_list.setRowCount(count)
    for k in range(0, count):  # цикл по списку по строкам

        listR = R1_list.get(R1_list.id == k + 1)
        my_win.tableWidget_R_list.setItem(k, 0, QTableWidgetItem(str(listR.r1_number)))
        et = str(listR.r1_list)
        padded = ('    ' + et)[-4:]  # make all elements the same length
        my_win.tableWidget_R_list.setItem(k, 1, QTableWidgetItem(padded))
        my_win.tableWidget_R_list.setItem(k, 2, QTableWidgetItem(listR.r1_fname))
        my_win.tableWidget_R_list.setItem(k, 3, QTableWidgetItem(listR.r1_bithday))
        my_win.tableWidget_R_list.setItem(k, 4, QTableWidgetItem(listR.r1_city))

    my_win.tableWidget_R_list.resizeColumnsToContents()  # ставит размер столбцов согласно записям

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
    num = count + 1
    add_coach(ch, num)

    with db:

        idc = Coach.get(Coach.coach == ch)
        plr = Player(num=num, player=pl, bday=bd, rank=rn, city=ct, region=rg,
                     razryad=rz, coach_id=idc).save()

    add_city()
    element = str(rn)
    rn = ('    ' + element)[-4:]  # make all elements the same length
    spisok = (str(num), pl, bd, rn, ct, rg, rz, ch)

    for i in range(0, 8):  # добавляет в tablewidget
        my_win.tableWidget.setItem(count, i, QTableWidgetItem(spisok[i]))

    my_win.lineEdit_Family_name.clear()
    my_win.lineEdit_bday.clear()
    my_win.lineEdit_R.clear()
    my_win.lineEdit_city_list.clear()
    my_win.lineEdit_coach.clear()

    my_win.tableWidget.resizeColumnsToContents()


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


def tab():
    """Изменяет вкладку tabWidget в зависимости от вкладки toolBox"""
    tw = my_win.tabWidget.currentIndex()
    tb = my_win.toolBox.currentIndex()
    if tw == tb:
        return
    else:
        my_win.tabWidget.setCurrentIndex(tw)

        if tw == 0:
            db_select_title()
        if tw == 1:
            my_win.tableWidget.show()
            my_win.tableWidget_R_list.hide()
            fill_table()
        my_win.toolBox.setCurrentIndex(tw)


def page():
    """Изменяет вкладку toolBox в зависимости от вкладки tabWidget"""
    tw = my_win.tabWidget.currentIndex()
    tb = my_win.toolBox.currentIndex()
    if tb == tw:
        return
    else:
        my_win.toolBox.setCurrentIndex(tb)
        if tb == 0:
            db_select_title()
        if tb == 1:
            my_win.tableWidget.show()
            my_win.tableWidget_R_list.hide()
            fill_table()
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


def find_coach():  # Поиск тренера в базе
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


def button_title_made_enable(state):
    """включает кнопку - создание титула - если отмечен чекбокс, защита от случайного нажатия"""
    if state == 2:  # если флажок установлен
        my_win.Button_title_made.setEnabled(True)
    else:
        my_win.Button_title_made.setEnabled(False)


def button_title_edit_enable(state):
    """включает кнопку - редактирование титула - если отмечен чекбокс, защита от случайного нажатия"""
    if state == 2:  # если флажок установлен
        my_win.Button_title_edit.setEnabled(True)
        tab()
    else:
        my_win.Button_title_edit.setEnabled(False)

# ====== отслеживание изменения текста в полях ============
my_win.lineEdit_Family_name.textChanged.connect(find_in_rlist)  # в поле поиска и вызов функции
my_win.lineEdit_coach.textChanged.connect(find_coach)

my_win.listWidget.itemDoubleClicked.connect(dclick_in_listwidget)

my_win.tabWidget.currentChanged.connect(tab)
my_win.toolBox.currentChanged.connect(page)

# =======  срабатывание кнопок =========
my_win.checkBox.stateChanged.connect(button_title_made_enable)
my_win.checkBox_edit.stateChanged.connect(button_title_edit_enable)

my_win.Button_add_player.clicked.connect(add_player)  # добавляет игроков в список и базу

my_win.Button_title_made.clicked.connect(title_made)  # вызов окна диалога выбора изображения для вставки в титул
# my_win.Button_title_edit.clicked.connect(db_select_title)
my_win.Button_sort_R.clicked.connect(sort)
my_win.Button_sort_Name.clicked.connect(sort)
# my_win.Button_export.clicked.connect(export)
my_win.Button_title_edit.clicked.connect(title_pdf)
# my_win.Button_view.clicked.connect(handlePreview)

sys.exit(app.exec())


