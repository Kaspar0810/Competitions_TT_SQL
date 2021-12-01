# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
# import dbm
import numpy as np

import comp_system
import tbl_data
import sqlite3

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
from playhouse.migrate import *

import sys
import xlrd
import pandas as pd
import openpyxl as op
import pdf
import os


# from playhouse.sqlite_ext import SqliteExtDatabase, backup_to_file, backup

from PyQt6 import QtCore, QtGui, QtWidgets, QtPrintSupport, Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from datetime import *

from start_form import Ui_Form
from main_window import Ui_MainWindow  # импортируем из модуля (графического интерфейса main_window) класс Ui_MainWindow
from pdf import *

from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import Paragraph, Table, TableStyle, Image, SimpleDocTemplate, PageTemplate
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.platypus import PageBreak
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER

from reportlab.platypus.frames import Frame
from functools import partial


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
        self.toolBox.setCurrentIndex(0)
        # ++ отключение страниц
        self.tabWidget.setTabEnabled(1, True)
        self.tabWidget.setTabEnabled(2, False)
        self.tabWidget.setTabEnabled(3, False)
        self.tabWidget.setTabEnabled(4, False)
        self.tabWidget.setTabEnabled(5, False)

        self.toolBox.setItemEnabled(1, True)
        self.toolBox.setItemEnabled(2, False)
        self.toolBox.setItemEnabled(3, False)
        self.toolBox.setItemEnabled(4, False)
        self.toolBox.setItemEnabled(5, False)

    # ====== создание строки меню ===========
    def _createMenuBar(self):
        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)  # разрешает показ менюбара

        # меню Соревнования
        fileMenu = QMenu("Соревнования", self)  # основное
        menuBar.addMenu(fileMenu)

        go_to = fileMenu.addMenu("Перейти к")  # подменю с выбором (addMenu добавляет к пункту возможность выбора)
        fileMenu.addSeparator()  # вставляет разделительную черту
        fileMenu.addAction(self.systemAction)  # подменю без выбора (addAction создает сразу действие)
        choice = fileMenu.addMenu("Жеребьевка")
        saveList = fileMenu.addMenu("Сохранить")
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)
        # меню Редактировать
        editMenu = menuBar.addMenu("Редактировать")  # основное
        #  создание подменю
        go_to.addAction(self.go_to_Action)  # подменю выбора соревнования
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
        # меню просмотр
        view_Menu = menuBar.addMenu("Просмотр")
        view_Menu.addAction(self.all_comp_Action)
        view_Menu.addAction(self.view_gr_Action)
        view_Menu.addAction(self.view_pf_Action)
        view_Menu.addAction(self.view_final_Action)
        # меню помощь
        help_Menu = menuBar.addMenu("Помощь")  # основное
    #  создание действий меню
    def _createAction(self):
        self.helpAction = QAction(self)
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
        self.choice_pf_Action = QAction("Полуфиналы")  # подменю жеребьевка -полуфиналы-
        self.choice_fin_Action = QAction("Финалы")  # подменю жеребьевка -финалы-
        self.all_comp_Action = QAction("Полные соревнования")
        self.view_gr_Action = QAction("Группы")
        self.view_pf_Action = QAction("Полуфиналы")
        self.view_final_Action = QAction("Финалы")
        self.go_to_Action = QAction("пусто")

    def _connectActions(self):
        # Connect File actions
        # self.newAction.triggered.connect(self.newFile)
        self.systemAction.triggered.connect(self.system_made)
        self.system_edit_Action.triggered.connect(self.system_edit)
        self.exitAction.triggered.connect(self.exit)
        self.savelist_Action.triggered.connect(self.saveList)
        self.choice_gr_Action.triggered.connect(self.choice)
        self.choice_fin_Action.triggered.connect(self.choice)

        self.go_to_Action.triggered.connect(self.open)
        # Connect Рейтинг actions
        self.rAction.triggered.connect(self.r_File)
        self.r1Action.triggered.connect(self.r1_File)
        # Connect Help actions
        self.helpAction.triggered.connect(self.help)

    def newFile(self):
        # Logic for creating a new file goes here...
        my_win.textEdit.setText("Нажата кнопка меню соревнования")
        gamer = db_select_title()

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
        sender = self.sender()
        gamer = my_win.lineEdit_title_gamer.text()
        system = System.select().order_by(System.id).where(System.title_id == title_id())  # находит system id последнего
        if sender == self.choice_gr_Action:  # нажат подменю жеребъевка групп
            for stage in system:
                if stage.stage == "Предварительный":
                    if stage.choice_flag == True:
                        reply = QMessageBox.information(my_win, 'Уведомление',
                                                        "Жеребъевка была произведена,\nесли хотите сделать "
                                                        "повторно\nнажмите-ОК-, если нет то - Cancel-",
                                                        QMessageBox.StandardButtons.Ok,
                                                        QMessageBox.StandardButtons.Cancel)
                        if reply == QMessageBox.StandardButtons.Ok:
                            my_win.tabWidget.setCurrentIndex(2)
                            choice_gr_automat()
                            my_win.tabWidget.setCurrentIndex(3)
                        else:
                            return
                    else:
                        my_win.tabWidget.setCurrentIndex(2)
                        choice_gr_automat()

        elif sender == self.choice_fin_Action:  # нажат подменю жеребъевка финалов
            fin = select_choice_final()
            system = System.get(System.stage == fin)
            if system.choice_flag == True:  # проверка флаг на жеребъевку финала
                reply = QMessageBox.information(my_win, 'Уведомление', f"Жеребъевка {fin} была произведена,"
                                                                       f"\nесли хотите сделать "
                                                                       "повторно\nнажмите-ОК-, "
                                                                       "если нет то - Cancel-",
                                                QMessageBox.StandardButtons.Ok,
                                                QMessageBox.StandardButtons.Cancel)
                if reply == QMessageBox.StandardButtons.Ok:
                    choice_setka(fin)
                else:
                    return
            else:
                # ========= необходимо проверить на правильность желания жеребъевки
                choice_setka(fin)

    def system_made(self):
        system_competition()

    def system_edit(self):
        system_competition()

    def help(self):
        pass

    def open(self):
        go_to()
        # db_select_title()

app = QApplication(sys.argv)
my_win = MainWindow()
my_win.setWindowTitle("Соревнования по настольному теннису")


class StartWindow(QMainWindow, Ui_Form):
    """Стартовое окно приветствия"""
    def __init__(self):
        super(StartWindow, self).__init__()
        self.setupUi(self)  # загружает настройки формы(окна) из QT
        self.setWindowTitle('Добро пожаловать в COMPETITIONS_TT')
        self.Button_open.clicked.connect(self.open)
        self.Button_new.clicked.connect(self.new)
        self.Button_old.clicked.connect(self.load_old)
        self.Button_R.clicked.connect(self.r_load)
        self.LinkButton.clicked.connect(self.last_comp)
        self.Button_open.setEnabled(False)

        self.pb = QProgressBar()
        self.pb.setMinimum(0)
        self.pb.setMaximum(100)

        dbase()
        count = len(Title.select())
        if count != 0:
            t_id = Title.select().order_by(Title.id.desc()).get()  # получение последней записи в таблице
            id = t_id.id
            old_title = Title.get(Title.id == id)
            last_comp = old_title.full_name_comp
            self.LinkButton.setText(f"{last_comp}")
        else:
            self.LinkButton.setText("Список прошедших соревнований пуст")
            self.LinkButton.setEnabled(False)
            self.Button_open.setEnabled(False)
            self.Button_old.setEnabled(False)

    def last_comp(self):
        """открытие последних соревнований"""
        gamer = db_select_title()
        tab_enabled(gamer)
        self.close()
        my_win.show()

    def open(self):
        gamer = db_select_title()
        self.close()
        my_win.setWindowTitle(f"Соревнования по настольному теннису. {gamer}")
        my_win.show()

    def new(self):
        """запускает новые соревнования"""
        gamer = ("Мальчики", "Девочки", "Юноши", "Девушки", "Мужчины", "Женщины")
        gamer, ok = QInputDialog.getItem(my_win, "Участники", "Выберите категорию спортсменов", gamer, 0, False)

        title = Title(name="", sredi="", vozrast="", data_start="", data_end="", mesto="", referee="",
                      kat_ref="", secretary="", kat_sek="", gamer=gamer, full_name_comp="").save()
        t_id = Title.select().order_by(Title.id.desc()).get()  # получение последней записи в таблице
        title_id = t_id.id
        db_r(gamer)
        system = System(title_id=title_id, total_athletes=0, total_group=0,
                        max_player=0, stage="", page_vid="", label_string="", kol_game_string="",
                        choice_flag=False, score_flag=5, visible_game=False).save()
        self.close()
        tab_enabled(gamer)
        my_win.show()

    def r_load(self):
        pass
        # wb = op.Workbook()
        # # # data = []
        # # # data_tmp = []
        # fname = QFileDialog.getOpenFileName(my_win, "Выбрать файл R-листа", "", "Excels files (*.xls *.xlsx)")
        # filepatch = str(fname[0])
        # rp = filepatch.rindex("/")
        # RPath = filepatch[rp + 1: len(filepatch)]
        # wb.save(fileName=RPath)
        #
        # excel_data = pd.read_excel(RPath)  # читает  excel файл Pandas
        # data_pandas = pd.DataFrame(excel_data)  # получает Dataframe
        # column = data_pandas.columns.ravel().tolist()  # создает список заголовков столбцов
        # count = len(data_pandas)  # кол-во строк в excel файле
        # for i in range(0, count):  # цикл по строкам
        #     for col in column: # цикл по столбцам
        #         val = data_pandas.iloc[i][col]
        #         data_tmp.append(val)  # получает временный список строки
        #     data.append(data_tmp.copy())  # добавляет в список Data
        #     data_tmp.clear()  # очищает временный список

    def load_old(self):
        """загружает в комбобокс архивные соревнования"""
        self.label_4.show()
        t_id = Title.select().order_by(Title.id.desc())  # получение последней записи в таблице
        n = 6
        for i in t_id:
            old_comp = i.name
            gamer = i.gamer
            data_start = i.data_start
            data_finish = i.data_end
            n -= 1
            if n != 5:
                if old_comp != "":
                    self.comboBox.addItem(f"{old_comp}. {gamer}")
                    self.label_4.setText(f"сроки: с {data_start} по {data_finish}")
                else:
                    return
        if fir_window.comboBox.currentText() != "":
            fir_window.Button_open.setEnabled(True)

def dbase():
    """Создание DB и таблиц"""
    with db:
        db.create_tables([Title, R_list_m, R_list_d, Region, City, Player, R1_list_m, R1_list_d, Coach, System,
                              Result, Game_list, Choice, Delete_player])


def db_r(gamer):  # table_db присваивает по умолчанию значение R_list
    """переходит на функцию выбора файла рейтинга в зависимости от текущего или январского,
     а потом загружает список регионов базу данных"""
    if gamer == "Мальчики" or gamer == "Юноши" or gamer == "Мужчины":
        table_db = R_list_m
        ext = "(*_m.xlsx, *_m.xls)"
    else:
        table_db = R_list_d
        ext = "(*_w.xlsx, *_w.xls)"
    fname = QFileDialog.getOpenFileName(my_win, "Выбрать файл R-листа", "", f"Excels files {ext}")
    load_listR_in_db(fname, table_db)
    my_win.statusbar.showMessage("Текущий рейтинг загружен")
    if gamer == "Мальчики" or gamer == "Юноши" or gamer == "Мужчины":
        table_db = R1_list_m
        ext = "(*01_m.xlsx, *01_m.xls)"
    else:
        table_db = R1_list_d
        ext = "(*01_w.xlsx, *01_w.xls)"
    fname = QFileDialog.getOpenFileName(my_win, "Выбрать файл R-листа", "", f"Excels files {ext}")
    load_listR_in_db(fname, table_db)
    my_win.statusbar.showMessage("Январский рейтинг загружен")
    # не помню зачем сделал отдельно январский рейтинг
    # if gamer == "Мальчики" or gamer == "Юноши" or gamer == "Мужчины":
    #     table_db = R1_list_m
    # else:
    #     table_db = R1_list_d
    #
    #     fname = QFileDialog.getOpenFileName(my_win, "Выбрать файл R-листа", "", "Excels files (*_01*.xlsx *_01*.xls)")
    #     load_listR_in_db(table_db, fname)
    #     my_win.statusbar.showMessage("Текущий рейтинг загружен")
    # добавляет в таблицу регионы
    t = Title.select().order_by(Title.id.desc()).get()  # получение последней записи в таблице
    title = t.id
    if title == 1:
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
    my_win.statusbar.showMessage("Список регионов загружен", 5000)  # показывает статус бар на 5 секунд
    my_win.lineEdit_title_nazvanie.hasFocus()


def load_listR_in_db(fname, table_db):
    """при отсутствии выбора файла рейтинга, позволяет выбрать вторично или выйти из диалога
    если выбор был сделан загружает в базу данных"""
    filepatch = str(fname[0])
    if table_db == R_list_m or table_db == R_list_d:
        r = "текущим"
    elif table_db == R1_list_m or table_db == R1_list_d:
        r = "январским"
    if filepatch == "":
        message = f"Вы не выбрали файл с {r} рейтингом!" \
                  "если хотите выйти, нажмите <Ок>" \
                  "если хотите вернуться, нажмите <Отмена>"
        reply = QtWidgets.QMessageBox.information(my_win, 'Уведомление', message,
                                                  QtWidgets.QMessageBox.StandardButtons.Ok,
                                                  QtWidgets.QMessageBox.StandardButtons.Cancel)
        if reply == QMessageBox.StandardButtons.Ok:
            return
        else:
            db_r(table_db)
    else:
        data = []
        data_tmp = []

        rlist = table_db.delete().execute()

        excel_data = pd.read_excel(filepatch)  # читает  excel файл Pandas
        data_pandas = pd.DataFrame(excel_data)  # получает Dataframe
        column = data_pandas.columns.ravel().tolist()  # создает список заголовков столбцов
        count = len(data_pandas)  # кол-во строк в excel файле
        for i in range(0, count):  # цикл по строкам
            for col in column:  # цикл по столбцам
                val = data_pandas.iloc[i][col]
                data_tmp.append(val)  # получает временный список строки
            data.append(data_tmp.copy())  # добавляет в список Data
            data_tmp.clear()  # очищает временный список
        with db:
            table_db.insert_many(data).execute()


def region():
    """добавляет из таблицы в комбобокс регионы"""
    if my_win.comboBox_region.currentIndex() > 0:  # проверка на заполненность комбобокса данными
        return
    else:
        with db:
            for r in range(1, 86):
                reg = Region.get(Region.id == r)
                my_win.comboBox_region.addItem(reg.region)

fir_window = StartWindow()  # Создаём объект класса ExampleApp
fir_window.show()  # Показываем окно



#  ==== наполнение комбобоксов ==========
page_orient = ("альбомная", "книжная")
kategoria_list = ("2-я кат.", "1-я кат.", " ССВК")
mylist = ('мальчиков и девочек', 'юношей и девушек', 'мужчин и женщин')
raz = ("б/р", "3-юн", "2-юн", "1-юн", "3-р", "2-р", "1-р", "КМС", "МС", "МСМК", "ЗМС")
res = ("все игры", "завершенные", "не сыгранные")
stages1 = ("", "Одна таблица", "Предварительный", "Полуфиналы", "Финальный", "Суперфинал")
stages2 = ("", "Полуфиналы", "Финальный", "Суперфинал")
stages3 = ("", "Финальный", "Суперфинал")
vid_setki = ("", "Сетка (-2)", "Сетка (с розыгрышем всех мест)", "Сетка (за 1-3 место)", "Круговая система")


my_win.comboBox_page_vid.addItems(page_orient)
my_win.comboBox_etap_1.addItems(stages1)
my_win.comboBox_etap_2.addItems(stages2)
my_win.comboBox_etap_3.addItems(stages3)
my_win.comboBox_kategor_ref.addItems(kategoria_list)
my_win.comboBox_kategor_sek.addItems(kategoria_list)
my_win.comboBox_sredi.addItems(mylist)
my_win.comboBox_razryad.addItems(raz)
my_win.comboBox_filter_played.addItems(res)
my_win.comboBox_filter_played_fin.addItems(res)
my_win.comboBox_table.addItems(vid_setki)
my_win.comboBox_table_2.addItems(vid_setki)
my_win.comboBox_one_table.addItems(vid_setki)

