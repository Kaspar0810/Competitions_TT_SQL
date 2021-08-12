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


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None, *args, **kwargs) -> object:
        QMainWindow.__init__(self)
        self.setupUi(self)

        self._createAction()
        self._createMenuBar()
        self._connectActions()

        self.menuBar()

        self.Button_title_made.setEnabled(False)

        self.tabWidget.setCurrentIndex(0)  # текущая страница

        # choice = Choice.get(Choice.id == 1)
        # choice_tbl = choice.posev_group
        # if choice_tbl > 0:
        #     self.tabWidget.setTabEnabled(2, True)  # выключает отдельные вкладки
        #     self.tabWidget.setTabEnabled(3, False)
        #     self.tabWidget.setTabEnabled(4, False)
        #     self.tabWidget.setTabEnabled(5, False)
        # else:
        # self.tabWidget.setTabEnabled(2, True)  # выключает отдельные вкладки
        # self.tabWidget.setTabEnabled(3, False)
        # self.tabWidget.setTabEnabled(4, False)
        # self.tabWidget.setTabEnabled(5, False)

        self.toolBox.setCurrentIndex(0)

    # ====== создание строки меню ===========
    def _createMenuBar(self):
        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)  # разрешает показ менюбара
        # меню Соревнования
        fileMenu = QMenu("Соревнования", self)  # основное
        menuBar.addMenu(fileMenu)

        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.systemAction)
        choice = fileMenu.addMenu("Жеребьевка")
        saveList = fileMenu.addMenu("Сохранить")
        fileMenu.addAction(self.exitAction)
        # меню Редактировать
        editMenu = menuBar.addMenu("Редактировать")  # основное
        #  создание подменю
        choice.addAction(self.choice_gr_Action)  # подменю группы
        choice.addAction(self.choice_pf_Action)  # подменю полуфиналы
        choice.addAction(self.choice_fin_Action)  # подменю финалы
        saveList.addAction(self.savelist_Action)
        ed_Menu = editMenu.addMenu("Редактор")
        ed_Menu.addAction(self.title_Action)
        ed_Menu.addAction(self.list_Action)
        ed_Menu.addAction(self.system_edit_Action)
        find_Menu = editMenu.addMenu("Поиск")
        find_Menu.addAction(self.find_r_Action)
        find_Menu.addAction(self.find_r1_Action)
        # меню Рейтинг
        rank_Menu = menuBar.addMenu("Рейтинг")  # основное
        rank_Menu.addAction(self.rAction)
        rank_Menu.addAction(self.r1Action)
        # меню помощь
        help_Menu = menuBar.addMenu("Помощь")  # основное
        # help_Menu.addAction(self.helpAction)

    #  создание действий меню
    def _createAction(self):
        self.newAction = QAction(self)
        self.helpAction = QAction(self)
        self.newAction.setText("Создать новые")
        self.systemAction = QAction("Система соревнований")
        self.exitAction = QAction("Выход")
        self.rAction = QAction("Текущий рейтинг")
        self.r1Action = QAction("Рейтинг за январь")
        self.title_Action = QAction("Титульный лист")  # подменю редактор
        self.list_Action = QAction("Список участников")
        self.system_edit_Action = QAction("Система соревнования")
        self.find_r_Action = QAction("Поиск в текущем рейтинге")  # подменю поиск
        self.find_r1_Action = QAction("Поиск в январском рейтинге")
        self.savelist_Action = QAction("Список")  # подменю сохранить
        self.choice_gr_Action = QAction("Группы")  # подменю жеребьевка -группы-
        self.choice_pf_Action = QAction("Полуфиналы")  # подменю жеребьевка -пполуфиналы-
        self.choice_fin_Action = QAction("Финалы")  # подменю жеребьевка -финалы-

    def _connectActions(self):
        # Connect File actions
        self.newAction.triggered.connect(self.newFile)
        self.systemAction.triggered.connect(self.system_made)
        self.system_edit_Action.triggered.connect(self.system_edit)
        self.exitAction.triggered.connect(self.exit)
        self.savelist_Action.triggered.connect(self.saveList)
        self.choice_gr_Action.triggered.connect(self.choice)
        # Connect Рейтинг actions
        self.rAction.triggered.connect(self.r_File)
        self.r1Action.triggered.connect(self.r1_File)
        # Connect Help actions
        self.helpAction.triggered.connect(self.help)

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

    def choice(self):
        t = Title.select().order_by(Title.id.desc()).get()  # получение id последнего соревнования
        system = System.select().order_by(System.id).where(System.title_id == t).get()  # находит system id последнего
        if system.choice_flag == True:
            reply = QMessageBox.information(my_win, 'Уведомление', "Жеребъевка была произведена,\nесли хотите сделать "
                                                                   "повторно\nнажмите-ОК-, если нет то - Cancel-",
                                            QMessageBox.StandardButtons.Ok,
                                            QMessageBox.StandardButtons.Cancel)
            if reply == QMessageBox.StandardButtons.Ok:
                my_win.tabWidget.setCurrentIndex(2)
                choice_gr_automat()
            else:
                return
        else:
            my_win.tabWidget.setCurrentIndex(2)
            choice_gr_automat()

    def system_made(self):
        system_competition()

    def system_edit(self):
        system_competition()

    def help(self):
        pass


app = QApplication(sys.argv)
my_win = MainWindow()
my_win.setWindowTitle("Соревнования по настольному теннису")
my_win.show()

#  ==== наполнение комбобоксов ==========
page_orient = ("альбомная", "книжная")
kategoria_list = ("2-я кат.", "1-я кат.", " ССВК")
mylist = ('мальчиков и девочек', 'юношей и девушек', 'мужчин и женщин')
raz = ("б/р", "3-юн", "2-юн", "1-юн", "3-р", "2-р", "1-р", "КМС", "МС", "МСМК", "ЗМС")
res = ("все игры", "завершенные", "не сыгранные")
stages1 = ("1 таблица", "Предварительный", "Полуфиналы", "Финальный", "Суперфинал")
stages2 = ("Полуфиналы", "Финальный", "Суперфинал")

my_win.comboBox_page_vid.addItems(page_orient)
my_win.comboBox_etap_1.addItems(stages1)
my_win.comboBox_etap_2.addItems(stages2)
my_win.comboBox_kategor_ref.addItems(kategoria_list)
my_win.comboBox_kategor_sek.addItems(kategoria_list)
my_win.comboBox_sredi.addItems(mylist)
my_win.comboBox_razryad.addItems(raz)
my_win.comboBox_filter_played.addItems(res)

# ставит сегодняшнюю дату в виджете календарь
my_win.dateEdit_start.setDate(date.today())
my_win.dateEdit_end.setDate(date.today())


def dbase():
    """Создание DB и таблиц"""
    with db:
        db.create_tables([Title, R_list, Region, City, Player, R1_list, Coach, System, Result, Game_list, Choice])
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


def system_edit():
    """редактирование системы"""
    pass
    system_made()

# def system_update(kg, stroka_kol_group):
#     """Обновляет таблицу система кол-во игроков, кол-во групп и прочее"""
#     sender = my_win.sender()  # сигнал от кнопки
#     ps = Player.select()
#     ta = len(ps)
#     e = int(ta) % int(kg)  # если количество участников не равно делится на группы
#     t = int(ta) // int(kg)  # если количество участников равно делится на группы
#     title = Title.select().order_by(Title.id.desc()).get()  # получение последней записи в таблице
#     if sender == my_win.Button_etap_made:
#         system = System.get(System.id == title.id)  # находит в базе запись в таблице -system- по данным соревнованиям
#         if e == 0:
#             system.max_player = t
#         else:
#             system.max_player = t + 1
#         system.total_athletes = ta
#         system.total_group = kg
#         system.stage = my_win.comboBox_etap_1.currentText()
#         system.page_vid = my_win.comboBox_page_vid.currentText()
#         system.label_string = stroka_kol_group
#     else:
#         pass
#     system.save()


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
    if sg == "1 таблица":
        pass
    else:  # предварительный этап
        for i in range(1, count_system + 1):
            system = System(id=cs, title_id=t, total_athletes=total_athletes, total_group=total_group,
                            max_player=max_player, stage=sg, page_vid=page_v, label_string="", kol_game_string="",
                            choice_flag=False, score_flag=False).save()
    player_in_table()
    my_win.checkBox_2.setChecked(False)
    my_win.checkBox_3.setChecked(False)
    my_win.Button_system_made.setEnabled(False)
    my_win.Button_1etap_made.setEnabled(False)
    my_win.Button_2etap_made.setEnabled(False)


def region():
    """добавляет из таблицы в комбобокс регионы"""
    if my_win.comboBox_region.currentIndex() > 0:  # проверка на заполненость комбокса данными
        return
    else:
        with db:
            for r in range(1, 86):
                reg = Region.get(Region.id == r)
                my_win.comboBox_region.addItem(reg.region)


