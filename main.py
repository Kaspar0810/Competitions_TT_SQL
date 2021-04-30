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
from PyQt6.Qt import *
from PyQt6.QtGui import *
# from PyQt6.QtCore import pyqtSignal, QObject, QEvent
from datetime import *
from main_window import Ui_MainWindow  # импортируем из модуля (графического интерфейса main_window) класс Ui_MainWindow
from fpdf import FPDF
from models import *

# from csv import reader


FPDF.SYSTEM_TTFONTS = '/library/fonts'
pdf = FPDF()


# Создаем собственный класс MainWindow, унаследованный от класса графического интерфейса Mainwindow
# и класса QMainWindow

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None, *args, **kwargs):
        QMainWindow.__init__(self)
        self.setupUi(self)
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
        for i in range(0, 6):  # закрашивает заголовки таблиц зеленым цветом
            item = QtWidgets.QTableWidgetItem()
            item.setBackground(QtGui.QColor(0, 255, 150))
            self.tableWidget_R_list.setHorizontalHeaderItem(i, item)
        collumn_label = ["Место", "  Рейтинг", "Фамилия Имя", "Дата рождения", "Город"]
        self.tableWidget_R_list.setHorizontalHeaderLabels(collumn_label)
        self.tableWidget_R_list.isSortingEnabled()
        self.tableWidget_R_list.hide()
        self.menuBar()

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
        self.r1Action = QAction("Рейтинг за январь", self)

    def _connectActions(self):
        # Connect File actions
        self.newAction.triggered.connect(self.newFile)
        # Connect Рейтинг actions
        self.rAction.triggered.connect(self.r_File)

    def newFile(self):
        # Logic for creating a new file goes here...
        my_win.textEdit.setText("Нажата кнопка меню соревнования")

    def r_File(self):
        # Logic for creating a new file goes here...
        fill_table_R_list()

    # def dbase():  # Создание DB и таблиц
    #
    #     with db:
    #         db.create_tables([Titul, R_list, Region, City, Player, R1_list, Coach])


app = QApplication(sys.argv)
my_win = MainWindow()
my_win.setWindowTitle("Соревнования по настольному теннису")
my_win.show()

with db:  # добавляет из таблицы в комбобокс регионы
    for r in range(1, 86):
        reg = Region.get(Region.id == r)
        my_win.comboBox_region.addItem(reg.region)

#  ==== наполнение комбоксов ==========
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


# def dbase():  # Создание DB и таблиц
#
#     with db:
#         db.create_tables([Titul, R_list, Region, City, Player, R1_list, Coach])


def db_insert_titul():  # Вставляем запись в таблицу титул

    with db:
        nazv = Titul(name=nm, vozrast=vz, data_start=ds, data_end=de, mesto=ms, referee=rf,
                     kat_ref=kr, secretary=sk, kat_sek=ks).save()


def db_select_titul():  # извлекаем из таблицы данные и заполняем поля титула для редактирования

    with db:
        tituls = Titul.get(Titul.id == 1)
        my_win.lineEdit_titul_nazvanie.setText(tituls.name)
        my_win.lineEdit_titul_vozrast.setText(tituls.vozrast)
        my_win.dateEdit_start.setDate(tituls.data_start)
        my_win.dateEdit_end.setDate(tituls.data_end)
        my_win.lineEdit_city_titul.setText(tituls.mesto)
        my_win.lineEdit_refery.setText(tituls.referee)
        my_win.comboBox_kategor_ref.setCurrentText(tituls.kat_ref)
        my_win.lineEdit_sekretar.setText(tituls.secretary)
        my_win.comboBox_kategor_sek.setCurrentText(tituls.kat_sek)


def db_r():  # Загружает рейтинг лист в базу данных
    pass
    # fname = QFileDialog.getOpenFileName(my_win, "Выбрать файл R-листа", "", "Excels files (*.xlsx)")
    # filepatch = str(fname[0])
    # rp = filepatch.rindex("/")
    # RPath = filepatch[rp + 1: len(filepatch)]
    # wb = op.load_workbook(RPath)
    # s = wb.sheetnames[0]
    # sheet = wb[s]
    # for r in range(2, 4500):
    #     if sheet.cell(row=r, column=2).value is None:
    #         break

    # rows = r - 1
    # data = []
    #
    # for i in range(2, rows):
    #     A = sheet['A%s' % i].value
    #     B = sheet['B%s' % i].value
    #     C = sheet['C%s' % i].value
    #     D = sheet['D%s' % i].value
    #     E = sheet['E%s' % i].value
    #     data.append([A, B, C, D, E])
    #
    # with db:
    #     R_list.insert_many(data).execute()