# ставит сегодняшнюю дату в виджете календарь
my_win.dateEdit_start.setDate(date.today())
my_win.dateEdit_end.setDate(date.today())


def tab_enabled(gamer):
    """Включает вкладки в зависимости от создании системы и жеребьевки"""
    sender = my_win.sender()
    title = title_id()
    count_title = len(Title.select())
        #============== вставляет в меня выбора название другого соревнования
    t_id = Title.select().order_by(Title.id.desc())  # получает все Title, отсортированные Я-А
    n = 6
    for i in t_id:
        t = i.id
        old_comp = i.name
        old_data = i.data_start
        old_gamer = i.gamer
        comp = f"{old_comp}.{old_data}.{old_gamer}"
        if title != t:  # сравнивает id открытых соревнований и открываемых и меняет надпись в меню
            my_win.go_to_Action.setText(comp)
    if gamer == "":
        gamer = my_win.lineEdit_title_gamer.text()
    if count_title != 0:  # когда создаются новые соревноания
        my_win.setWindowTitle(f"Соревнования по настольному теннису. {gamer}")
        system = System.select().where(System.title_id == title_id())  # находит system id первого
        count = len(system)
        stage = []
        for i in system:
            st = i.stage
            stage.append(st)
        count_stage = len(stage)
        if count_stage > 1:  # если система еще не создана, то выключает отдельные вкладки при переходе на другое сорев
            if count > 0:
                my_win.tabWidget.setTabEnabled(2, True)  # выключает отдельные вкладки
                my_win.toolBox.setItemEnabled(2, True)
                for i in stage:
                    if i == "Одна таблица":
                        pass
                    elif i == "Предварительный":
                        system = System.get(System.id == title_id() and System.stage == i)
                        flag = system.choice_flag
                        if flag is True:
                            my_win.tabWidget.setTabEnabled(3, True)
                    elif i == "Полуфиналы":
                        my_win.tabWidget.setTabEnabled(4, True)
                    elif i == "1-й финал" or i == "финальный":
                        system = System.get(System.id == title_id() and System.stage == i)
                        flag = system.choice_flag
                        if flag is True:
                            my_win.tabWidget.setTabEnabled(5, True)
                my_win.tabWidget.setCurrentIndex(0)
        else:
            my_win.tabWidget.setTabEnabled(2, True)  # выключает отдельные вкладки
            my_win.tabWidget.setTabEnabled(3, False)
            my_win.tabWidget.setTabEnabled(4, False)
            my_win.tabWidget.setTabEnabled(5, False)
            my_win.tabWidget.setCurrentIndex(0)
    else:
        my_win.tabWidget.setTabEnabled(2, True)  # выключает отдельные вкладки
        my_win.tabWidget.setTabEnabled(3, False)
        my_win.tabWidget.setTabEnabled(4, False)
        my_win.tabWidget.setTabEnabled(5, False)


def db_insert_title(title_str):
    """Вставляем запись в таблицу титул"""
    nm = title_str[0]
    sr = title_str[1]
    vz = title_str[2]
    ds = title_str[3]
    de = title_str[4]
    ms = title_str[5]
    rf = title_str[6]
    kr = title_str[7]
    sk = title_str[8]
    ks = title_str[9]
    gm = title_str[10]
    fn = title_str[11]
    t = Title.select().order_by(Title.id.desc()).get()  # получение последней записи в таблице
    nazv = Title(id=t, name=nm, sredi=sr, vozrast=vz, data_start=ds, data_end=de, mesto=ms, referee=rf,
                 kat_ref=kr, secretary=sk, kat_sek=ks, gamer=gm, full_name_comp=fn).save()


def go_to():
    """переход на предыдущие соревнования и обратно при нажатии меню -перейти к-"""
    full_name = my_win.go_to_Action.text()  # полное название к которым переходим
    tit = Title.get(Title.id == title_id())
    name = tit.name
    data = tit.data_start
    gamer_current = tit.gamer
    full_name_current = f"{name}.{data}.{gamer_current}"  # полное название текущих соревнований
    my_win.go_to_Action.setText(full_name_current)  # присваиваем новый текст соревнований в меню -перейти к-
    titles = Title.get(Title.full_name_comp == full_name)
    gamer = titles.gamer
    my_win.lineEdit_title_nazvanie.setText(titles.name)
    my_win.lineEdit_title_vozrast.setText(titles.vozrast)
    my_win.dateEdit_start.setDate(titles.data_start)
    my_win.dateEdit_end.setDate(titles.data_end)
    my_win.lineEdit_city_title.setText(titles.mesto)
    my_win.lineEdit_refery.setText(titles.referee)
    my_win.comboBox_kategor_ref.setCurrentText(titles.kat_ref)
    my_win.lineEdit_sekretar.setText(titles.secretary)
    my_win.comboBox_kategor_sek.setCurrentText(titles.kat_sek)
    my_win.lineEdit_title_gamer.setText(titles.gamer)
    tab_enabled(gamer)
    my_win.tabWidget.setCurrentIndex(0)
    player_list = Player.select().where(Player.title_id == title_id())
    fill_table(player_list)  # заполняет TableWidget списком игроков


def db_select_title():
    """извлекаем из таблицы данные и заполняем поля титула для редактирования или просмотра"""
    sender = fir_window.sender()  # от какой кнопки сигнал

    if sender == my_win.go_to_Action:  # переход к соревнованиям из меню основного окна
        full_name = my_win.go_to_Action.text()  # полное название к которым переходим
        tit = Title.get(Title.id == title_id())
        name = tit.name
        data = tit.data_start
        gamer_current = tit.gamer
        full_name_current = f"{name}.{data}.{gamer_current}"  # полное название текущих соревнований
        my_win.go_to_Action.setText(full_name_current)   # присваиваем новый текст соревнований в меню -перейти к-
        titles = Title.get(Title.full_name_comp == full_name)
        gamer = titles.gamer
    elif sender == my_win.toolBox or sender.text() != "Открыть":
        titles = Title.get(Title.id == title_id())
        name = titles.name
        gamer = titles.gamer
    else:  # сигнал от кнопки с текстом -открыть- соревнования из архива (стартовое окно)
        txt = fir_window.comboBox.currentText()
        key = txt.rindex(".")
        gamer = txt[39:]
        name = txt[:37]
        sroki= fir_window.label_4.text()
        data = sroki[9:19]
        full_name = f"{name}.{data}.{gamer}"
        titles = Title.get(Title.full_name_comp == full_name)

    my_win.lineEdit_title_nazvanie.setText(titles.name)
    my_win.lineEdit_title_vozrast.setText(titles.vozrast)
    my_win.dateEdit_start.setDate(titles.data_start)
    my_win.dateEdit_end.setDate(titles.data_end)
    my_win.lineEdit_city_title.setText(titles.mesto)
    my_win.lineEdit_refery.setText(titles.referee)
    my_win.comboBox_kategor_ref.setCurrentText(titles.kat_ref)
    my_win.lineEdit_sekretar.setText(titles.secretary)
    my_win.comboBox_kategor_sek.setCurrentText(titles.kat_sek)
    my_win.lineEdit_title_gamer.setText(titles.gamer)
    tab_enabled(gamer)
    return gamer


def system_edit():
    """редактирование системы"""
    system_made()


def system_made():
    """Заполняет таблицу система кол-во игроков, кол-во групп и прочее"""
    # t = Title.select().where(Title.id == title_id()) # последний id соревнований (текуших)
    ce = System.select().where(System.title_id == title_id()).get()  # находит system id последнего
    # ce = System.get(System.id == t.id)  # получаем id system текущих соревнований
    cs = System.select().where(System.id == ce)  # все строки, где title_id соревнований
    count_system = len(cs)  # получение количества записей (этапов) в системе
    sg = my_win.comboBox_etap_1.currentText()
    page_v = my_win.comboBox_page_1.currentText()
    total_group = ce.total_group
    total_athletes = ce.total_athletes
    max_player = ce.max_player
    if sg == "одна таблица":
        system = System(id=cs, title_id=t, total_athletes=total_athletes, total_group=0,
                        max_player=0, stage=sg, page_vid=page_v, label_string="", kol_game_string="",
                        choice_flag=False, score_flag=5, visible_game=False).save()
    else:  # предварительный этап
        for i in range(1, count_system + 1):
            system = System(id=cs, title_id=t, total_athletes=total_athletes, total_group=total_group,
                            max_player=max_player, stage=sg, page_vid=page_v, label_string="", kol_game_string="",
                            choice_flag=False, score_flag=5, visible_game=False).save()
    player_in_table()
    my_win.checkBox_2.setChecked(False)
    my_win.checkBox_3.setChecked(False)
    my_win.Button_system_made.setEnabled(False)
    my_win.Button_1etap_made.setEnabled(False)
    my_win.Button_2etap_made.setEnabled(False)


def load_tableWidget():
    """Заполняет таблицу списком или рейтингом в зависимости от выбора"""
    msgBox = QMessageBox
    gamer = my_win.lineEdit_title_gamer.text()
    tb = my_win.tabWidget.currentIndex()
    sender = my_win.menuWidget().sender()  # сигнал указывающий какой пункт меню нажат
    if sender == my_win.rAction or sender == my_win.r1Action:  # нажат пункт меню -текущий рейтинг- или -рейтинг январский
        z = 6
        column_label = ["№", "Место", "  Рейтинг", "Фамилия Имя", "Дата рождения", "Город"]
    elif my_win.tabWidget.currentIndex() == 3 or my_win.tabWidget.currentIndex() == 5:
        z = 14
        column_label = ["№", "Этапы", "Группа/ финал", "Встреча", "Игрок_1", "Игрок_2", "Победитель", "Очки",
                        "Общий счет",
                        "Счет в партии", "Проигравший", "Очки", "Счет в партии", " title_id"]
    elif my_win.tabWidget.currentIndex() == 2 or sender == my_win.choice_gr_Action or sender == my_win.choice_fin_Action:
        z = 19
        column_label = ["№", "Id", "Фамилия Имя", "Регион", "Тренер(ы)", "Рейтинг", "Основной", "Предварительный",
                        "Посев",
                        "Место в группе", "ПФ", "Посев в ПФ", "Место", "Финал", "Посев в финале", "Место", "Суперфинал"]
    elif my_win.checkBox_6.isChecked():
        z = 11
        column_label = ["№", "Фамилия, Имя", "Дата рождения", "Рейтинг", "Город", "Регион", "Разряд",
                        "Тренер(ы)"]
    else:
        z = 11  # кол-во столбцов должно быть равно (fill_table -column_count-)
        column_label = ["№", "Фамилия, Имя", "Дата рождения", "Рейтинг", "Город", "Регион", "Разряд",
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
    if sender == my_win.rAction:  # нажат пункт меню -текущий рейтинг- и загружает таблицу с рейтингом
        fill_table_R_list()
    elif sender == my_win.r1Action:  # нажат пункт меню -рейтинг за январь- и загружает таблицу с рейтингом
        fill_table_R1_list()
    elif my_win.checkBox_6.checkState() is True:  # нажат пункт  -просмотр удаленных игроков-
        del_player_table()
    elif my_win.tabWidget.currentIndex() == 3 or my_win.tabWidget.currentIndex() == 5:  # таблица результатов
        flag = ready_choice()
        if flag is True:
            fill_table_results(tb)
    elif my_win.tabWidget.currentIndex() == 2 or sender == my_win.choice_gr_Action:
        if sender == my_win.choice_fin_Action:  # таблица жеребьевки
            pass
        else:
            fill_table_choice()
            hide_show_columns(tb)
    else:  # загружает таблицу со списком
        player_list = Player.select().where(Player.title_id == title_id()).order_by(Player.rank.desc())
        count = len(player_list)
        if count != 0:
            fill_table(player_list)
            hide_show_columns(tb)


def title_string():
    """ переменные строк титульного листа """
    title_str = []
    title = Title.select().order_by(Title.id.desc()).get()  # получение последней записи в таблице

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
    gm = title.gamer
    fn = f"{nm}.{ds}.{gm}"

    title_str.append(nm)
    title_str.append(sr)
    title_str.append(vz)
    title_str.append(ds)
    title_str.append(de)
    title_str.append(ms)
    title_str.append(rf)
    title_str.append(kr)
    title_str.append(sk)
    title_str.append(ks)
    title_str.append(gm)
    title_str.append(fn)
    return title_str


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
    title_str = title_string()
    if my_win.Button_title_made.text() == "Редактировать":
        title_update()
        return
    else:
        db_insert_title(title_str)
    title_pdf()
    my_win.checkBox.setChecked(False)  # после заполнения титула выключает чекбокс
    my_win.Button_title_made.setText("Создать")
    region()
    t = Title.select().order_by(Title.id.desc()).get()  # получение последней записи в таблице
    s = System.select().order_by(System.id.desc()).get()  # получение последнего id системы соревнования

    with db:
        System.create_table()
        sys = System(id=s, title_id=t, total_athletes=0, total_group=0, max_player=0, stage="", page_vid="",
                     label_string="", kol_game_string="", choice_flag=False, score_flag=5, visible_game=False).save()


def title_update():
    """обновляет запись титула, если был он изменен"""
    title_str = title_string()
    nm = title_str[0]
    sr = title_str[1]
    vz = title_str[2]
    ds = title_str[3]
    de = title_str[4]
    ms = title_str[5]
    rf = title_str[6]
    kr = title_str[7]
    sk = title_str[8]
    ks = title_str[9]
    # gm = title_str[10]

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
    # nazv.gamer = gm
    nazv.save()


def find_in_rlist():
    """при создании списка участников ищет спортсмена в текущем R-листе"""
    t_id = Title.get(Title.id == title_id())
    gamer = t_id.gamer
    if gamer == "Девочки" or gamer == "Девушки" or gamer == "Женщины":
        r_list = R_list_d
    else:
        r_list = R_list_m

    my_win.listWidget.clear()
    my_win.textEdit.clear()
    fp = my_win.lineEdit_Family_name.text()
    fp = fp.capitalize()  # Переводит первую букву в заглавную
    p = r_list.select()
    p = p.where(r_list.r_fname ** f'{fp}%')  # like
    if (len(p)) == 0:
        my_win.textEdit.setText("Нет спортсменов в рейтинг листе")
    else:
        for pl in p:
            full_stroka = f"{pl.r_fname}, {str(pl.r_list)}, {pl.r_bithday}, {pl.r_city}"
            my_win.listWidget.addItem(full_stroka)


def fill_table(player_list):
    """заполняет таблицу со списком участников QtableWidget спортсменами из db"""
    player_selected = player_list.dicts().execute()
    # for p in player_list:
    # for p in player_selected:
    #     player = p.player
    row_count = len(player_selected)  # кол-во строк в таблице
    if row_count != 0:  # список удаленных игроков пуст
        column_count = len(player_selected[0])  # кол-во столбцов в таблице
        my_win.tableWidget.setRowCount(row_count)  # вставляет в таблицу необходимое кол-во строк
        for row in range(row_count):  # добавляет данные из базы в TableWidget
            for column in range(column_count):
                if column == 7:  # преобразует id тренера в фамилию
                    coach_id = str(list(player_selected[row].values())[column])
                    coach = Coach.get(Coach.id == coach_id)
                    item = coach.coach
                else:
                    item = str(list(player_selected[row].values())[column])
                my_win.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
        my_win.tableWidget.resizeColumnsToContents()  # ставит размер столбцов согласно записям
        for i in range(0, row_count):  # отсортировывает номера строк по порядку
            my_win.tableWidget.setItem(i, 0, QTableWidgetItem(str(i + 1)))
    else:
        my_win.tableWidget.setRowCount(row_count)  # вставляет в таблицу необходимое кол-во строк
        my_win.statusbar.showMessage("Удаленных участников соревнований нет", 10000)


def fill_table_R_list():
    """заполняет таблицу списком из текущего рейтинг листа"""
    player_rlist = R_list_m.select().order_by(R_list_m.r_fname)
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
    player_rlist = R1_list_m.select().order_by(R1_list_m.r1_fname)
    player_r1 = player_rlist.dicts().execute()
    row_count = len(player_r1)  # кол-во строк в таблице
    column_count = len(player_r1[0])  # кол-во столбцов в таблице
    my_win.tableWidget.setRowCount(row_count)  # вставляет в таблицу необходимое кол-во строк

    for row in range(row_count):  # добавляет данные из базы в TableWidget
        for column in range(column_count):
            item = str(list(player_r1[row].values())[column])
            my_win.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))

    my_win.tableWidget.resizeColumnsToContents()  # ставит размер столбцов согласно записям