def load_tableWidget():
    """Заполняет таблицу списком или рейтингом в зависимости от выбора"""
    sender = my_win.menuWidget().sender()  # сигнал указывающий какой пункт меню нажат
    if sender == my_win.rAction or sender == my_win.r1Action:  # нажат пункт меню -текущий рейтинг- или -рейтинг январский
        z = 6
        column_label = ["№", "Место", "  Рейтинг", "Фамилия Имя", "Дата рождения", "Город"]
    elif my_win.tabWidget.currentIndex() == 3:
        z = 14
        column_label = ["№", "Этапы", "Группа", "Встреча", "Игрок_1", "Игрок_2", "Победитель", "Очки", "Общий счет",
                        "Счет в партии", "Проигравший", "Очки", "Счет в партии", " title_id"]
    elif my_win.tabWidget.currentIndex() == 2 or sender == my_win.choice_gr_Action:
        z = 18
        column_label = ["№", "id", "Фамилия Имя", "Регион", "Тренер(ы)", "Рейтинг", "Основной", "Предварительный",
                        "Посев",
                        "Место в группе", "ПФ", "Посев в ПФ", "Место", "Финал", "Посев в финале", "Место", "Суперфинал"]
    else:
        z = 10
        column_label = ["№", "id", "Фамилия, Имя", "Дата рождения", "Рейтинг", "Город", "Регион", "Разряд",
                        "Тренер(ы)", "Место"]

    my_win.tableWidget.setColumnCount(z)
    my_win.tableWidget.setRowCount(1)
    my_win.tableWidget.verticalHeader().hide()
    for i in range(0, z):  # закрашивает заголовки таблиц  рейтинга зеленым цветом
        item = QtWidgets.QTableWidgetItem()
        item.setBackground(QtGui.QColor(0, 255, 150))
        my_win.tableWidget.setHorizontalHeaderItem(i, item)
    my_win.tableWidget.setHorizontalHeaderLabels(column_label)
    my_win.tableWidget.isSortingEnabled()
    my_win.tableWidget.show()
    if sender == my_win.rAction:  # нажат пункт меню -текущий рейтинг- и загружет таблицу с рейтингом
        fill_table_R_list()
    elif sender == my_win.r1Action:  # нажат пункт меню -рейтинг за январь- и загружет таблицу с рейтингом
        fill_table_R1_list()
    elif my_win.tabWidget.currentIndex() == 3:  # таблица результатов
        fill_table_results()
    elif my_win.tabWidget.currentIndex() == 2 or sender == my_win.choice_gr_Action:  # таблица жеребьевки
        fill_table_choice()
    else:  # загружает таблицу со списком
        player_list = Player.select().order_by(Player.rank.desc())
        fill_table(player_list)


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
        a = sheet['B%s' % i].value
        reg.append([a])
    with db:
        Region.insert_many(reg).execute()
    region()
    sb = "Список регионов загружен"
    sb.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
    my_win.statusbar.showMessage("Список регионов загружен", 5000)  # показывает статус бар на 5 секунд
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


def title_pdf():
    """сохранение в PDF формате титульной страницы"""
    string_data = pdf.data_title_string()
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
    t = Title.select().order_by(Title.id.desc()).get()  # получение последней записи в таблице
    sg = my_win.comboBox_etap_1.currentText()
    page_v = my_win.comboBox_page_1.currentText()
    with db:
        System.create_table()
        sys = System(title_id=t, total_athletes=0, total_group=0, max_player=0, stage=sg, page_vid=page_v,
                     label_string="", kol_game_string="", choice_flag=False, score_flag=False).save()


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


def fill_table(player_list=Player.select().order_by(Player.rank.desc())):
    """заполняет таблицу со списком участников QtableWidget спортсменами из db"""
    player_selected = player_list.dicts().execute()

    row_count = len(player_selected)  # кол-во строк в таблице
    column_count = len(player_selected[0])  # кол-во столбцов в таблице
    my_win.tableWidget.setRowCount(row_count)  # вставляет в таблицу необходимое кол-во строк

    for row in range(row_count):  # добвляет данные из базы в TableWidget
        for column in range(column_count):
            if column == 8:  # преобразует id тренера в фамилию
                coach_id = str(list(player_selected[row].values())[column])
                coach = Coach.get(Coach.id == coach_id)
                item = coach.coach
            else:
                item = str(list(player_selected[row].values())[column])
            my_win.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
    my_win.tableWidget.hideColumn(1)  # скрывает столбец id
    my_win.tableWidget.resizeColumnsToContents()  # ставит размер столбцов согласно записям

    for i in range(0, row_count):  # отсортировывает номера строк по порядку
        my_win.tableWidget.setItem(i, 0, QTableWidgetItem(str(i + 1)))


def fill_table_R_list():
    """заполняет таблицу списком из текущего рейтинг листа"""
    player_rlist = R_list.select().order_by(R_list.r_fname)
    player_r = player_rlist.dicts().execute()
    row_count = len(player_r)  # кол-во строк в таблице
    column_count = len(player_r[0])  # кол-во столбцов в таблице
    my_win.tableWidget.setRowCount(row_count)  # вставляет в таблицу необходимое кол-во строк

    for row in range(row_count):  # добвляет данные из базы в TableWidget
        for column in range(column_count):
            item = str(list(player_r[row].values())[column])
            my_win.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))

    my_win.tableWidget.resizeColumnsToContents()  # ставит размер столбцов согласно записям


def fill_table_R1_list():
    """заполняет таблицу списком из январского рейтинг листа"""
    player_rlist = R1_list.select().order_by(R1_list.r1_fname)
    player_r1 = player_rlist.dicts().execute()
    row_count = len(player_r1)  # кол-во строк в таблице
    column_count = len(player_r1[0])  # кол-во столбцов в таблице
    my_win.tableWidget.setRowCount(row_count)  # вставляет в таблицу необходимое кол-во строк

    for row in range(row_count):  # добвляет данные из базы в TableWidget
        for column in range(column_count):
            item = str(list(player_r1[row].values())[column])
            my_win.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))

    my_win.tableWidget.resizeColumnsToContents()  # ставит размер столбцов согласно записям


def fill_table_results():
    """заполняет таблицу результатов QtableWidget из db result"""
    result = Result.select()  # проверка есть ли записи в таблице -result-
    count = len(result)  # если 0, то записей нет
    flag = ready_system()
    if flag is True and count == 0:
        message = "Надо сделать жербъевку предварительного этапа.\nХотите ее создать?"
        reply = QtWidgets.QMessageBox.question(my_win, 'Уведомление', message,
                                               QtWidgets.QMessageBox.StandardButtons.Yes,
                                               QtWidgets.QMessageBox.StandardButtons.No)
        if reply == QtWidgets.QMessageBox.StandardButtons.Yes:
            choice_gr_automat()
        else:
            return

    elif flag is False and count == 0:
        message = "Сначала надо создать систему соревнований\nзатем произвести жербъевку.\n" \
                  "Хотите начать ее создавать?"
        reply = QtWidgets.QMessageBox.question(my_win, 'Уведомление', message,
                                               QtWidgets.QMessageBox.StandardButtons.Yes,
                                               QtWidgets.QMessageBox.StandardButtons.No)
        if reply == QtWidgets.QMessageBox.StandardButtons.Yes:
            system_competition()
        else:
            return
    else:
        player_result = Result.select().order_by(Result.id)
        result_list = player_result.dicts().execute()
        row_count = len(result_list)  # кол-во строк в таблице
        column_count = len(result_list[0])  # кол-во столбцов в таблице
        my_win.tableWidget.setRowCount(row_count)  # вставляет в таблицу необходимое кол-во строк

        for row in range(row_count):  # добвляет данные из базы в TableWidget
            for column in range(column_count):
                item = str(list(result_list[row].values())[column])
                my_win.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
        my_win.tableWidget.showColumn(6)  # поазывает столбец победитель
        my_win.tableWidget.hideColumn(11)
        my_win.tableWidget.hideColumn(12)
        my_win.tableWidget.hideColumn(13)
        my_win.tableWidget.resizeColumnsToContents()  # ставит размер столбцов согласно записям


def fill_table_choice():
    """заполняет таблицу жеребьевка QtableWidget из db choice"""
    player_choice = Choice.select().order_by(Choice.rank.desc())
    choice_list = player_choice.dicts().execute()
    row_count = len(choice_list)  # кол-во строк в таблице
    column_count = len(choice_list[0])  # кол-во столбцов в таблице
    my_win.tableWidget.setRowCount(row_count)  # вставляет в таблицу необходимое кол-во строк

    for row in range(row_count):  # добвляет данные из базы в TableWidget
        for column in range(column_count):
            item = str(list(choice_list[row].values())[column])
            my_win.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
    hide_show_columns()
    my_win.tableWidget.resizeColumnsToContents()  # ставит размер столбцов согласно записям
    for i in range(0, row_count):  # отсортировывает номера строк по порядку
        my_win.tableWidget.setItem(i, 0, QTableWidgetItem(str(i + 1)))


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


