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

from PyQt6 import QtCore, QtGui, QtWidgets, QtPrintSupport
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTextEdit, QVBoxLayout,\
    QDateEdit, QWidget, QPushButton, QHBoxLayout
from PyQt6.QtGui import *
from PyQt6.QtCore import pyqtSignal, QObject
from datetime import *
from main_window import Ui_MainWindow  # импортируем из модуля (графического интерфейса main_window) класс Ui_MainWindow
from fpdf import FPDF
from models import *
from csv import reader
import keyword

FPDF.SYSTEM_TTFONTS = '/library/fonts'
pdf = FPDF()


# Создаем собственный класс MainWindow, унаследованный от класса графического интерфейса Mainwindow
# и класса QMainWindow
class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None, *args, **kwargs):
        QMainWindow.__init__(self)
        self.setupUi(self)


def dbase():  # Создание DB и таблицы titul и заносит в нее название соревнования

    with db:
        db.create_tables([Titul, R_list])


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
        my_win.lineEdit_city.setText(tituls.mesto)
        my_win.lineEdit_refery.setText(tituls.referee)
        my_win.comboBox_kategor_ref.setCurrentText(tituls.kat_ref)
        my_win.lineEdit_sekretar.setText(tituls.secretary)
        my_win.comboBox_kategor_sek.setCurrentText(tituls.kat_sek)


def titul_made():

    age = my_win.lineEdit_titul_vozrast.text()
    p = age.count(" ")
    if p == 2:
        god = int(age[3:5])
        age = date.today().year - (god - 1)  # год рождения и младше могут играть
    elif p == 4:
        age = int(age[0:5])  # год рождения и младше могут играть
    global nm, vz, ds, de, ms, rf, kr, sk, ks
    nm = my_win.lineEdit_titul_nazvanie.text()
    vz = my_win.lineEdit_titul_vozrast.text()
    ds = my_win.dateEdit_start.text()
    de = my_win.dateEdit_end.text()
    ms = my_win.lineEdit_city.text()
    rf = my_win.lineEdit_refery.text()
    sk = my_win.lineEdit_sekretar.text()
    kr = my_win.comboBox_kategor_ref.currentText()
    ks = my_win.comboBox_kategor_sek.currentText()
    dbase()
    db_insert_titul()
    titul_pdf()
    my_win.pushButton_titul_made.setEnabled(0)  # после заполнения титула выключает кнопку
    my_win.pushButton_titul_edit.setEnabled(1)


# def titul_edit():
#     db_select_titul()


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


def find_in_rlist():
    fp = my_win.lineEdit_Find_Rlist.text()
    p = R_list.select()
    p = p.where(R_list.r_fname ** f'%{fp}%')  # like
    for pl in p:
        print((pl.r_fname, pl.r_list))
        my_win.textEdit.setText(pl.r_fname, pl.r_list)


def view():  #  просмотр PDF страницы

    pass


def db_r():  #  Загружает рейинг лист в базу данных

    fname = QFileDialog.getOpenFileName(my_win, "Выбрать файл R-листа", "", "Excels files (*.xlsx)")
    filepatch = str(fname[0])
    rp = filepatch.rindex("/")
    RPath = filepatch[rp + 1: len(filepatch)]
    wb = op.load_workbook(RPath)
    s = wb.sheetnames[0]
    sheet = wb[s]
    for r in range(2, 4500):
        if sheet.cell(row=r, column=2).value is None:
            break

    rows = r - 1
    data = []

    for i in range(2, rows):
        A = sheet['A%s' % i].value
        B = sheet['B%s' % i].value
        C = sheet['C%s' % i].value
        D = sheet['D%s' % i].value
        E = sheet['E%s' % i].value
        data.append([A, B, C, D, E])

    with db:
        R_list.insert_many(data).execute()


# def parse_file(fname="2021_04_m.csv"):
#     with open(fname) as f:
#         csv = reader(f, delimiter=';')
#         players_gen = (p for p in csv)
#
#         for p in players_gen:
#             # r_fname = get_player(p[2])
#             number = number(p[0])
#             r_list = r_list(p[1])
#             r_fname = r_fname(p[2])
#             b_bithday = b_bithday(p[3])
#             r_city = r_city(p[4])
#             R_list.create(number=number, r_list=r_list, r_fname=r_fname, b_bithday=b_bithday, r_city=r_city)


# def get_player(r_fname):
#     if r_fname not in r_csv:
#         r_csv[r_fname] = R_list.create(r_fname=r_fname)
#     return r_csv[r_fname]

    # r_csv = {}

app = QApplication(sys.argv)
my_win = MainWindow()
my_win.show()




def tab(tw):  # Изменяет вкладку tabWidget в зависимости
    #  от вкладки toolBox
    if tw == 0:
        db_select_titul()
    my_win.tabWidget.setCurrentIndex(tw)


my_win.toolBox.currentChanged.connect(tab)

def page(tb):  # Изменяет вкладку toolBox в зависимости
    # от вкладки tabWidget
    if tb == 0:
        db_select_titul()
    my_win.toolBox.setCurrentIndex(tb)

my_win.tabWidget.currentChanged.connect(page)


kategoria_list = ("2-я кат.", "1-я кат.", " ССВК")
my_win.comboBox_kategor_ref.addItems(kategoria_list)
my_win.comboBox_kategor_sek.addItems(kategoria_list)
mylist = ('мальчиков и девочек', 'юношей и девушек', 'мужчин и женщин')
my_win.comboBox_sredi.addItems(mylist)
my_win.dateEdit_start.setDate(date.today())  # ставит сегодняшнюю дату
my_win.dateEdit_end.setDate(date.today())
my_win.pushButton_titul_edit.setEnabled(1)


my_win.pushButton_find.clicked.connect(find_in_rlist)

my_win.pushButton_Rlist.clicked.connect(db_r)  #  выбор и загрузка рейтинга

my_win.pushButton_view.clicked.connect(db_r)
# Нажатие кнопки и вызов функции "On_click"
my_win.pushButton_titul_made.clicked.connect(titul_made)
# вызов окна диалога выбора изображения для вставки в титул
my_win.pushButton_titul_edit.clicked.connect(db_select_titul)

sys.exit(app.exec())