def fill_table_results(tb):
    """заполняет таблицу результатов QtableWidget из db result"""
    tb = my_win.tabWidget.currentIndex()
    result = Result.select()  # проверка есть ли записи в таблице -result-
    count = len(result)  # если 0, то записей нет
    player_result = Result.select().order_by(Result.id)
    flag = ready_system()
    if flag is False and count == 0:
        message = "Надо сделать жербьевку предварительного этапа.\nХотите ее создать?"
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
        # надо выбрать, что загружать в зависимости от вкладки группы, пф или финалы
        if tb == 3:
            player_result = Result.select().order_by(Result.id).where(Result.system_stage == "Предварительный")
        elif tb == 4:
            player_result = Result.select().order_by(Result.id)
        elif tb == 5:
            player_result = Result.select().where(Result.system_stage == "Финальный")
            count = len(player_result)
            if count == 0:
                return
        result_list = player_result.dicts().execute()
        row_count = len(result_list)  # кол-во строк в таблице
        column_count = len(result_list[0])  # кол-во столбцов в таблице
        my_win.tableWidget.setRowCount(row_count)  # вставляет в таблицу необходимое кол-во строк
        row_result = []
        for row in range(row_count):  # добавляет данные из базы в TableWidget
            for column in range(column_count):
                item = str(list(result_list[row].values())[column])
                if column < 6:
                    row_result.append(item)
                    my_win.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                elif column == 6:
                    row_result.append(item)
                    if row_result[6] != "None" and row_result[6] != "":  # встреча сыграна
                        if row_result[4] == row_result[6]:
                            my_win.tableWidget.item(row, 4).setForeground(QBrush(QColor(255, 0, 0)))  # окрашивает текст
                            # в красный цвет 1-ого игрока
                        else:
                            my_win.tableWidget.item(row, 5).setForeground(QBrush(QColor(255, 0, 0)))  # окрашивает текст
                            # в красный цвет 2-ого игрока
                    else:
                        my_win.tableWidget.item(row, 4).setForeground(QBrush(QColor(0, 0, 0)))  # в черный цвет 1-ого
                        my_win.tableWidget.item(row, 5).setForeground(QBrush(QColor(0, 0, 0)))  # в черный цвет 2-ого
                    row_result.clear()
                    my_win.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                elif column > 6:
                    my_win.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))

        my_win.tableWidget.showColumn(6)  # показывает столбец победитель
        my_win.tableWidget.hideColumn(10)
        my_win.tableWidget.hideColumn(11)
        my_win.tableWidget.hideColumn(12)
        my_win.tableWidget.hideColumn(13)
        my_win.tableWidget.resizeColumnsToContents()  # ставит размер столбцов согласно записям


def fill_table_choice():
    """заполняет таблицу жеребьевки"""
    gamer = my_win.lineEdit_title_gamer.text()
    player_choice = Choice.select().where(Choice.title_id == title_id()).order_by(Choice.rank.desc())
    choice_list = player_choice.dicts().execute()
    row_count = len(choice_list)  # кол-во строк в таблице
    if row_count != 0:
        column_count = len(choice_list[0])  # кол-во столбцов в таблице
        my_win.tableWidget.setRowCount(row_count)  # вставляет в таблицу необходимое кол-во строк
        for row in range(row_count):  # добвляет данные из базы в TableWidget
            for column in range(column_count):
                item = str(list(choice_list[row].values())[column])
                my_win.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
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
    player_list = Player.select().where(Player.title_id == title_id())
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
    fn = f"{pl}/ {ct}"

    add_coach(ch, num)
    ms = ""
    idc = Coach.get(Coach.coach == ch)
    if my_win.checkBox_6.isChecked():  # если отмечен флажок -удаленные-, то восстанавливает игрока и удаляет из
        # таблицы -удаленные-
        row = my_win.tableWidget.currentRow()
        with db:
            player_del = Delete_player.get(Delete_player.player == my_win.tableWidget.item(row, 1).text())
            pl_id = player_del.player_del_id
            player_del.delete_instance()
            plr = Player(player_id=pl_id, player=pl, bday=bd, rank=rn, city=ct, region=rg,
                         razryad=rz, coach_id=idc, full_name = fn, mesto=ms, title_id=title_id()).save()
        spisok = (str(num), pl, bd, rn, ct, rg, rz, ch, ms)
        for i in range(0, 9):  # добавляет в tablewidget
            my_win.tableWidget.setItem(count, i, QTableWidgetItem(spisok[i]))
        load_tableWidget()  # заново обновляет список
        player_list = Player.select().where(Player.title_id == title_id())  # выделяет все строки базы данных
        count = len(player_list)  # подсчитывает новое кол-во игроков
        my_win.label_46.setText(f"Всего: {count} участников")
        my_win.checkBox_6.setChecked(False)  # сбрасывает флажок -удаленные-
    else:  # просто редактирует игрока
        txt = my_win.Button_add_edit_player.text()
        if txt == "Редактировать":
            with db:
                plr = Player.get(Player.player == pl)
                plr.player=pl
                plr.bday=bd
                plr.rank=rn
                plr.city=ct
                plr.region=rg
                plr.razryad=rz
                plr.coach_id=idc
                plr.full_name=fn
                plr.save()
        elif txt == "Добавить":
            with db:
                player = Player(player=pl, bday=bd, rank=rn, city=ct, region=rg, razryad=rz,
                                coach_id=idc, mesto="", full_name=fn, title_id=title_id() ).save()
        spisok = (str(num), pl, bd, rn, ct, rg, rz, ch, ms)
        for i in range(0, 9):  # добавляет в tablewidget
            my_win.tableWidget.setItem(count + 1, i, QTableWidgetItem(spisok[i]))
        load_tableWidget()  # заново обновляет список
        my_win.label_46.setText(f"Всего: {count + 1} участников")
        player_list = Player.select().where(Player.title_id == title_id())
        list_player_pdf(player_list)
        my_win.lineEdit_Family_name.clear()
        my_win.lineEdit_bday.clear()
        my_win.lineEdit_R.clear()
        my_win.lineEdit_city_list.clear()
        my_win.lineEdit_coach.clear()


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


def load_combobox_filter_final():
    """заполняет комбобокс фильтр финалов для таблицы результаты"""
    my_win.comboBox_filter_final.clear()
    system = System.select().order_by(System.id).where(System.title_id == title_id())  # находит system id последнего
    fin = ["все финалы"]
    for sys in system:
        if sys.stage != "Предварительный" and sys.stage != "Полуфиналы":
            if sys.choice_flag is True:
                fin.append(sys.stage)
    my_win.comboBox_filter_final.addItems(fin)


def load_combobox_filter_group():
    """заполняет комбобокс фильтр групп для таблицы результаты"""
    gamer = my_win.lineEdit_title_gamer.text()
    etap = []
    gr_txt = []
    sender = my_win.menuWidget().sender()
    my_win.comboBox_filter_group.clear()
    my_win.comboBox_filter_choice.clear()

    system = System.select().order_by(System.id).where(System.title_id == title_id())  # находит system id последнего
    for i in system:
        e = i.stage
        etap.append(e)  # получает список этапов на данных соревнованиях
    if etap[0] != "":
        fir_e = "Предварительный"
        flag = e in etap
        if flag == True:
            sf = system.select().where(System.stage == fir_e).get()
            kg = int(sf.total_group)  # количество групп

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
    gamer = my_win.lineEdit_title_gamer.text()
    tb = my_win.toolBox.currentIndex()
    sf = System.select().where(System.title_id == title_id())
    if tb == 0:
        db_select_title()
        my_win.tableWidget.show()
        player_list = Player.select().where(Player.title_id == title_id())
        fill_table(player_list)  # заполняет TableWidget списком игроков
    elif tb == 1:  # -список участников-
        region()
        load_tableWidget()
        my_win.tableWidget.show()
        my_win.Button_del_player.setEnabled(False)
        my_win.Button_add_edit_player.setText("Добавить")
        my_win.statusbar.showMessage("Список участников соревнований", 5000)
        player_list = Player.select().where(Player.title_id == title_id())
        count = len(player_list)
        my_win.label_46.setText(f"Всего: {count} участников")
    elif tb == 2:  # -система-
        player_list = Player.select().where(Player.title_id == title_id())
        count = len(player_list)
        my_win.label_8.setText(f"Всего участников: {str(count)} человек")
        st_count = len(sf)
        if st_count != 1:
            load_combobox_filter_group()

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
        my_win.label_34.hide()
        my_win.label_35.hide()
        my_win.label_50.hide()
        my_win.comboBox_etap_1.hide()
        my_win.comboBox_etap_2.hide()
        my_win.comboBox_etap_3.hide()
        my_win.comboBox_etap_4.hide()
        my_win.comboBox_table_2.hide()
        my_win.spinBox_kol_group.hide()
        my_win.comboBox_table.hide()
        my_win.comboBox_one_table.hide()

        flag = ready_system()

        if flag is False:  # система еще не создана
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
            sum_game = []
            for i in sf:  # цикл по таблице -system-
                stage.append(i.stage)  # добавляет в список этап
                table.append(i.label_string)  # добавляет в список система
                game.append(i.kol_game_string)  # добавляет в список кол-во игр
            count = len(game)
            for i in range(0, count):  # подсчитывает сумму игр
                txt = game[i]
                t = txt.find(" ")
                txt = int(txt[0:t])
                sum_game.append(txt)
                if i == 0:
                    my_win.label_9.setText(stage[0])
                    my_win.label_12.setText(table[0])
                    my_win.label_19.setText(game[0])
                    my_win.label_9.show()
                    my_win.label_12.show()
                    my_win.label_19.show()
                elif i == 1:
                    my_win.label_23.setText(stage[1])
                    my_win.label_27.setText(game[1])
                    my_win.label_28.setText(table[1])
                    my_win.label_23.show()
                    my_win.label_27.show()
                    my_win.label_28.show()
                elif i == 2:
                    my_win.label_32.setText(stage[2])
                    my_win.label_30.setText(game[2])
                    my_win.label_31.setText(table[2])
                    my_win.label_30.show()
                    my_win.label_31.show()
                    my_win.label_32.show()

            total_game = sum(sum_game)
            my_win.comboBox_table.hide()
            my_win.comboBox_page_vid.setEnabled(False)
            my_win.Button_etap_made.setEnabled(False)
            my_win.Button_system_made.setEnabled(False)
            my_win.label_33.setText(f"Всего {total_game} игр")
            my_win.label_33.show()
        load_tableWidget()
    elif tb == 3:  # вкладка -группы-
        my_win.checkBox_7.setChecked(False)
        my_win.checkBox_8.setChecked(False)
        flag = ready_choice()
        if flag is False:
            result = msgBox.information(my_win, "", "Необходимо сделать жеребьевку\nпредварительного этапа.",
                                        msgBox.StandardButtons.Ok, msgBox.StandardButtons.Cancel)
            if result != msgBox.StandardButtons.Ok:
                return
            else:
                my_win.tabWidget.setCurrentIndex(2)
                choice_gr_automat()
                sf.choice_flag = True
                sf.save()
            my_win.tabWidget.setCurrentIndex(3)
        else:  # жеребьевка сделана
            my_win.tableWidget.show()
            my_win.Button_Ok.setDisabled(True)
            load_combobox_filter_group()
            load_tableWidget()
            load_combo()
            match_score_db()  # флаг, показывающий записывать счет в партиях или нет
            my_win.label_16.hide()
    elif tb == 4:
        my_win.tableWidget.hide()
    elif tb == 5:
        my_win.checkBox_9.setChecked(False)
        my_win.checkBox_10.setChecked(False)
        my_win.tableWidget.show()
        my_win.Button_Ok_fin.setDisabled(False)
        load_combobox_filter_final()
        load_tableWidget()
        load_combo()
        match_score_db()
        my_win.label_16.hide()


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
            return
        else:
            cch = Coach(coach=ch, player_id=num).save()


def find_player_in_R():
    """если есть необходимость в поиске игрок в рейтинг листах январском или текущем"""
    pass


def sort(self):
    """сортировка таблицы QtableWidget (по рейтингу или по алфавиту)"""
    sender = my_win.sender()  # сигнал от кнопки

    if sender == my_win.Button_sort_R:  # в зависимости от сигала кнопки идет сортировка
        player_list = Player.select().where(Player.title_id == title_id()).order_by(Player.rank.desc())  # сортировка по рейтингу
    elif sender == my_win.Button_sort_Name:
        player_list = Player.select().where(Player.title_id == title_id()).order_by(Player.player)  # сортировка по алфавиту
    elif sender == my_win.Button_sort_mesto:
        player_list = Player.select().where(Player.title_id == title_id()).order_by(
            Player.mesto)  # сортировка по месту
    fill_table(player_list)
    list_player_pdf(player_list)


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
        title_str = title_string()
        nm = title_str[0]
        ds = title_str[3]
        de = title_str[4]
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


def list_player_pdf(player_list):
    """создание списка участников в pdf файл"""
    story = []  # Список данных таблицы участников
    elements = []  # Список Заголовки столбцов таблицы
    tit = Title.get(Title.id == title_id())

    gamer = tit.gamer
    count = len(player_list)  # количество записей в базе
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
              rowHeights=None)  # ширина столбцов, если None-автоматическая
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
    story.append(Paragraph(f'Список участников. {gamer}', h3))
    story.append(t)

    doc = SimpleDocTemplate("table_list.pdf", pagesize=A4)
    doc.build(story, onFirstPage=comp_system.func_zagolovok, onLaterPages=comp_system.func_zagolovok)


def exit_comp():
    """нажата кнопка -выход-"""
    msgBox = QMessageBox
    result = msgBox.question(my_win, "", "Вы действительно хотите выйти из программы?",
                             msgBox.StandardButtons.Ok, msgBox.StandardButtons.Cancel)
    if result == msgBox.StandardButtons.Ok:
        my_win.close()
        backup()
    else:
        pass


def system_competition():
    """выбор системы проведения"""
    sender = my_win.sender()
    flag_system = ready_system()
    if sender == my_win.systemAction or sender == my_win.choice_gr_Action or sender == my_win.tabWidget \
            or sender == my_win.toolBox or sender == my_win.system_edit_Action:
        # нажат меню -система- или -жеребьевка- или вкладка -система-
        if sender == my_win.system_edit_Action:
            sb = "Изменение системы проведения соревнования."
            my_win.statusbar.showMessage(sb)
            clear_db_before_edit()  # очищает таблицы перед новой системой соревнования (system, choice)
            my_win.spinBox_kol_group.hide()
            my_win.comboBox_etap_1.setEnabled(True)
            my_win.comboBox_etap_2.setEnabled(True)
            my_win.comboBox_etap_3.setEnabled(True)
            my_win.comboBox_etap_1.show()
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
            choice_tbl_made()  # заполнение db списком для жеребьевки
            my_win.tabWidget.setCurrentIndex(2)
        elif flag_system is True:
            flag_choice = ready_choice()
            if flag_choice is True:
                sb = "Система и жербьевка создана."
            elif flag_choice is False:
                sb = "Система создана, теперь необходимо произвести жеребьевку. " \
                     "Войдите в меню -соревнования- и выберите -жеребьевка-"
            my_win.statusbar.showMessage(sb)
        elif flag_system is False:
            sb = "Выбор системы проведения соревнования."
            my_win.statusbar.showMessage(sb)
            my_win.spinBox_kol_group.hide()
            my_win.comboBox_etap_1.setEnabled(True)
            my_win.comboBox_etap_2.setEnabled(True)
            my_win.comboBox_etap_3.setEnabled(True)
            my_win.comboBox_etap_1.show()
            my_win.comboBox_etap_2.hide()
            my_win.comboBox_etap_3.hide()
            my_win.label_10.hide()
            my_win.label_15.hide()
            my_win.label_17.hide()
            my_win.label_23.hide()
            my_win.label_27.hide()
            my_win.label_28.hide()
            my_win.comboBox_table.hide()
            player = Player.select().where(Player.title_id == title_id())
            count = len(player)
            if count != 0:
                choice_tbl_made()  # заполнение db списком для жеребъевки
                my_win.tabWidget.setCurrentIndex(2)
            else:
                reply = QMessageBox.information(my_win, 'Уведомление',
                                                "У Вас нет ни одного спортсмена.\nСначала необходимо создать "
                                                "список участников соревнований.\n Перейти к созданию списка?",
                                                QMessageBox.StandardButtons.Ok,
                                                QMessageBox.StandardButtons.Cancel)
                if reply == QMessageBox.StandardButtons.Ok:
                    my_win.tabWidget.setCurrentIndex(1)
                    my_win.lineEdit_Family_name.setFocus()
                else:
                    return
    elif sender == my_win.tabWidget:
        my_win.spinBox_kol_group.hide()
        my_win.comboBox_etap_1.setEnabled(True)
        my_win.comboBox_etap_2.setEnabled(True)
        my_win.comboBox_etap_3.setEnabled(True)
        my_win.comboBox_etap_1.show()
        my_win.comboBox_etap_2.hide()
        my_win.comboBox_etap_3.hide()
        my_win.label_10.show()
        my_win.label_15.hide()
        my_win.label_17.hide()
    elif sender == my_win.comboBox_etap_1:
        ct = my_win.comboBox_etap_1.currentText()
        if ct == "Одна таблица":
            my_win.comboBox_one_table.show()
            my_win.spinBox_kol_group.hide()
            my_win.label_11.hide()
            my_win.label_9.hide()
        elif ct == "Предварительный":
            my_win.spinBox_kol_group.show()
            my_win.comboBox_one_table.hide()
            my_win.label_9.show()
            my_win.label_9.setText("Предварительный этап")
            my_win.label_11.show()
            my_win.label_12.hide()
            my_win.comboBox_page_vid.setEnabled(True)
    elif sender == my_win.comboBox_etap_2:
        my_win.label_23.show()
        my_win.label_27.hide()
        my_win.label_28.hide()
        my_win.comboBox_table.show()
    elif sender == my_win.comboBox_etap_3:
        my_win.label_32.show()
        my_win.label_30.hide()
        my_win.label_31.hide()
        my_win.comboBox_table_2.show()
    else:  # скрывает и выключает label и combobox этапов систем
        my_win.label_10.hide()
        my_win.label_15.hide()
        my_win.label_17.hide()
        my_win.comboBox_etap_1.setEnabled(False)
        my_win.comboBox_etap_2.setEnabled(False)
        my_win.comboBox_etap_3.setEnabled(False)