def load_combobox_filter_group():
    """заполняет комбобокс фильтр групп для таблицы результаты"""
    sender = my_win.menuWidget().sender()
    my_win.comboBox_filter_group.clear()
    my_win.comboBox_filter_choice.clear()
    t = Title.select().order_by(Title.id.desc()).get()  # получение id последнего соревнования
    system = System.select().order_by(System.id).where(System.title_id == t).get()  # находит system id последнего
    gr_txt = []
    kg = int(system.total_group)  # количество групп

    if sender == my_win.choice_gr_Action:
        my_win.comboBox_filter_choice.addItem("все группы")
        for i in range(1, kg + 1):
            txt = f"{i} группа"
            gr_txt.append(txt)
        my_win.comboBox_filter_choice.addItems(gr_txt)
    elif my_win.tabWidget.currentIndex() == 2 and my_win.radioButton_3.isCheckable():
        my_win.comboBox_filter_choice.addItem("все группы")
        for i in range(1, kg + 1):
            txt = f"{i} группа"
            gr_txt.append(txt)
        my_win.comboBox_filter_choice.addItems(gr_txt)
    elif my_win.tabWidget.currentIndex() == 3:
        my_win.comboBox_filter_group.addItem("все группы")
        for i in range(1, kg + 1):
            txt = f"{i} группа"
            gr_txt.append(txt)
        my_win.comboBox_filter_group.addItems(gr_txt)


def tab():
    """Изменяет вкладку tabWidget в зависимости от вкладки toolBox"""
    tw = my_win.tabWidget.currentIndex()
    my_win.toolBox.setCurrentIndex(tw)


def page():
    """Изменяет вкладку toolBox в зависимости от вкладки tabWidget"""
    msgBox = QMessageBox()
    tb = my_win.toolBox.currentIndex()
    if tb == 0:
        db_select_title()
        my_win.tableWidget.show()
    elif tb == 1:  # -список участников-
        region()
        load_tableWidget()
        my_win.tableWidget.show()
        my_win.statusbar.showMessage("Список участников соревнований", 5000)
    elif tb == 2:  # -система-
        player_list = Player.select()
        count = len(player_list)
        my_win.label_8.setText(f"Всего участников: {str(count)} человек")
        t = Title.select().order_by(Title.id.desc()).get()  # получение id последнего соревнования
        st = System.select().where(System.title_id == t)
        st_count = len(st)
        s = System.select().order_by(System.id).where(System.title_id == t).get()  # находит system id последнего
        # соревнования
        last_id = s.id
        tg = s.total_group
        my_win.label_9.hide()
        my_win.label_10.hide()
        my_win.label_11.hide()
        my_win.label_12.hide()
        my_win.label_15.hide()
        my_win.label_17.hide()
        my_win.label_19.hide()
        my_win.label_23.hide()
        my_win.label_27.hide()
        my_win.label_28.hide()
        my_win.label_29.hide()
        my_win.label_30.hide()
        my_win.label_31.hide()
        my_win.label_32.hide()
        my_win.comboBox_etap_1.hide()
        my_win.comboBox_etap_2.hide()
        my_win.comboBox_etap_3.hide()
        my_win.comboBox_etap_4.hide()
        my_win.comboBox_table_2.hide()
        my_win.spinBox_kol_group.hide()
        my_win.comboBox_table.hide()
        if tg == 0:  # система еще не создана
            result = msgBox.information(my_win, "", "Хотите создать систему соревнований?",
                                        msgBox.StandardButtons.Ok, msgBox.StandardButtons.Cancel)
            if result == msgBox.StandardButtons.Ok:
                my_win.statusbar.showMessage("Создание системы соревнования", 10000)
                choice_tbl_made()  # создание таблицы жеребьевка, заполняет db списком участников для жеребъевки
                my_win.label_10.show()
                my_win.comboBox_etap_1.show()
            else:
                return
        else:
            stage = []
            table = []
            game = []
            for i in range(last_id, st_count + 1):  # цикл по таблице -system-
                s = System.get(System.id == i)
                stage.append(s.stage)  # добавляет в список этап
                table.append(s.label_string)  # добавляет в список система
                game.append(s.kol_game_string)  # добавляет в список кол-во игр
            my_win.comboBox_table.hide()
            my_win.comboBox_page_vid.setEnabled(False)
            my_win.Button_etap_made.setEnabled(False)
            my_win.Button_system_made.setEnabled(False)
            my_win.label_9.setText(stage[0])
            my_win.label_12.setText(table[0])
            my_win.label_19.setText(game[0])
            my_win.label_23.setText(stage[1])
            my_win.label_28.setText(table[1])
            my_win.label_27.setText(game[1])
            my_win.label_9.show()
            my_win.label_12.show()
            my_win.label_19.show()
            my_win.label_23.show()
            my_win.label_28.show()
            my_win.label_27.show()

        load_tableWidget()
        load_combobox_filter_group()
        my_win.radioButton_3.setChecked(True)
    elif tb == 3:  # вкладка -групппы-
        t = Title.select().order_by(Title.id.desc()).get()  # получение id последнего соревнования
        sf = System.get(System.title_id == t)
        state_greb = sf.choice_flag
        if state_greb == False:
            result = msgBox.information(my_win, "", "Необходимо сделать жеребъевку\nпредварительного этапа.",
                                        msgBox.StandardButtons.Ok, msgBox.StandardButtons.Cancel)
            if result == msgBox.StandardButtons.Ok:
                # my_win.tabWidget.setCurrentIndex(2)
                choice_gr_automat()
                sf.choice_flag = True
                sf.save()
            else:
                return
        state = sf.score_flag  # флаг, показывающий записывать счет в партиях или нет
        if sf.score_flag == True:  # отмечает чекбокс в зависимости от значения в db -system-
            my_win.checkBox_4.setChecked(True)
        else:
            my_win.checkBox_4.setChecked(False)
        game_in_visible(state)  # скрывает или показывает поля ввода счета
        my_win.tableWidget.show()
        my_win.Button_Ok.setDisabled(True)
        my_win.radioButton_match_5.setChecked(True)
        load_combobox_filter_group()
        load_tableWidget()
        load_combo()
        my_win.label_16.hide()
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
    if sender == my_win.Button_sort_R:  # в зависимости от сигала кнопки идет сортировка
        player_list = Player.select().order_by(Player.rank.desc())  # сортировка по рейтингу
    else:
        player_list = Player.select().order_by(Player.player)  # сортировка по алфавиту
    fill_table(player_list)


def button_etap_made_enabled(state):
    """включает кнопку - создание таблиц - если отмечен чекбокс, защита от случайного нажатия"""
    if state == 2:
        my_win.tabWidget.setTabEnabled(2, True)
        pass
        # my_win.Button_etap_made.setEnabled(True)
        # my_win.Button_2etap_made.setEnabled(True)
        # my_win.spinBox_kol_group.show()
    else:
        pass
        # my_win.Button_1etap_made.setEnabled(False)
        # my_win.Button_2etap_made.setEnabled(False)
        # my_win.spinBox_kol_group.hide()


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


def button_system_made_enable(state):
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
              rowHeights=None)  # ширина столбцов, если None-автомтическая
    t.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), "DejaVuSerif"),  # Использую импортированный шрифт
                           ('FONTSIZE', (0, 0), (-1, -1), 7),  # Использую импортированный шрифта размер
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 1),  # межстрочный верхний инервал
                           ('TOPPADDING', (0, 0), (-1, -1), 1),  # межстрочный нижний инервал
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # вериткальное выравнивание в ячейке заголовка
                           ('ALIGN', (0, 0), (-1, kp * -1), 'CENTER'),  # горизонтальное выравнивание в ячейке
                           ('BACKGROUND', (0, 0), (-1, kp * -1), colors.yellow),
                           ('TEXTCOLOR', (0, 0), (-1, kp * -1), colors.darkblue),
                           ('LINEABOVE', (0, 0), (-1, kp * -1), 1, colors.blue),
                           ('INNERGRID', (0, 0), (-1, -1), 0.05, colors.black),  # цвет и толщину внутренних линий
                           ('BOX', (0, 0), (-1, -1), 0.5, colors.black)  # внешние границы таблицы
                           ]))

    h3 = PS("normal", fontSize=12, fontName="DejaVuSerif-Italic", leftIndent=150,
            firstLineIndent=-20)  # стиль параграфа
    h3.spaceAfter = 10  # промежуток после заголовка
    story.append(Paragraph('Список участников', h3))
    story.append(t)

    doc = SimpleDocTemplate("table_list.pdf", pagesize=A4)
    doc.build(story, onFirstPage=comp_system.func_zagolovok, onLaterPages=comp_system.func_zagolovok)


def exit_comp():
    pass
    print("хотите выйти")