#  добавляет файл рейтинга за январь
#     fname = QFileDialog.getOpenFileName(my_win, "Выбрать файл R1-листа", "", "Excels files (*01_m.xlsx)")
#     filepatch = str(fname[0])
#     rp = filepatch.rindex("/")
#     RPath = filepatch[rp + 1: len(filepatch)]
#     wb = op.load_workbook(RPath)
#     s = wb.sheetnames[0]
#     sheet = wb[s]
#     for r in range(2, 4500):
#         if sheet.cell(row=r, column=2).value is None:
#             break
#
#     rows = r - 1
#     data = []
#
#     for i in range(2, rows):
#         A = sheet['A%s' % i].value
#         B = sheet['B%s' % i].value
#         C = sheet['C%s' % i].value
#         D = sheet['D%s' % i].value
#         E = sheet['E%s' % i].value
#         data.append([A, B, C, D, E])
#
#     with db:
#         R1_list.insert_many(data).execute()

#  добавляет в таблицу регионы
#     reg = []
#
#     for i in range(1, 86):
#         A = sheet['B%s' % i].value
#
#         reg.append([A])
#     with db:
#         Region.insert_many(reg).execute()

def titul_stroka():  # переменные строк титульного листа
    global nm, vz, ds, de, ms, rf, kr, sk, ks

    nm = my_win.lineEdit_titul_nazvanie.text()
    vz = my_win.lineEdit_titul_vozrast.text()
    ds = my_win.dateEdit_start.text()
    de = my_win.dateEdit_end.text()
    ms = my_win.lineEdit_city_titul.text()
    rf = my_win.lineEdit_refery.text()
    sk = my_win.lineEdit_sekretar.text()
    kr = my_win.comboBox_kategor_ref.currentText()
    ks = my_win.comboBox_kategor_sek.currentText()


def titul_made():  # создание тильного листа соревнования
    age = my_win.lineEdit_titul_vozrast.text()
    p = age.count(" ")
    if p == 2:
        god = int(age[3:5])
        age = date.today().year - (god - 1)  # год рождения и младше могут играть
    elif p == 4:
        age = int(age[0:5])  # год рождения и младше могут играть
    titul_stroka()
    # dbase()
    db_insert_titul()
    titul_pdf()
    my_win.pushButton_titul_made.setEnabled(0)  # после заполнения титула выключает кнопку
    my_win.pushButton_titul_edit.setEnabled(1)


def titul_update():  # обновляет запись титула

    titul_stroka()
    nazv = Titul.get(Titul.id == 1)
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


def titul_pdf():  # сохранение в PDF формате титульной страницы

    pdf = FPDF()
    pdf.add_page()
    message = "Хотите добавить изображение в титульный лист?"
    reply = QtWidgets.QMessageBox.question(my_win, 'Уведомление', message,
                                           QtWidgets.QMessageBox.StandardButtons.Yes,
                                           QtWidgets.QMessageBox.StandardButtons.No)
    if reply == QtWidgets.QMessageBox.StandardButtons.Yes:
        fname = QFileDialog.getOpenFileName(my_win, "Выбрать изображение", "/desktop", "Image files (*.jpg, *.png)")
        filepatch = str(fname[0])
        pdf.image(filepatch, x=80, y=100)

    pdf.add_font('DejaVu', '', 'DejaVuSerif.ttf', uni=True)
    pdf.set_font("DejaVu", "", 10)
    pdf.cell(200, 10, txt='Федерация настольного тенниса России', ln=1, align="C")
    pdf.cell(200, 10, txt='Федерация настольного тенниса Нижегородской области', ln=2, align="C")
    pdf.ln(20)  # ниже на 20 строк
    pdf.add_font('DejaVu', '', 'DejaVuSerif-Italic.ttf', uni=True)
    pdf.set_font("DejaVu", "", 22)
    pdf.cell(200, 10, txt=my_win.lineEdit_titul_nazvanie.text(), ln=23, align="C")
    pdf.add_font('DejaVu', 'I', 'DejaVuSerif-Italic.ttf', uni=True)
    pdf.set_font("DejaVu", "", 18)
    stroka_2 = ("среди " + my_win.comboBox_sredi.currentText() + " " + my_win.lineEdit_titul_vozrast.text())
    pdf.cell(200, 10, txt=stroka_2, ln=0, align="C")
    pdf.set_font("DejaVu", "", 14)
    pdf.ln(150)
    pdf.cell(200, 10, txt="г. " + my_win.lineEdit_city.text(), ln=174, align="c")
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
        stroka_data = str(ds) + " - " + str(de) + " " + month_st + " " + str(ys) + " г."
    else:
        month_end = months_list[me - 1]
        stroka_data = str(ds) + " " + month_st + " - " + str(de) + " " + month_end + " " + str(ys) + " г."
    pdf.cell(200, 10, txt=stroka_data, ln=0, align="C")
    pdf.output("titul.pdf")