def one_table():
    """система соревнований из одной таблицы запись в System"""
    if my_win.comboBox_one_table.currentText() == "Круговая система":
        t_id = title_id()
        system = System.get(System.title_id == t_id)
        sys_id = system.id
        player = Player.select().where(Player.title_id == t_id)
        count = len(player)
        kol_game = count // 2 * (count - 1)
    load_tableWidget()
    stage = my_win.comboBox_etap_1.currentText()
    choice = Choice.select().where(Choice.title_id == t_id)
    for i in choice:
        i.basic = stage
        i.save()
    sg = my_win.comboBox_one_table.currentText()
    pl_choice = Choice.select().where(Choice.title_id == t_id)
    page_v = my_win.comboBox_page_vid.currentText()
    string_table = my_win.label_50.text()
    player_choice = pl_choice.select().order_by(Choice.rank.desc())
    system.title_id = t_id
    system.total_athletes = count
    system.total_group = 1
    system.stage = sg
    system.label_string = string_table
    system.kol_game_string = kol_game
    system.page_vid = page_v
    system.save()


def kol_player_in_group():
    """подсчет кол-во групп и человек в группах"""
    sender = my_win.sender()  # сигнал от кнопки
    gamer = my_win.lineEdit_title_gamer.text()
    kg = my_win.spinBox_kol_group.text()  # количество групп
    player_list = Player.select().where(Player.title_id == title_id())
    count = len(player_list)  # количество записей в базе
    e1 = int(count) % int(kg)  # остаток отделения, если 0, то участники равно делится на группы
    p = int(count) // int(kg)  # если количество участников равно делится на группы (кол-во групп)
    g1 = int(kg) - e1  # кол-во групп, где наименьшее кол-во спортсменов
    p2 = str(p + 1)  # кол-во человек в группе с наибольшим их количеством
    if e1 == 0:  # то в группах равное количество человек -e1-
        stroka_kol_group = f"{kg} группы по {str(p)} чел."
        skg = int((p * (p - 1) / 2) * int(kg))
        mp = p
    else:
        stroka_kol_group = f"{str(g1)} групп(а) по {str(p)} чел. и {str(e1)} групп(а) по {str(p2)} чел."
        p = int(p)
        skg = int((((p * (p - 1)) / 2 * g1) + ((p * (p - 1)) / 2 * e1)))
        mp = p2
    stroka_kol_game = f"{skg} игр"
    my_win.label_11.hide()
    my_win.label_12.setText(stroka_kol_group)
    my_win.label_12.show()
    my_win.label_19.setText(stroka_kol_game)
    my_win.label_19.show()
    my_win.Button_etap_made.setEnabled(True)
    if sender == my_win.Button_etap_made:
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
        # view_file = "setka_16_1_финал.pdf"
    elif tw == 1:
        view_file = "table_list.pdf"
    elif tw == 2:
        pass
    elif tw == 3:  # вкладка группы
        view_file = "table_group.pdf"
    elif tw == 4:
        pass
    elif tw == 5:
        view_file = "setka_16_1_финал.pdf"
    os.system(f"open {view_file}")