def system_competition():
    """выбор системы проведения"""
    sender = my_win.sender()
    msgBox = QMessageBox
    t = Title.select().order_by(Title.id.desc()).get()  # получение последней записи в таблице
    s = System.select().where(System.title_id == t)
    system = System.select().order_by(System.id).where(System.title_id == t).get()  # находит system id первого
    count = len(s)
    # total_player = system.total_athletes
    if sender == my_win.systemAction or sender == my_win.choice_gr_Action or sender == my_win.tabWidget\
            or sender == my_win.toolBox or sender == my_win.system_edit_Action:
        # нажат меню -система- или -жеребъевка- или вкладка -система-
        if sender == my_win.system_edit_Action:
            # result = msgBox.information(my_win, "", "Хотите изменить систему соревнований?",
            #                             msgBox.StandardButtons.Ok, msgBox.StandardButtons.Cancel)
            # if result == msgBox.StandardButtons.Ok:
            sb = "Изменение системы проведения соревнования."
            my_win.statusbar.showMessage(sb)
            clear_db_before_edit()  # очищает таблицы перед новой системой соревнования (system, choice)
            my_win.spinBox_kol_group.hide()
            my_win.comboBox_etap_1.setEnabled(True)
            my_win.comboBox_etap_2.setEnabled(True)
            my_win.comboBox_etap_3.setEnabled(True)
            my_win.comboBox_etap_1.show()
            my_win.comboBox_etap_1.setCurrentText("1 таблица")
            my_win.comboBox_etap_2.hide()
            my_win.comboBox_etap_3.hide()
            my_win.comboBox_etap_4.hide()
            my_win.label_10.hide()
            my_win.label_15.hide()
            my_win.label_17.hide()
            my_win.label_23.hide()
            my_win.label_27.hide()
            my_win.label_28.hide()
            my_win.label_29.hide()
            my_win.label_30.hide()
            my_win.label_31.hide()
            my_win.label_32.hide()
            my_win.comboBox_table.hide()
            my_win.comboBox_table_2.hide()
            choice_tbl_made()  # заполнение db списком для жеребъевки
            my_win.tabWidget.setCurrentIndex(2)
            # else:
            #     return
        elif count > 0:  # система была создана
            sb = "Система создана, теперь необходимо произвести жеребъевку. " \
                 "Войдите в меню -соревнования- и выберите -жеребъевка-"
            my_win.statusbar.showMessage(sb)
        elif count == 0:
            sb = "Выбор системы проведения соревнования."
            my_win.statusbar.showMessage(sb)
            my_win.spinBox_kol_group.hide()
            my_win.comboBox_etap_1.setEnabled(True)
            my_win.comboBox_etap_2.setEnabled(True)
            my_win.comboBox_etap_3.setEnabled(True)
            my_win.comboBox_etap_1.show()
            my_win.comboBox_etap_1.setCurrentText("1 таблица")
            my_win.comboBox_etap_2.hide()
            my_win.comboBox_etap_3.hide()
            my_win.label_10.hide()
            my_win.label_15.hide()
            my_win.label_17.hide()
            my_win.label_23.hide()
            my_win.label_27.hide()
            my_win.label_28.hide()
            my_win.comboBox_table.hide()
            choice_tbl_made()  # заполнение db списком для жеребъевки
            my_win.tabWidget.setCurrentIndex(2)
    elif sender == my_win.tabWidget:
        my_win.spinBox_kol_group.hide()
        my_win.comboBox_etap_1.setEnabled(True)
        my_win.comboBox_etap_2.setEnabled(True)
        my_win.comboBox_etap_3.setEnabled(True)
        my_win.comboBox_etap_1.show()
        my_win.comboBox_etap_1.setCurrentText("1 таблица")
        my_win.comboBox_etap_2.hide()
        my_win.comboBox_etap_3.hide()
        my_win.label_10.show()
        my_win.label_15.hide()
        my_win.label_17.hide()
    elif sender == my_win.comboBox_etap_1:
        ct = my_win.comboBox_etap_1.currentText()
        if ct == "1 таблица":
            my_win.spinBox_kol_group.hide()
            my_win.label_11.hide()
        elif ct == "Предварительный":
            my_win.spinBox_kol_group.show()
            my_win.label_9.show()
            my_win.label_9.setText("Предварительный этап")
            my_win.label_11.show()
            my_win.label_12.hide()
            my_win.comboBox_page_vid.setEnabled(True)
    elif sender == my_win.comboBox_etap_2:
        ct = my_win.comboBox_etap_2.currentText()
        if ct == "Полуфиналы":
            my_win.label_23.setText("Полуфиналы")
        elif ct == "Финальный":
            my_win.label_23.setText("Финальный этап")
        my_win.label_23.show()
        my_win.label_27.hide()
        my_win.label_28.hide()
        vid_setki = ("Сетка (-2)", "Сетка (с розыгрышем всех мест)", "Сетка (за 1-3 место)", "Круговая система")
        my_win.comboBox_table.addItems(vid_setki)
        my_win.comboBox_table.show()
        kpt, ok = QInputDialog.getInt(my_win, "Число участников", "Введите число участников,\nвыходящих "
                                                                  "из группы в 1-й финал")
        str_setka = total_game_table(kpt)
        if ok:
            my_win.label_28.show()
            my_win.label_28.setText(str_setka)
            # total_game_table(str_setka)
        #     # if total_player - player_in_final == 0:
        #     #     my_win.statusbar("Система создана.", 5000)
        #     # else:
        #         # my_win.comboBox_etap_3.show()
        # else:
        #     return
        my_win.comboBox_table.hide()
        my_win.Button_etap_made.setEnabled(True)
        my_win.comboBox_page_vid.setEnabled(True)
    else:  # скрывает и выключает label и combobox этапов систем
        my_win.label_10.hide()
        my_win.label_15.hide()
        my_win.label_17.hide()
        my_win.comboBox_etap_1.setEnabled(False)
        my_win.comboBox_etap_2.setEnabled(False)
        my_win.comboBox_etap_3.setEnabled(False)


def kol_player_in_group():
    """подсчет кол-во групп и человек в группах"""
    sender = my_win.sender()  # сигнал от кнопки
    kg = my_win.spinBox_kol_group.text()  # количество групп
    player_list = Player.select()
    count = len(player_list)  # колличество записей в базе
    e1 = int(count) % int(kg)  # остаток отделения, если 0, то участники равно делится на группы
    p = int(count) // int(kg)  # если количество участников равно делится на группы (кол-во групп)
    g1 = int(kg) - e1  # кол-во групп, где наименьшее кол-во спортсменов
    p2 = str(p + 1)  # кол-во человек в группе с наибольшим их количеством
    if e1 == 0:  # то в группах равное количесто человек -e1-
        stroka_kol_group = f"{kg} группы по {str(p)} чел."
        skg = int((p * (p - 1) / 2) * int(kg))
        mp = p
    else:
        stroka_kol_group = f"{str(g1)} групп(а) по {str(p)} чел. и {str(e1)} групп(а) по {str(p2)} чел."
        p = int(p)
        skg = int((((p * (p - 1)) / 2 * g1) + ((p * (p - 1)) / 2 * e1)))
        mp = p2
    stroka_kol_game = f"{skg} игр"

    my_win.label_12.setText(stroka_kol_group)
    my_win.label_12.show()
    my_win.label_19.setText(stroka_kol_game)
    my_win.label_19.show()
    my_win.Button_etap_made.setEnabled(True)
    if sender == my_win.Button_etap_made:
        my_win.label_11.show()
        my_win.label_11.setText(f"{kg} групп:")
        my_win.Button_etap_made.setEnabled(False)
        my_win.comboBox_page_vid.setEnabled(False)
        my_win.spinBox_kol_group.hide()
        my_win.comboBox_etap_2.setVisible(True)
        my_win.label_15.show()
# ====== запись в таблицу db -system- первый этап
        s = System.select().order_by(System.id.desc()).get()
        system = System.get(System.id == s)
        system.max_player = mp
        system.total_athletes = count
        system.total_group = kg
        system.stage = my_win.comboBox_etap_1.currentText()
        system.page_vid = my_win.comboBox_page_vid.currentText()
        system.label_string = stroka_kol_group
        system.kol_game_string = stroka_kol_game
        system.save()
    load_combobox_filter_group()


# def kol_game_in_table_or_setka(kpt):
#     """подсчитывает кол-во игр в группах, сетке"""
#     t = Title.select().order_by(Title.id.desc()).get()  # получение последней записи в таблице
#     s = System.select().order_by(System.id).where(System.title_id == t).get()  # находит system id последнего
#     player_in_final = s.total_group * kpt
#     if my_win.comboBox_table.currentIndex() == 0:
#         vt = "Сетка (-2) на"
#     elif my_win.comboBox_table.currentIndex() == 1:
#         vt = "Чистая сетка (с розыгрышем всех мест) на"
#     elif my_win.comboBox_table.currentIndex() == 2:
#         vt = "Чистая сетка (с играми за 1 - 3 места) на"
#     elif my_win.comboBox_table.currentIndex() == 3:
#         vt = "Круговая таблица на"
#     stroka_setka = f"{vt} {player_in_final} участников"


def page_vid():
    """присваивает переменной значение выборат вида страницы"""
    # t = Title.select().order_by(Title.id.desc()).get()  # получение id последнего соревнования
    # s = System.select().order_by(System.id).where(System.title_id == t).get()  # находит system id последнего
    # pv = s.page_vid
    if my_win.comboBox_page_vid.currentText() == "альбомная":
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
        view_file = "table_group.pdf"
    elif tw == 4:
        pass
    elif tw == 5:
        pass
    os.system(f"open {view_file}")