def find_in_rlist(fp):  # поиск спортсмена в R-листе
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


def fill_table():  # заполняет таблицу QtableWidget спортсменами из db
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


def add_player():  # добавляет игрока в список и базу
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


def dclick_in_listwidget():  # Находит фамилию в рейтинге или фамилию тренера
    # и загружают в соответсвующие поля списка
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


def tab(tw):  # Изменяет вкладку tabWidget в зависимости от вкладки toolBox

    if tw == 0:
        db_select_titul()
    my_win.tabWidget.setCurrentIndex(tw)
    if tw == 1:
        my_win.tableWidget.show()
        my_win.tableWidget_R_list.hide()
        fill_table()


def page(tb):  # Изменяет вкладку toolBox в зависимости от вкладки tabWidget

    if tb == 0:
        db_select_titul()
    my_win.toolBox.setCurrentIndex(tb)
    if tb == 1:
        my_win.tableWidget.show()
        my_win.tableWidget_R_list.hide()
        fill_table()


def add_city():  # добавляет в таблицу города и регионы
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


def add_coach(ch, num):  # Если нет тренера в базе то добавляет

    coach = Coach.select()
    for c in coach:
        coa = Coach.select().where(Coach.coach == ch)

        if bool(coa):
            my_win.textEdit.setText("Такой тренер(ы) существует")
        else:
            cch = Coach(coach=ch, player_id=num).save()


def export():
    pass


def sort(self):  # сортировка таблицы QtableWidget (по рейтингу или по алфавиту)
    sender = my_win.sender()  # сигнал от кнопки
    player_list = Player.select()
    count = len(player_list)  # колличество записей в базе
    if sender == my_win.pushButton_sort_R:  # в зависимости от сигала кнопки идет сортировка
        my_win.tableWidget.sortItems(3, QtCore.Qt.SortOrder.DescendingOrder)  # сортировка  Я-А 3-ого столбца
    else:
        my_win.tableWidget.sortItems(1, QtCore.Qt.SortOrder.AscendingOrder)  # сортировка  А-Я 1-ого столбца

    for i in range(0, count):  # отсортировывает номера строк по порядку
        my_win.tableWidget.setItem(i, 0, QTableWidgetItem(str(i + 1)))


def handlePreview(self):
    pass


def handlePaintRequest(self, printer):
    pass


def r_listing():
    pass


# ====== отслеживание изменения текста в полях ============
my_win.lineEdit_Family_name.textChanged.connect(find_in_rlist)  # в поле поиска и вызов функции
my_win.lineEdit_coach.textChanged.connect(find_coach)

my_win.listWidget.itemDoubleClicked.connect(dclick_in_listwidget)

my_win.tabWidget.currentChanged.connect(page)
my_win.toolBox.currentChanged.connect(tab)

# =======  срабатывание кнопок =========
my_win.pushButton_add_player.clicked.connect(add_player)  # добавляет игроков в список и базу
# my_win.pushButton_db.clicked.connect(dbase)  # создание базы данных и таблиц
my_win.pushButton_titul_edit.setEnabled(False)  # выключает кнопку после создания титула
my_win.pushButton_Rlist.clicked.connect(fill_table_R_list)  # выбор и загрузка рейтинга

my_win.pushButton_titul_made.clicked.connect(titul_made)  # вызов окна диалога выбора изображения для вставки в титул
# my_win.pushButton_titul_edit.clicked.connect(db_select_titul)
my_win.pushButton_sort_R.clicked.connect(sort)
my_win.pushButton_sort_Name.clicked.connect(sort)
my_win.pushButton_export.clicked.connect(export)
my_win.pushButton_titul_edit.clicked.connect(titul_update)
my_win.pushButton_view.clicked.connect(handlePreview)

sys.exit(app.exec())