def player_in_setka(fin):
    """заполняет таблицу Game_list данными спортсменами из сетки tds - список списков данных из сетки, а затем
    заполняет таблицу -Result-"""
    t = Title.select().order_by(Title.id.desc()).get()  # получение id последнего соревнования
    s = System.select().order_by(System.id).where(System.title_id == t)  # находит system id последнего
    count = len(s)
    for i in s:  # перебирает в цикле строки в табл System где последний titul_id
        if i.stage == fin:
            mp = i.max_player
            mg = i.kol_game_string
    space = mg.find(" ")
    game = int(mg[:space])
    sd_full = []
    sd = []
    tds = comp_system.setka_16_made(fin)  # создание сетки со спортсменами согласно жеребьевки
    for r in tds:
        if r != "bye":
            space = r.find(" ")  # находит пробел перед именем
            symbol = r.find("/")  # находит черту отделяющий город
            sl = r[:space + 2]  # удаляет все после пробела кроме первой буквы имени
            sl_full = r[:symbol]
            family = f'{sl}.'  # добавляет точку к имени
            sd.append(family)
            sd_full.append(sl_full)
        else:
            sd.append(r)
            sd_full.append(r)
    k = 0
    for i in range(1, mp + 1):  # записывает в Game_List спортсменов участников сетки
        family_player = sd[i - 1]
        k += 1
        with db:
            game_list = Game_list(number_group=fin, rank_num_player=k, player_group=family_player,
                                  system_id=s).save()
    st = "Финальный"
    for i in range(1, mp // 2 + 1):  # присваивает встречи 1-ого тура и записывает в тбл Results
        num_game = i
        pl1 = sd_full[i * 2 - 2]
        pl2 = sd_full[i * 2 - 1]
        if pl1 is not None and pl2 is not None:
            with db:
                results = Result(number_group=fin, system_stage=st, player1=pl1, player2=pl2,
                                 tours=num_game, title_id=s).save()
    for i in range(mp // 2 + 1, game + 1):  # дополняет номера будущих встреч
        pl1 = ""
        pl2 = ""
        with db:
            results = Result(number_group=fin, system_stage=st, player1=pl1, player2=pl2,
                             tours=i, title_id=s).save()


def player_in_table():
    """заполняет таблицу Game_list данными спортсменами из группы td - список списков данных из групп"""
    gamer = my_win.lineEdit_title_gamer.text()
    s = System.select().where(System.title_id == title_id()).get()  # находит system id последнего
    kg = s.total_group
    st = s.stage
    pv = s.page_vid
    comp_system.table_made(pv, title_id())  # создание таблиц групп со спортсменами согласно жеребьевки
    tdt = tbl_data.table_data(kg, title_id())  # вызов функции, где получаем список всех участников по группам
    for p in range(0, kg):  # цикл заполнения db таблиц -game list- и  -Results-
        gr = tdt[p]
        count_player = len(gr) // 2  # максимальное кол-во участников в группе
        number_group = str(p + 1) + ' группа'
        k = 0  # кол-во спортсменов в группе
        for i in range(0, count_player * 2 - 1, 2):
            family_player = gr[i][1]  # фамилия игрока
            fp = len(family_player)  # подсчет кол-во знаков в фамилия, если 0 значит игрока нет
            if fp > 0:  # если строка (фамилия игрока) не пустая идет запись в db
                k += 1
                with db:
                    game_list = Game_list(number_group=number_group, rank_num_player=k, player_group=family_player,
                                          system_id=s).save()
        if fp == 0 and k != 0 or k == count_player:  # если 1-я строка (фамилия игрока) пустая выход из группы
            cp = k - 3
            tour = comp_system.tour(cp)
            if cp == 0:
                kol_tours = 1
            else:
                kol_tours = len(tour)  # кол-во туров
            game = len(tour[0])  # кол-во игр в туре
            for r in range(0, kol_tours):
                tours = tour[r]  # игры тура
                for d in range(0, game):  # цикл по играм тура
                    if game == 3:  # если в группе 3 человека
                        match = tour[d]  # матч в туре
                    else:  # в группе более 3 спортсменов
                        match = tours[d]  # матч в туре
                        znak = match.find("-")
                    first = int(match[:znak])  # игрок под номером в группе
                    second = int(match[znak + 1:])  # игрок под номером в группе
                    pl1 = gr[first * 2 - 2][1]  # фамилия первого игрока
                    pl2 = gr[second * 2 - 2][1]  # фамилия второго игрока
                    with db:
                        results = Result(number_group=number_group, system_stage=st, player1=pl1, player2=pl2,
                                         tours=match, title_id=title_id()).save()


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


def match_score_db():
    """кол-во партий и запись счета партий по умолчанию в db"""
    etap = []
    kol_set = []
    gamer = my_win.lineEdit_title_gamer.text()
    tab = my_win.tabWidget.currentIndex()
    system = System.select().where(System.title_id == title_id())

    for i in system:
        e = i.stage
        etap.append(e)  # получает список этапов на данных соревнованиях

    if tab == 3:
        fir_e = "Предварительный"
        flag = e in etap
        if flag == True:
            sf = system.select().where(System.stage == fir_e).get()
            match = sf.score_flag
            state = sf.visible_game  # флаг, показывающий записывать счет в партиях или нет

        if state is False:  # изменяет состояние на Bool в зависимости от цифрового кода CheckBox
            my_win.checkBox_4.setChecked(False)
        elif state is True:
            my_win.checkBox_4.setChecked(True)

        if my_win.radioButton_match_3.isChecked():
            kol_set.append(3)
        else:
            kol_set.append(0)
        if my_win.radioButton_match_5.isChecked():
            kol_set.append(5)
        else:
            kol_set.append(0)
        if my_win.radioButton_match_7.isChecked():
            kol_set.append(7)
        else:
            kol_set.append(0)
        for i in range(0, 3):
            if kol_set[i] > 0:
                match_check = kol_set[i]
                break
            else:
                match_check = 0
        if match_check == 0:
            if match == 3:
                my_win.radioButton_match_3.setChecked(True)  # устанавливает галочку
            elif match == 5:
                my_win.radioButton_match_5.setChecked(True)  # устанавливает галочку
            elif match == 7:
                my_win.radioButton_match_7.setChecked(True)  # устанавливает галочку
        elif match != match_check:
            with db:
                sf.score_flag = match_check
                sf.save()
            match = match_check
        state_check = state
        game_in_visible(state_check, match)
    elif tab == 4:  # вкладка -полуфиналы-
        pass
    else:  # вкладка -финалы-
        fir_e = "1-й финал"
        flag = e in etap
        if flag == True:
            sf = system.select().where(System.stage == fir_e).get()
            match = sf.score_flag
            state = sf.visible_game  # флаг, показывающий записывать счет в партиях или нет
        if state is False:  # изменяет состояние на Bool в зависимости от цифрового кода CheckBox
            my_win.checkBox_5.setChecked(False)
        elif state is True:
            my_win.checkBox_5.setChecked(True)
        if my_win.radioButton_match_4.isChecked():
            kol_set.append(3)
        else:
            kol_set.append(0)
        if my_win.radioButton_match_6.isChecked():
            kol_set.append(5)
        else:
            kol_set.append(0)
        if my_win.radioButton_match_8.isChecked():
            kol_set.append(7)
        else:
            kol_set.append(0)
        for i in range(0, 3):
            if kol_set[i] > 0:
                match_check = kol_set[i]
                break
            else:
                match_check = 0
        if match_check == 0:
            if match == 3:
                my_win.radioButton_match_4.setChecked(True)  # устанавливает галочку
            elif match == 5:
                my_win.radioButton_match_6.setChecked(True)  # устанавливает галочку
            elif match == 7:
                my_win.radioButton_match_8.setChecked(True)  # устанавливает галочку
        elif match != match_check:
            with db:
                sf.score_flag = match_check
                sf.save()
            match = match_check
        state_check = state
        game_in_visible(state_check, match)


def game_in_visible(state_check, match=5, final="1-й финал"):
    """видимость полей для счета в партии, flag показывает из скольки партий играется матч,
    state_check - нажат чекбокс (видимость полей счета или нет), если 2 значит нажат"""

    tab = my_win.tabWidget.currentIndex()
    gamer = my_win.lineEdit_title_gamer.text()
    sf = System.get(System.title_id == title_id())

    if tab == 3:
        state = sf.visible_game
        if state_check == 0:  # изменяет состояние на Bool в зависимости от цифрового кода CheckBox
            state_check = False
            my_win.checkBox_4.setChecked(False)
        elif state_check == 2:
            state_check = True
            my_win.checkBox_4.setChecked(True)
        if state != state_check:
            with db:
                sf.visible_game = state_check
                sf.save()
            state = sf.visible_game
    elif tab == 4:
        pass
    elif tab == 5:
        r = my_win.tableWidget.currentRow()
        if r == -1 or r == 0:
            final == "1-й финал"
        else:
            final = my_win.tableWidget.item(r, 2).text()  # из какого финала пара игроков в данный момент
        system = sf.get(System.stage == final)
        state = system.visible_game
        if state_check == 0 or state_check is False:  # изменяет состояние на Bool в зависимости от цифрового кода CheckBox
            state_check = False
            my_win.checkBox_5.setChecked(False)
        elif state_check == 2:
            state_check = True
            my_win.checkBox_5.setChecked(True)
        if state != state_check:
            with db:
                system.visible_game = state_check
                system.save()
            state = system.visible_game

    if state is False:
        my_win.lineEdit_pl1_s1_fin.setVisible(False)
        my_win.lineEdit_pl2_s1_fin.setVisible(False)
        my_win.lineEdit_pl1_s2_fin.setVisible(False)
        my_win.lineEdit_pl2_s2_fin.setVisible(False)
        my_win.lineEdit_pl1_s3_fin.setVisible(False)
        my_win.lineEdit_pl2_s3_fin.setVisible(False)
        my_win.lineEdit_pl1_s4_fin.setVisible(False)
        my_win.lineEdit_pl2_s4_fin.setVisible(False)
        my_win.lineEdit_pl1_s5_fin.setVisible(False)
        my_win.lineEdit_pl2_s5_fin.setVisible(False)
        my_win.lineEdit_pl1_s6_fin.setVisible(False)
        my_win.lineEdit_pl2_s6_fin.setVisible(False)
        my_win.lineEdit_pl1_s7_fin.setVisible(False)
        my_win.lineEdit_pl2_s7_fin.setVisible(False)
        my_win.label_22.setVisible(False)
    else:
        if tab == 3:  # вкладка -группы- проверка какая стоит галочка (сколько партий)
            if my_win.radioButton_match_3.isChecked():
                match = 3
                my_win.lineEdit_pl1_s1.setVisible(True)
                my_win.lineEdit_pl2_s1.setVisible(True)
                my_win.lineEdit_pl1_s2.setVisible(True)
                my_win.lineEdit_pl2_s2.setVisible(True)
                my_win.lineEdit_pl1_s3.setVisible(True)
                my_win.lineEdit_pl2_s3.setVisible(True)
                my_win.lineEdit_pl1_s4.setVisible(False)
                my_win.lineEdit_pl2_s4.setVisible(False)
                my_win.lineEdit_pl1_s5.setVisible(False)
                my_win.lineEdit_pl2_s5.setVisible(False)
                my_win.lineEdit_pl1_s6.setVisible(False)
                my_win.lineEdit_pl2_s6.setVisible(False)
                my_win.lineEdit_pl1_s7.setVisible(False)
                my_win.lineEdit_pl2_s7.setVisible(False)
            elif my_win.radioButton_match_5.isChecked():
                match = 5
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
                my_win.lineEdit_pl1_s6.setVisible(False)
                my_win.lineEdit_pl2_s6.setVisible(False)
                my_win.lineEdit_pl1_s7.setVisible(False)
                my_win.lineEdit_pl2_s7.setVisible(False)
            elif my_win.radioButton_match_7.isChecked():
                match = 7
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
                my_win.lineEdit_pl1_s6.setVisible(True)
                my_win.lineEdit_pl2_s6.setVisible(True)
                my_win.lineEdit_pl1_s7.setVisible(True)
                my_win.lineEdit_pl2_s7.setVisible(True)
            my_win.label_22.setVisible(True)
        elif tab == 4:
            pass
        else:
            if my_win.radioButton_match_4.isChecked():
                match = 3
                my_win.lineEdit_pl1_s1_fin.setVisible(True)
                my_win.lineEdit_pl2_s1_fin.setVisible(True)
                my_win.lineEdit_pl1_s2_fin.setVisible(True)
                my_win.lineEdit_pl2_s2_fin.setVisible(True)
                my_win.lineEdit_pl1_s3_fin.setVisible(True)
                my_win.lineEdit_pl2_s3_fin.setVisible(True)
                my_win.lineEdit_pl1_s4_fin.setVisible(False)
                my_win.lineEdit_pl2_s4_fin.setVisible(False)
                my_win.lineEdit_pl1_s5_fin.setVisible(False)
                my_win.lineEdit_pl2_s5_fin.setVisible(False)
                my_win.lineEdit_pl1_s6_fin.setVisible(False)
                my_win.lineEdit_pl2_s6_fin.setVisible(False)
                my_win.lineEdit_pl1_s7_fin.setVisible(False)
                my_win.lineEdit_pl2_s7_fin.setVisible(False)
            elif my_win.radioButton_match_6.isChecked():
                match = 5
                my_win.lineEdit_pl1_s1_fin.setVisible(True)
                my_win.lineEdit_pl2_s1_fin.setVisible(True)
                my_win.lineEdit_pl1_s2_fin.setVisible(True)
                my_win.lineEdit_pl2_s2_fin.setVisible(True)
                my_win.lineEdit_pl1_s3_fin.setVisible(True)
                my_win.lineEdit_pl2_s3_fin.setVisible(True)
                my_win.lineEdit_pl1_s4_fin.setVisible(True)
                my_win.lineEdit_pl2_s4_fin.setVisible(True)
                my_win.lineEdit_pl1_s5_fin.setVisible(True)
                my_win.lineEdit_pl2_s5_fin.setVisible(True)
                my_win.lineEdit_pl1_s6_fin.setVisible(False)
                my_win.lineEdit_pl2_s6_fin.setVisible(False)
                my_win.lineEdit_pl1_s7_fin.setVisible(False)
                my_win.lineEdit_pl2_s7_fin.setVisible(False)
            elif my_win.radioButton_match_8.isChecked():
                match = 7
                my_win.lineEdit_pl1_s1_fin.setVisible(True)
                my_win.lineEdit_pl2_s1_fin.setVisible(True)
                my_win.lineEdit_pl1_s2_fin.setVisible(True)
                my_win.lineEdit_pl2_s2_fin.setVisible(True)
                my_win.lineEdit_pl1_s3_fin.setVisible(True)
                my_win.lineEdit_pl2_s3_fin.setVisible(True)
                my_win.lineEdit_pl1_s4_fin.setVisible(True)
                my_win.lineEdit_pl2_s4_fin.setVisible(True)
                my_win.lineEdit_pl1_s5_fin.setVisible(True)
                my_win.lineEdit_pl2_s5_fin.setVisible(True)
                my_win.lineEdit_pl1_s6_fin.setVisible(True)
                my_win.lineEdit_pl2_s6_fin.setVisible(True)
                my_win.lineEdit_pl1_s7_fin.setVisible(True)
                my_win.lineEdit_pl2_s7_fin.setVisible(True)
            my_win.label_40.setVisible(True)


def select_player_in_list():
    """выводит данные игрока в поля редактирования или удаления"""
    r = my_win.tableWidget.currentRow()
    # family = my_win.tableWidget.item(r, 2).text()
    # birthday = my_win.tableWidget.item(r, 3).text()
    # rank = my_win.tableWidget.item(r, 4).text()
    # city = my_win.tableWidget.item(r, 5).text()
    # region = my_win.tableWidget.item(r, 6).text()
    # rn = len(region)
    # razrayd = my_win.tableWidget.item(r, 7).text()
    # coach = my_win.tableWidget.item(r, 8).text()
#========================
    family = my_win.tableWidget.item(r, 1).text()
    birthday = my_win.tableWidget.item(r, 2).text()
    rank = my_win.tableWidget.item(r, 3).text()
    city = my_win.tableWidget.item(r, 4).text()
    region = my_win.tableWidget.item(r, 5).text()
    rn = len(region)
    razrayd = my_win.tableWidget.item(r, 6).text()
    coach = my_win.tableWidget.item(r, 7).text()
#================================
    my_win.lineEdit_Family_name.setText(family)
    my_win.lineEdit_bday.setText(birthday)
    my_win.lineEdit_R.setText(rank)
    my_win.lineEdit_city_list.setText(city)
    my_win.comboBox_region.setCurrentText(region)
    my_win.comboBox_razryad.setCurrentText(razrayd)
    my_win.lineEdit_coach.setText(coach)
    my_win.Button_add_edit_player.setEnabled(True)
    if my_win.checkBox_6.isChecked(): # отмечен флажок -удаленные-
        my_win.Button_del_player.setEnabled(False)
        my_win.Button_add_edit_player.setText("Восстановить")
    else:
        my_win.Button_del_player.setEnabled(True)
        my_win.Button_add_edit_player.setEnabled(True)
        my_win.Button_add_edit_player.setText("Редактировать")


def select_player_in_game():
    """выводит фамилии игроков встречи"""
    tab = my_win.tabWidget.currentIndex()
    r = my_win.tableWidget.currentRow()

    if tab == 1:
        select_player_in_list()
    elif tab == 3:  # вкладка -группы-
        fin = System.get(System.title_id == title_id() and System.stage == "Предварительный")
        state_check = fin.visible_game
        game_in_visible(state_check=state_check)
    elif tab == 4:
        pass
    elif tab == 5:  # вкладка -финалы-
        final = my_win.tableWidget.item(r, 2).text()  # из какого финала пара игроков в данный момент
        fin = System.get(System.title_id == title_id() and System.stage == final)
        state_check = fin.visible_game
        game_in_visible(state_check=state_check, final=final)

    if tab == 3 or tab == 4 or tab == 5:
        win_pole = my_win.tableWidget.item(r, 6).text()  # поле победителя (если заполнено, значит встреча сыграна)
        if win_pole != "None" and win_pole != "":  # если встреча сыграна, то заполняет поля общий счет
            sc = my_win.tableWidget.item(r, 8).text()
            pl1 = my_win.tableWidget.item(r, 4).text()
            pl2 = my_win.tableWidget.item(r, 5).text()
            if pl1 == my_win.tableWidget.item(r, 6).text():
                if sc != "": # если в сетке недостающие игроки (bye), то нет счета
                    sc1 = sc[0]
                    sc2 = sc[4]
                else:  # оставляет поля общий счет пустыми
                    sc1 = ""
                    sc2 = ""
            else:
                if sc != "":  # если в сетке недостающие игроки (bye), то нет счета
                    sc1 = sc[4]
                    sc2 = sc[0]
                else:
                    sc1 = ""
                    sc2 = ""
            if tab == 3:
                my_win.lineEdit_pl1_score_total.setText(sc1)
                my_win.lineEdit_pl2_score_total.setText(sc2)
                my_win.lineEdit_player1.setText(pl1)
                my_win.lineEdit_player2.setText(pl2)
                my_win.lineEdit_pl1_s1.setFocus()
            elif tab == 4:
                pass
            else:
                my_win.lineEdit_pl1_score_total_fin.setText(sc1)
                my_win.lineEdit_pl2_score_total_fin.setText(sc2)
                my_win.lineEdit_player1_fin.setText(pl1)
                my_win.lineEdit_player2_fin.setText(pl2)
                my_win.lineEdit_pl1_s1_fin.setFocus()
        else:
            pl1 = my_win.tableWidget.item(r, 4).text()
            pl2 = my_win.tableWidget.item(r, 5).text()
            if tab == 3:
                my_win.checkBox_7.setEnabled(True)
                my_win.checkBox_8.setEnabled(True)
                my_win.lineEdit_player1.setText(pl1)
                my_win.lineEdit_player2.setText(pl2)
                my_win.lineEdit_pl1_s1.setFocus()
            elif tab == 4:
                pass
            elif tab == 5:
                my_win.lineEdit_player1_fin.setText(pl1)
                my_win.lineEdit_player2_fin.setText(pl2)
                my_win.lineEdit_pl1_s1_fin.setFocus()
        my_win.tableWidget.selectRow(r)


def delete_player():
    """удаляет игрока из списка и заносит его в архив"""
    msgBox = QMessageBox
    t_id = title_id()
    r = my_win.tableWidget.currentRow()
#=================
    player_del = my_win.tableWidget.item(r, 1).text()
    player_id = Player.get(Player.player == player_del)
    birthday = my_win.tableWidget.item(r, 2).text()
    rank = my_win.tableWidget.item(r, 3).text()
    player_city_del = my_win.tableWidget.item(r, 4).text()
    region = my_win.tableWidget.item(r, 5).text()
    razryad = my_win.tableWidget.item(r, 6).text()
    coach = my_win.tableWidget.item(r, 7).text()
    full_name = f"{player_del}/ {player_city_del}"
#=================
    coach_id = Coach.get(Coach.coach == coach)
    result = msgBox.question(my_win, "", f"Вы действительно хотите удалить\n"
                                         f" {player_del} город {player_city_del}?",
                             msgBox.StandardButtons.Ok, msgBox.StandardButtons.Cancel)
    if result == msgBox.StandardButtons.Ok:
        with db:
            del_player = Delete_player(player_del_id=player_id, bday=birthday, rank=rank, city=player_city_del,
                                       region=region, razryad=razryad, coach_id=coach_id, full_name =full_name,
                                       player=player_del, title_id=t_id).save()

            player = Player.get(Player.player == my_win.tableWidget.item(r, 1).text())
            player.delete_instance()
        my_win.lineEdit_Family_name.clear()
        my_win.lineEdit_bday.clear()
        my_win.lineEdit_R.clear()
        my_win.lineEdit_city_list.clear()
        my_win.lineEdit_coach.clear()
        # load_tableWidget()
        player_list = Player.select().where(Player.title_id == title_id())
        count = len(player_list)
        my_win.label_46.setText(f"Всего: {count} участников")
    else:
        return


def focus():
    """переводит фокус на следующую позицию
    sum_total_game список (1-й колво очков которые надо набрать, 2-й сколько уже набрали)"""
    msgBox = QMessageBox
    sender = my_win.sender()  # в зависимости от сигала кнопки идет сортировка
    system = System.select().where(System.title_id == title_id())
    tab = my_win.tabWidget.currentIndex()
    if tab == 3:
        sys = system.select().where(System.stage == "Предварительный").get()
        sf = sys.score_flag  # флаг из скольки партий играется матч
        if sender == my_win.lineEdit_pl1_s1:
            if my_win.lineEdit_pl1_s1.text() == "":
                msgBox.critical(my_win, "", "Ошибка при вводе счета!")
                my_win.lineEdit_pl1_s1.setFocus()
            else:
                 my_win.lineEdit_pl2_s1.setFocus()
        elif sender == my_win.lineEdit_pl2_s1:
            if my_win.lineEdit_pl2_s1.text() == "":
                msgBox.critical(my_win, "", "Ошибка при вводе счета!")
                my_win.lineEdit_pl2_s1.setFocus()
            else:
                sum_total_game = score_in_game()  # подсчет очков в партии
                my_win.lineEdit_pl1_s2.setFocus()
        elif sender == my_win.lineEdit_pl1_s2:
            if my_win.lineEdit_pl1_s2.text() == "":
                msgBox.critical(my_win, "", "Ошибка при вводе счета!")
                my_win.lineEdit_pl1_s2.setFocus()
            else:
                my_win.lineEdit_pl2_s2.setFocus()
        elif sender == my_win.lineEdit_pl2_s2:  # нажал ентер на счете 2-ого игрока 2-й партии
            if my_win.lineEdit_pl2_s2.text() == "":
                msgBox.critical(my_win, "", "Ошибка при вводе счета!")
                my_win.lineEdit_pl2_s2.setFocus()
            else:
                sum_total_game = score_in_game()
                if sum_total_game[0] != sum_total_game[1]:
                    my_win.lineEdit_pl1_s3.setFocus()
                else:
                    my_win.Button_Ok.setFocus()
        elif sender == my_win.lineEdit_pl1_s3:
            if my_win.lineEdit_pl1_s3.text() == "":
                msgBox.critical(my_win, "", "Ошибка при вводе счета!")
                my_win.lineEdit_pl1_s3.setFocus()
            else:
                my_win.lineEdit_pl2_s3.setFocus()
        elif sender == my_win.lineEdit_pl2_s3:  # нажал ентер на счете 2-ого игрока 3-й партии
            if my_win.lineEdit_pl2_s3.text() == "":
                msgBox.critical(my_win, "", "Ошибка при вводе счета!")
                my_win.lineEdit_pl2_s3.setFocus()
            else:
                sum_total_game = score_in_game()
                if sum_total_game[0] != sum_total_game[1]:
                    my_win.lineEdit_pl1_s4.setFocus()
                else:
                    my_win.Button_Ok.setFocus()
        elif sender == my_win.lineEdit_pl1_s4:
            if my_win.lineEdit_pl1_s4.text() == "":
                msgBox.critical(my_win, "", "Ошибка при вводе счета!")
                my_win.lineEdit_pl1_s4.setFocus()
            else:
                my_win.lineEdit_pl2_s4.setFocus()
        elif sender == my_win.lineEdit_pl2_s4:  # нажал ентер на счете 2-ого игрока 4-й партии
            if my_win.lineEdit_pl2_s4.text() == "":
                msgBox.critical(my_win, "", "Ошибка при вводе счета!")
                my_win.lineEdit_pl2_s4.setFocus()
            else:
                sum_total_game = score_in_game()
                if sum_total_game[0] != sum_total_game[1]:
                    my_win.lineEdit_pl1_s5.setFocus()
                else:
                    my_win.Button_Ok.setFocus()
        elif sender == my_win.lineEdit_pl1_s5:
            if my_win.lineEdit_pl1_s5.text() == "":
                msgBox.critical(my_win, "", "Ошибка при вводе счета!")
                my_win.lineEdit_pl1_s5.setFocus()
            else:
                my_win.lineEdit_pl2_s5.setFocus()
        elif sender == my_win.lineEdit_pl2_s5:  # нажал ентер на счете 2-ого игрока 5-й партии
            if my_win.lineEdit_pl2_s5.text() == "":
                msgBox.critical(my_win, "", "Ошибка при вводе счета!")
                my_win.lineEdit_pl2_s5.setFocus()
            else:
                sum_total_game = score_in_game()
                if sum_total_game[0] != sum_total_game[1]:
                    my_win.Button_Ok.setFocus()
                else:
                    my_win.Button_Ok.setFocus()
    elif tab == 5:
        r = my_win.tableWidget.currentRow()
        final = my_win.tableWidget.item(r, 2).text()  # из какого финала пара игроков в данный момент
        sys = system.select().where(System.stage == final).get()
        sf = sys.score_flag  # флаг из скольки партий играется матч
        if sender == my_win.lineEdit_pl1_s1_fin:  # 1-й игрок 1-я партия
            if my_win.lineEdit_pl1_s1_fin.text() == "":
                msgBox.critical(my_win, "", "Ошибка при вводе счета!")
                my_win.lineEdit_pl1_s1_fin.setFocus()
            else:
                my_win.lineEdit_pl2_s1_fin.setFocus()
        elif sender == my_win.lineEdit_pl2_s1_fin:  # 2-й игрок 1-я партия
            if my_win.lineEdit_pl2_s1_fin.text() == "":
                msgBox.critical(my_win, "", "Ошибка при вводе счета!")
                my_win.lineEdit_pl2_s1_fin.setFocus()
            else:
                sum_total_game = score_in_game()  # подсчет очков в партии
                my_win.lineEdit_pl1_s2_fin.setFocus()
        elif sender == my_win.lineEdit_pl1_s2_fin:  # нажал ентер на счете 2-ого игрока 2-й партии
            if my_win.lineEdit_pl1_s2_fin.text() == "":
                msgBox.critical(my_win, "", "Ошибка при вводе счета!")
                my_win.lineEdit_pl1_s2_fin.setFocus()
            else:
                my_win.lineEdit_pl2_s2_fin.setFocus()
        elif sender == my_win.lineEdit_pl2_s2_fin:
            if my_win.lineEdit_pl2_s2_fin.text() == "":
                msgBox.critical(my_win, "", "Ошибка при вводе счета!")
                my_win.lineEdit_pl2_s2_fin.setFocus()
            else:
                sum_total_game = score_in_game()  # подсчет очков в партии
                # ====================
                count = len(sum_total_game)
                if count == 0:
                    my_win.lineEdit_pl2_s2_fin.setFocus()
                else:
                # =====================
                    if sum_total_game[0] != sum_total_game[1]:
                        my_win.lineEdit_pl1_s3_fin.setFocus()  # переводит фокус на следующее поле
                    else:
                        my_win.Button_Ok_fin.setFocus()  # переводит фокус на кнопку -ОК-
        elif sender == my_win.lineEdit_pl1_s3_fin:
            if my_win.lineEdit_pl1_s3_fin.text() == "":
                msgBox.critical(my_win, "", "Ошибка при вводе счета!")
                my_win.lineEdit_pl1_s3_fin.setFocus()
            else:
                my_win.lineEdit_pl2_s3_fin.setFocus()
        elif sender == my_win.lineEdit_pl2_s3_fin:  # нажал ентер на счете 2-ого игрока 3-й партии
            if my_win.lineEdit_pl2_s3_fin.text() == "":
                msgBox.critical(my_win, "", "Ошибка при вводе счета!")  # если забыл написать счет и нажал ентер
                my_win.lineEdit_pl2_s3_fin.setFocus()
            else:
                sum_total_game = score_in_game()  # подсчет очков в партии
                #====================
                count = len(sum_total_game)
                if count == 0:
                    my_win.lineEdit_pl2_s3_fin.setFocus()
                else:
                #=====================
                    if sum_total_game[0] != sum_total_game[1]:
                        my_win.lineEdit_pl1_s4_fin.setFocus()
                    else:
                        my_win.Button_Ok_fin.setFocus()
        elif sender == my_win.lineEdit_pl1_s4_fin:
            if my_win.lineEdit_pl1_s4_fin.text() == "":
                msgBox.critical(my_win, "", "Ошибка при вводе счета!")
                my_win.lineEdit_pl1_s4_fin.setFocus()
            else:
                my_win.lineEdit_pl2_s4_fin.setFocus()
        elif sender == my_win.lineEdit_pl2_s4_fin:  # нажал ентер на счете 2-ого игрока 4-й партии
            if my_win.lineEdit_pl2_s4_fin.text() == "":
                msgBox.critical(my_win, "", "Ошибка при вводе счета!")
                my_win.lineEdit_pl2_s4_fin.setFocus()
            else:
                sum_total_game = score_in_game()  # подсчет очков в партии
                # ====================
                count = len(sum_total_game)
                if count == 0:
                    my_win.lineEdit_pl2_s4_fin.setFocus()
                else:
                # =====================
                    if sum_total_game[0] != sum_total_game[1]:
                        my_win.lineEdit_pl1_s5_fin.setFocus()
                    else:
                        my_win.Button_Ok_fin.setFocus()
        elif sender == my_win.lineEdit_pl1_s5_fin:
            if my_win.lineEdit_pl1_s5_fin.text() == "":
                msgBox.critical(my_win, "", "Ошибка при вводе счета!")
                my_win.lineEdit_pl1_s5_fin.setFocus()
            else:
                my_win.lineEdit_pl2_s5_fin.setFocus()
        elif sender == my_win.lineEdit_pl2_s5_fin:  # нажал ентер на счете 2-ого игрока 5-й партии
            if my_win.lineEdit_pl2_s5_fin.text() == "":
                msgBox.critical(my_win, "", "Ошибка при вводе счета!")
                my_win.lineEdit_pl2_s5_fin.setFocus()
            else:
                sum_total_game = score_in_game()  # подсчет очков в партии
                # ====================
                count = len(sum_total_game)
                if count == 0:
                    my_win.lineEdit_pl2_s5_fin.setFocus()
                else:
                # =====================
                    if sum_total_game[0] != sum_total_game[1]:
                        my_win.lineEdit_pl1_s5_fin.setFocus()
                    else:
                        my_win.Button_Ok_fin.setFocus()


def score_in_game():
    """считает общий счет в партиях"""
    msgBox = QMessageBox
    # =================
    system = System.select().where(System.title_id == title_id())
    #====================
    total_score = []
    ts1 = []
    ts2 = []
    total_game = []
    sum_total_game = []
    tab = my_win.tabWidget.currentIndex()
    s11 = s21 = s12 = s22 = s13 = s23 = s14 = s24 = s15 = s25 = s16 = s26 = s17 = s27 = 0
    # поля ввода счета в партии
    if tab == 3:
        sys = system.select().where(System.stage == "Предварительный").get()
        sf = sys.score_flag  # флаг из скольки партий играется матч
        #==========
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
        s16 = my_win.lineEdit_pl1_s6.text()
        s26 = my_win.lineEdit_pl2_s6.text()
        s17 = my_win.lineEdit_pl1_s7.text()
        s27 = my_win.lineEdit_pl2_s7.text()
    elif tab == 4:
        pass
    elif tab == 5:
        r = my_win.tableWidget.currentRow()
        final = my_win.tableWidget.item(r, 2).text()  # из какого финала пара игроков в данный момент
        sys = system.select().where(System.stage == final).get()
        sf = sys.score_flag  # флаг из скольки партий играется матч
        s11 = my_win.lineEdit_pl1_s1_fin.text()
        s21 = my_win.lineEdit_pl2_s1_fin.text()
        s12 = my_win.lineEdit_pl1_s2_fin.text()
        s22 = my_win.lineEdit_pl2_s2_fin.text()
        s13 = my_win.lineEdit_pl1_s3_fin.text()
        s23 = my_win.lineEdit_pl2_s3_fin.text()
        s14 = my_win.lineEdit_pl1_s4_fin.text()
        s24 = my_win.lineEdit_pl2_s4_fin.text()
        s15 = my_win.lineEdit_pl1_s5_fin.text()
        s25 = my_win.lineEdit_pl2_s5_fin.text()
        s16 = my_win.lineEdit_pl1_s6_fin.text()
        s26 = my_win.lineEdit_pl2_s6_fin.text()
        s17 = my_win.lineEdit_pl1_s7_fin.text()
        s27 = my_win.lineEdit_pl2_s7_fin.text()
    if sf == 3:
        total_score.append(s11)
        total_score.append(s21)
        total_score.append(s12)
        total_score.append(s22)
        total_score.append(s13)
        total_score.append(s23)
    elif sf == 5:
        total_score.append(s11)
        total_score.append(s21)
        total_score.append(s12)
        total_score.append(s22)
        total_score.append(s13)
        total_score.append(s23)
        total_score.append(s14)
        total_score.append(s24)
        total_score.append(s15)
        total_score.append(s25)
    elif sf == 7:
        total_score.append(s11)
        total_score.append(s21)
        total_score.append(s12)
        total_score.append(s22)
        total_score.append(s13)
        total_score.append(s23)
        total_score.append(s14)
        total_score.append(s24)
        total_score.append(s15)
        total_score.append(s25)
        total_score.append(s16)
        total_score.append(s26)
        total_score.append(s17)
        total_score.append(s27)
    point = 0
    n = len(total_score)
    #  максимальное кол-во партий
    if sf == 3:
        max_game = 2
    elif sf == 5:
        max_game = 3
    elif sf == 7:
        max_game = 4

    for i in range(0, n, 2):
        if total_score[i] != "":
            sc1 = total_score[i]
            sc2 = total_score[i + 1]
            flag = control_score(sc1, sc2)

            if flag is True:
                if int(sc1) > int(sc2):
                    point = 1
                    ts1.append(point)
                else:
                    point = 1
                    ts2.append(point)
                st1 = sum(ts1)
                st2 = sum(ts2)
                #==============
                if tab == 3:
                    my_win.lineEdit_pl1_score_total.setText(str(st1))
                    my_win.lineEdit_pl2_score_total.setText(str(st2))
                    if st1 == max_game or st2 == max_game:  # сравнивает максимальное число очков и набранные очки одним из игроков
                        my_win.Button_Ok.setEnabled(True)  # если игрок набрал макс очки активиоует кнопку ОК и переводит на нее фокус
                        my_win.Button_Ok.setFocus()
                    total_game.append(st1)
                    total_game.append(st2)
                    max_score = max(total_game)  # находит максимальное число очков из сыгранных партий
                    sum_total_game.append(max_game)  # добавляет в список максимальное число очков которые надо набрать
                    sum_total_game.append(max_score)  # добавляет в список максимальное число очков которые уже набрал игрок
                elif tab == 4:
                    pass
                elif tab == 5:
                    my_win.lineEdit_pl1_score_total_fin.setText(str(st1))
                    my_win.lineEdit_pl2_score_total_fin.setText(str(st2))
                    if st1 == max_game or st2 == max_game:  # сравнивает максимальное число очков и набранные очки одним из игроков
                        my_win.Button_Ok_fin.setEnabled(True)  # если игрок набрал макс очки активирует кнопку ОК и переводит на нее фокус
                        my_win.Button_Ok_fin.setFocus()
                    total_game.append(st1)
                    total_game.append(st2)
                    max_score = max(total_game)  # находит максимальное число очков из сыгранных партий
                    if i == 0:
                        sum_total_game.append(max_game)  # добавляет в список максимальное число очков которые надо набрать
                        sum_total_game.append(max_score)  # добавляет в список максимальное число очков которые уже набрал игрок
                    else:
                        sum_total_game[0] = max_game
                        sum_total_game[1] = max_score
                 #===============
            elif flag is False:
                # желательно сюда ввести чтобы фокус ставился на туже ячейку
                sum_total_game = []

    return sum_total_game


def control_score(sc1, sc2):
    """проверка на правильность ввода счета"""
    msgBox = QMessageBox

    sc1 = int(sc1)
    sc2 = int(sc2)
    if sc1 > 35 or sc2 > 35:
        result = msgBox.question(my_win, "", "Вы уверенны в правильности счета в партии?\n"
                                             f"{sc1} : {sc2}",
                                 msgBox.StandardButtons.Ok, msgBox.StandardButtons.Cancel)
        if result == msgBox.StandardButtons.Ok:
            flag = True
        elif result == msgBox.StandardButtons.Cancel:
            return
    if sc1 == 11:
        if 9 >= sc2 >= 0:
            flag = True
        elif sc2 == 13:
            flag = True
        else:
            flag = False
    elif sc1 > 11:
        if sc2 == sc1 - 2:
            flag = True
        elif sc2 == sc1 + 2:
            flag = True
        else:
            flag = False
    elif 0 <= sc1 < 10:
        if sc2 == 11:
            flag = True
        else:
            flag = False
    elif sc1 == 10:
        if sc2 == 12:
            flag = True
        else:
            flag = False

    if flag == False:
        result = msgBox.information(my_win, "", "Проверьте правильность ввода\n счета в партии!",
                                    msgBox.StandardButtons.Ok)
        flag = False
        return flag
    elif flag == True:
        return flag


def enter_score(none_player=0):
    """заносит в таблицу -результаты- победителя, счет и т.п."""
    tab = my_win.tabWidget.currentIndex()
    system = System.select().order_by(System.id).where(System.title_id == title_id())  # находит system id последнего
    if tab == 3:
        if none_player == 0:
            st1 = int(my_win.lineEdit_pl1_score_total.text())
            st2 = int(my_win.lineEdit_pl2_score_total.text())
            w = 2
            l = 1
        else:
            if none_player == 1:  # не явился 1-й игрок
                st1 = "L"
                st2 = "W"
            elif none_player == 2:  # не явился 2-й игрок
                st1 = "W"
                st2 = "L"
            w = 2
            l = 0
            my_win.lineEdit_pl1_score_total.setText(st1)
            my_win.lineEdit_pl2_score_total.setText(st2)
    elif tab == 4:
        pass
    elif tab == 5:
        if my_win.lineEdit_player1_fin.text() == "bye" or my_win.lineEdit_player2_fin.text() == "bye":
            if my_win.lineEdit_player1_fin.text() != "bye":
                winner = my_win.lineEdit_player1_fin.text()
                loser = my_win.lineEdit_player2_fin.text()
            else:
                winner = my_win.lineEdit_player2_fin.text()
                loser = my_win.lineEdit_player1_fin.text()
            w = ""
            l = ""
            winner_string = ""
            ts_winner = ""
            ts_loser = ""
        else:
            if none_player == 0:
                st1 = int(my_win.lineEdit_pl1_score_total_fin.text())
                st2 = int(my_win.lineEdit_pl2_score_total_fin.text())
                w = 2
                l = 1
            else:
                if none_player == 1:
                    st1 = "L"
                    st2 = "W"
                elif none_player == 2:
                    st1 = "W"
                    st2 = "L"
                w = 2
                l = 0
                my_win.lineEdit_pl1_score_total_fin.setText(st1)
                my_win.lineEdit_pl2_score_total_fin.setText(st2)

    r = my_win.tableWidget.currentRow()
    id = my_win.tableWidget.item(r, 0).text()
    num_game = my_win.tableWidget.item(r, 3).text()
    fin = my_win.tableWidget.item(r, 2).text()

    if my_win.lineEdit_player1_fin.text() != "bye" and my_win.lineEdit_player2_fin.text() != "bye":
            if st1 > st2 or none_player == 2:
                if tab == 3:
                    winner = my_win.lineEdit_player1.text()
                    loser = my_win.lineEdit_player2.text()
                elif tab == 4:
                     pass
                elif tab == 5:
                    winner = my_win.lineEdit_player1_fin.text()
                    loser = my_win.lineEdit_player2_fin.text()
                ts_winner = f"{st1} : {st2}"
                ts_loser = f"{st2} : {st1}"
            else:
                if tab == 3:
                    winner = my_win.lineEdit_player2.text()
                    loser = my_win.lineEdit_player1.text()
                elif tab == 4:
                    pass
                elif tab == 5:
                    winner = my_win.lineEdit_player2_fin.text()
                    loser = my_win.lineEdit_player1_fin.text()
                ts_winner = f"{st2} : {st1}"
                ts_loser = f"{st1} : {st2}"
            if none_player == 0:
                winner_string = string_score_game()
            else:
                winner_string = ts_winner

    with db:
        result = Result.get(Result.id == id)
        result.winner = winner
        result.points_win = w
        result.score_win = winner_string
        result.score_in_game = ts_winner
        result.loser = loser
        result.points_loser = l
        result.score_loser = ts_loser
        result.save()
    if tab == 5:
        snoska = tbl_data.numer_game(num_game)
        if snoska[0] != 0:
            with db:  # записывает в db таблицу Result победителя и проигравшего
                player = winner
                for k in range(0, 2):
                    res = Result.select().where(Result.number_group == fin)  # номер id куда записывается победитель
                    for result in res:
                        id = result.tours
                        if int(id) == snoska[k]:
                            if result.player1 is None or result.player1 == "":
                                result.player1 = player
                            else:
                                result.player2 = player
                            result.save()
                            player = loser
                            break
                    # player = loser
    fill_table_results(tb=0)

    if tab == 3:
        my_win.lineEdit_pl1_s1.setText("")  # очищает поля ввода счета в партии
        my_win.lineEdit_pl2_s1.setText("")
        my_win.lineEdit_pl1_s2.setText("")
        my_win.lineEdit_pl2_s2.setText("")
        my_win.lineEdit_pl1_s3.setText("")
        my_win.lineEdit_pl2_s3.setText("")
        my_win.lineEdit_pl1_s4.setText("")
        my_win.lineEdit_pl2_s4.setText("")
        my_win.lineEdit_pl1_s5.setText("")
        my_win.lineEdit_pl2_s5.clear()
        my_win.lineEdit_pl1_score_total.clear()  # очищает поля общего счета
        my_win.lineEdit_pl2_score_total.clear()
        my_win.lineEdit_player1.clear()  # очищает поля фамилии игроков
        my_win.lineEdit_player2.clear()
        fin = my_win.tableWidget.item(r, 1).text()
        my_win.checkBox_7.setChecked(False)
        my_win.checkBox_8.setChecked(False)
    elif tab == 4:
        pass
    elif tab == 5:
        my_win.lineEdit_pl1_s1_fin.clear()  # очищает поля ввода счета в партии
        my_win.lineEdit_pl2_s1_fin.clear()
        my_win.lineEdit_pl1_s2_fin.clear()
        my_win.lineEdit_pl2_s2_fin.clear()
        my_win.lineEdit_pl1_s3_fin.clear()
        my_win.lineEdit_pl2_s3_fin.clear()
        my_win.lineEdit_pl1_s4_fin.clear()
        my_win.lineEdit_pl2_s4_fin.clear()
        my_win.lineEdit_pl1_s5_fin.clear()
        my_win.lineEdit_pl2_s5_fin.clear()
        my_win.lineEdit_pl1_score_total_fin.clear()  # очищает поля общего счета
        my_win.lineEdit_pl2_score_total_fin.clear()
        my_win.lineEdit_player1_fin.clear()  # очищает поля фамилии игроков
        my_win.lineEdit_player2_fin.clear()
    # ===== вызов функции заполнения таблицы pdf группы сыгранными играми
    system = System.select().order_by(System.id).where(System.title_id == title_id() and System.stage == fin).get()  # находит

    if system.stage == "Предварительный":
        pv = system.page_vid
        comp_system.table_made(pv, title_id())
        filter_gr(pl=False)
    elif system.stage == fin:
        system_table = system.label_string
        table_max_player = system.max_player
        txt = system_table.find("на")
        table = system_table[:txt - 1]
        if table == "Сетка (с розыгрышем всех мест)":
            if table_max_player == 16:
                pv = system.page_vid
                comp_system.setka_16_made(fin=fin)
            elif table_max_player == 32:
                pass
        filter_fin()


def string_score_game():
    """создает строку со счетом победителя"""
    tab = my_win.tabWidget.currentIndex()
    if my_win.radioButton_match_3.isChecked() or my_win.radioButton_match_4.isChecked():  # зависимости от кол-во партий
        g = 2
    elif my_win.radioButton_match_5.isChecked() or my_win.radioButton_match_6.isChecked():
        g = 3
    else:
        g = 4
    if tab == 3:
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
    elif tab == 4:
        pass
    elif tab == 5:
        st1 = int(my_win.lineEdit_pl1_score_total_fin.text())
        st2 = int(my_win.lineEdit_pl2_score_total_fin.text())
        s11 = my_win.lineEdit_pl1_s1_fin.text()
        s21 = my_win.lineEdit_pl2_s1_fin.text()
        s12 = my_win.lineEdit_pl1_s2_fin.text()
        s22 = my_win.lineEdit_pl2_s2_fin.text()
        s13 = my_win.lineEdit_pl1_s3_fin.text()
        s23 = my_win.lineEdit_pl2_s3_fin.text()
        s14 = my_win.lineEdit_pl1_s4_fin.text()
        s24 = my_win.lineEdit_pl2_s4_fin.text()
        s15 = my_win.lineEdit_pl1_s5_fin.text()
        s25 = my_win.lineEdit_pl2_s5_fin.text()
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
        if (g == 2 and st1 == 2 and st2 == 0) or (g == 2 and st2 == 0 and st1 == 2):  # из 3-х партий 2-0
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
            n1 = str(f"-{s21}")
        if int(s12) < int(s22):  # 2-й сет
            n2 = s12
        else:
            n2 = str(f"-{s22}")
        if (g == 2 and st1 == 2 and st2 == 0) or (g == 2 and st1 == 0 and st2 == 2):  # из 3-х партий 2-0
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


def result_filter_name():
    """отсортировывает встречи с участием игрока"""
    cp = my_win.comboBox_find_name.currentText()
    cp = cp.title()  # Переводит первую букву в заглавную
    c = Result.select()
    c = c.where(Result.player1 ** f'{cp}%')  # like
    result_list = c.dicts().execute()
    row_count = len(result_list)  # кол-во строк в таблице
    column_count = 13  # кол-во столбцов в таблице
    my_win.tableWidget.setRowCount(row_count)  # вставляет в таблицу необходимое кол-во строк

    for row in range(row_count):  # добавляет данные из базы в TableWidget
        for column in range(column_count):
            item = str(list(result_list[row].values())[column])
            my_win.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))