def player_in_table():
    """заполняет таблицу Game_list данными спортсменами из группы tdt - список списков данных из групп"""
    t = Title.select().order_by(Title.id.desc()).get()  # получение id последнего соревнования
    s = System.select().order_by(System.id).where(System.title_id == t).get()  # находит system id последнего
    kg = s.total_group
    ct = s.max_player
    st = s.stage
    pv = s.page_vid

    comp_system.table_made(pv)
    tdt = tbl_data.total_data_table(kg)

    for p in range(0, kg):
        gr = tdt[p]
        number_group = str(p + 1) + ' группа'
        k = 0
        for i in range(0, ct * 2 - 1, 2):
            family_player = gr[i][1]  # фамилия игрока
            fp = len(family_player)
            if fp > 0:  # если строка (фамилия игрока) не пустая идет запсь в db
                k += 1
                with db:
                    game_list = Game_list(number_group=number_group, rank_num_player=k, player_group=family_player,
                                          system_id=s).save()
            elif fp == 0 and k == 0:  # если 1-я строка (фамилия игрока) пустая выход из группы
                break
        if fp == 0 or ct == k:  # после считывания игроков в группе идет запись игроков по турам в таблицу -result-
            cp = k - 3
            tour = comp_system.tour(cp)
            game = k // 2  # кол-во игр в туре
            if game == 1:
                kk = k
            else:
                kk = k - 1
            for r in range(0, kk):
                tours = tour[r]  # игры тура
                for d in range(0, game):
                    if game == 1:  # если в группе 3 человека
                        match = tours  # матч в туре
                    elif game == 2:  # если в группе 4 человека
                        match = tours[d]  # матч в туре
                    elif game == 3:  # если в группе 5 человека
                        match = tours[d]  # матч в туре
                    elif game == 4:  # если в группе 6 человека
                        match = tours[d]  # матч в туре
                    first = int(match[0])  # игрок под номером в группе
                    second = int(match[2])  # игрок под номером в группе
                    pl1 = gr[first * 2 - 2][1]  # фамилия первого игрока
                    pl2 = gr[second * 2 - 2][1]  # фамилия второго игрока

                    with db:
                        # Result.create_table()
                        results = Result(number_group=number_group, system_stage=st, player1=pl1, player2=pl2,
                                         tours=match, title_id=s).save()
        else:
            pass
            print("ok")


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


def game_in_visible(state):
    """видимость полей для счета в партии"""
    t = Title.select().order_by(Title.id.desc()).get()  # получение id последнего соревнования
    # sys = System.select().order_by(System.id).where(System.title_id == t).get()  # находит system id последнего
    if state is True or state == 2:  # поставлена галочка
        my_win.lineEdit_pl1_s1.setVisible(True)
        my_win.lineEdit_pl2_s1.setVisible(True)
        my_win.lineEdit_pl1_s2.setVisible(True)
        my_win.lineEdit_pl2_s2.setVisible(True)
        my_win.lineEdit_pl1_s3.setVisible(True)
        my_win.lineEdit_pl2_s3.setVisible(True)
        my_win.lineEdit_pl1_s4.setVisible(True)
        my_win.lineEdit_pl2_s4.setVisible(True)
        my_win.lineEdit_pl1_s5.setVisible(True)
        my_win.lineEdit_pl2_s5.setVisible(True)
        my_win.label_22.setVisible(True)
        sf = System.get(System.title_id == t)
        with db:
            sf.score_flag = True
            sf.save()
    else:
        my_win.lineEdit_pl1_s1.setVisible(False)
        my_win.lineEdit_pl2_s1.setVisible(False)
        my_win.lineEdit_pl1_s2.setVisible(False)
        my_win.lineEdit_pl2_s2.setVisible(False)
        my_win.lineEdit_pl1_s3.setVisible(False)
        my_win.lineEdit_pl2_s3.setVisible(False)
        my_win.lineEdit_pl1_s4.setVisible(False)
        my_win.lineEdit_pl2_s4.setVisible(False)
        my_win.lineEdit_pl1_s5.setVisible(False)
        my_win.lineEdit_pl2_s5.setVisible(False)
        my_win.label_22.setVisible(False)
        sf = System.get(System.title_id == t)
        with db:
            sf.score_flag = False
            sf.save()


def select_player_in_game():
    """выодит фамилии игроков встречи"""
    r = my_win.tableWidget.currentRow()
    win_pole = my_win.tableWidget.item(r, 6).text()
    if win_pole != "None" and win_pole != "":  # если встреча сыграна, то заполняет поля общий счет
        sc = my_win.tableWidget.item(r, 8).text()
        pl1 = my_win.tableWidget.item(r, 4).text()
        pl2 = my_win.tableWidget.item(r, 5).text()
        if Result.score_win != "" & Result.score_win != "None":  # если игры со счетом, от при редакитровании открывать поля
            my_win.lineEdit_pl1_s1.setVisible(True)
            my_win.lineEdit_pl2_s1.setVisible(True)
            my_win.lineEdit_pl1_s2.setVisible(True)
            my_win.lineEdit_pl2_s2.setVisible(True)
            my_win.lineEdit_pl1_s3.setVisible(True)
            my_win.lineEdit_pl2_s3.setVisible(True)
            my_win.lineEdit_pl1_s4.setVisible(True)
            my_win.lineEdit_pl2_s4.setVisible(True)
            my_win.lineEdit_pl1_s5.setVisible(True)
            my_win.lineEdit_pl2_s5.setVisible(True)

        if pl1 == my_win.tableWidget.item(r, 6).text():
            sc1 = sc[0]
            sc2 = sc[4]
        else:
            sc1 = sc[4]
            sc2 = sc[0]
        my_win.lineEdit_pl1_score_total.setText(sc1)
        my_win.lineEdit_pl2_score_total.setText(sc2)
        my_win.lineEdit_player1.setText(pl1)
        my_win.lineEdit_player2.setText(pl2)
        my_win.lineEdit_pl1_s1.setFocus()
    else:
        pl1 = my_win.tableWidget.item(r, 4).text()
        pl2 = my_win.tableWidget.item(r, 5).text()
        my_win.lineEdit_player1.setText(pl1)
        my_win.lineEdit_player2.setText(pl2)
        my_win.lineEdit_pl1_s1.setFocus()
    my_win.tableWidget.selectRow(r)


def focus():
    """перводит фокус на следующую позицию"""
    sender = my_win.sender()  # в зависимости от сигала кнопки идет сортировка
    if sender == my_win.lineEdit_pl1_s1:
        my_win.lineEdit_pl2_s1.setFocus()  # ставит фокус на 2-ого игрока 1-й партии
    elif sender == my_win.lineEdit_pl2_s1:  # подсчитвает общий счет и ставит фокус на 1-ого игрока 2-й партии
        score_in_game()
        my_win.lineEdit_pl1_s2.setFocus()
    elif sender == my_win.lineEdit_pl1_s2:
        my_win.lineEdit_pl2_s2.setFocus()  # ставит фокус на 2-ого игрока 2-й партии
    elif sender == my_win.lineEdit_pl2_s2:  # подсчитвает общий счет и ставит фокус на 1-ого игрока 3-й партии
        score_in_game()
        my_win.lineEdit_pl1_s3.setFocus()
    elif sender == my_win.lineEdit_pl1_s3:
        my_win.lineEdit_pl2_s3.setFocus()  # ставит фокус на 2-ого игрока 3-й партии
    elif sender == my_win.lineEdit_pl2_s3:  # подсчитвает общий счет и ставит фокус на 1-ого игрока 4-й партии
        score_in_game()
        my_win.lineEdit_pl1_s4.setFocus()
    elif sender == my_win.lineEdit_pl1_s4:
        my_win.lineEdit_pl2_s4.setFocus()  # ставит фокус на 2-ого игрока 4-й партии
    elif sender == my_win.lineEdit_pl2_s4:  # подсчитвает общий счет и ставит фокус на 1-ого игрока 5-й партии
        score_in_game()
        my_win.lineEdit_pl1_s5.setFocus()
    elif sender == my_win.lineEdit_pl1_s5:
        my_win.lineEdit_pl2_s5.setFocus()  # ставит фокус на 2-ого игрока 5-й партии
    elif sender == my_win.lineEdit_pl2_s5:  # подсчитвает общий счет и ставит фокус на 1-ого игрока 5-й партии
        score_in_game()
        my_win.Button_Ok.setFocus()


def score_in_game():
    """считает общий счет в партиях"""

    def setfocus():
        """если один игрок уже выйграл, то переводит фокус на кнопку ОК"""
        if st1 == 3 or st2 == 3:
            my_win.Button_Ok.setEnabled(True)
            return

    # поля ввода счета в партии
    s11 = my_win.lineEdit_pl1_s1.text()
    s21 = my_win.lineEdit_pl2_s1.text()
    s12 = my_win.lineEdit_pl1_s2.text()
    s22 = my_win.lineEdit_pl2_s2.text()
    s13 = my_win.lineEdit_pl1_s3.text()
    s23 = my_win.lineEdit_pl2_s3.text()
    s14 = my_win.lineEdit_pl1_s4.text()
    s24 = my_win.lineEdit_pl2_s4.text()
    s15 = my_win.lineEdit_pl1_s5.text()
    s25 = my_win.lineEdit_pl2_s5.text()

    if int(s11) > int(s21):
        st1 = 1
        st2 = 0
    else:
        st1 = 0
        st2 = 1
    if s12 == "":
        pass
    else:  # 2-я игра
        if int(s12) > int(s22):
            st1 = int(st1) + 1
        else:
            st2 = int(st2) + 1
        if s13 == "":
            pass
        else:  # 3-я игра
            if int(s13) > int(s23):
                st1 = int(st1) + 1
            else:
                st2 = int(st2) + 1
            setfocus()
            if s14 == "":
                pass
            else:  # 4-я игра
                if int(s14) > int(s24):
                    st1 = int(st1) + 1
                else:
                    st2 = int(st2) + 1
                setfocus()
                if s15 == "":
                    pass
                else:  # 5-я игра
                    if int(s15) > int(s25):
                        st1 = int(st1) + 1
                    else:
                        st2 = int(st2) + 1
                    setfocus()

    my_win.lineEdit_pl1_score_total.setText(str(st1))
    my_win.lineEdit_pl2_score_total.setText(str(st2))