def filter_fin():
    """фильтрует таблицу -Result- на вкладке финалы"""
    msgBox = QMessageBox
    result = Result.select().where(Result.title_id == title_id())  # находит system id последнего
    num_game_fin = my_win.lineEdit_num_game_fin.text()
    final = my_win.comboBox_filter_final.currentText()
    name = my_win.comboBox_find_name_fin.currentText()
    name = name.title()  # делает Заглавными буквы слов
    played = my_win.comboBox_filter_played_fin.currentText()
    fltr = Result.select().where(Result.system_stage == "Финальный")
    system = System.select().order_by(System.id).where(System.title_id == title_id())  # находит system id последнего
    fin = []

    if final == "все финалы" and played == "все игры" and num_game_fin == "" :
        if name == "":
            count = len(fltr)
            my_win.label_38.setText(f'Всего в финалах {count} игры')
            for i in range(0, count):
                my_win.tableWidget.showRow(i)
        else:  # выбор по фамилии спортсмена
            row = 0
            fltr = Result.select().where(Result.system_stage == "Финальный")
            for result_name in fltr:
                row += 1
                if result_name.player1 == name or result_name.player2 == name:
                    pass
                else:
                    my_win.tableWidget.hideRow(row - 1)
    elif final != "все финалы" and played == "не сыгранные" and num_game_fin == "":  # один из финалов встречи которые не сыгранные
        fl = Result.select().where(Result.number_group == final)
        fltr = fl.select().where(Result.points_win != 2 and Result.points_win == None)
        count = len(fltr)
        my_win.label_38.setText(f'Всего в {final} не сыгранно {count} игры')
    elif final != "все финалы" and played == "завершенные" and num_game_fin == "":
        fltr_played = []
        fltr = Result.select().where(Result.number_group == final)
        for fl in fltr:
            if fl.winner is not None:
                win = fl.winner
                fltr_played.append(win)
        count_pl = len(fltr_played)
        my_win.label_38.setText(f'Завершено в {final} {count_pl} игры')
    elif final != "все финалы" and played == "все игры" and num_game_fin == "":
        fltr = Result.select().where(Result.number_group == final)
        count = len(fltr)
        my_win.label_38.setText(f'Всего в {final} {count} игры')
    elif final == "все финалы" and played == "завершенные" and num_game_fin == "":
        fltr_played = []
        fltr = Result.select().where(Result.system_stage == "Финальный")
        for fl in fltr:
            if fl.winner is not None:
                win = fl.winner
                fltr_played.append(win)
        count_pl = len(fltr_played)
        my_win.label_38.setText(f' Всего сыграно во всех финалах {count_pl} игры')
    else:
        if final != "все финалы" and num_game_fin != "":
            fltr = Result.select().where(Result.number_group == final)
        else:
            for sys in system:  # отбирает финалы с сеткой
                if sys.stage != "Предварительный" and sys.stage != "Полуфиналы":
                    txt = sys.label_string
                    txt = txt[:5]
                    if txt == "Сетка":
                        fin.append(sys.stage)
            fin, ok = QInputDialog.getItem(my_win, "Финалы", "Выберите финал, где искать номер встречи.", fin, 0, False)
            fltr = Result.select().where(Result.number_group == fin)
        row = 0
        for result_list in fltr:
            row += 1
            if result_list.tours == num_game_fin:
                num_game_fin = int(num_game_fin)
                r = num_game_fin - 1
                my_win.tableWidget.selectRow(r)
                item = my_win.tableWidget.item(r, 5)
                my_win.tableWidget.scrollToItem(item)  # переводит выделенную строку в видимую часть экрана
                break

    result_list = fltr.dicts().execute()

    my_win.label_38.show()
    row_count = len(fltr)  # кол-во строк в таблице
    column_count = 13  # кол-во столбцов в таблице
    my_win.tableWidget.setRowCount(row_count)  # вставляет в таблицу необходимое кол-во строк

    for row in range(row_count):  # добавляет данные из базы в TableWidget
        for column in range(column_count):
            item = str(list(result_list[row].values())[column])
            my_win.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))


def filter_gr(pl=False):
    """фильтрует таблицу -результаты- на вкладке группы"""
    msgBox = QMessageBox
    group = my_win.comboBox_filter_group.currentText()
    name = my_win.comboBox_find_name.currentText()
    name = name.title()  # делает Заглавными буквы слов
    played = my_win.comboBox_filter_played.currentText()

    if group == "все группы" and my_win.comboBox_find_name.currentText() != "":
        if pl == False:
            fltr = Result.select().where(Result.player1 == name)
        else:
            fltr = Result.select().where(Result.player2 == name)
    elif group == "все группы" and played == "все игры":
        fltr = Result.select()
    elif group == "все группы" and played == "завершенные":
        fltr = Result.select().where(Result.points_win == 2)
    elif group != "все группы" and played == "завершенные":
        fl = Result.select().where(Result.number_group == group)
        fltr = fl.select().where(Result.points_win == 2)
    elif group != "все группы" and played == "не сыгранные":
        fl = Result.select().where(Result.number_group == group)
        fltr = fl.select().where(Result.points_win != 2 and Result.points_win == None)
    elif group == "все группы" and played == "не сыгранные":
        fltr = Result.select().where(Result.points_win != 2 and Result.points_win == None)
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

    for row in range(row_count):  # добавляет данные из базы в TableWidget
        for column in range(column_count):
            item = str(list(result_list[row].values())[column])
            my_win.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))

    if my_win.comboBox_find_name.currentText() != "" and pl == False:
        result = msgBox.question(my_win, "", "Продолжить поиск игр с участием\n"
                                             f"{name} ?",
                                 msgBox.StandardButtons.Ok, msgBox.StandardButtons.Cancel)
        if result == msgBox.StandardButtons.Ok:
            pl = True
            filter_gr(pl)
        elif result == msgBox.StandardButtons.Cancel:
            my_win.comboBox_find_name.clear()
            return
    else:
        my_win.comboBox_find_name.clear()


def load_combo():
    """загружает комбобокс поиска спортсмена на вкладке группы, пф и финалы фамилиями спортсменов"""
    mp = Player.select()
    text = []
    for i in mp:  # цикл по таблице базы данных (I это id строк)
        tt = Player.get(Player.id == i)
        text.append(tt.player)
    my_win.comboBox_find_name.addItems(text)
    my_win.comboBox_find_name_fin.addItems(text)
    my_win.comboBox_find_name.setCurrentText("")
    my_win.comboBox_find_name_fin.setCurrentText("")


def reset_filter():
    """сбрасывает критерии фильтрации"""
    sender = my_win.sender()
    if sender == my_win.Button_reset_filter:
        my_win.comboBox_find_name.setCurrentText("")
        my_win.comboBox_filter_played.setCurrentText("все игры")
        my_win.comboBox_filter_group.setCurrentText("все группы")
        filter_gr()
    elif sender == my_win.Button_reset_filter_fin:
        my_win.comboBox_find_name_fin.setCurrentText("")
        my_win.comboBox_filter_played_fin.setCurrentText("все игры")
        my_win.comboBox_filter_final.setCurrentText("все финалы")
        my_win.lineEdit_num_game_fin.setText("")
        filter_fin()


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
            choice_tbl_made()  # заполняет db жеребьевка
            system_competition()  # создает систему соревнований


def choice_gr_automat():
    """проба автоматической жеребьевки групп, записывает в таблицу Choice номер группы и посев"""
    load_tableWidget()
    gamer = my_win.lineEdit_title_gamer.text()
    sys = System.select().order_by(System.id).where(System.title_id == title_id()).get()  # находит system id последнего
    s_id = sys.id
    group = sys.total_group
    mp = sys.max_player
    tp = sys.total_athletes
    pl_choice = Choice.select().where(Choice.title_id == title_id())
    player_choice = pl_choice.select().order_by(Choice.rank.desc())
    h = 0
    for k in range(1, mp + 1):  # цикл посевов
        # вставить проверку на окончание посева
        if k % 2 != 0:  # направление посева с последней группы до 1-й
            start = 0
            end = group
            step = 1
            p = 1
        else:  # направление посева с 1-й до последней группы
            start = group
            end = 0
            step = -1
            p = 0
        for i in range(start, end, step):  # №-й посев
            if h < tp:
                txt = str(f'{i + p} группа')
                id = int(my_win.tableWidget.item(h, 1).text())  # ищет id игрока
                ch_id = Choice.get(Choice.player_choice == id)  # находит id таблицы choice, соответсвующий игроку
                choice_id = ch_id.id
                h += 1
                with db:  # запись в таблицу Choice результа жеребъевки
                    grp = Choice.get(Choice.id == choice_id)
                    grp.group = txt
                    grp.posev_group = k
                    grp.save()
    if tp == h:
        fill_table_choice()
    with db:  # записывает в систему, что произведена жеребъевка
        system = System.get(System.id == s_id)
        system.choice_flag = True
        system.save()
    player_in_table()


def choice_setka(fin):
    """проба жеребьевки сетки на 16"""
    sys = System.select().order_by(System.id).where(System.title_id == title_id()).get()  # находит system id последнего
    system = sys.get(System.stage == fin)
    flag = system.choice_flag
    if flag is True:  # перед повторной жеребьевкой
        del_choice = Game_list.select().where(Game_list.number_group == fin)
        for i in del_choice:
            i.delete_instance()  # удаляет строки финала (fin) из таблицы -Game_list
        del_result = Result.select().where(Result.number_group == fin)
        for i in del_result:
            i.delete_instance() # удаляет строки финала (fin) из таблицы -Result-
    with db:  # записывает флаг жеребьевки финала
        sys = System.get(System.stage == fin)
        sys.choice_flag = True
        sys.save()
    player_in_setka(fin)
    load_tableWidget()


def choice_tbl_made():
    """создание таблицы жеребьевка, заполняет db списком участников для жеребъевки"""
    gamer = my_win.lineEdit_title_gamer.text()
    player = Player.select().order_by(Player.rank.desc()).where(Player.title_id == title_id())
    count = len(player)
    choice = Choice.select().where(Choice.title_id == title_id())
    chc = len(choice)
    if chc == 0:
        for i in player:
            pl = Player.get(Player.id == i)
            cch = Coach.get(Coach.id == pl.coach_id)
            coach = cch.coach
            chc = Choice(player_choice=pl, family=pl.player, region=pl.region, coach=coach, rank=pl.rank,
                         title_id=title_id()).save()


def choice_filter_group():
    """фильтрует таблицу жеребьевка по группам"""
    gamer = my_win.lineEdit_title_gamer.text()
    fg = my_win.comboBox_filter_choice.currentText()
    if fg == "все группы":
        player_choice = Choice.select().where(Choice.title_id == title_id())
    else:
        p_choice = Choice.select().order_by(Choice.posev_group).where(Choice.group == fg)
        player_choice = p_choice.select().where(Choice.title_id == title_id())
    count = len(player_choice)
    choice_list = player_choice.dicts().execute()
    row_count = len(choice_list)  # кол-во строк в таблице
    column_count = 10  # кол-во столбцов в таблице
    my_win.tableWidget.setRowCount(row_count)  # вставляет в таблицу необходимое кол-во строк
    if row_count != 0:
        for row in range(row_count):  # добвляет данные из базы в TableWidget
            for column in range(column_count):
                item = str(list(choice_list[row].values())[column])
                my_win.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))

        my_win.tableWidget.resizeColumnsToContents()  # ставит размер столбцов согласно записям
        color_region_in_tableWidget(fg)
        for d in range(0, row_count):  # сортирует нумерация по порядку
            my_win.tableWidget.setItem(d, 0, QTableWidgetItem(str(d + 1)))


def color_region_in_tableWidget(fg):
    """смена цвета шрифта в QtableWidget -fg- номер группы"""
    reg = []
    rid = []
    if fg != "все группы":
        line = Choice.select().order_by(Choice.posev_group).where(Choice.group == fg)  # выбирает все строки той группы (fg)
        count = len(line)
        for i in line:
            r = Choice.get(Choice.id == i)
            r_id = r.id
            region = r.region
            region = str(region.rstrip())  # удаляет пробел в конце строки
            reg.append(region)
            rid.append(r_id)
        if len(reg) != 0:
            for x in reg:
                count_region = reg.count(x)
                if count_region > 1:  # если повторяющихся регионов больше одного
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