def enter_score():
    """заносит в таблицу -результаты- победителя, счет и т.п."""
    st1 = int(my_win.lineEdit_pl1_score_total.text())
    st2 = int(my_win.lineEdit_pl2_score_total.text())

    r = my_win.tableWidget.currentRow()
    id = my_win.tableWidget.item(r, 0).text()
    if st1 > st2:
        winner = my_win.lineEdit_player1.text()
        my_win.tableWidget.item(r, 6).setForeground(QBrush(QColor(255, 0, 0)))  # окрашивает текст в красный цвет
        loser = my_win.lineEdit_player2.text()
        ts_winner = f"{st1} : {st2}"
        ts_loser = f"{st2} : {st1}"
    else:
        winner = my_win.lineEdit_player2.text()
        my_win.tableWidget.item(r, 7).setForeground(QBrush(QColor(255, 0, 0)))  # окрашивает текст в красный цвет
        loser = my_win.lineEdit_player1.text()
        ts_winner = f"{st2} : {st1}"
        ts_loser = f"{st1} : {st2}"
    winner_string = string_score_game()
    with db:
        result = Result.get(Result.id == id)
        result.winner = winner
        result.points_win = "2"
        result.score_win = winner_string
        result.score_in_game = ts_winner
        result.loser = loser
        result.points_loser = "1"
        result.score_loser = ts_loser
        result.save()
    fill_table_results()

    my_win.lineEdit_pl1_s1.setText("")  # очищает поля ввода счета в партии
    my_win.lineEdit_pl2_s1.setText("")
    my_win.lineEdit_pl1_s2.setText("")
    my_win.lineEdit_pl2_s2.setText("")
    my_win.lineEdit_pl1_s3.setText("")
    my_win.lineEdit_pl2_s3.setText("")
    my_win.lineEdit_pl1_s4.setText("")
    my_win.lineEdit_pl2_s4.setText("")
    my_win.lineEdit_pl1_s5.setText("")
    my_win.lineEdit_pl2_s5.setText("")

    my_win.lineEdit_pl1_score_total.setText("")  # очищает поля общего счета
    my_win.lineEdit_pl2_score_total.setText("")

    my_win.lineEdit_player1.setText("")  # очищает поля фамилии игроков
    my_win.lineEdit_player2.setText("")
    # ===== вызов функции заполнения таблицы pdf группы сыгранными играми
    pv = landscape(A4)
    comp_system.table_made(pv)


def string_score_game():
    """создает строку со счетом победителя"""
    if my_win.radioButton_match_3.isChecked():  # зависимости от кол-во партий
        g = 2
    elif my_win.radioButton_match_5.isChecked():
        g = 3
    else:
        g = 4
    # поля ввода счета в партии
    st1 = int(my_win.lineEdit_pl1_score_total.text())
    st2 = int(my_win.lineEdit_pl2_score_total.text())
    s11 = my_win.lineEdit_pl1_s1.text()
    s21 = my_win.lineEdit_pl2_s1.text()
    s12 = my_win.lineEdit_pl1_s2.text()
    s22 = my_win.lineEdit_pl2_s2.text()
    s13 = my_win.lineEdit_pl1_s3.text()
    s23 = my_win.lineEdit_pl2_s3.text()
    s14 = my_win.lineEdit_pl1_s4.text()
    s24 = my_win.lineEdit_pl2_s4.text()
    s15 = my_win.lineEdit_pl1_s5.text()
    s25 = my_win.lineEdit_pl2_s5.text()
    # создание строки счета победителя
    if st1 > st2:
        if int(s11) > int(s21):  # 1-й сет
            n1 = s21
        else:
            n1 = str(f"-{s11}")
        if int(s12) > int(s22):  # 2-й сет
            n2 = s22
        else:
            n2 = str(f"-{s12}")
        if (g == 2 and st1 == 2 and st2 == 0) or (g == 2 and st2 == 0 and st2 == 2):  # из 3-х партий 2-0
            winner_string = f"({n1},{n2})"
            return winner_string
        if int(s13) > int(s23):  # 3-й сет
            n3 = s23
        else:
            n3 = str(f"-{s13}")
        if (g == 2 and st1 == 2 and st2 == 1) or (g == 2 and st2 == 2 and st1 == 1) or \
                (g == 3 and st1 == 3 and st2 == 0) or (g == 3 and st1 == 0 and st2 == 3):  # из 3-х  2-1 или из 5-и 3-0
            winner_string = f"({n1},{n2},{n3})"
            return winner_string
        if int(s14) > int(s24):  # 4-й сет
            n4 = s24
        else:
            n4 = str(f"-{s14}")
        if (g == 4 and st1 == 4 and st2 == 0) or (g == 4 and st1 == 0 and st2 == 4) or \
                (g == 3 and st1 == 3 and st2 == 1) or (g == 3 and st1 == 1 and st2 == 3):  # из 5-и 3-1 или из 7-и 4-0
            winner_string = f"({n1},{n2},{n3},{n4})"
            return winner_string
        if int(s15) > int(s25):  # 5-й сет
            n5 = s25
        else:
            n5 = str(f"-{s15}")
        if (g == 4 and st1 == 4 and st2 == 1) or (g == 4 and st1 == 1 and st2 == 4) or \
                (g == 3 and st1 == 3 and st2 == 2) or (g == 3 and st1 == 2 and st2 == 3):  # из 5-и 3-2 или из 7-и 4-1
            winner_string = f"({n1},{n2},{n3},{n4},{n5})"
            return winner_string

    else:
        if int(s11) < int(s21):  # 1-й сет
            n1 = s11
        else:
            n1 = str(f"-{s12}")
        if int(s12) < int(s22):  # 2-й сет
            n2 = s12
        else:
            n2 = str(f"-{s22}")
        if (g == 2 and st1 == 2 and st2 == 0) or (g == 2 and st2 == 0 and st2 == 2):  # из 3-х партий 2-0
            winner_string = f"({n1},{n2})"
            return winner_string
        if int(s13) < int(s23):  # 3-й сет
            n3 = s13
        else:
            n3 = str(f"-{s23}")
        if (g == 2 and st1 == 2 and st2 == 1) or (g == 2 and st2 == 2 and st1 == 1) or \
                (g == 3 and st1 == 3 and st2 == 0) or (g == 3 and st1 == 0 and st2 == 3):  # из 3-х  2-1 или из 5-и 3-0
            winner_string = f"({n1},{n2},{n3})"
            return winner_string
        if int(s14) < int(s24):  # 4-й сет
            n4 = s14
        else:
            n4 = str(f"-{s24}")
        if (g == 4 and st1 == 4 and st2 == 0) or (g == 4 and st1 == 0 and st2 == 4) or \
                (g == 3 and st1 == 3 and st2 == 1) or (g == 3 and st1 == 1 and st2 == 3):  # из 5-и 3-1 или из 7-и 4-0
            winner_string = f"({n1},{n2},{n3},{n4})"
            return winner_string
        if int(s15) < int(s25):  # 5-й сет
            n5 = s15
        else:
            n5 = str(f"-{s25}")
        if (g == 4 and st1 == 4 and st2 == 1) or (g == 4 and st1 == 1 and st2 == 4) or \
                (g == 3 and st1 == 3 and st2 == 2) or (g == 3 and st1 == 2 and st2 == 3):  # из 5-и 3-2 или из 7-и 4-1
            winner_string = f"({n1},{n2},{n3},{n4},{n5})"
            return winner_string


def result_filter_group():
    """фильтрует таблицу -результаты- по группам"""
    fg = my_win.comboBox_filter_group.currentText()
    player_result = Result.select().where(Result.number_group == fg)
    result_list = player_result.dicts().execute()
    row_count = len(result_list)  # кол-во строк в таблице
    column_count = 13  # кол-во столбцов в таблице
    my_win.tableWidget.setRowCount(row_count)  # вставляет в таблицу необходимое кол-во строк

    for row in range(row_count):  # добвляет данные из базы в TableWidget
        for column in range(column_count):
            item = str(list(result_list[row].values())[column])
            my_win.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))

    my_win.tableWidget.hideColumn(11)
    my_win.tableWidget.hideColumn(12)
    my_win.tableWidget.hideColumn(13)
    my_win.tableWidget.resizeColumnsToContents()  # ставит размер столбцов согласно записям
    for d in range(0, row_count):  # сортирует нумерация по порядку
        my_win.tableWidget.setItem(d, 0, QTableWidgetItem(str(d + 1)))