def hide_show_columns(tb):
    """скрывает или показывает столбцы TableWidget"""
    if tb == 2:
        my_win.tableWidget.hideColumn(1)
        my_win.tableWidget.showColumn(9)
    elif tb == 1:
        my_win.tableWidget.showColumn(1)
        my_win.tableWidget.hideColumn(9)
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
    if my_win.comboBox_etap_1.currentText() == "Одна таблица":
        one_table()
    if my_win.comboBox_etap_1.currentText() == "Предварительный" and my_win.comboBox_etap_2.isHidden():
        kol_player_in_group()
    elif my_win.comboBox_etap_2.currentText() == "Финальный" and my_win.comboBox_etap_3.isHidden():
        total_game_table(kpt=0, fin="", pv="", cur_index=0)
    elif my_win.comboBox_etap_3.currentText() == "Финальный" and my_win.comboBox_etap_4.isHidden():
        total_game_table(kpt=0, fin="", pv="", cur_index=0)


def total_game_table(kpt, fin, pv, cur_index):
    """количество участников в сетке и кол-во игр"""
    msgBox = QMessageBox
    gamer = my_win.lineEdit_title_gamer.text()
    system = System.select().order_by(System.id).where(System.title_id == title_id()).get()  # находит system id последнего
    total_player = system.total_athletes
    if kpt != 0:  # подсчет кол-во игр из выбора кол-ва игроков вышедших из группы и системы финала
        player_in_final = system.total_group * kpt

        if cur_index == 1:
            vt = "Сетка (-2) на"
            my_win.comboBox_page_vid.setCurrentText("книжная")
        elif cur_index == 2:
            vt = "Сетка (с розыгрышем всех мест) на"
            my_win.comboBox_page_vid.setCurrentText("книжная")
        elif cur_index == 3:
            vt = "Сетка (с играми за 1-3 места) на"
            my_win.comboBox_page_vid.setCurrentText("книжная")
        elif cur_index == 4:
            vt = "Круговая таблица на"
        pv = my_win.comboBox_page_vid.currentText()
        str_setka = f"{vt} {player_in_final} участников"
        s = System.select().order_by(System.id.desc()).get()
        total_athletes = s.total_athletes
        if player_in_final == 8:
            g = 12
        elif player_in_final == 12:
            g = 28
        elif player_in_final == 16:
            if cur_index == 1:
                g = 38
            elif cur_index == 2:
                g = 32
        stroka_kol_game = f"{g} игр"

        if total_athletes > player_in_final:
            final = fin
        else:
            final = "финальный"
        system = System(title_id=title_id(), total_athletes=total_athletes, total_group=0, kol_game_string=stroka_kol_game,
                        max_player=player_in_final, stage=final, page_vid=pv, label_string=str_setka, choice_flag=0,
                        score_flag=5, visible_game=False).save()
        return [str_setka, player_in_final, total_athletes, stroka_kol_game]
    else:  # нажата кнопка создания этапа, если еще не все игроки посеяны в финал, то продолжает этапы соревнования
        sys_last = System.select().where(System.title_id == title_id() and System.stage ** '%финал')  # отбирает записи, где
        # титул id и стадия содержит слово финал (1 и 2 заменяет %)
        count = len(sys_last)
        system = System.select().order_by(System.id).where(System.title_id == title_id() and System.stage ** '%финал').get()
        sys_id = system.id
        sum_final = []
        for i in range(0, count):
            st = System.get(System.id == sys_id + i)
            player_in_etap = st.max_player
            sum_final.append(player_in_etap)
        total_final = sum(sum_final)
        if total_final >= total_player:  # подсчитывает все ли игроки распределены по финалам
            result = msgBox.question(my_win, "", "Система соревнований создана.\n"
                                                 "Теперь необходимо сделать жеребъевку\n"
                                                 "предварительного этапа.\n"
                                                 "Хотите ее сделать сейчас?",
                                     msgBox.StandardButtons.Ok, msgBox.StandardButtons.Cancel)
            if result == msgBox.StandardButtons.Ok:
                choice_gr_automat()
                tab_enabled(gamer)
            else:
                return
        else:
            my_win.comboBox_table.hide()
            my_win.comboBox_etap_3.show()
            my_win.Button_etap_made.setEnabled(True)
            my_win.comboBox_page_vid.setEnabled(True)


def clear_db_before_edit():
    """очищает таблицы при повторном создании системы"""
    system = System.select().where(System.title_id == title_id())
    for i in system:  # удаляет все записи
        i.delete_instance()
    sys = System(title_id=title_id(), total_athletes=0, total_group=0, max_player=0, stage="", page_vid="",
                 label_string="", kol_game_string="", choice_flag=False, score_flag=5, visible_game=False).save()
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
    gamer = my_win.lineEdit_title_gamer.text()
    sid_first = System.select().where(System.title_id == title_id())  # находит system id первого
    count = len(sid_first)
    if count > 1:
        my_win.statusbar.showMessage("Система соревнований создана", 5000)
        flag = True
    else:
        my_win.statusbar.showMessage("Необходимо создать систему соревнований", 500)
        flag = False
    return flag


def ready_choice():
    """проверка на готовность жеребьевки групп"""
    gamer = my_win.lineEdit_title_gamer.text()
    system = System.select().order_by(System.id).where(System.title_id == title_id()).get()  # находит system id последнего
    flag_greb = system.choice_flag
    if flag_greb is True:
        my_win.statusbar.showMessage("Жеребьевка сделана", 5000)
        flag = True
    else:
        my_win.statusbar.showMessage("Жеребьевка групп еще не выполнена", 5000)
        flag = False
    return flag


def select_choice_final():
    """выбор жеребьевки финала"""
    # t = Title.select().order_by(Title.id.desc()).get()  # получение последней записи в таблице
    system = System.select().order_by(System.id).where(System.title_id == title_id()).get()  # находит system id последнего

    fin = []
    for sys in system.select():
        if sys.stage != "Предварительный" and sys.stage != "Полуфиналы":
            fin.append(sys.stage)

    fin, ok = QInputDialog.getItem(my_win, "Выбор финала", "Выберите финал для жеребъевки", fin, 0, False)
    if ok:
        return fin
    my_win.tabWidget.setCurrentIndex(5)


# def proba():
#     """добавление столбца в существующую таблицу"""
#     my_db = SqliteDatabase('comp_db.db')
#     migrator = SqliteMigrator(my_db)
#     title_id = ForeignKeyField(Title, unique=True, default=u)  # новый столбец, его поле и значение по умолчанию
#     with db:
#         migrate(migrator.add_column('delete_players', 'title_id', title_id))
#====================================
    # id_full_name = {}
    # player = Player.select().where(Player.title_id == t)
    # for pl in player:
    #     player_id = pl.id
    #     city = pl.city
    #     name = pl.player
    #     # space = name.find(" ")  # находит пробел отделяющий имя от фамилии
    #     # family_slice = name[:space + 2]  # получает отдельно фамилия и первую букву имени
    #     fn = f"{name}/ {city}"
    #     with db:
    #         pl.full_name = fn
    #         pl.save()


    #=========================
    # t = Title.select().order_by(Title.id.desc()).get()  # получение последней записи в таблице
    # with db:
    #     Delete_player.create_table()
    #========================
        # System.create_table()
        # sys = System(title_id=t, total_athletes=0, total_group=0, max_player=0, stage="", page_vid="", label_string="",
        #              kol_game_string="", choice_flag=False, score_flag=5, visible_game=False).save()


def del_player_table():
    """таблица удаленных игроков на данных соревнованиях"""
    if my_win.checkBox_6.isChecked():
        my_win.tableWidget.hideColumn(8)
        player_list = Delete_player.select().where(Delete_player.title_id == title_id())
        count = len(player_list)
        if count == 0:
            my_win.statusbar.showMessage("Удаленных участников соревнований нет", 10000)
            fill_table(player_list)
        else:
            load_tableWidget()
            fill_table(player_list)
            my_win.statusbar.showMessage("Список удаленных участников соревнований", 10000)
            if my_win.lineEdit_Family_name.text() != "":
                my_win.Button_add_edit_player.setText("Восстановить")
                my_win.Button_add_edit_player.setEnabled(True)
            else:
                my_win.Button_add_edit_player.setEnabled(False)
    else:
        player_list = Player.select().where(Player.title_id == title_id())
        fill_table(player_list)
        my_win.tableWidget.showColumn(8)
        my_win.Button_add_edit_player.setText("Добавить")
        my_win.Button_add_edit_player.setEnabled(True)
        my_win.statusbar.showMessage("Список участников соревнований", 10000)


def kol_player_in_final():
    """выбор из комбобокс сколько выходит из группы в финал"""
    sender = my_win.sender()
    pv = my_win.comboBox_page_vid.currentText()
    fin = ""
    if sender == my_win.comboBox_one_table:
        if my_win.comboBox_one_table.currentText() == "Круговая система":
            player = Player.select().where(Player.title_id == title_id())
            count = len(player)
            kol_game = count // 2 * (count - 1)
            my_win.label_50.show()
            my_win.label_19.show()
            my_win.label_19.setText(f"{kol_game} игр.")
            my_win.label_33.setText(f"Всего: {kol_game} игр.")
            my_win.label_50.setText(f"{count} человек по круговой системе.")
            my_win.comboBox_one_table.hide()

    else:
        if sender == my_win.comboBox_table:
            cur_index = my_win.comboBox_table.currentIndex()
            ct = my_win.comboBox_etap_2.currentText()
            if ct == "Полуфиналы":
                my_win.label_23.setText("Полуфиналы")
            elif ct == "Финальный":
                my_win.label_23.setText("Финальный этап")
                fin = "1-й финал"
        elif sender == my_win.comboBox_table_2:
            cur_index = my_win.comboBox_table_2.currentIndex()
            ct = my_win.comboBox_etap_3.currentText()
            if ct == "Финальный":
                my_win.label_32.setText("Финальный этап")
                fin = "2-й финал"
        kpt, ok = QInputDialog.getInt(my_win, "Число участников", "Введите число участников,\nвыходящих "
                                                                  f"из группы в {fin}")
        list = total_game_table(kpt, fin, pv, cur_index)  # возвращает из функции несколько значения в списке
        if ok:
            if sender == my_win.comboBox_table:
                my_win.label_27.show()
                my_win.label_27.setText(list[3])  # пишет кол-во игр 2-ого этапа
                my_win.label_28.show()
                my_win.label_28.setText(list[0])
                if list[2] - list[1] == 0:  # подсчитывает все ли игроки распределены по финалам
                    my_win.statusbar.showMessage("Система создана.", 10000)
                else:
                    my_win.comboBox_table.hide()
            elif sender == my_win.comboBox_table_2:
                my_win.label_30.setText(list[3])
                my_win.label_30.show()
                my_win.label_31.setText(list[0])
                my_win.label_31.show()
                if list[2] - list[1] == 0:  # подсчитывает все ли игроки распределены по финалам
                    my_win.statusbar("Система создана.", 10000)
                else:
                    my_win.comboBox_table_2.hide()
            my_win.Button_etap_made.setEnabled(True)
            my_win.comboBox_page_vid.setEnabled(True)


# def proba():
#     with db:
#        Player.create_table()




def no_play():
    """победа по неявке соперника"""
    sender = my_win.sender()
    if sender == my_win.checkBox_7 or sender == my_win.checkBox_9:
        none_player = 1
    else:
        none_player = 2
    enter_score(none_player)


def backup():
    """резервное копирование базы данных"""
    try:
        db = sqlite3.connect('comp_db.db')
        db_backup = sqlite3.connect('comp_db_backup.db')
        with db_backup:
            db.backup(db_backup, pages=3, progress=None)
        my_win.statusbar.showMessage("Резервное копирование базы данных завершено успешно", 5000)  # показывает статус бар на 5 секунд
    except sqlite3.Error as error:
        my_win.statusbar.showMessage("Ошибка при копировании базы данных", 5000)  # показывает статус бар на 5 секунд
    finally:
        if (db_backup):
            db_backup.close()
            db.close()
            my_win.close()


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



# ===== переводит фокус на поле ввода счета в партии вкладки -группа-
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
# ===== переводит фокус на полее ввода счета в партии вкладки -финалы-
my_win.lineEdit_pl1_s1_fin.returnPressed.connect(focus)
my_win.lineEdit_pl2_s1_fin.returnPressed.connect(focus)
my_win.lineEdit_pl1_s2_fin.returnPressed.connect(focus)
my_win.lineEdit_pl2_s2_fin.returnPressed.connect(focus)
my_win.lineEdit_pl1_s3_fin.returnPressed.connect(focus)
my_win.lineEdit_pl2_s3_fin.returnPressed.connect(focus)
my_win.lineEdit_pl1_s4_fin.returnPressed.connect(focus)
my_win.lineEdit_pl2_s4_fin.returnPressed.connect(focus)
my_win.lineEdit_pl1_s5_fin.returnPressed.connect(focus)
my_win.lineEdit_pl2_s5_fin.returnPressed.connect(focus)

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

my_win.comboBox_one_table.currentTextChanged.connect(kol_player_in_final)
my_win.comboBox_table.currentTextChanged.connect(kol_player_in_final)
my_win.comboBox_table_2.currentTextChanged.connect(kol_player_in_final)
my_win.comboBox_etap_1.currentTextChanged.connect(system_competition)
my_win.comboBox_etap_2.currentTextChanged.connect(system_competition)
my_win.comboBox_etap_3.currentTextChanged.connect(system_competition)
my_win.comboBox_page_vid.currentTextChanged.connect(page_vid)
my_win.comboBox_filter_final.currentTextChanged.connect(game_in_visible)
my_win.comboBox_filter_choice.currentTextChanged.connect(choice_filter_group)


# my_win.comboBox_filter_group.currentTextChanged.connect(result_filter_group)
# my_win.comboBox_filter_played.currentTextChanged.connect(result_filter_played)

# =======  отслеживание переключение чекбоксов =========
my_win.radioButton_3.toggled.connect(load_combobox_filter_group)

my_win.radioButton_match_3.toggled.connect(match_score_db)
my_win.radioButton_match_5.toggled.connect(match_score_db)
my_win.radioButton_match_7.toggled.connect(match_score_db)


my_win.checkBox.stateChanged.connect(button_title_made_enable)  # при изменении чекбокса активирует кнопку создать
# my_win.checkBox_2.stateChanged.connect(button_etap_made_enabled)  # при изменении чекбокса активирует кнопку создать
my_win.checkBox_3.stateChanged.connect(button_system_made_enable)  # при изменении чекбокса активирует кнопку создать
my_win.checkBox_4.stateChanged.connect(game_in_visible)  # при изменении чекбокса показывает поля для ввода счета
my_win.checkBox_5.stateChanged.connect(game_in_visible)  # при изменении чекбокса показывает поля для ввода счета финала
my_win.checkBox_6.stateChanged.connect(del_player_table)  # при изменении чекбокса показывает список удаленных игроков
my_win.checkBox_7.stateChanged.connect(no_play)  # поражение по неявке
my_win.checkBox_8.stateChanged.connect(no_play)  # поражение по неявке
# =======  нажатие кнопок =========


my_win.Button_Ok.setAutoDefault(True)  # click on <Enter>
my_win.Button_Ok_fin.setAutoDefault(True)  # click on <Enter>

my_win.Button_reset_filter.clicked.connect(reset_filter)
my_win.Button_reset_filter_fin.clicked.connect(reset_filter)
my_win.Button_filter_fin.clicked.connect(filter_fin)
my_win.Button_filter.clicked.connect(filter_gr)
my_win.Button_etap_made.clicked.connect(etap_made)  # рисует таблицы группового этапа и заполняет game_list
my_win.Button_system_made.clicked.connect(player_in_table)  # заполнение таблицы Game_list
my_win.Button_add_edit_player.clicked.connect(add_player)  # добавляет игроков в список и базу
my_win.Button_group.clicked.connect(player_in_table)  # вносит спортсменов в группы
my_win.Button_title_made.clicked.connect(title_made)  # записывает в базу или редактирует титул
my_win.Button_Ok.clicked.connect(enter_score)  # записывает в базу счет в партии встречи
my_win.Button_Ok_fin.clicked.connect(enter_score)  # записывает в базу счет в партии встречи
my_win.Button_del_player.clicked.connect(delete_player)

# my_win.Button_proba.clicked.connect(proba)

my_win.Button_sort_mesto.clicked.connect(sort)
my_win.Button_sort_R.clicked.connect(sort)
my_win.Button_sort_Name.clicked.connect(sort)
my_win.Button_view.clicked.connect(view)

sys.exit(app.exec())