def result_filter_played():
    pass
    # """фильтрует таблицу -результаты- по сыгранным встречам"""
    # sender = my_win.sender()
    # fplayed = my_win.comboBox_filter_played.currentText()
    # if sender == my_win.Button_reset_filter:
    #     my_win.comboBox_filter_played.setCurrentText("все игры")
    #     fplayed = "все игры"
    # if fplayed == "не сыгранные":
    #     sg = "осталось сыграть:"
    #     player_result = Result.select().where(Result.points_win == None)
    # elif fplayed == "завершенные":
    #     player_result = Result.select().where(Result.points_win >= 0)
    #     sg = "всего сыграно:"
    # else:
    #     player_result = Result.select()
    #     sg = "всего игр:"
    # result_list = player_result.dicts().execute()
    # row_count = len(result_list)  # кол-во строк в таблице
    # my_win.label_16.setText(f"{sg} {row_count}")
    # column_count = 13  # кол-во столбцов в таблице
    # my_win.tableWidget.setRowCount(row_count)  # вставляет в таблицу необходимое кол-во строк
    #
    # for row in range(row_count):  # добвляет данные из базы в TableWidget
    #     for column in range(column_count):
    #         item = str(list(result_list[row].values())[column])
    #         my_win.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
    #
    # my_win.tableWidget.hideColumn(10)
    # my_win.tableWidget.hideColumn(11)
    # my_win.tableWidget.hideColumn(12)
    # my_win.tableWidget.hideColumn(13)
    # my_win.tableWidget.resizeColumnsToContents()  # ставит размер столбцов согласно записям


def result_filter_name():
    """отсортировает встречи с участие игрока"""
    cp = my_win.comboBox_find_name.currentText()
    cp = cp.title()  # Переводит первую букву в заглавную
    c = Result.select()
    c = c.where(Result.player1 ** f'{cp}%')  # like
    result_list = c.dicts().execute()
    row_count = len(result_list)  # кол-во строк в таблице
    column_count = 13  # кол-во столбцов в таблице
    my_win.tableWidget.setRowCount(row_count)  # вставляет в таблицу необходимое кол-во строк

    for row in range(row_count):  # добвляет данные из базы в TableWidget
        for column in range(column_count):
            item = str(list(result_list[row].values())[column])
            my_win.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))


def filter():
    """фильтрует таблицу -результаты-"""
    group = my_win.comboBox_filter_group.currentText()
    name = my_win.comboBox_find_name.currentText()
    name = name.title()  # делает Заглавными буквы слов
    played = my_win.comboBox_filter_played.currentText()

    if group == "все группы" and played == "все игры":
        fltr = Result.select()
    elif group == "все группы" and played == "завершенные":
        fltr = Result.select().where(Result.points_win == 2)
    elif group != "все группы" and played == "завершенные":
        fltr = Result.select().where(Result.number_group == group and Result.points_win == 2)
    elif group != "все группы" and played == "не сыгранные":
        fltr = Result.select().where(Result.number_group == group and Result.points_win == None)
    elif group == "все группы" and played == "не сыгранные":
        fltr = Result.select().where(Result.points_win != 2 or Result.points_win == None)
    elif group != "все группы" and played == "все игры":
        fltr = Result.select().where(Result.number_group == group)

    result_list = fltr.dicts().execute()
    row_count = len(result_list)  # кол-во строк в таблице
    if played == "завершенные":
        my_win.label_16.setText(f"сыграно {row_count} встреч")
    elif played == "не сыгранные":
        my_win.label_16.setText(f"не сыграно еще {row_count} встреч(а)")
    else:
        my_win.label_16.setText(f"всего {row_count} встреч(а)")
    my_win.label_16.show()
    column_count = 13  # кол-во столбцов в таблице
    my_win.tableWidget.setRowCount(row_count)  # вставляет в таблицу необходимое кол-во строк

    for row in range(row_count):  # добвляет данные из базы в TableWidget
        for column in range(column_count):
            item = str(list(result_list[row].values())[column])
            my_win.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))


def load_combo():
    """загружает комбобокс фамилиями спортсменов"""
    mp = Player.select()
    mp_count = len(mp)
    for i in range(1, mp_count + 1):
        tt = Player.get(Player.id == i)
        text = tt.player
        my_win.comboBox_find_name.addItem(text)
    my_win.comboBox_find_name.setCurrentText("")


def reset_filter():
    """сбрасывает критерии фильтрации"""
    my_win.comboBox_find_name.setCurrentText("")
    my_win.comboBox_filter_played.setCurrentText("все игры")
    my_win.comboBox_filter_group.setCurrentText("все группы")
    filter()


def choice_table():
    """заполняется таблица жеребьевка из меню -создание системы-"""
    msgBox = QMessageBox()
    s = System.select().order_by(System.id.desc()).get()
    system = System.get(System.id == s)
    pl = Player.select()
    pl = len(pl)
    mp = system.total_athletes
    if mp == 0:  # система еще не создана (mp - всего человек в списке)
        result = msgBox.information(my_win, "", "Хотите создать систему соревнований?",
                                    msgBox.StandardButtons.Ok, msgBox.StandardButtons.Cancel)
        if result == msgBox.StandardButtons.Ok:
            choice_tbl_made()  # заполняет db жеребъевка
            system_competition()  # создает систему соревнований


def choice_gr_automat():
    """проба автоматической жеребьевки групп"""
    sender = my_win.sender()
    if sender == my_win.choice_gr_Action:
        load_tableWidget()
        t = Title.select().order_by(Title.id.desc()).get()  # получение id последнего соревнования
        sys = System.select().order_by(System.id).where(System.title_id == t).get()  # находит system id последнего
        s_id = sys.id
        group = sys.total_group
        mp = sys.total_athletes
        player_choice = Choice.select().order_by(Choice.rank.desc())
        choice_list = player_choice.dicts().execute()
        h = 0
        for k in range(1, mp + 1):
            if k % 2 != 0:
                start = 0
                end = group
                step = 1
                p = 1
            else:
                start = group
                end = 0
                step = -1
                p = 0
            for i in range(start, end, step):  # 1-й посев
                txt = str(f'{i + p} группа')
                id = int(my_win.tableWidget.item(h, 1).text())
                h += 1
                with db:
                    grp = Choice.get(Choice.id == id)
                    grp.group = txt
                    grp.posev_group = k
                    grp.save()
                    if mp == h:
                        fill_table_choice()
                        return
            with db:
                system = System.get(System.id == s_id)
                system.choice_flag = True
                system.save()
            player_in_table()


def choice_tbl_made():
    """создание таблицы жеребьевка, заполняет db списком участников для жеребъевки"""
    pl = Player.select()
    pl = len(pl)
    choice = Choice.select()
    chc = len(choice)
    if chc == 0:
        for i in range(1, pl + 1):
            pl = Player.get(Player.id == i)
            cch = Coach.get(Coach.id == pl.coach_id)
            coach = cch.coach
            chc = Choice(player_choice=pl, family=pl.player, region=pl.region, coach=coach, rank=pl.rank).save()


def choice_filter_group():
    """фильтрует таблицу жеребьевка по группам"""
    fg = my_win.comboBox_filter_choice.currentText()
    player_choice = Choice.select().order_by(Choice.posev_group)
    choice_list = player_choice.dicts().execute()
    row_count = len(choice_list)  # кол-во строк в таблице
    column_count = 10  # кол-во столбцов в таблице
    my_win.tableWidget.setRowCount(row_count)  # вставляет в таблицу необходимое кол-во строк

    for row in range(row_count):  # добвляет данные из базы в TableWidget
        for column in range(column_count):
            item = str(list(choice_list[row].values())[column])
            my_win.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))

    my_win.tableWidget.resizeColumnsToContents()  # ставит размер столбцов согласно записям
    color_in_tableWidget(fg)
    for d in range(0, row_count):  # сортирует нумерация по порядку
        my_win.tableWidget.setItem(d, 0, QTableWidgetItem(str(d + 1)))


def color_in_tableWidget(fg):
    """смена цвета шрифта в QtableWidget -fg- номер группы"""
    reg = []
    line = Choice.select().order_by(Choice.posev_group).where(Choice.group == fg)  # выбирает все строки той группы (fg)
    for i in line:
        r = Choice.get(Choice.id == i)
        region = r.region
        region = str(region.rstrip())  # удаляет пробел в конце строки
        reg.append(region)
    if len(reg) != 0:
        for x in reg:
            count_region = reg.count(x)
            if count_region > 1:  # если поворяющихся регионов больше одного
                rows = my_win.tableWidget.rowCount()  # кол-во строк в отсортированной таблице
                for i in range(rows):
                    txt = my_win.tableWidget.item(i, 3).text()
                    txt = txt.rstrip()  # удаляет пробел в конце строки
                    if txt == x:
                        my_win.tableWidget.item(i, 3).setForeground(QBrush(QColor(255, 0, 0)))  # окрашивает текст в
                        # красный цвет
                    else:
                        my_win.tableWidget.item(i, 3).setForeground(QBrush(QColor(0, 0, 0)))  # окрашивает текст в
                        # черный цвет


def hide_show_columns():
    """скрывает или показывает столбцы TableWidget"""
    my_win.tableWidget.hideColumn(1)
    my_win.tableWidget.hideColumn(6)
    my_win.tableWidget.hideColumn(10)
    my_win.tableWidget.hideColumn(11)
    my_win.tableWidget.hideColumn(12)
    my_win.tableWidget.hideColumn(13)
    my_win.tableWidget.hideColumn(14)
    my_win.tableWidget.hideColumn(15)
    my_win.tableWidget.hideColumn(16)
    my_win.tableWidget.hideColumn(17)
    my_win.tableWidget.hideColumn(18)
    my_win.tableWidget.hideColumn(19)


def etap_made():
    """создание этапов соревнований"""
    if my_win.comboBox_etap_1.currentText() == "Предварительный" and my_win.comboBox_etap_2.isHidden():
        kol_player_in_group()
    elif my_win.comboBox_etap_2.currentText() == "Финальный" and my_win.comboBox_etap_3.isHidden():
        total_game_table(kpt=0)
    elif my_win.comboBox_etap_3.currentText() == "Финальный" and my_win.comboBox_etap_4.isHidden():
        total_game_table(kpt=0)


def total_game_table(kpt):
    """количество участников в сетке и кол-во игр"""
    t = Title.select().order_by(Title.id.desc()).get()  # получение последней записи в таблице
    system = System.select().order_by(System.id).where(System.title_id == t).get()  # находит system id последнего
    if kpt != 0:  # подсчет кол-во игр из выбора кол-ва игроков вышедших из группы и системы финала
        player_in_final = system.total_group * kpt
        if my_win.comboBox_table.currentIndex() == 0:
            vt = "Сетка (-2) на"
        elif my_win.comboBox_table.currentIndex() == 1:
            vt = "Чистая сетка (с розыгрышем всех мест) на"
        elif my_win.comboBox_table.currentIndex() == 2:
            vt = "Чистая сетка (с играми за 1 - 3 места) на"
        elif my_win.comboBox_table.currentIndex() == 3:
            vt = "Круговая таблица на"
        str_setka = f"{vt} {player_in_final} участников"
        s = System.select().order_by(System.id.desc()).get()
        total_athletes = s.total_athletes
        f = str_setka.find("на")  # ищет вхождение слова -на-
        fsp = str_setka.find(" ", f + 3)  # номер вхождения пробела в строку после слова -на-
        f_num = str_setka[f + 3:fsp]
        f_num = int(f_num)
        if f_num == 8:
            stroka_kol_game = "12 игр"
        elif f_num == 12:
            stroka_kol_game = "28 игр"
        elif f_num == 16:
            stroka_kol_game = "38 игр"
        if total_athletes > f_num:
            fin = "1-й финал"
        else:
            fin = "финальный"
        system = System(title_id=t, total_athletes=total_athletes, total_group=0, kol_game_string=stroka_kol_game,
                        max_player=player_in_final, stage=fin, page_vid=A4, label_string=str_setka, choice_flag=0,
                        score_flag=0).save()
        return str_setka
    else:  # нажата кнопка создания этапа
        system = System.select().order_by(System.id.desc()).get()  # находит system id последнего
        my_win.label_27.setText(system.kol_game_string)  # пишет кол-во игр 2-ого этапа
        my_win.label_27.show()


def clear_db_before_edit():
    """очищает таблицы при повторном создании системы"""
    t = Title.select().order_by(Title.id.desc()).get()  # получение последней записи в таблице
    sid_last = System.select().order_by(System.id.desc()).get()  # получает последний id системы
    sid_first = System.select().order_by(System.id).where(System.title_id == t).get()  # находит system id первого
    sf = sid_first.id
    sl = sid_last.id
    for i in range(sf, sl + 1):  # удаляет все записи
        sd = System.get(System.id == i)
        sd.delete_instance()
    sys = System(title_id=t, total_athletes=0, total_group=0, max_player=0, stage="", page_vid="",
                 label_string="", kol_game_string="", choice_flag=False, score_flag=False).save()
    gl = Game_list.select()
    g_count = len(gl)
    for i in range(1, g_count + 1):
        gl_d = Game_list.get(Game_list.id == i)
        gl_d.delete_instance()
    chc = Choice.select()
    ch_count = len(chc)
    for i in range(1, ch_count + 1):
        ch_d = Choice.get(Choice.id == i)
        ch_d.delete_instance()
    rs = Result.select()
    r_count = len(rs)
    for i in range(1, r_count + 1):
        r_d = Result.get(Result.id == i)
        r_d.delete_instance()


def ready_system():
    """проверка на готовность системы"""
    t = Title.select().order_by(Title.id.desc()).get()  # получение последней записи в таблице
    sid_first = System.select().where(System.title_id == t)  # находит system id первого
    count = len(sid_first)
    if count > 1:
        my_win.statusbar.showMessage("Система соревнований создана", 500)
        flag = True
    else:
        my_win.statusbar.showMessage("Необходимо создать систему соревнований", 500)
        flag = False
    return flag


def flag():
    pass
    t = Title.select().order_by(Title.id.desc()).get()  # получение последней записи в таблице
    with db:
        System.create_table()
        sys = System(title_id=t, total_athletes=0, total_group=0, max_player=0, stage="", page_vid="", label_string="",
                     kol_game_string="", choice_flag=False, score_flag=False).save()

# ===== переводит фокус на полее ввода счета в партии
my_win.lineEdit_pl1_s1.returnPressed.connect(focus)
my_win.lineEdit_pl2_s1.returnPressed.connect(focus)
my_win.lineEdit_pl1_s2.returnPressed.connect(focus)
my_win.lineEdit_pl2_s2.returnPressed.connect(focus)
my_win.lineEdit_pl1_s3.returnPressed.connect(focus)
my_win.lineEdit_pl2_s3.returnPressed.connect(focus)
my_win.lineEdit_pl1_s4.returnPressed.connect(focus)
my_win.lineEdit_pl2_s4.returnPressed.connect(focus)
my_win.lineEdit_pl1_s5.returnPressed.connect(focus)
my_win.lineEdit_pl2_s5.returnPressed.connect(focus)

# ====== отслеживание изменения текста в полях ============

# my_win.lineEdit_find_name.textChanged.connect(result_filter_name)
my_win.lineEdit_Family_name.textChanged.connect(find_in_rlist)  # в поле поиска и вызов функции
my_win.lineEdit_coach.textChanged.connect(find_coach)
# ============= двойной клик
my_win.listWidget.itemDoubleClicked.connect(dclick_in_listwidget)  # двойной клик по listWidget (рейтинг, тренеры)
my_win.tableWidget.doubleClicked.connect(select_player_in_game)  # двойной клик по строке игроков в таблице -результаты-

my_win.tabWidget.currentChanged.connect(tab)
my_win.toolBox.currentChanged.connect(page)
# ==================================
my_win.spinBox_kol_group.textChanged.connect(kol_player_in_group)
# ======== изменение индекса комбобоксов ===========
my_win.comboBox_etap_1.currentTextChanged.connect(system_competition)
my_win.comboBox_etap_2.currentTextChanged.connect(system_competition)
my_win.comboBox_page_vid.currentTextChanged.connect(page_vid)
# my_win.comboBox_table.currentTextChanged.connect(total_player_table)
my_win.comboBox_filter_choice.currentTextChanged.connect(choice_filter_group)
# my_win.comboBox_filter_group.currentTextChanged.connect(result_filter_group)
# my_win.comboBox_filter_played.currentTextChanged.connect(result_filter_played)

# =======  отслеживание переключение чекбоксов =========
my_win.radioButton_3.toggled.connect(load_combobox_filter_group)

my_win.checkBox.stateChanged.connect(button_title_made_enable)  # при изменении чекбокса активирует кнопку создать
my_win.checkBox_2.stateChanged.connect(button_etap_made_enabled)  # при изменении чекбокса активирует кнопку создать
my_win.checkBox_3.stateChanged.connect(button_system_made_enable)  # при изменении чекбокса активирует кнопку создать
my_win.checkBox_4.stateChanged.connect(game_in_visible)  # при изменении чекбокса показывает поля для ввода счета
# =======  нажатие кнопок =========
my_win.Button_reset_filter.clicked.connect(reset_filter)
my_win.Button_filter.clicked.connect(filter)
my_win.Button_etap_made.clicked.connect(etap_made)  # рисует таблицы группового этапа и заполняет game_list
my_win.Button_system_made.clicked.connect(player_in_table)  # заполнение таблицы Game_list
my_win.Button_add_player.clicked.connect(add_player)  # добавляет игроков в список и базу
my_win.Button_group.clicked.connect(player_in_table)  # вносит спортсменов в группы
my_win.Button_title_made.clicked.connect(title_made)  # записывает в базу или редактирует титул
my_win.Button_Ok.clicked.connect(enter_score)  # записывает в базу счет в парти встречи
my_win.Button_proba.clicked.connect(flag)

my_win.Button_sort_R.clicked.connect(sort)
my_win.Button_sort_Name.clicked.connect(sort)
my_win.Button_view.clicked.connect(view)

sys.exit(app.exec())
