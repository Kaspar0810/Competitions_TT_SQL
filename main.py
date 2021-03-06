# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from ast import Break
from operator import truediv
from queue import Empty
from numpy import False_
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.platypus import PageBreak
from reportlab.lib.styles import ParagraphStyle as PS, getSampleStyleSheet
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib import colors
from reportlab.lib.colors import *
from reportlab.platypus import Paragraph, TableStyle, Table, Image, SimpleDocTemplate
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas
from main_window import Ui_MainWindow
from start_form import Ui_Form
from datetime import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport, Qt
from models import *
from collections import Counter
from itertools import *
# import datetime
import os
import openpyxl as op
import pandas as pd
import sys
import sqlite3
import pathlib
from pathlib import Path
import random
# from playhouse.migrate import *

if not os.path.isdir("table_pdf"):  # создает папку 
     os.mkdir("table_pdf")


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

if __name__ == '__main__':
    print_hi('PyCharm')

# from playhouse.sqlite_ext import SqliteExtDatabase, backup_to_file, backup

registerFontFamily('DejaVuSerif', normal='DejaVuSerif',
                   bold='DejaVuSerif-Bold', italic='DejaVuSerif-Italic')
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
        self.Button_system_made.setEnabled(False)
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
        # подменю с выбором (addMenu добавляет к пункту возможность выбора)
        go_to = fileMenu.addMenu("Перейти к")
        fileMenu.addSeparator()  # вставляет разделительную черту
        # подменю без выбора (addAction создает сразу действие)
        system = fileMenu.addMenu("Система")
        choice = fileMenu.addMenu("Жеребьевка")
        saveList = fileMenu.addMenu("Сохранить")
        fileMenu.addSeparator()
        last_comp = fileMenu.addMenu("Последние")
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)
        # меню Редактировать
        editMenu = menuBar.addMenu("Редактировать")  # основное
        # меню Печать
        printMenu = menuBar.addMenu("Печать") # основное

        # ============ создание подменю

        go_to.addAction(self.go_to_Action)  # подменю выбора соревнования
        # last_comp.addAction(self.last_Action)  # подменю прошлых соревнований
        system.addAction(self.system_made_Action)  # подменю создание системы
        system.addAction(self.system_edit_Action)  # подменю редактирование системы
        choice.addAction(self.choice_gr_Action)  # подменю группы
        choice.addAction(self.choice_pf_Action)  # подменю полуфиналы
        choice.addAction(self.choice_fin_Action)  # подменю финалы
        saveList.addAction(self.savelist_Action)
        # add_last = last_comp.addMenu("Последние")
        last_comp.addAction(self.first_comp_Action)
        last_comp.addAction(self.second_comp_Action)
        last_comp.addAction(self.third_comp_Action)
        last_comp.addAction(self.fourth_comp_Action)
        last_comp.addAction(self.fifth_comp_Action)
        ed_Menu = editMenu.addMenu("Жеребьевка")
        ed_Menu.addAction(self.ed_gr_Action)
        ed_Menu.addAction(self.ed_pf_Action)
        ed_Menu.addAction(self.ed_fin_Action)
        ed_Menu.addAction(self.system_edit_Action)
        find_Menu = editMenu.addMenu("Поиск")
        find_Menu.addAction(self.find_r_Action)
        find_Menu.addAction(self.find_r1_Action)
        editMenu.addAction(self.vid_edit_Action)  #в осн меню -Редактировать- добавлен пункт сразу с акцией -Вид страницы этапов
        # меню Рейтинг
        rank_Menu = menuBar.addMenu("Рейтинг")  # основное
        rank_Menu.addAction(self.rAction)
        rank_Menu.addAction(self.r1Action)
        # меню печать
        print_Menu = printMenu.addMenu("Чистые таблицы")        
        print_Menu.addAction(self.clear_s16_Action)
        print_Menu.addAction(self.clear_s16_2_Action)
        print_Menu.addAction(self.clear_s32_Action)
        print_Menu.addAction(self.clear_s32_full_Action)
        print_Menu.addAction(self.clear_s32_2_Action)

        # меню просмотр
        view_Menu = menuBar.addMenu("Просмотр")
        view_Menu.addAction(self.all_comp_Action)
        view_Menu.addAction(self.view_list_Action)
        view_Menu.addAction(self.view_gr_Action)
        view_Menu.addAction(self.view_pf_Action)
        v_Menu = view_Menu.addMenu("Финалы")
        v_Menu.addAction(self.view_fin1_Action)
        v_Menu.addAction(self.view_fin2_Action)
        v_Menu.addAction(self.view_fin3_Action)
        v_Menu.addAction(self.view_fin4_Action)

        view_Menu.addAction(self.view_one_table_Action)
        # меню помощь
        help_Menu = menuBar.addMenu("Помощь")  # основное
    #  создание действий меню

    def _createAction(self):
        self.helpAction = QAction(self)
        self.system_edit_Action = QAction("Редактировать")
        self.system_made_Action = QAction("Создать")
        self.exitAction = QAction("Выход")
        self.rAction = QAction("Текущий рейтинг")
        self.r1Action = QAction("Рейтинг за январь")
        self.first_comp_Action = QAction("пусто")
        self.second_comp_Action = QAction("пусто")
        self.third_comp_Action = QAction("пусто")
        self.fourth_comp_Action = QAction("пусто")
        self.fifth_comp_Action = QAction("пусто")
        self.ed_gr_Action = QAction("Редактировать группы")  # подменю редактор
        self.ed_pf_Action = QAction("Редактировать полуфиналы")
        self.ed_fin_Action = QAction("Редактировать финалы")
        self.vid_edit_Action = QAction("Вид страницы этапов")

        self.find_r_Action = QAction("Поиск в текущем рейтинге")  # подменю поиск
        self.find_r1_Action = QAction("Поиск в январском рейтинге")
        self.savelist_Action = QAction("Список")  # подменю сохранить
        # подменю жеребьевка -группы-
        self.choice_gr_Action = QAction("Группы")
        # подменю жеребьевка -полуфиналы-
        self.choice_pf_Action = QAction("Полуфиналы")
        self.choice_fin_Action = QAction("Финалы")  # подменю жеребьевка -финалы-
        self.all_comp_Action = QAction("Полные соревнования")
        self.view_list_Action = QAction("Список участников")
        self.view_gr_Action = QAction("Группы")
        self.view_pf_Action = QAction("Полуфиналы")

        self.view_one_table_Action = QAction("Одна таблица")
        self.go_to_Action = QAction("пусто")
        # self.last_Action = QAction("пусто")
        # подменю -печать-
        self.clear_s16_Action = QAction("Сетка 16")
        self.clear_s16_2_Action = QAction("Сетка 16 минус 2")
        self.clear_s32_2_Action = QAction("Сетка 32 минус 2")
        self.clear_s32_full_Action = QAction("Сетка 32 прогрессивная")
        self.clear_s32_Action = QAction("Сетка 32 (1-3 места)")
        # ======== подменю финалы ============= сделать в зависимости от кол-во финалов остальные невидимые

        self.view_fin1_Action = QAction("1-финал")
        self.view_fin2_Action = QAction("2-финал")
        self.view_fin3_Action = QAction("3-финал")
        self.view_fin4_Action = QAction("4-финал")
        self.view_fin1_Action.setVisible(True)  # делает пункт меню не видимым
        self.view_fin2_Action.setVisible(True)  # делает пункт меню не видимым
        self.view_fin3_Action.setVisible(False)  # делает пункт меню не видимым
        self.view_fin4_Action.setVisible(False)  # делает пункт меню не видимым

    def _connectActions(self):
        # Connect File actions
        # self.newAction.triggered.connect(self.newFile)
        self.system_made_Action.triggered.connect(self.system_made)
        self.system_edit_Action.triggered.connect(self.system_edit)
        self.vid_edit_Action.triggered.connect(self.vid_edit)
        self.exitAction.triggered.connect(self.exit)
        self.savelist_Action.triggered.connect(self.saveList)
        self.choice_gr_Action.triggered.connect(self.choice)
        self.choice_fin_Action.triggered.connect(self.choice)
        self.view_list_Action.triggered.connect(self.view)
        self.view_one_table_Action.triggered.connect(self.view)
        self.view_gr_Action.triggered.connect(self.view)
        self.view_fin1_Action.triggered.connect(self.view)
        self.view_fin2_Action.triggered.connect(self.view)
        self.view_fin3_Action.triggered.connect(self.view)
        self.view_fin4_Action.triggered.connect(self.view)
        self.clear_s16_Action.triggered.connect(self.print_clear)
        self.clear_s32_full_Action.triggered.connect(self.print_clear)
        self.clear_s32_Action.triggered.connect(self.print_clear)
        self.clear_s32_2_Action.triggered.connect(self.print_clear)

        self.first_comp_Action.triggered.connect(self.last)
        self.second_comp_Action.triggered.connect(self.last)
        self.third_comp_Action.triggered.connect(self.last)
        self.fourth_comp_Action.triggered.connect(self.last)
        self.fifth_comp_Action.triggered.connect(self.last)

        self.go_to_Action.triggered.connect(self.open)
        # Connect Рейтинг actions
        self.rAction.triggered.connect(self.r_File)

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
        msg = QMessageBox
        sender = self.sender()
        if sender == self.choice_gr_Action:  # нажат подменю жеребъевка групп
            system = System.select().where(System.title_id == title_id())
            for stage in system:
                if stage.stage == "Предварительный":
                    if stage.choice_flag == True:
                        reply = msg.information(my_win, 'Уведомление',
                                                        "Жеребъевка была произведена,\nесли хотите сделать "
                                                        "повторно\nнажмите -ОК-, если нет то - Cancel-",
                                                        msg.Ok, msg.Cancel)

                        if reply == msg.Ok:
                            my_win.tabWidget.setCurrentIndex(2)
                            clear_db_before_choice()
                            choice_gr_automat()
                            my_win.tabWidget.setCurrentIndex(3)
                        else:
                            return
                    else:
                        my_win.tabWidget.setCurrentIndex(2)
                        choice_gr_automat()
        elif sender == self.choice_fin_Action:  # нажат подменю жеребьевка финалов
            fin = select_choice_final()
            sys = System.select().where(System.title_id == title_id())
            system = sys.select().where(System.stage == fin).get()
            type = system.type_table

            if fin is not None:
                sys = System.get(System.stage == fin)
                check_flag = check_choice(fin)
                if check_flag is True:
                    if sys.choice_flag == True:  # проверка флаг на жеребьевку финала
                        reply = msg.information(my_win, 'Уведомление', f"Жеребъевка {fin} была произведена,"
                                                                            f"\nесли хотите сделать "
                                                                            "повторно\nнажмите-ОК-, "
                                                                            "если нет то - Cancel-",
                                                        msg.Ok,
                                                        msg.Cancel)
                        if reply == msg.Ok:
                            if type == "круг":
                                player_fin_on_circle(fin)
                            else:
                                choice_setka(fin)
                        else:
                            return
                    else:
                        if type == "круг":
                            player_fin_on_circle(fin)
                        else:
                            choice_setka(fin)
                else:
                    return
            else:
                return
           
    def system_made(self):
        system_competition()

    def system_edit(self):
        system_competition()

    def help(self):
        pass

    def open(self):
        go_to()

    def view(self):
        view()
    
    def vid_edit(self):
        change_page_vid()

    def print_clear(self):
        """Печать чистых таблиц"""
        change_dir()
        sender = self.sender()
        if sender == self.clear_s32_Action:
            setka_32_made(fin="1-й финал")
        elif sender == self.clear_s32_full_Action:
            setka_32_full_made(fin="1-й финал")
        elif sender == self.clear_s32_2_Action:
            setka_32_2_made(fin="1-й финал")
        elif sender == self.clear_s16_Action:
            setka_16_full_made(fin="1-й финал")

        view()

    def last(self):
        """открыте соревнований из пункта меню - последние-"""
        sender = self.sender()
        if sender == self.first_comp_Action:
            go_to()
        elif sender == self.second_comp_Action:
            go_to()
        elif sender == self.third_comp_Action:
            go_to()
        elif sender == self.fourth_comp_Action:
            go_to()
        elif sender == self.fifth_comp_Action:
            go_to()


app = QApplication(sys.argv)
my_win = MainWindow()
my_win.setWindowTitle("Соревнования по настольному теннису")

# def change_menu():
#     """"""
#     t = title_id()
#     MainWindow._createAction()
#     my_win.view_fin3_Action.setVisible(True)  # делает пункт меню не видимым


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
            # получение последней записи в таблице
            t_id = Title.select().order_by(Title.id.desc()).get()
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
        full_name = db_select_title()
        self.close()
        my_win.setWindowTitle(f"Соревнования по настольному теннису. {full_name}")
        my_win.show()


    def new(self):
        """запускает новые соревнования"""
        msgBox = QMessageBox
        result = msgBox.question(my_win, "", "Вы действительно хотите создать новые соревнования?",
                                 msgBox.Ok, msgBox.Cancel)
        if result == msgBox.Ok:
            gamer = ("Мальчики", "Девочки", "Юноши",
                     "Девушки", "Мужчины", "Женщины")
            gamer, ok = QInputDialog.getItem(
                my_win, "Участники", "Выберите категорию спортсменов", gamer, 0, False)

            title = Title(name="", sredi="", vozrast="", data_start="", data_end="", mesto="", referee="",
                          kat_ref="", secretary="", kat_sek="", gamer=gamer, full_name_comp="", pdf_comp="",
                          short_name_comp="").save()
            # получение последней записи в таблице
            t_id = Title.select().order_by(Title.id.desc()).get()
            title_id = t_id.id
            db_r(gamer)
            system = System(title_id=title_id, total_athletes=0, total_group=0, max_player=0, stage="", type_table="",
                            page_vid="", label_string="", kol_game_string="", choice_flag=False, score_flag=5,
                            visible_game=True, stage_exit="", mesta_exit=0).save()
            self.close()
            tab_enabled(gamer)
            my_win.show()
        else:
            return

    def last_competition():
        """заполняе меню -последние- прошедшими соревнованиями 5 штук"""
        go_to()
    

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
        # получение последней записи в таблице
        t_id = Title.select().order_by(Title.id.desc())
        n = 6
        for i in t_id:
            old_comp = i.name
            gamer = i.gamer
            n -= 1
            if n != 5:
                if old_comp != "":
                    self.comboBox.addItem(f"{old_comp}. {gamer}")
                else:
                    return
            full_name = i.full_name_comp
            if n > 5:
                break
            if n == 4: 
                if full_name != "":
                    my_win.first_comp_Action.setText(full_name)
                else:
                    my_win.first_comp_Action.setText("Пусто")
            elif n == 3: 
                if full_name != "":
                    my_win.second_comp_Action.setText(full_name)
                else:
                    my_win.second_comp_Action.setText("Пусто")
            elif n == 2: 
                if full_name != "":
                    my_win.third_comp_Action.setText(full_name)
                else:
                    my_win.third_comp_Action.setText("Пусто")
            elif n == 1: 
                if full_name != "":
                    my_win.fourth_comp_Action.setText(full_name)
                else:
                    my_win.fourth_comp_Action.setText("Пусто")
            elif n == 0: 
                if full_name != "":
                    my_win.fifth_comp_Action.setText(full_name)
                else:
                    my_win.fifth_comp_Action.setText("Пусто")
            # i += 1      

        if fir_window.comboBox.currentText() != "":
            fir_window.Button_open.setEnabled(True)
            t_id = Title.select().order_by(Title.id.desc()).get()
            k = (t_id.id) - 1
            title = Title.get(Title.id == k)
            old_comp = title.name
            gamer = title.gamer
            data_start = title.data_start
            data_finish = title.data_end
            fir_window.comboBox.setCurrentText(f"{old_comp}. {gamer}")
            fir_window.label_4.setText(f"сроки: с {data_start} по {data_finish}")


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
        ext = f"(*_m.xlsx, *_m.xls)"
    else:
        table_db = R_list_d
        ext = f"(*_w.xlsx, *_w.xls)"
    fname = QFileDialog.getOpenFileName(
        my_win, "Выбрать файл R-листа", "", f"Excels files {ext}")
    if fname == ("", ""):
        # получение последней записи в таблице
        title = Title.select().order_by(Title.id.desc()).get()
        system = System.get(Title.id == title)
        system.delete_instance()
        title.delete_instance()
        return
    control_R_list(fname, gamer)
    load_listR_in_db(fname, table_db)
    my_win.statusbar.showMessage("Текущий рейтинг загружен")
    if gamer == "Мальчики" or gamer == "Юноши" or gamer == "Мужчины":
        table_db = R1_list_m
        ext = "(*01_m.xlsx, *01_m.xls)"
    else:
        table_db = R1_list_d
        ext = "(*01_w.xlsx, *01_w.xls)"
    fname = QFileDialog.getOpenFileName(
        my_win, "Выбрать файл R-листа", "", f"Excels files {ext}")
    load_listR_in_db(fname, table_db)
    my_win.statusbar.showMessage("Январский рейтинг загружен")
    # добавляет в таблицу регионы
    # получение последней записи в таблице
    t = Title.select().order_by(Title.id.desc()).get()
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
    # показывает статус бар на 5 секунд
    my_win.statusbar.showMessage("Список регионов загружен", 5000)
    my_win.lineEdit_title_nazvanie.hasFocus()


def control_R_list(fname, gamer):
    """проверка рейтинга текущему месяцу"""
    filepatch = str(fname[0])
    znak = filepatch.rfind("/")
    month_vybor = filepatch[znak + 6:znak + 8]
    d = date.today()
    current_month = d.strftime("%m")
    if current_month != month_vybor:
        message = "Вы выбрали файл не с актуальным рейтингом!\nесли все равно хотите его использовать, нажмите <Ок>\nесли хотите вернуться, нажмите <Отмена>"
        reply = QtWidgets.QMessageBox.information(my_win, 'Уведомление', message,
                                                  QtWidgets.QMessageBox.Ok,
                                                  QtWidgets.QMessageBox.Cancel)
        if reply == QMessageBox.Ok:
            return
        else:
            db_r(gamer)
    else:
        return


def load_listR_in_db(fname, table_db):
    """при отсутствии выбора файла рейтинга, позволяет выбрать вторично или выйти из диалога
    если выбор был сделан загружает в базу данных"""
    filepatch = str(fname[0])
    if table_db == R_list_m or table_db == R_list_d:
        r = "текущим"
    elif table_db == R1_list_m or table_db == R1_list_d:
        r = "январским"
    if filepatch == "":
        message = f"Вы не выбрали файл с {r} рейтингом!\nесли хотите выйти, нажмите <Ок>\nесли хотите вернуться, нажмите <Отмена>"
        reply = QtWidgets.QMessageBox.information(my_win, 'Уведомление', message,
                                                  QtWidgets.QMessageBox.Ok,
                                                  QtWidgets.QMessageBox.Cancel)
        if reply == QMessageBox.Ok:
            return
        else:
            db_r(table_db)
    else:
        data = []
        data_tmp = []

        rlist = table_db.delete().execute()

        excel_data = pd.read_excel(filepatch)  # читает  excel файл Pandas
        data_pandas = pd.DataFrame(excel_data)  # получает Dataframe
        # создает список заголовков столбцов
        column = data_pandas.columns.ravel().tolist()
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


def change_sroki():
    """изменение текста label формы стартового окна в зависимости от выбора соревнования"""
    t_id = Title.select().order_by(Title.id.desc()).get()
    k = t_id.id - 1
    tit = Title.get(Title.id == k)
    index = fir_window.comboBox.currentIndex()
    id = k - index
    title = Title.get(Title.id == id)
    data_start = title.data_start
    data_finish = title.data_end
    fir_window.label_4.setText(f"сроки: с {data_start} по {data_finish}")


#  ==== наполнение комбобоксов ==========
page_orient = ("альбомная", "книжная")
kategoria_list = ("2-я кат.", "1-я кат.", " ССВК")
mylist = ('мальчиков и девочек', 'юношей и девушек', 'мужчин и женщин')
raz = ("б/р", "3-юн", "2-юн", "1-юн", "3-р",
       "2-р", "1-р", "КМС", "МС", "МСМК", "ЗМС")
res = ("все игры", "завершенные", "не сыгранные")
stages1 = ("", "Одна таблица", "Предварительный",
           "Полуфиналы", "Финальный", "Суперфинал")
stages2 = ("", "Полуфиналы", "Финальный", "Суперфинал")
stages3 = ("", "Финальный", "Суперфинал")
vid_setki = ("", "Сетка (-2)", "Сетка (с розыгрышем всех мест)",
             "Сетка (за 1-3 место)", "Круговая система")


my_win.comboBox_page_vid.addItems(page_orient)
# my_win.comboBox_etap_1.addItems(stages1)
# my_win.comboBox_etap_2.addItems(stages2)
# my_win.comboBox_etap_3.addItems(stages3)
# my_win.comboBox_etap_4.addItems(stages3)
# my_win.comboBox_etap_5.addItems(stages3)
my_win.comboBox_kategor_ref.addItems(kategoria_list)
my_win.comboBox_kategor_sek.addItems(kategoria_list)
my_win.comboBox_sredi.addItems(mylist)
my_win.comboBox_razryad.addItems(raz)
my_win.comboBox_filter_played.addItems(res)
my_win.comboBox_filter_played_fin.addItems(res)
# my_win.comboBox_table.addItems(vid_setki)
# my_win.comboBox_table_2.addItems(vid_setki)
# my_win.comboBox_table_3.addItems(vid_setki)
# my_win.comboBox_table_4.addItems(vid_setki)
# my_win.comboBox_one_table.addItems(vid_setki)

def clear_add_combobox():
    """"""
    my_win.comboBox_etap_1.clear()
    my_win.comboBox_etap_2.clear()
    my_win.comboBox_etap_3.clear()
    my_win.comboBox_etap_4.clear()
    my_win.comboBox_etap_5.clear()
    my_win.comboBox_etap_1.addItems(stages1)
    my_win.comboBox_etap_2.addItems(stages2)
    my_win.comboBox_etap_3.addItems(stages3)
    my_win.comboBox_etap_4.addItems(stages3)
    my_win.comboBox_etap_5.addItems(stages3)
    my_win.comboBox_table.clear()
    my_win.comboBox_table_2.clear()
    my_win.comboBox_table_3.clear()
    my_win.comboBox_table_4.clear()
    my_win.comboBox_one_table.clear()
    my_win.comboBox_table.addItems(vid_setki)
    my_win.comboBox_table_2.addItems(vid_setki)
    my_win.comboBox_table_3.addItems(vid_setki)
    my_win.comboBox_table_4.addItems(vid_setki)
    my_win.comboBox_one_table.addItems(vid_setki) 


# ставит сегодняшнюю дату в виджете календарь
my_win.dateEdit_start.setDate(date.today())
my_win.dateEdit_end.setDate(date.today())


def tab_enabled(gamer):
    """Включает вкладки в зависимости от создании системы и жеребьевки"""
    sender = my_win.sender()
    title = title_id()  # id текущего соревнования
    count_title = len(Title.select())
    tit = Title.select().order_by(Title.id.desc()).get()  # получает последний title.id
    t_next = tit.id
    n = 6
    if sender == fir_window.LinkButton:  # если переход со стартового окна последение соревнование
        t = t_next - 1
        t_id = Title.get(Title.id == t)
    else:
        if t_next > title:
            t_id = Title.get(Title.id == t_next)
        else:
            t_id = Title.get(Title.id == t_next - 1)

    old_comp = t_id.name
    old_data = t_id.data_start
    old_gamer = t_id.gamer
    comp = f"{old_comp}.{old_data}.{old_gamer}"
    my_win.go_to_Action.setText(comp)
    last_competition()
    if gamer == "":
        gamer = my_win.lineEdit_title_gamer.text()
    if count_title != 0:  # когда создаются новые соревнования
        my_win.setWindowTitle(f"Соревнования по настольному теннису. {gamer}")
        system = System.select().where(System.title_id == title)  # находит system id первого
        count = len(system)
        stage = []
        for i in system:
            st = i.stage
            stage.append(st)
        count_stage = len(stage)
        if count_stage >= 1:  # если система еще не создана, то выключает отдельные вкладки при переходе на другое сорев
            if count > 0:
                # выключает отдельные вкладки
                my_win.tabWidget.setTabEnabled(2, True)
                my_win.toolBox.setItemEnabled(2, True)
                for i in stage:
                    if i == "Одна таблица":
                        system = System.get(
                            System.title_id == title and System.stage == i)
                        flag = system.choice_flag
                        if flag is True:
                            my_win.tabWidget.setTabEnabled(3, False_)
                            my_win.tabWidget.setTabEnabled(5, True)
                    elif i == "Предварительный":
                        system = System.get(
                            System.id == title and System.stage == i)
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
                    elif i == "":
                        my_win.tabWidget.setTabEnabled(3, False)
                        my_win.tabWidget.setTabEnabled(4, False)
                        my_win.tabWidget.setTabEnabled(5, False)
                my_win.tabWidget.setCurrentIndex(1)
        else:
            # выключает отдельные вкладки
            my_win.tabWidget.setTabEnabled(2, True)
            my_win.tabWidget.setTabEnabled(3, False)
            my_win.tabWidget.setTabEnabled(4, False)
            my_win.tabWidget.setTabEnabled(5, False)
            my_win.tabWidget.setCurrentIndex(1)
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
    short_name, ok = QInputDialog.getText(my_win, "Краткое имя соревнования", "Создайте краткое имя соревнования,\nдля"
                                          " отбражения в названии файла при "
                                          "сохранении,\nиспользуете латинские буквы"
                                          " без пробелов.\n"
                                          "В формате название, возраст участников_дата,"
                                          " месяц, год и кто "
                                          "играет.")
    if ok:
        # получение последней записи в таблице
        t = Title.select().order_by(Title.id.desc()).get()
        nazv = Title(id=t, name=nm, sredi=sr, vozrast=vz, data_start=ds, data_end=de, mesto=ms, referee=rf,
                     kat_ref=kr, secretary=sk, kat_sek=ks, gamer=gm, full_name_comp=fn, pdf_comp="",
                     short_name_comp=short_name).save()
    else:
        return


def go_to():
    """переход на предыдущие соревнования и обратно при нажатии меню -перейти к- или из меню -последние-"""
    msgBox = QMessageBox
    sender = my_win.sender()
    tit = Title.get(Title.id == title_id())
    name = tit.name
    data = tit.data_start
    gamer_current = tit.gamer
    # полное название текущих соревнований
    full_name_current = f"{name}.{data}.{gamer_current}"

    if sender == my_win.first_comp_Action:
        full_name = my_win.first_comp_Action.text()
    elif sender == my_win.second_comp_Action:
        full_name = my_win.second_comp_Action.text()
    elif sender == my_win.third_comp_Action:
        full_name = my_win.third_comp_Action.text()
    elif sender == my_win.fourth_comp_Action:
        full_name = my_win.fourth_comp_Action.text()
    elif sender == my_win.fifth_comp_Action:
        full_name = my_win.fifth_comp_Action.text()
    elif sender == my_win.go_to_Action:
        full_name = my_win.go_to_Action.text()  # полное название к которым переходим 
        # присваиваем новый текст соревнований в меню -перейти к-
        my_win.go_to_Action.setText(full_name_current)

    if full_name == full_name_current:
        reply = msgBox.information(my_win, 'Уведомление', 'Данные соревнования уже открыты.',
                                    msgBox.Ok)
  
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
    my_win.tabWidget.setCurrentIndex(1)  # открывает вкладку список
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
        # полное название текущих соревнований
        full_name_current = f"{name}.{data}.{gamer_current}"
        # присваиваем новый текст соревнований в меню -перейти к-
        my_win.go_to_Action.setText(full_name_current)
        titles = Title.get(Title.full_name_comp == full_name)
        gamer = titles.gamer
    elif sender == my_win.toolBox or sender.text() != "Открыть":
        titles = Title.get(Title.id == title_id())
        name = titles.name
        gamer = titles.gamer
    # сигнал от кнопки с текстом -открыть- соревнования из архива (стартовое окно)
    else:
        change_sroki()
        txt = fir_window.comboBox.currentText()
        key = txt.rindex(".")
        gamer = txt[39:]
        name = txt[:37]
        sroki = fir_window.label_4.text()
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
    # tab_enabled(gamer)

    return gamer


def system_edit():
    """редактирование системы"""
    system_made()


def system_made():
    """Заполняет таблицу система кол-во игроков, кол-во групп и прочее"""
    t = Title.select().where(Title.id == title_id())  # последний id соревнований (текуших)
    # находит system id последнего
    ce = System.select().where(System.title_id == t).get()
    # все строки, где title_id соревнований
    cs = System.select().where(System.id == ce)
    count_system = len(cs)  # получение количества записей (этапов) в системе
    sg = my_win.comboBox_one_table.currentText()
    page_v = my_win.comboBox_page_1.currentText()
    total_group = ce.total_group
    total_athletes = ce.total_athletes
    max_player = ce.max_player
    if sg == "одна таблица":
        system = System(id=cs, title_id=t, total_athletes=total_athletes, total_group=0,
                        max_player=0, stage=sg, page_vid=page_v, label_string="", kol_game_string="",
                        choice_flag=False, score_flag=5, visible_game=True).save()
    else:  # предварительный этап
        for i in range(1, count_system + 1):
            system = System(id=cs, title_id=t, total_athletes=total_athletes, total_group=total_group,
                            max_player=max_player, stage=sg, page_vid=page_v, label_string="", kol_game_string="",
                            choice_flag=False, score_flag=5, visible_game=True).save()
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
    # сигнал указывающий какой пункт меню нажат
    sender = my_win.menuWidget().sender()
    # нажат пункт меню -текущий рейтинг- или -рейтинг январский
    if sender == my_win.rAction or sender == my_win.r1Action:
        z = 6
        column_label = ["№", "Место", "  Рейтинг",
                        "Фамилия Имя", "Дата рождения", "Город"]
    elif tb == 3 or tb == 5:
        z = 15
        column_label = ["№", "Этапы", "Группа/ финал", "Встреча", "Игрок_1", "Игрок_2", "Победитель", "Очки",
                        "Общий счет",
                        "Счет в партии", "Проигравший", "Очки", "Счет в партии", " title_id"]
    elif tb == 2 or sender == my_win.choice_gr_Action or sender == my_win.choice_fin_Action:
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
    elif tb == 3 or tb == 5:  # таблица результатов
        p = 0
        if tb == 3:
            stage = "Предварительный"
            fill_table_results()
        else:
            system = System.select().where(System.title_id == title_id())  # должен получить первый номер id 
            choice_flag = {} # словарь финал - жеребьевка
            stg = []
            for i in system:
                if i.stage != "Предварительный":
                    stage = i.stage
                    stg.append(stage)
                    flag = ready_choice(stage)
                    choice_flag[stage] = flag

            for k in stg:
                p = 0
                if choice_flag[k] == True:
                    p += 1
            if p > 0:
                fill_table_results()

    elif tb == 2 or sender == my_win.choice_gr_Action:
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
    # получение последней записи в таблице
    title = Title.select().order_by(Title.id.desc()).get()

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
    msgBox = QMessageBox
    string_data = data_title_string()
    nz = my_win.lineEdit_title_nazvanie.text()
    sr = my_win.comboBox_sredi.currentText()
    vz = my_win.lineEdit_title_vozrast.text()
    ct = my_win.lineEdit_city_title.text()

    message = "Хотите добавить изображение в титульный лист?"
    reply = msgBox.question(my_win, 'Уведомление', message,
                                           msgBox.QMessageBo.Yes,
                                           msgBox.No)
    if reply == msgBox.Yes:
        fname = QFileDialog.getOpenFileName(
            my_win, "Выбрать изображение", "/desktop", "Image files (*.jpg, *.png)")
        filepatch = str(fname[0])
    else:
        filepatch = None

    t_id = Title.get(Title.id == title_id())
    short_name = t_id.short_name_comp
    canvas = Canvas(f"title_{short_name}.pdf", pagesize=A4)

    if filepatch == None:
        canvas.setFont("DejaVuSerif-Italic", 14)
        canvas.drawString(
            5 * cm, 28 * cm, "Федерация настольного тенниса России")
        canvas.drawString(
            3 * cm, 27 * cm, "Федерация настольного тенниса Нижегородской области")
        canvas.setFont("DejaVuSerif-Italic", 20)
        canvas.drawString(2 * cm, 23 * cm, nz)
        canvas.setFont("DejaVuSerif-Italic", 16)
        canvas.drawString(2.5 * cm, 22 * cm, f"среди {sr} {vz}")
        canvas.setFont("DejaVuSerif-Italic", 14)
        canvas.drawString(5.5 * cm, 5 * cm, f"г. {ct} Нижегородская область")
        canvas.drawString(7.5 * cm, 4 * cm, string_data)
    else:
        canvas.drawImage(filepatch, 7 * cm, 12 * cm, 6.9 * cm, 4.9 * cm,
                         mask=[0, 2, 0, 2, 0, 2])  # делает фон прозрачным
        canvas.setFont("DejaVuSerif-Italic", 14)
        canvas.drawString(
            5 * cm, 28 * cm, "Федерация настольного тенниса России")
        canvas.drawString(
            3 * cm, 27 * cm, "Федерация настольного тенниса Нижегородской области")
        canvas.setFont("DejaVuSerif-Italic", 20)
        canvas.drawString(2 * cm, 23 * cm, nz)
        canvas.setFont("DejaVuSerif-Italic", 16)
        canvas.drawString(2.5 * cm, 22 * cm, f"среди {sr} {vz}")
        canvas.setFont("DejaVuSerif-Italic", 14)
        canvas.drawString(5.5 * cm, 5 * cm, f"г. {ct} Нижегородская область")
        canvas.drawString(7.5 * cm, 4 * cm, string_data)
    canvas.save()


def title_made():
    """создание тильного листа соревнования"""
    title_str = title_string()
    if my_win.Button_title_made.text() == "Редактировать":
        title_update()
        return
    else:
        db_insert_title(title_str)
    title_pdf()
    # после заполнения титула выключает чекбокс
    my_win.checkBox.setChecked(False)
    my_win.Button_title_made.setText("Создать")
    region()
    # получение последней записи в таблице
    t = Title.select().order_by(Title.id.desc()).get()
    # получение последнего id системы соревнования
    s = System.select().order_by(System.id.desc()).get()

    with db:
        System.create_table()
        sys = System(id=s, title_id=t, total_athletes=0, total_group=0, max_player=0, stage="", page_vid="",
                     label_string="", kol_game_string="", choice_flag=False, score_flag=5, visible_game=True).save()


def data_title_string():
    """получение строки начало и конец соревнований для вставки в титульный лист"""
    months_list = ("января", "февраля", "марта", "апреля", "мая", "июня", "июля",
                   "августа", "сентября", "октября", "ноября", "декабря")
    # получение последней записи в таблице
    title = Title.select().order_by(Title.id.desc()).get()
    datastart = str(title.data_start)
    dataend = str(title.data_end)
    ds = datastart[8:10]  # получаем число день из календаря
    ms = datastart[5:7]  # получаем число месяц из календаря
    ys = datastart[0:4]  # получаем число год из календаря
    # ye = int(dataend[0:4])
    me = dataend[5:7]
    de = dataend[8:10]
    month_st = months_list[int(ms) - 1]
    if de > ds:  # получаем строку начало и конец соревнования в
        # одном месяце или два месяца если начало и конец в разных месяцах
        return f"{ds}-{de} {month_st} {ys} г."
    else:
        month_end = months_list[int(me) - 1]
        return f"{ds} {month_st}-{de} {month_end} {ys} г."


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
    row_count = len(player_selected)  # кол-во строк в таблице
    if row_count != 0:  # список удаленных игроков пуст
        column_count = len(player_selected[0])  # кол-во столбцов в таблице
        # вставляет в таблицу необходимое кол-во строк
        my_win.tableWidget.setRowCount(row_count)
        for row in range(row_count):  # добавляет данные из базы в TableWidget
            for column in range(column_count):
                if column == 7:  # преобразует id тренера в фамилию
                    coach_id = str(list(player_selected[row].values())[column])
                    coach = Coach.get(Coach.id == coach_id)
                    item = coach.coach
                else:
                    item = str(list(player_selected[row].values())[column])
                my_win.tableWidget.setItem(
                    row, column, QTableWidgetItem(str(item)))
        # ставит размер столбцов согласно записям
        my_win.tableWidget.resizeColumnsToContents()
        for i in range(0, row_count):  # отсортировывает номера строк по порядку
            my_win.tableWidget.setItem(i, 0, QTableWidgetItem(str(i + 1)))
    else:
        # вставляет в таблицу необходимое кол-во строк
        my_win.tableWidget.setRowCount(row_count)
        my_win.statusbar.showMessage(
            "Удаленных участников соревнований нет", 10000)


def fill_table_R_list():
    """заполняет таблицу списком из текущего рейтинг листа"""
    player_rlist = R_list_m.select().order_by(R_list_m.r_fname)
    player_r = player_rlist.dicts().execute()
    row_count = len(player_r)  # кол-во строк в таблице
    column_count = len(player_r[0])  # кол-во столбцов в таблице
    # вставляет в таблицу необходимое кол-во строк
    my_win.tableWidget.setRowCount(row_count)

    for row in range(row_count):  # добвляет данные из базы в TableWidget
        for column in range(column_count):
            item = str(list(player_r[row].values())[column])
            my_win.tableWidget.setItem(
                row, column, QTableWidgetItem(str(item)))

    # ставит размер столбцов согласно записям
    my_win.tableWidget.resizeColumnsToContents()


def fill_table_R1_list():
    """заполняет таблицу списком из январского рейтинг листа"""
    player_rlist = R1_list_m.select().order_by(R1_list_m.r1_fname)
    player_r1 = player_rlist.dicts().execute()
    row_count = len(player_r1)  # кол-во строк в таблице
    column_count = len(player_r1[0])  # кол-во столбцов в таблице
    # вставляет в таблицу необходимое кол-во строк
    my_win.tableWidget.setRowCount(row_count)

    for row in range(row_count):  # добавляет данные из базы в TableWidget
        for column in range(column_count):
            item = str(list(player_r1[row].values())[column])
            my_win.tableWidget.setItem(
                row, column, QTableWidgetItem(str(item)))

    # ставит размер столбцов согласно записям
    my_win.tableWidget.resizeColumnsToContents()


def fill_table_results():
    """заполняет таблицу результатов QtableWidget из db result"""
    msg = QMessageBox
    tb = my_win.tabWidget.currentIndex()
    if tb == 3:
        stage = "Предварительный"
    elif tb == 4:
        pass
    else:
        stage = my_win.comboBox_filter_final.currentText()
        if stage == "Одна таблица":
            stage = "Одна таблица"
        else:
            stage = "Финальный"
    result = Result.select().where(Result.title_id == title_id())
    pl_result = result.select().order_by(Result.id)
    pr = pl_result.select().where(Result.system_stage == stage)  # проверка есть ли записи в таблице -result-
    count = len(pr)  # если 0, то записей нет
    flag = ready_system()
    if flag is True and count == 0:
        message = "Надо сделать жербьевку предварительного этапа.\nХотите ее создать?"
        reply = msg.question(my_win, 'Уведомление', message, msg.Yes, msg.No)
        if reply == msg.Yes:
            choice_gr_automat()
        else:
            return
    elif flag is False and count == 0:
        message = "Сначала надо создать систему соревнований\nзатем произвести жербьевку.\n" \
                  "Хотите начать ее создавать?"
        reply = msg.question(my_win, 'Уведомление', message, msg.Yes, msg.No)
        if reply == msg.Yes:
            system_competition()
        else:
            return
    else:
        # надо выбрать, что загружать в зависимости от вкладки группы, пф или финалы
        if tb == 3:
            player_result = pl_result.select().where(Result.system_stage == "Предварительный")
        elif tb == 4:
            player_result = result.select().order_by(Result.id)
        elif tb == 5:  # здесь надо выбрать финалы (круг или сетка)
            player_result = result.select().order_by(Result.id).where(Result.title_id == title_id() and
                                                                      Result.system_stage == stage)  # проверка есть ли записи в таблице -result-
            # player_result = pl_result.select().where(Result.system_stage == stage)
            count_result = len(player_result)
            if count_result == 0:
                return
        result_list = player_result.dicts().execute()
        row_count = len(result_list)  # кол-во строк в таблице
        column_count = len(result_list[0])  # кол-во столбцов в таблице
        # вставляет в таблицу необходимое кол-во строк
        my_win.tableWidget.setRowCount(row_count)
        row_result = []
        for row in range(row_count):  # добавляет данные из базы в TableWidget
            for column in range(column_count):
                item = str(list(result_list[row].values())[column])
                if column < 6:
                    row_result.append(item)
                    my_win.tableWidget.setItem(
                        row, column, QTableWidgetItem(str(item)))
                elif column == 6:
                    row_result.append(item)
                    if row_result[6] != "None" and row_result[6] != "":  # встреча сыграна
                        if row_result[4] == row_result[6]:
                            my_win.tableWidget.item(row, 4).setForeground(
                                QBrush(QColor(255, 0, 0)))  # окрашивает текст
                            # в красный цвет 1-ого игрока
                        else:
                            my_win.tableWidget.item(row, 5).setForeground(
                                QBrush(QColor(255, 0, 0)))  # окрашивает текст
                            # в красный цвет 2-ого игрока
                    else:
                        my_win.tableWidget.item(row, 4).setForeground(
                            QBrush(QColor(0, 0, 0)))  # в черный цвет 1-ого
                        my_win.tableWidget.item(row, 5).setForeground(
                            QBrush(QColor(0, 0, 0)))  # в черный цвет 2-ого
                    row_result.clear()
                    my_win.tableWidget.setItem(
                        row, column, QTableWidgetItem(str(item)))
                elif column > 6:
                    my_win.tableWidget.setItem(
                        row, column, QTableWidgetItem(str(item)))

        my_win.tableWidget.showColumn(6)  # показывает столбец победитель
        my_win.tableWidget.hideColumn(10)
        my_win.tableWidget.hideColumn(11)
        my_win.tableWidget.hideColumn(12)
        my_win.tableWidget.hideColumn(13)
        # ставит размер столбцов согласно записям
        my_win.tableWidget.resizeColumnsToContents()


def fill_table_choice():
    """заполняет таблицу жеребьевки"""
    gamer = my_win.lineEdit_title_gamer.text()
    player_choice = Choice.select().where(Choice.title_id == title_id()).order_by(Choice.rank.desc())
    choice_list = player_choice.dicts().execute()
    row_count = len(choice_list)  # кол-во строк в таблице
    if row_count != 0:
        column_count = len(choice_list[0])  # кол-во столбцов в таблице
        # вставляет в таблицу необходимое кол-во строк
        my_win.tableWidget.setRowCount(row_count)
        for row in range(row_count):  # добавляет данные из базы в TableWidget
            for column in range(column_count):
                item = str(list(choice_list[row].values())[column])
                my_win.tableWidget.setItem(
                    row, column, QTableWidgetItem(str(item)))
        # ставит размер столбцов согласно записям
        my_win.tableWidget.resizeColumnsToContents()
        for i in range(0, row_count):  # отсортировывает номера строк по порядку
            my_win.tableWidget.setItem(i, 0, QTableWidgetItem(str(i + 1)))


def fill_table_after_choice():
    """заполняет TableWidget после жеребьевки """
    choice = Choice.select().where(Choice.title_id == title_id())
    pl_choice = choice.select().order_by(Choice.group)
    player_choice = pl_choice.select().order_by(Choice.posev_group)
    choice_list = player_choice.dicts().execute()
    row_count = len(choice_list)  # кол-во строк в таблице
    if row_count != 0:
        column_count = len(choice_list[0])  # кол-во столбцов в таблице
        # вставляет в таблицу необходимое кол-во строк
        my_win.tableWidget.setRowCount(row_count)
        for row in range(row_count):  # добавляет данные из базы в TableWidget
            for column in range(column_count):
                item = str(list(choice_list[row].values())[column])
                my_win.tableWidget.setItem(
                    row, column, QTableWidgetItem(str(item)))
        # ставит размер столбцов согласно записям
        my_win.tableWidget.resizeColumnsToContents()
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
                         razryad=rz, coach_id=idc, full_name=fn, mesto=ms, title_id=title_id()).save()
        my_win.checkBox_6.setChecked(False)  # сбрасывает флажок -удаленные-
    else:  # просто редактирует игрока
        txt = my_win.Button_add_edit_player.text()
        if txt == "Редактировать":
            with db:
                plr = Player.get(Player.player == pl)
                plr.player = pl
                plr.bday = bd
                plr.rank = rn
                plr.city = ct
                plr.region = rg
                plr.razryad = rz
                plr.coach_id = idc
                plr.full_name = fn
                plr.save()
        elif txt == "Добавить":
            with db:
                player = Player(player=pl, bday=bd, rank=rn, city=ct, region=rg, razryad=rz,
                                coach_id=idc, mesto="", full_name=fn, title_id=title_id()).save()
    spisok = (str(num), pl, bd, rn, ct, rg, rz, ch, ms)
    for i in range(0, 9):  # добавляет в tablewidget
        my_win.tableWidget.setItem(count + 1, i, QTableWidgetItem(spisok[i]))
    load_tableWidget()  # заново обновляет список
    player_list = Player.select().where(Player.title_id == title_id())
    count = len(player_list)  # подсчитывает новое кол-во игроков
    my_win.label_46.setText(f"Всего: {count} участников")
    list_player_pdf(player_list)
    my_win.lineEdit_Family_name.clear()
    my_win.lineEdit_bday.clear()
    my_win.lineEdit_R.clear()
    my_win.lineEdit_city_list.clear()
    my_win.lineEdit_coach.clear()


def dclick_in_listwidget():
    """Находит фамилию спортсмена в рейтинге или фамилию тренера и заполняет соответсвующие поля списка"""
    text = my_win.listWidget.currentItem().text()
    # если строка "тренер" пустая значит заполняются поля игрока
    tc = my_win.lineEdit_coach.text()
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
    system = System.select().where(System.title_id == title_id())  # находит system id последнего
    fin = ["все финалы"]
    for sys in system:
        if sys.stage == "Одна таблица":
            fin = []
            if sys.choice_flag is True:
                fin.append(sys.stage)
        elif sys.stage != "Предварительный" and sys.stage != "Полуфиналы":
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
        my_win.Button_clear_del.setEnabled(False)
        my_win.Button_add_edit_player.setText("Добавить")
        my_win.statusbar.showMessage("Список участников соревнований", 5000)
        player_list = Player.select().where(Player.title_id == title_id())
        count = len(player_list)
        my_win.label_46.setText(f"Всего: {count} участников")
    elif tb == 2:  # -система-
        result = Result.select().where(Result.title_id == title_id())
        result_played = result.select().where(Result.winner != "")
        count_result = len(result_played)
        player_list = Player.select().where(Player.title_id == title_id())
        count = len(player_list)
        my_win.label_8.setText(f"Всего участников: {str(count)} человек")
        my_win.label_52.setText(f"Сыграно: {count_result} игр.")
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
        my_win.label_59.hide()
        my_win.label_55.hide()
        my_win.label_56.hide()
        my_win.label_53.hide()
        my_win.label_58.hide()
        my_win.label_60.hide()
        my_win.label_61.hide()
        my_win.label_62.hide()
        my_win.comboBox_etap_1.hide()
        my_win.comboBox_etap_2.hide()
        my_win.comboBox_etap_3.hide()
        my_win.comboBox_etap_4.hide()
        my_win.comboBox_etap_5.hide()
        my_win.comboBox_table.hide()
        my_win.comboBox_table_2.hide()
        my_win.comboBox_table_3.hide()
        my_win.comboBox_table_4.hide()
        my_win.spinBox_kol_group.hide()
        my_win.comboBox_one_table.hide()

        flag = ready_system()

        if flag is False:  # система еще не создана
            my_win.statusbar.showMessage("Создание системы соревнования", 10000)
            my_win.label_10.show()
            my_win.comboBox_etap_1.show()
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
                if i == 0:  # показывает в зависимости от этапов финал, кол-во игр
                    my_win.label_9.setText(stage[0])
                    my_win.label_19.setText(game[0])
                    my_win.label_12.setText(table[0])
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
                elif i == 3:
                    my_win.label_55.setText(stage[3])
                    my_win.label_53.setText(game[3])
                    my_win.label_61.setText(table[3])
                    my_win.label_55.show()
                    my_win.label_53.show()
                    my_win.label_61.show()
                elif i == 4:
                    my_win.label_56.setText(stage[3])
                    my_win.label_58.setText(game[3])
                    my_win.label_62.setText(table[3])
                    my_win.label_56.show()
                    my_win.label_58.show()
                    my_win.label_62.show()

            total_game = sum(sum_game)
            my_win.comboBox_table.hide()
            my_win.comboBox_page_vid.setEnabled(False)
            my_win.Button_etap_made.setEnabled(False)
            my_win.Button_system_made.setEnabled(False)
            my_win.label_33.setText(f"Всего {total_game} игр")
            my_win.label_33.show()
        load_tableWidget()
    elif tb == 3:  # вкладка -группы-
        my_win.checkBox_7.setEnabled(False)
        my_win.checkBox_8.setEnabled(False)
        my_win.checkBox_7.setChecked(False)
        my_win.checkBox_8.setChecked(False)
        flag = ready_choice(stage="Предварительный")
        if flag is False:
            result = msgBox.information(my_win, "", "Необходимо сделать жеребьевку\nпредварительного этапа.",
                                        msgBox.Ok, msgBox.Cancel)
            if result != msgBox.Ok:
                return
            else:
                my_win.tabWidget.setCurrentIndex(2)
                choice_gr_automat()
                sf.choice_flag = True
                sf.save()
            my_win.tabWidget.setCurrentIndex(3)
        else:  # жеребьевка сделана
            my_win.tableWidget.show()
            my_win.Button_Ok.setEnabled(False)
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
        my_win.checkBox_9.setEnabled(False)
        my_win.checkBox_10.setEnabled(False)
        my_win.tableWidget.show()
        my_win.Button_Ok_fin.setEnabled(False)
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


def sort():
    """сортировка таблицы QtableWidget (по рейтингу или по алфавиту)"""
    sender = my_win.sender()  # сигнал от кнопки

    if sender == my_win.Button_sort_R:  # в зависимости от сигала кнопки идет сортировка
        player_list = Player.select().where(Player.title_id == title_id()).order_by(
            Player.rank.desc())  # сортировка по рейтингу
    elif sender == my_win.Button_sort_Name:
        player_list = Player.select().where(Player.title_id == title_id()).order_by(
            Player.player)  # сортировка по алфавиту
    elif sender == my_win.Button_sort_mesto:
        player_list = Player.select().where(Player.title_id == title_id()
                                            ).order_by(Player.mesto)  # сортировка по месту

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
        # получение последней записи в таблице
        t = Title.select().order_by(Title.id.desc()).get()
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
    from reportlab.platypus import Table
    story = []  # Список данных таблицы участников
    elements = []  # Список Заголовки столбцов таблицы
    tit = Title.get(Title.id == title_id())
    short_name = tit.short_name_comp
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
                           # Использую импортированный шрифта размер
                           ('FONTSIZE', (0, 0), (-1, -1), 7),
                           # межстрочный верхний инервал
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
                           # межстрочный нижний инервал
                           ('TOPPADDING', (0, 0), (-1, -1), 1),
                           # вериткальное выравнивание в ячейке заголовка
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                           # горизонтальное выравнивание в ячейке
                           ('ALIGN', (0, 0), (-1, kp * -1), 'CENTER'),
                           ('BACKGROUND', (0, 0), (-1, kp * -1), colors.yellow),
                           ('TEXTCOLOR', (0, 0), (-1, kp * -1), colors.darkblue),
                           ('LINEABOVE', (0, 0), (-1, kp * -1), 1, colors.blue),
                           # цвет и толщину внутренних линий
                           ('INNERGRID', (0, 0), (-1, -1), 0.05, colors.black),
                           # внешние границы таблицы
                           ('BOX', (0, 0), (-1, -1), 0.5, colors.black)
                           ]))

    h3 = PS("normal", fontSize=12, fontName="DejaVuSerif-Italic", leftIndent=150,
            firstLineIndent=-20)  # стиль параграфа
    h3.spaceAfter = 10  # промежуток после заголовка
    story.append(Paragraph(f'Список участников. {gamer}', h3))
    story.append(t)

    doc = SimpleDocTemplate(f"table_list_{short_name}.pdf", pagesize=A4)
    change_dir()
    doc.build(story, onFirstPage=func_zagolovok, onLaterPages=func_zagolovok)


def exit_comp():
    """нажата кнопка -выход-"""
    msgBox = QMessageBox
    result = msgBox.question(my_win, "Выход из программы", "Вы действительно хотите выйти из программы?",
                             msgBox.Ok, msgBox.Cancel)
    if result == msgBox.Ok:
        my_win.close()
        backup()
    else:
        pass


def system_competition():
    """выбор системы проведения"""
    msgBox = QMessageBox
    sender = my_win.sender()
    tit = Title.get(Title.id == title_id())
    gamer = tit.gamer
    flag_system = ready_system()
    if sender == my_win.system_made_Action or sender == my_win.system_edit_Action:
        clear_add_combobox()
        # нажат меню -система- или -жеребьевка- или вкладка -система-
        if sender == my_win.system_edit_Action:
            sb = "Изменение системы проведения соревнования."
            my_win.statusbar.showMessage(sb)
            result = msgBox.question(my_win, "", "Вы хотите изменить систему соревнований?",
                                    msgBox.Ok, msgBox.Cancel)
            if result == msgBox.Ok:
                # очищает таблицы перед новой системой соревнования (system, choice)
                clear_db_before_edit()
                tab_enabled(gamer)  # показывает вкладки по новому
                choice_tbl_made()  # заполняет db жеребьевка
                flag_system = False
                stage = ""
            else:
                return
        elif sender == my_win.system_made_Action: 
            sb = "Создание системы проведения соревнования."
            my_win.statusbar.showMessage(sb)
            result = msgBox.question(my_win, "", "Вы хотите создать систему соревнований?",
                                msgBox.Ok, msgBox.Cancel)
            if result == msgBox.Ok:
                choice_tbl_made()  # заполняет db жеребьевка
            else:
                return
        my_win.spinBox_kol_group.hide()
        my_win.comboBox_etap_1.setEnabled(True)
        my_win.comboBox_etap_2.setEnabled(True)
        my_win.comboBox_etap_3.setEnabled(True)
        my_win.comboBox_etap_4.setEnabled(True)
        my_win.comboBox_etap_5.setEnabled(True)
        my_win.comboBox_etap_1.show()
        my_win.comboBox_etap_2.hide()
        my_win.comboBox_etap_3.hide()
        my_win.comboBox_etap_4.hide()
        my_win.comboBox_etap_5.hide()
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
        my_win.label_55.hide()
        my_win.label_56.hide()
        my_win.label_53.hide()
        my_win.label_58.hide()
        my_win.label_59.hide()
        
        my_win.comboBox_table.hide()
        my_win.comboBox_table_2.hide()
        my_win.comboBox_table_3.hide()
        my_win.comboBox_table_4.hide()
        my_win.tabWidget.setTabEnabled(2, True)
        # my_win.toolBox.setTabEnabled(2, True)

        if flag_system is True:
            flag_choice = ready_choice(stage)
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
            my_win.comboBox_etap_4.setEnabled(True)
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
            my_win.label_53.hide()

            my_win.comboBox_table.hide()
            player = Player.select().where(Player.title_id == title_id())
            count = len(player)
            if count != 0:
                my_win.tabWidget.setCurrentIndex(2)
            else:
                reply = QMessageBox.information(my_win, 'Уведомление',
                                                "У Вас нет ни одного спортсмена.\nСначала необходимо создать "
                                                "список участников соревнований.\n Перейти к созданию списка?",
                                                msgBox.Ok,
                                                msgBox.Cancel)
                if reply == msgBox.Ok:
                    my_win.tabWidget.setCurrentIndex(1)
                    my_win.lineEdit_Family_name.setFocus()
                else:
                    return
    elif sender == my_win.tabWidget:
        my_win.spinBox_kol_group.hide()
        my_win.comboBox_etap_1.setEnabled(True)
        my_win.comboBox_etap_2.setEnabled(True)
        my_win.comboBox_etap_3.setEnabled(True)
        my_win.comboBox_etap_4.setEnabled(True)
        my_win.comboBox_etap_5.setEnabled(True)
        my_win.comboBox_etap_1.show()
        my_win.comboBox_etap_2.hide()
        my_win.comboBox_etap_3.hide()
        my_win.comboBox_etap_4.hide()
        my_win.comboBox_etap_5.hide()
        my_win.label_10.show()
        my_win.label_15.hide()
        my_win.label_17.hide()
        my_win.label_29.hide()
        my_win.label_59.hide()
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
        my_win.label_32.hide()
        my_win.label_55.hide()
        my_win.label_56.hide()
        my_win.label_30.hide()
        my_win.label_53.hide()
        my_win.label_58.hide()
        my_win.comboBox_table.show()
    elif sender == my_win.comboBox_etap_3:
        my_win.label_32.show()
        my_win.label_30.hide()
        my_win.label_31.hide()
        my_win.comboBox_table_2.show()
    elif sender == my_win.comboBox_etap_4:
        my_win.label_55.show()
        my_win.label_53.hide()
        my_win.comboBox_table_3.show()
    elif sender == my_win.comboBox_etap_5:
        my_win.label_56.show()
        my_win.label_58.hide()
        my_win.comboBox_table_4.show()
    else:  # скрывает и выключает label и combobox этапов систем
        my_win.label_10.hide()
        my_win.label_15.hide()
        my_win.label_17.hide()
        my_win.comboBox_etap_1.setEnabled(False)
        my_win.comboBox_etap_2.setEnabled(False)
        my_win.comboBox_etap_3.setEnabled(False)
        my_win.comboBox_etap_4.setEnabled(False)


def one_table(fin, mesto_in_group, group):
    """система соревнований из одной таблицы запись в System"""
    t_id = title_id()
    system = System.select().where(System.title_id == t_id)
    for sys in system:
        if sys.stage == fin:  # если финал играется по кругу
            type_tbl = sys.type_table
            if type_tbl == "круг":
                count_player = mesto_in_group["выход"]
                mesta_exit = mesto_in_group["место"]
                count = group * count_player

                kol_game = f"{count // 2 * (count - 1)} игр"
                my_win.Button_etap_made.setEnabled(False)
                my_win.comboBox_page_vid.setEnabled(False)
            elif type_tbl == "сетка":
                count_player = mesto_in_group["выход"]
                mesta_exit = mesto_in_group["место"]

            load_tableWidget()

            choice = Choice.select().where(
                Choice.title_id == t_id and Choice.mesto_group == mesta_exit)  # отбирает
            # записи жеребьевки после игр в группах (места которые вышли в финал)
            player_choice = choice.select().order_by(Choice.group)
            con = len(player_choice)

            for i in player_choice:  # записывает в таблицу Choice
                i.final = fin
                i.posev_final = mesta_exit
                i.save()

            string_table = my_win.label_50.text()
            system = System.get(System.title_id == title_id() and System.stage == fin)
            system.choice_flag = 1
            system.save()
            return


def kol_player_in_group():
    """подсчет кол-во групп и человек в группах"""
    sender = my_win.sender()  # сигнал от кнопки
    gamer = my_win.lineEdit_title_gamer.text()
    kg = my_win.spinBox_kol_group.text()  # количество групп
    player_list = Player.select().where(Player.title_id == title_id())
    type_table = "группы"
    count = len(player_list)  # количество записей в базе
    # остаток отделения, если 0, то участники равно делится на группы
    e1 = count % int(kg)
    # если количество участников равно делится на группы (кол-во групп)
    p = count // int(kg)
    g1 = int(kg) - e1  # кол-во групп, где наименьшее кол-во спортсменов
    g2 = int(p + 1)  # кол-во человек в группе с наибольшим их количеством
    if e1 == 0:  # то в группах равное количество человек -e1-
        stroka_kol_group = f"{kg} группы по {str(p)} чел."
        skg = int((p * (p - 1) / 2) * int(kg))
        mp = p
    else:
        stroka_kol_group = f"{str(g1)} групп(а) по {str(p)} чел. и {str(e1)} групп(а) по {str(g2)} чел."
        p = int(p)
        skg = int((((p * (p - 1)) / 2 * g1) + ((g2 * (g2 - 1)) / 2 * e1)))
        mp = g2
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
        my_win.comboBox_etap_2.setCurrentText("")
        my_win.label_15.show()
        # ====== запись в таблицу db -system- первый этап
        s = System.select().order_by(System.id.desc()).get()
        system = System.get(System.id == s)
        system.max_player = mp
        system.total_athletes = count
        system.total_group = kg
        system.stage = my_win.comboBox_etap_1.currentText()
        system.type_table = type_table
        system.page_vid = my_win.comboBox_page_vid.currentText()
        system.label_string = stroka_kol_group
        system.kol_game_string = stroka_kol_game
        system.save()
    load_combobox_filter_group()


def page_vid():
    """присваивает переменной значение выборат вида страницы"""
    if my_win.comboBox_page_vid.currentText() == "альбомная":
        pv = landscape(A4)
    else:
        pv = A4
    return pv


def view():
    """просмотр PDF файлов средствами OS"""
    from sys import platform
    change_dir()  # смена директории на папку с pdf файлами
    sender = my_win.sender()
    t_id = Title.get(Title.id == title_id())
    short_name = t_id.short_name_comp

    if sender == my_win.all_comp_Action:
        view_file = f"Title_{short_name}.pdf"
    elif sender == my_win.view_list_Action:
        my_win.tabWidget.setCurrentIndex(1)
        player_list = Player.select().where(Player.title_id == title_id())  # сортировка по алфавиту
        list_player_pdf(player_list)
        view_file = f"table_list_{short_name}.pdf"
    elif sender == my_win.view_gr_Action:  # вкладка группы
        view_file = f"table_group_{short_name}.pdf"
    elif sender == my_win.view_fin1_Action:
        view_file = f"1-финал_{short_name}.pdf"
    elif sender == my_win.view_fin2_Action:
        view_file = f"2-финал_{short_name}.pdf"
    elif sender == my_win.view_one_table_Action:
        view_file = f"one_table_{short_name}.pdf"
    elif sender == my_win.clear_s32_Action:
        view_file = "1-финал_чист_32_сетка.pdf"
    elif sender == my_win.clear_s16_Action:
        view_file = "1-финал_чист_16_сетка.pdf"
    elif sender == my_win.clear_s32_full_Action:
        view_file = "1-финал_чист_32_full_сетка.pdf"
    elif sender == my_win.clear_s32_2_Action:
        view_file = "1-финал_чист_32_2_сетка.pdf"
    
    
 
    if platform == "linux" or platform == "linux2":  # linux
        pass
    elif platform == "darwin":  # OS X
        os.system(f"open {view_file}")
    elif platform == "win32":  # Windows...
        os.system(f"{view_file}")
    change_dir()


def player_in_setka(fin):
    """заполняет таблицу Game_list данными спортсменами из сетки tds - список списков данных из сетки, а затем
    заполняет таблицу -Result-"""
    s = System.select().where(System.title_id == title_id())  # находит system id последнего
    for i in s:  # перебирает в цикле строки в табл System где последний titul_id
        if i.stage == fin:
            mp = i.max_player
            mg = i.kol_game_string
            tabel_string = i.label_string
    space = mg.find(" ")
    game = int(mg[:space])
    sd_full = []
    sd = []
    # создание сетки со спортсменами согласно жеребьевки
    if tabel_string == "Сетка (с розыгрышем всех мест) на 16 участников":
        tds = setka_16_full_made(fin)
    elif tabel_string == "Сетка (с розыгрышем всех мест) на 32 участников":
        tds = setka_32_full_made(fin)

    for r in tds:
        if r != "bye":
            space = r.find(" ")  # находит пробел перед именем
            symbol = r.find("/")  # находит черту отделяющий город
            # удаляет все после пробела кроме первой буквы имени
            sl = r[:space + 2]
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
                                  system_id=s, title_id=title_id()).save()
    st = "Финальный"
    for i in range(1, mp // 2 + 1):  # присваивает встречи 1-ого тура и записывает в тбл Results
        num_game = i
        pl1 = sd_full[i * 2 - 2]
        pl2 = sd_full[i * 2 - 1]
        if pl1 is not None and pl2 is not None:
            with db:
                results = Result(number_group=fin, system_stage=st, player1=pl1, player2=pl2,
                                 tours=num_game, title_id=title_id()).save()
    for i in range(mp // 2 + 1, game + 1):  # дополняет номера будущих встреч
        pl1 = ""
        pl2 = ""
        with db:
            results = Result(number_group=fin, system_stage=st, player1=pl1, player2=pl2,
                             tours=i, title_id=title_id()).save()


def player_fin_on_circle(fin):
    """заполняет таблицу Game_list данными спортсменами из группы, которые будут играть в финале по кругу
     td - список списков данных из групп"""
    gr = []
    player_final = {}
    parametrs_final = {}
    mesto = 1
    system = System.select().where(System.title_id == title_id()
                                   )  # находит system id последнего
    for s in system:
        if s.stage == "Предварительный":
            sys = system.select().where(System.stage == "Предварительный").get()
            group = sys.total_group
        else:
            final = s.stage
            if final == fin:
                pl_final = s.max_player // group
                parametrs_final["выход"] = pl_final
                parametrs_final["место"] = mesto

                player_final[final] = parametrs_final.copy()
                mesto = mesto + s.max_player
                break

    mesto_in_group = player_final[fin]

    # вызов функции, где получаем список всех участников по группам
    one_table(fin, mesto_in_group, group)
    choice = Choice.select().order_by(Choice.group).where(Choice.title_id == title_id() and
                                                          Choice.mesto_group == mesto_in_group["место"])

    system_id = System.get(System.title_id == title_id()
                           and System.stage == fin)
    st = "Финальный"
    k = 0
    t_id = title_id()
    for p in choice:  # цикл заполнения db таблиц -game list-
        k += 1
        player = p.family
        gr.append(player)
        game_list = Game_list(number_group=fin, rank_num_player=k, player_group=player, system_id=system_id,
                              title_id=t_id)
        game_list.save()
    tours = tours_list(k - 3)
    round = 0
    for tour in tours:
        round += 1
        for match in tour:
            znak = match.find("-")
            first = int(match[:znak])  # игрок под номером в группе
            second = int(match[znak + 1:])  # игрок под номером в группе
            pl1 = gr[first - 1]
            pl2 = gr[second - 1]
            results = Result(number_group=fin, system_stage=st, player1=pl1, player2=pl2,
                             tours=match, title_id=title_id(), round=round)
            results.save()


def player_in_table():
    """заполняет таблицу Game_list данными спортсменами из группы td - список списков данных из групп и записывает
    встречи по турам в таблицу -Result- """
    system = System.select().where(System.title_id == title_id()).get()  # находит system id последнего
    kg = system.total_group
    stage = system.stage
    table = system.label_string
    pv = system.page_vid
    # создание таблиц групп со спортсменами согласно жеребьевки в PDF
    table_made(pv, stage)
    # вызов функции, где получаем список всех участников по группам
    tdt_all = table_data(stage, kg)
    tdt = tdt_all[0]
    for p in range(0, kg):  # цикл заполнения db таблиц -game list- и  -Results-
        gr = tdt[p]
        count_player = len(gr) // 2  # максимальное кол-во участников в группе
        number_group = str(p + 1) + ' группа'
        k = 0  # кол-во спортсменов в группе
        for i in range(0, count_player * 2 - 1, 2):
            family_player = gr[i][1]  # фамилия игрока
            # подсчет кол-во знаков в фамилия, если 0 значит игрока нет
            fp = len(family_player)
            if fp > 0:  # если строка (фамилия игрока) не пустая идет запись в db
                k += 1
                with db:
                    game_list = Game_list(number_group=number_group, rank_num_player=k, player_group=family_player,
                                          system_id=system, title_id=title_id()).save()
        # если 1-я строка (фамилия игрока) пустая выход из группы
        if fp == 0 and k != 0 or k == count_player:
            cp = k - 3
            tour = tours_list(cp)
            kol_tours = len(tour)  # кол-во туров
            game = len(tour[0])  # кол-во игр в туре
            for r in range(0, kol_tours):
                round = r + 1
                tours = tour[r]  # игры тура
                for d in range(0, game):  # цикл по играм тура
                    match = tours[d]  # матч в туре
                    znak = match.find("-")
                    first = int(match[:znak])  # игрок под номером в группе
                    # игрок под номером в группе
                    second = int(match[znak + 1:])
                    pl1 = gr[first * 2 - 2][1]  # фамилия первого игрока
                    pl2 = gr[second * 2 - 2][1]  # фамилия второго игрока
                    with db:
                        results = Result(number_group=number_group, system_stage=stage, player1=pl1, player2=pl2,
                                         tours=match, title_id=title_id(), round=round).save()


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


def match_score_db():
    """кол-во партий и запись счета партий по умолчанию в db"""
    etap = []
    kol_set = []
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
        game_in_visible()
    elif tab == 4:  # вкладка -полуфиналы-
        pass
    else:  # вкладка -финалы-
        vid_finala = my_win.comboBox_filter_final.currentText()
        if vid_finala == "все финалы":
            state = True
            match = 5
        else:
            sf = system.select().where(System.stage == vid_finala).get()
            match = sf.score_flag
            state = sf.visible_game  # флаг, показывающий записывать счет в партиях или нет

        # ====================
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
        game_in_visible()


def game_in_visible():
    """видимость полей для счета в партии, flag показывает из скольки партий играется матч,
    state_check - нажат чекбокс (видимость полей счета или нет), если 2 значит нажат"""
    r = my_win.tableWidget.currentRow()  # если r -1, то не нажата не одна строка
    tab = my_win.tabWidget.currentIndex()
    sender = my_win.sender()
    system = System.select().where(System.title_id == title_id())
    # =================
    count = len(system)
    flag = 0  # флаг переключения состояния чекбокса
    state_check = False
    # изменение состояния чекбокс (видимость полей для счета)
    if sender == my_win.checkBox_4:
        state_check = my_win.checkBox_4.isChecked()
    elif sender == my_win.checkBox_5:
        state_check = my_win.checkBox_5.isChecked()
    else:  # если flag = 1, то чекбокс не изменялся
        flag = 1

    if count == 1:  # значит соревнования из одной таблицы
        k = System.get(System.title_id == title_id())
        state = k.visible_game
        if flag != 1:
            if state != state_check:
                with db:
                    k.visible_game = state_check
                    k.save()
                state = k.visible_game
        visible_field(state)
    elif count > 1:
        if r >= 0:  # двойной клик по строке встречи
            if tab == 3:
                my_win.checkBox_4.setEnabled(True)
                # из какой группы пара игроков в данный момент
                final = my_win.tableWidget.item(r, 1).text()
            elif tab == 4:
                pass
            else:
                my_win.checkBox_5.setEnabled(True)
                # из какого финала пара игроков в данный момент
                final = my_win.tableWidget.item(r, 2).text()
            # ===============
            if final != "":
                k = system.select().where(System.stage == final).get()
                state = k.visible_game
            else:
                return
            # ================
            if flag == 1:
                if tab == 3:
                    state_check = my_win.checkBox_4.isChecked()
                elif tab == 4:
                    pass
                else:
                    my_win.checkBox_5.setChecked(state)
                    state_check = my_win.checkBox_5.isChecked()
        else:  # просто загружена вкладка
            if tab == 3:
                for k in system:
                    if k.stage == "Предварительный":
                        state = k.visible_game
                        if state_check == 0:  # изменяет состояние на Bool в зависимости от цифрового кода CheckBox
                            state_check = False
                            my_win.checkBox_4.setChecked(False)
                        elif state_check == 2:
                            state_check = True
                            my_win.checkBox_4.setChecked(True)
            elif tab == 4:
                pass
            elif tab == 5:
                my_win.checkBox_5.setEnabled(True)
                if count == 1:
                    final = "Одна таблица"
                    k = System.get(System.title_id == title_id() and System.stage == final)
                    state = k.visible_game
                else:
                    if r == -1:
                        final = "1-й финал"
                        state = True
                    else:
                        # из какого финала пара игроков в данный момент
                        final = my_win.tableWidget.item(r, 2).text()
                        k = System.get(System.title_id == title_id() and System.stage == final)
                        state = k.visible_game

        if flag == 0:
            if state != state_check:
                with db:
                    k.visible_game = state_check
                    k.save()
                state = k.visible_game
        visible_field(state)


def visible_field(state):
    """включает или выключает поля для ввода счета"""
    tab = my_win.tabWidget.currentIndex()
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
        # вкладка -группы- проверка какая стоит галочка (сколько партий)
        if tab == 3:
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

    family = my_win.tableWidget.item(r, 1).text()
    birthday = my_win.tableWidget.item(r, 2).text()
    rank = my_win.tableWidget.item(r, 3).text()
    city = my_win.tableWidget.item(r, 4).text()
    region = my_win.tableWidget.item(r, 5).text()
    rn = len(region)
    razrayd = my_win.tableWidget.item(r, 6).text()
    coach = my_win.tableWidget.item(r, 7).text()
# ================================
    my_win.lineEdit_Family_name.setText(family)
    my_win.lineEdit_bday.setText(birthday)
    my_win.lineEdit_R.setText(rank)
    my_win.lineEdit_city_list.setText(city)
    my_win.comboBox_region.setCurrentText(region)
    my_win.comboBox_razryad.setCurrentText(razrayd)
    my_win.lineEdit_coach.setText(coach)
    my_win.Button_add_edit_player.setEnabled(True)
    if my_win.checkBox_6.isChecked():  # отмечен флажок -удаленные-
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
    elif tab ==2:
        change_choice_group()
    elif tab == 3:  # вкладка -группы-
        my_win.checkBox_7.setEnabled(True)
        my_win.checkBox_8.setEnabled(True)
        my_win.checkBox_7.setChecked(False)
        my_win.checkBox_8.setChecked(False)
    elif tab == 4:
        pass
    elif tab == 5:  # вкладка -финалы-
        my_win.checkBox_9.setEnabled(True)  # включает чекбоксы неявка
        my_win.checkBox_10.setEnabled(True)
        my_win.checkBox_9.setChecked(False)
        my_win.checkBox_10.setChecked(False)
        numer_game = my_win.tableWidget.item(r, 3).text()
        my_win.groupBox_match_2.setTitle(f"Встреча №{numer_game}")
    if tab == 3 or tab == 4 or tab == 5:
        game_in_visible()
        # поле победителя (если заполнено, значит встреча сыграна)
        win_pole = my_win.tableWidget.item(r, 6).text()
        if win_pole != "None" and win_pole != "":  # если встреча сыграна, то заполняет поля общий счет
            sc = my_win.tableWidget.item(r, 8).text()
            pl1 = my_win.tableWidget.item(r, 4).text()
            pl2 = my_win.tableWidget.item(r, 5).text()
            if pl1 == my_win.tableWidget.item(r, 6).text():
                # если в сетке недостающие игроки (bye), то нет счета
                if sc != "":
                    sc1 = sc[0]
                    sc2 = sc[4]
                else:  # оставляет поля общий счет пустыми
                    sc1 = ""
                    sc2 = ""
            else:
                # если в сетке недостающие игроки (bye), то нет счета
                if sc != "":
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
    r = my_win.tableWidget.currentRow()

    player_del = my_win.tableWidget.item(r, 1).text()
    player_id = Player.get(Player.player == player_del)
    birthday = my_win.tableWidget.item(r, 2).text()
    rank = my_win.tableWidget.item(r, 3).text()
    player_city_del = my_win.tableWidget.item(r, 4).text()
    region = my_win.tableWidget.item(r, 5).text()
    razryad = my_win.tableWidget.item(r, 6).text()
    coach = my_win.tableWidget.item(r, 7).text()
    full_name = f"{player_del}/ {player_city_del}"

    coach_id = Coach.get(Coach.coach == coach)
    result = msgBox.question(my_win, "", f"Вы действительно хотите удалить\n"
                                         f" {player_del} город {player_city_del}?",
                             msgBox.Ok, msgBox.Cancel)
    if result == msgBox.Ok:
        with db:
            del_player = Delete_player(player_del_id=player_id, bday=birthday, rank=rank, city=player_city_del,
                                       region=region, razryad=razryad, coach_id=coach_id, full_name=full_name,
                                       player=player_del, title_id=title_id()).save()

            player = Player.get(
                Player.player == my_win.tableWidget.item(r, 1).text())
            player.delete_instance()
        my_win.lineEdit_Family_name.clear()
        my_win.lineEdit_bday.clear()
        my_win.lineEdit_R.clear()
        my_win.lineEdit_city_list.clear()
        my_win.lineEdit_coach.clear()
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
    stage = my_win.comboBox_filter_final.currentText()
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
        # из какого финала пара игроков в данный момент
        final = my_win.tableWidget.item(r, 2).text()
        if stage == "Одна таблица":
            final = stage
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
                count = len(sum_total_game)
                if count == 0:
                    my_win.lineEdit_pl1_s3_fin.setFocus()
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
                # если забыл написать счет и нажал ентер
                msgBox.critical(my_win, "", "Ошибка при вводе счета!")
                my_win.lineEdit_pl2_s3_fin.setFocus()
            else:
                sum_total_game = score_in_game()  # подсчет очков в партии
                # ====================
                count = len(sum_total_game)
                if count == 0:
                    my_win.lineEdit_pl2_s3_fin.setFocus()
                else:
                    # =====================
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
    system = System.select().where(System.title_id == title_id())
    stage = my_win.comboBox_filter_final.currentText()
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
        # ==========
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
        # из какого финала пара игроков в данный момент
        final = my_win.tableWidget.item(r, 2).text()
        if stage == "Одна таблица":
            final = stage
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
                # ==============
                if tab == 3:
                    my_win.lineEdit_pl1_score_total.setText(str(st1))
                    my_win.lineEdit_pl2_score_total.setText(str(st2))
                    if st1 == max_game or st2 == max_game:  # сравнивает максимальное число очков и набранные очки одним из игроков
                        # если игрок набрал макс очки активиоует кнопку ОК и переводит на нее фокус
                        my_win.Button_Ok.setEnabled(True)
                        my_win.Button_Ok.setFocus()
                elif tab == 4:
                    pass
                elif tab == 5:
                    my_win.lineEdit_pl1_score_total_fin.setText(str(st1))
                    my_win.lineEdit_pl2_score_total_fin.setText(str(st2))
                    if st1 == max_game or st2 == max_game:  # сравнивает максимальное число очков и набранные очки одним из игроков
                        # если игрок набрал макс очки активирует кнопку ОК и переводит на нее фокус
                        my_win.Button_Ok_fin.setEnabled(True)
                        my_win.Button_Ok_fin.setFocus()
                total_game.append(st1)
                total_game.append(st2)
                # находит максимальное число очков из сыгранных партий
                max_score = max(total_game)
                if i == 0:
                    # добавляет в список макс число очков которые надо набрать
                    sum_total_game.append(max_game)
                    # добавляет в список макс число очков которые уже набрал игрок
                    sum_total_game.append(max_score)
                else:
                    sum_total_game[0] = max_game
                    sum_total_game[1] = max_score
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
                                 msgBox.Ok, msgBox.Cancel)
        if result == msgBox.Ok:
            flag = True
        elif result == msgBox.Cancel:
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
                                    msgBox.Ok)
        flag = False
        return flag
    elif flag == True:
        return flag


def enter_score(none_player=0):
    """заносит в таблицу -результаты- победителя, счет и т.п. sc_total [партии выигранные, проигранные, очки победителя
     очки проигравшего"""

    tab = my_win.tabWidget.currentIndex()
    r = my_win.tableWidget.currentRow()
    id = my_win.tableWidget.item(r, 0).text()
    num_game = my_win.tableWidget.item(r, 3).text()
    fin = my_win.tableWidget.item(r, 2).text()
       
    if tab == 3:
        stage = "Предварительный"
    elif tab == 4:
        pass
    else:  # финальный
        if fin == "1 группа":
            stage = "Одна таблица"
        else:
            stage = fin
    # находит system id последнего
    sys = System.select().where(System.title_id == title_id())
    system = sys.select().where(System.stage == stage).get()
    type = system.type_table

    if stage == "Предварительный":
        sc_total = circle_type(none_player, stage)
    elif stage == "Полуфиналы":
        pass
    elif stage == "Одна таблица":
        if type == "сетка":
            sc_total = setka_type(none_player)
        else:
            sc_total = circle_type(none_player, stage)
    else:  # финалы
        if type == "сетка":
            sc_total = setka_type(none_player)
        else:  # по кругу
            sc_total = circle_type(none_player, stage)
    st1 = sc_total[0]  # партия выигранные
    st2 = sc_total[1]  # партии проигранные
    w = sc_total[2]  # очки победителя
    l = sc_total[3]  # очки проигравшего
    if my_win.lineEdit_player1_fin.text() != "bye" and my_win.lineEdit_player2_fin.text() != "bye":
        if st1 > st2 or none_player == 2:  # выиграл 1-й участник
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
        else:  # выиграл 2-й участник
            if tab == 3:  # игры в подгруппах
                winner = my_win.lineEdit_player2.text()
                loser = my_win.lineEdit_player1.text()
            elif tab == 4:
                pass
            elif tab == 5:  # игры в финалах
                winner = my_win.lineEdit_player2_fin.text()
                loser = my_win.lineEdit_player1_fin.text()
            ts_winner = f"{st2} : {st1}"
            ts_loser = f"{st1} : {st2}"
        if none_player == 0:
            winner_string = string_score_game()  # пишет счет в партии
        else:
            # winner_string = ts_winner  # только общий счет
            if type == "сетка":
                winner_string = ""
    game_play = False

    with db:  # записывает в таблицу -Result- сыгранный матч
        result = Result.get(Result.id == id)
        result.winner = winner
        result.points_win = w
        result.score_win = winner_string
        result.score_in_game = ts_winner
        result.loser = loser
        result.points_loser = l
        result.score_loser = ts_loser
        result.save()

    if tab == 5:  # записывает в -Result- сыгранный матч со сносками на соответствующие строки победителя и проигравшего
        if type == "сетка":
            vid_setki = system.label_string  # вид сетки и кол-во участников
            # список 1-й номер победителя 2-й проигравшего
            snoska = numer_game(num_game, vid_setki)

            if snoska[0] != 0:
                with db:  # записывает в db таблицу Result победителя и проигравшего
                    player = winner
                    for k in range(0, 2):
                        match_num = result.tours  # номер встречи
                        game = snoska[2] * -1
                        if int(match_num) == game:
                            res_id = result.select().where(Result.tours == snoska[k]).get()
                            if int(match_num) % 2 != 0:
                                res_id.player1 = player
                            else:
                                res_id.player2 = player
                            res_id.save()
                            player = loser
                            # break
        elif type == "круг":
            pass
    fill_table_results()

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
    if stage == "Одна таблица":
        system = System.select().order_by(System.id).where(System.title_id == title_id()).get()
    else:
        sys = System.select().order_by(System.id).where(System.title_id == title_id())
        system = sys.select().where(System.stage == fin).get()
    if system.stage == "Предварительный":
        pv = system.page_vid
        table_made(pv, stage)
        filter_gr(pl=False)
    elif system.stage == "Одна таблица" or system.stage == fin:
        if system.type_table == "круг":
            pv = system.page_vid
            table_made(pv, stage)
        else:
            system_table = system.label_string
            pv = system.page_vid
            if system_table == "Сетка (с розыгрышем всех мест) на 16 участников":
                setka_16_full_made(fin)
            elif system_table == "Сетка (с розыгрышем всех мест) на 32 участников":
                setka_32_full_made(fin)
        filter_fin()


def setka_type(none_player):
    """сетка"""
    sc_total = []
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
    sc_total.append(st1)
    sc_total.append(st2)
    sc_total.append(w)
    sc_total.append(l)
    return sc_total


def circle_type(none_player, stage):
    """круговая таблица"""
    sc_total = []
    st1 = ""
    st2 = ""
    w = ""
    l = ""
    if stage == "Предварительный":
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
    # elif stage == "Финальный" or stage == "Одна таблица":
    else:
        if none_player == 0:
            st1 = int(my_win.lineEdit_pl1_score_total_fin.text())
            st2 = int(my_win.lineEdit_pl2_score_total_fin.text())
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
            my_win.lineEdit_pl1_score_total_fin.setText(st1)
            my_win.lineEdit_pl2_score_total_fin.setText(st2)

    sc_total.append(st1)
    sc_total.append(st2)
    sc_total.append(w)
    sc_total.append(l)
    return sc_total


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
    c = Result.select().where(Result.title_id == title_id())
    c = c.where(Result.player1 ** f'{cp}%')  # like
    result_list = c.dicts().execute()
    row_count = len(result_list)  # кол-во строк в таблице
    column_count = 13  # кол-во столбцов в таблице
    # вставляет в таблицу необходимое кол-во строк
    my_win.tableWidget.setRowCount(row_count)

    for row in range(row_count):  # добавляет данные из базы в TableWidget
        for column in range(column_count):
            item = str(list(result_list[row].values())[column])
            my_win.tableWidget.setItem(
                row, column, QTableWidgetItem(str(item)))


def filter_fin(pl=False):
    """фильтрует таблицу -Result- на вкладке финалы"""
    msgBox = QMessageBox
    num_game_fin = my_win.lineEdit_num_game_fin.text()
    final = my_win.comboBox_filter_final.currentText()
    name = my_win.comboBox_find_name_fin.currentText()
    round = my_win.lineEdit_tour.text()
    name = name.title()  # делает Заглавными буквы слов
    played = my_win.comboBox_filter_played_fin.currentText()
    system = System.select().order_by(System.id).where(
        System.title_id == title_id())  # находит system id последнего

    fin = []
    if final == "Одна таблица":
        fltr = Result.select().where(Result.title_id == title_id()
                                     and Result.system_stage == "Одна таблица")
        if final == "Одна таблица" and my_win.comboBox_find_name_fin.currentText() != "":
            if pl == False:
                fltr = Result.select().where(Result.title_id == title_id() and Result.player1 == name)
            else:
                fltr = Result.select().where(Result.title_id == title_id() and Result.player2 == name)
        else:
            if final == "Одна таблица" and played == "все игры" and num_game_fin == "" and round == "":
                fltr = Result.select().where(Result.system_stage == "Одна таблица")
                count = len(fltr)
                my_win.label_38.setText(f'Всего {count} игры')
            elif final == "Одна таблица" and played == "завершенные":
                fl = Result.select().where(Result.system_stage == "Одна таблица")
                fltr = fl.select().where(Result.winner != "")
                count = len(fltr)
                my_win.label_38.setText(f'Сыграно {count} игры')
            elif final == "Одна таблица" and played == "не сыгранные":
                fltr = Result.select().where(Result.system_stage ==
                                             "Одна таблица" and Result.points_win == None)
                count = len(fltr)
                my_win.label_38.setText(f'Не сыграно {count} игры')
            elif final == "Одна таблица" and played == "все игры" and num_game_fin == "" and round != "":
                fl = Result.select().where(Result.system_stage == "Одна таблица")
                fltr = fl.select().where(Result.round == round)
                count = len(fltr)
                my_win.label_38.setText(f'Всего {count} игры')
            elif final == "Одна таблица" and played == "все игры" and num_game_fin != "" and round == "":
                fl = Result.select().where(Result.system_stage == "Одна таблица")
                fltr = fl.select().where(Result.tours == num_game_fin)
    else:
        if final == "все финалы" and played == "все игры" and num_game_fin == "":
            filter = Result.select().where(Result.title_id == title_id())
            fltr = filter.select().where(Result.system_stage == "Финальный")
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
        # один из финалов встречи которые не сыгранные
        elif final != "все финалы" and played == "не сыгранные" and num_game_fin == "":
            fl = Result.select().where(Result.number_group == final)
            fltr = fl.select().where(Result.points_win != 2 and Result.points_win == None)
            count = len(fltr)
            my_win.label_38.setText(
                f'Всего в {final} не сыгранно {count} игры')
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
            my_win.label_38.setText(
                f' Всего сыграно во всех финалах {count_pl} игры')
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
                fin, ok = QInputDialog.getItem(
                    my_win, "Финалы", "Выберите финал, где искать номер встречи.", fin, 0, False)
                fltr = Result.select().where(Result.number_group == fin)
            row = 0
            for result_list in fltr:
                row += 1
                if result_list.tours == num_game_fin:
                    num_game_fin = int(num_game_fin)
                    r = num_game_fin - 1
                    my_win.tableWidget.selectRow(r)
                    item = my_win.tableWidget.item(r, 5)
                    # переводит выделенную строку в видимую часть экрана
                    my_win.tableWidget.scrollToItem(item)
                    break

    result_list = fltr.dicts().execute()

    my_win.label_38.show()
    row_count = len(fltr)  # кол-во строк в таблице
    column_count = 13  # кол-во столбцов в таблице
    # вставляет в таблицу необходимое кол-во строк
    my_win.tableWidget.setRowCount(row_count)

    for row in range(row_count):  # добавляет данные из базы в TableWidget
        for column in range(column_count):
            item = str(list(result_list[row].values())[column])
            my_win.tableWidget.setItem(
                row, column, QTableWidgetItem(str(item)))
            # =====================
    if my_win.comboBox_find_name_fin.currentText() != "" and pl == False:
        result = msgBox.question(my_win, "", "Продолжить поиск игр с участием\n"
                                             f"{name} ?",
                                 msgBox.Ok, msgBox.Cancel)
        if result == msgBox.Ok:
            pl = True
            filter_fin(pl)
        elif result == msgBox.Cancel:
            my_win.comboBox_find_name_fin.clear()
            return
    else:
        my_win.comboBox_find_name_fin.clear()


def filter_gr(pl=False):
    """фильтрует таблицу -результаты- на вкладке группы"""
    msgBox = QMessageBox
    group = my_win.comboBox_filter_group.currentText()
    name = my_win.comboBox_find_name.currentText()
    name = name.title()  # делает Заглавными буквы слов
    played = my_win.comboBox_filter_played.currentText()
    # отфильтровывает записи с id соревнования (title_id)
    fltr_id = Result.select().where(Result.title_id == title_id())
    if group == "все группы" and my_win.comboBox_find_name.currentText() != "":
        if pl == False:
            fltr = fltr_id.select().where(Result.player1 == name)
        else:
            fltr = fltr_id.select().where(Result.player2 == name)
    elif group == "все группы" and played == "все игры":
        fltr = fltr_id.select()
    elif group == "все группы" and played == "завершенные":
        fltr = fltr_id.select().where(Result.points_win == 2)
    elif group != "все группы" and played == "завершенные":
        fl = fltr_id.select().where(Result.number_group == group)
        fltr = fl.select().where(Result.points_win == 2)
    elif group != "все группы" and played == "не сыгранные":
        fl = fltr_id.select().where(Result.number_group == group)
        fltr = fl.select().where(Result.points_win != 2 and Result.points_win == None)
    elif group == "все группы" and played == "не сыгранные":
        fltr = fltr_id.select().where(Result.points_win != 2 and Result.points_win == None)
    elif group != "все группы" and played == "все игры":
        fltr = fltr_id.select().where(Result.number_group == group)

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
    # вставляет в таблицу необходимое кол-во строк
    my_win.tableWidget.setRowCount(row_count)

    for row in range(row_count):  # добавляет данные из базы в TableWidget
        for column in range(column_count):
            item = str(list(result_list[row].values())[column])
            my_win.tableWidget.setItem(
                row, column, QTableWidgetItem(str(item)))

    if my_win.comboBox_find_name.currentText() != "" and pl == False:
        result = msgBox.question(my_win, "", "Продолжить поиск игр с участием\n"
                                             f"{name} ?",
                                 msgBox.Ok, msgBox.Cancel)
        if result == msgBox.Ok:
            pl = True
            filter_gr(pl)
        elif result == msgBox.Cancel:
            my_win.comboBox_find_name.clear()
            return
    else:
        my_win.comboBox_find_name.clear()


def load_combo():
    """загружает комбобокс поиска спортсмена на вкладке группы, пф и финалы фамилиями спортсменов"""
    text = []
    player = Player.select().where(Player.title_id == title_id())
    for i in player:  # цикл по таблице базы данных (I это id строк)
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
        my_win.lineEdit_tour.setText("")
        my_win.lineEdit_num_game_fin.setText("")
        if my_win.comboBox_filter_final.currentText() == "Одна таблица":
            my_win.comboBox_filter_final.setCurrentText("Одна таблица")
        else:
            my_win.comboBox_filter_final.setCurrentText("все финалы")
        filter_fin()
    load_combo()


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
                                    msgBox.Ok, msgBox.Cancel)
        if result == msgBox.Ok:
            choice_tbl_made()  # заполняет db жеребьевка
            system_competition()  # создает систему соревнований


def choice_gr_automat():
    "новая система жеребьевки групп"
    " current_region_group - словарь (регион - список номеров групп куда можно сеять)"
    " reg_player - словарь регион ид игрока, player_current - список сеящихся игроков, posev - словарь всего посева"
    load_tableWidget()
    posev_tmp = {}
    reg_player = {}
    gr_region = {}
    posev_group = {}
    player_current = []
    pgt = []
    posev = {}
    group_list = []
    start = 0
    end = 1
    step = 0

    sys = System.select().where(System.title_id == title_id())
    sys_id = sys.select().where(System.stage == "Предварительный").get()
    group = sys_id.total_group
    max_player = sys_id.max_player  # максимальное число игроков в группе, оно же число посевов
    total_player = sys_id.total_athletes
    for b in range(1,max_player + 1):  # цикл создания словарей (номер посева, списки списков(номер группы и 0 вместо номера регионов))
        for x in range(1, group + 1):
            posev_group[x] = 0
        gr_region = posev_group.copy()
        posev[f"{b}_посев"] = gr_region
        posev_group.clear()
   
    pl_choice = Choice.select().order_by(Choice.rank.desc()).where(Choice.title_id == title_id())
    m = 1  # начальное число посева
    p = 0
    number_poseva = 0  # общий счетчик посева игроков
    reg_list = []
    player_list = []
    for np in pl_choice:
        choice = np.get(Choice.id == np)
        region = choice.region
        pl_id = choice.player_choice_id
        reg = Region.get(Region.region == region)
        region_id = reg.id 
        reg_list.append(region_id)
        player_list.append(pl_id)
    while number_poseva < total_player:
        p += 1
        if number_poseva == 0 or number_poseva % group == 0 :
            group_list = list(range(1, group + 1))  # получение списка групп с помощью функции range

        region_id = reg_list[number_poseva]
        pl_id = player_list[number_poseva]
        posev_tmp = posev[f"{m}_посев"]

        if m == 1:  # 1-й посев       
            posev_tmp[p] = region_id  # создает словарь группа - номер региона
            number_poseva += 1
            player_current.append(pl_id)
            reg_player[pl_id] = number_poseva  # словарь ид игрока его группа при посеве
            if number_poseva == group:  # если доходит окончания данного посева идет запись в db
                choice_save(m, player_current, reg_player)
        else:  # 2-й посев и т.д.
            current_region_group = {}  # словарь регион - список номеров групп куда можно сеять
            key_reg_previous = []
            current = region_player_current(number_poseva, reg_list, group, player_list)  # должен быть получен список текущих регионов посева
            key_reg_current = current[0]  # номера регионов текущего посева
            player_current = current[1]  # номера игроков (id)

            for o in previous_region_group.keys():  # цикл получения списка регионов предыдущих посевов уникальный
                key_reg_previous.append(o)
            pgt.clear()
            remains = total_player - number_poseva  # остаток посева
            finish = 0
            if remains > group: 
                finish = group  # если остаток больше кол-во групп
            else:
                finish = remains               
            for y in range(0, finish):
                group_list_tmp = []  
                z = key_reg_current[y] # список регионов которые уже были посеяны
                pgt.append(y + 1)  # номера групп которые уже посеяны будут удалены из списка

                if z not in key_reg_previous:  # если нет в списке, то добавляет полный список групп
                    current_region_group[z] = group_list
                else:
                    gr_del = previous_region_group[z]  # список групп где уже есть этот регион
                    group_list_tmp = list((Counter(group_list) - Counter(gr_del)).elements()) # удаляет из списка номера групп где уже есть регионы
                    r = len(group_list_tmp)
                    if r == 0:  # если во всех группах уже есть, то начинает опять полный список групп
                        current_region_group[z] = group_list  # получает словарь со списком групп куда сеять
                    else:
                        current_region_group[z] = group_list_tmp  # получает словарь со списком групп куда сеять
                 # система распределения по группам (посев), где m - номер посева начина со 2-ого посева
            sv = add_delete_region_group(key_reg_current, current_region_group, posev_tmp, m, posev, start, end, step, player_current)
            current.clear()
            number_poseva = number_poseva + sv
        if number_poseva != total_player:  # выход из системы жеребьевки при достижении оканчания
            if number_poseva == group * m:  # смена направления посева
                if m % 2 != 0:
                    start = group
                    end = 0
                    step = -1
                else:
                    start = 0
                    end = group
                    step = 1
                m += 1
                previous_region_group = posev_test(posev, group, m)  # возвращает словарь регион  - список номера групп, где он есть
        else:
            # fill_table_choice()
            fill_table_after_choice()
            with db:  # записывает в систему, что произведена жеребъевка
                system = System.get(System.id == sys_id)
                system.choice_flag = True
                system.save()
            player_in_table()
        group_list.clear()



def choice_setka_automat(fin, count_exit, choice_first, choice_second, choice_third, choice_fourth):
    """автоматическая жеребьевка сетки""" 
    first_posev = []
    second_posev = []
    third_posev = []
    fourth_posev = []
    posev_setki = {}


    first_number = [1, 32, 16, 17, 8, 9, 24, 25]
    second_number = [4, 29, 12, 20, 5, 28, 13, 21]
    third_number = [3, 30, 11, 19, 6, 27, 14, 22]
    fourth_number = [2, 31, 15, 18, 7, 10, 23, 26]

    count_sec_num = len(second_number)
    count_third_num = len(third_number)
    count_fourth_num = len(fourth_number)

    #===================================
    system = System.select().where(System.title_id == title_id())
    sys = system.select().where(System.stage == fin).get()
    syst = sys.select().where(System.stage == sys.stage_exit).get()
    choice = Choice.select().where(Choice.title_id == title_id())
    count_exit = sys.max_player // syst.total_group

    for posev in choice_first:
        psv = []
     
        family = posev.family
        group = posev.group
        pl_id = posev.player_choice_id
        region = posev.region
        player = Player.get(Player.id == pl_id)
        city = player.city

        psv.append(pl_id)
        psv.append(family)
        psv.append(region)
        psv.append(group)
        psv.append(city)
        first_posev.append(psv)

    num_id_player = {} # словарь номер сетки - id игрока
    # region_posev = []
    # region_list = []
    # region_tmp = []
    number_list = [] # посеянные номера в сетке
    # number_posev = []
    reg_list = []  # посеянные регионы в сетке
    region_number_posev = {}
    current_posev = []
    current_region_posev = {}
    # possible_number = {} # словарь возможных номеров для посева
    # possible_tmp = []
    # possible_variant = {}
    # key_list = []
    # val_list = []

    posev = [[1, 32], [16, 17], [8, 9, 24, 25]]
    count_posev = len(posev)
    l = 0
    for i in range(0, count_posev):
        sev = posev[i]  # список номеров посева
        count = len(sev) # количество номеров в посеве
        for w in range(0, count):
            num_set = sev[w]
            region = first_posev[l][2]

            if i == 1:
                for k in range(l, l + count):
                    region = first_posev[k][2]
                    current_region_posev[k] = region # словарь регионы, в текущем посеве по порядку
                for x in region_number_posev.keys():
                    number_list.append(x) # список уже посеянных номеров в сетке
                for v in region_number_posev.values():
                    reg_list.append(v) # список уже посеянных регионов
                current_posev = posev[i]

            current_sev = made_posev(first_posev, num_set, region, current_region_posev, current_posev, i, reg_list, number_list, sev)
            num_id_player[current_sev[0]] = current_sev[1]
                # l = current_sev[2]
            # elif i == 0:
            #     current_sev = made_posev(first_posev, num_set, region, current_region_posev, current_posev, i, reg_list, number_list, sev)
            #     num_id_player[current_sev[0]] = current_sev[1]
            l += 1


def possible_sev(current_region_posev, current_posev, number_list, reg_list, sev, i):
    """места в сетке куда можно сеять текущие регионы (центр сетки)"""
    possible_number = {}
    number_posev = []
    possible_variant = {}
    key_list = []
    val_list = []
    list_sev = []

    l = i + 1
    for m in current_region_posev.keys():
        reg = current_region_posev[m] # регион, который сеятся
        if reg not in reg_list:
            possible_number[l] = current_posev # если в списке нет посеянных регионов до добавляет все номера куда сеять
            posev_tmp = current_posev
        else:
            index = reg_list.index(reg)
            set_number = number_list[index] # номер где уже посеянна такая же область
                        
            for d in range(0, i):
                rl = reg_list[d]
                if reg != rl:
                    num = sev[d]
                    if set_number <= 32 // 2 and num >= 32 // 2:
                        number_posev.append(num)
            posev_tmp = number_posev.copy()
            possible_number[l] = posev_tmp # номер посева по порядку и список номеров в сетке куда можно сеять
        number_posev.clear()
        l += 1 
    count_dict =  len(possible_number)
    possible_variant.clear()
    for q in range(0, count_dict):
        possible_tmp = possible_number[i + q + 1]
        count_list = len(possible_tmp)
        possible_variant[i + q + 1] = count_list  # словарь(номер посева по порядку: число вариантов посева)
    key_list.clear()
    for key in possible_variant.keys():
        key_list.append(key)  # список номеров которые будут сеются
    val_list.clear()
    for val in possible_variant.values():
         val_list.append(val)  # список количество возможных вариантов сева

    if 1 in val_list: # если один вариант для посева
        pass
    else:
        rnd_number = random_generator(list_choice=posev_tmp)
        num_set = rnd_number
    list_sev.append(num_set)
    list_sev.append(possible_variant) 
    return list_sev


def made_posev(first_posev, num_set, region, current_region_posev, current_posev, i, reg_list, number_list, sev):
    """посев"""

    region_list = []
    region_posev = []
    possible_number = {}
    number_posev = []
    possible_variant = {}
    key_list = []
    val_list = []
    current_sev = []
    i += 1
    l = i + 1
    if i >= 1:
        for m in current_region_posev.keys():
            reg = current_region_posev[m] # регион, который сеятся
            if reg not in reg_list:
                possible_number[l] = current_posev # если в списке нет посеянных регионов до добавляет все номера куда сеять
                posev_tmp = current_posev
            else:
                index = reg_list.index(reg)
                set_number = number_list[index] # номер где уже посеянна такая же область
                            
                for d in range(0, i):
                    rl = reg_list[d]
                    if reg != rl:
                        num = sev[d]
                        if set_number <= 32 // 2 and num >= 32 // 2:
                            number_posev.append(num)
                posev_tmp = number_posev.copy()
                possible_number[l] = posev_tmp # номер посева по порядку и список номеров в сетке куда можно сеять
            number_posev.clear()
            l += 1 
        count_dict =  len(possible_number)
        possible_variant.clear()
        for q in range(0, count_dict):
            possible_tmp = possible_number[i + q + 1]
            count_list = len(possible_tmp)
            possible_variant[i + q + 1] = count_list  # словарь(номер посева по порядку: число вариантов посева)
        key_list.clear()
        for key in possible_variant.keys():
            key_list.append(key)  # список номеров которые будут сеются
        val_list.clear()
        for val in possible_variant.values():
            val_list.append(val)  # список количество возможных вариантов сева

        if 1 in val_list: # если один вариант для посева
            pass
        else:
            rnd_number = random_generator(list_choice=posev_tmp)
            num_set = rnd_number
 
        count_dict = len(possible_number)            


    # family = first_posev[i + 1][1]
    # city = first_posev[i + 1][4]
    region_list.append(num_set)
    region_list.append(first_posev[i + 1][2])
    region_tmp = region_list.copy()
    region_posev.append(region_tmp)
    region_list.clear()
    current_sev.append(num_set)
    current_sev.append(region)
    if i >= 1:
        del current_region_posev[i] # удаляет из словаря текущий посеянный регион
        if len(current_region_posev) != 0:
            for t in range(0, count_dict):
                possible_tmp = possible_number[i + t]
                if num_set in possible_tmp:
                    possible_tmp.remove(num_set)
        del possible_number[i] # удаляет из словаря посеянный порядковый номер
    l += 1

    return current_sev



def random_generator(list_choice):
    """выдает случайное число из предложенного списка"""
    rnd_number = random.choice(list_choice)
    return rnd_number



def add_delete_region_group(key_reg_current, current_region_group, posev_tmp, m, posev, start, end, step, player_current):
    """при добавлении в группу региона удалении номера группы из списка сеянных -b- номер группы
    -m- номер посева, kol_group_free - словарь регион и кол-во свободных групп"""
    free_list = []
    reg_list = []
    kol_group_free = {}
    reg_player = dict.fromkeys(player_current, 0)
    player_list = player_current.copy()
    sv = 0
    if start == 0:
        end = len(key_reg_current)
    else:
        start = len(key_reg_current)

    for s in range(start, end, step):
        sv += 1
        for i in key_reg_current:  # получение словаря (регион и кол-во мест (групп) куда можно сеять)
            tmp = current_region_group[i] 
            kol_reg = len(tmp)  # колво регионов (посевов)
            kol_group_free[i] = kol_reg
        free_list = list(kol_group_free.values())  # список кол-во свободных групп, куда можно сеять
        reg_list = list(kol_group_free.keys())  # список ключей (регионов)
        last = len(reg_list)  # кол-во остатка посева
        region = key_reg_current[0]  # номер региона, который сейчас сеется
        free_gr = kol_group_free[region]  # кол-во групп куда можно сеять
        # if 1 in free_list and last > 1 or last == 1 :  # проверка есть ли группа где осталось только одно места для посева
        if 1 in free_list and last > 1 or last == 1 and free_gr == 1 :  # проверка есть ли группа где осталось только одно места для посева
            # сделать посев 1 регион но много групп
            region = reg_list[free_list.index(1)]  # регион если в списке free list есть значение -1-, т.е. осталась одна группа
            u = current_region_group[region][0]  # номер группы
            posev_tmp[u] = region  # запись региона в группу (посев)
        else:
            if free_gr != 1:
                f = current_region_group[region]  # список номеров групп для посева текущего региона
                if m % 2 != 0:  # в зависимости от четности посева меняет направления посева групп в списке
                    f.sort()
                else:
                    f.sort(reverse = True)
                if s in f:
                    posev_tmp[s] = region
                    u = s #  присваивает переменной u - номер группы, если она идет по порядку
                else:
                    g = f[0]
                    posev_tmp[g] = region
                    u = g    # присваивает переменной u - номер группы, если она идет не по порядку
        # ====не правильное соответствие номера региона и номера группы
        # index = reg_list.index(region)  # проверить !!!!
        index = key_reg_current.index(region)
        p = player_list[index]
        reg_player[p] = u
        #=====================
        posev[f"{m}_посев"] = posev_tmp
        for d in key_reg_current:  # цикл удаления посеянных групп
            list_group = current_region_group[d]
            if u in list_group:  # находит сеяную группу и удаляет ее из списка групп
                list_group.remove(u)
        player_list.remove(p)       
        key_reg_current.remove(region)  # удаляет регион из списка как посеянный
        count_in_list = key_reg_current.count(region)
        if count_in_list == 0:  # если в посеве больше одного региона, то пропускает удаление из словаря
            del current_region_group[region] 
            del kol_group_free[region]

        if start > end:
            start -= 1
        else:
            start += 1 
    choice_save(m, player_current, reg_player)        
    return sv


def choice_save(m, player_current, reg_player):
    """запись в db результаты жеребьевки конкретного посева"""
    for i in player_current:
        num_group = reg_player[i]
        with db:  # запись в таблицу Choice результата жеребъевки
            choice = Choice.get(Choice.player_choice_id == i)
            choice.group = f"{num_group} группа"
            choice.posev_group = m
            choice.save()


def region_player_current(number_poseva, reg_list, group, player_list):
    """ создание списка номеров регионов в порядке посева для текущего номера посева """
    key_reg_current = []
    key_tmp = []
    player_current = []
    pl_tmp = []
    current = []
    r = 0
    p = 0
    start = number_poseva
    count = len(player_list)  # кол-во игрок
    remains = count - number_poseva  # остаток посева
    if remains > group: 
        end = start + group  # если остаток больше кол-во групп
    else:
        end = start + remains
    for k in range(start, end):
        r = reg_list[k]
        key_tmp.append(r)
        p = player_list[k]
        pl_tmp.append(p)

    key_reg_current = key_tmp.copy()
    player_current = pl_tmp.copy()
    key_tmp.clear()
    pl_tmp.clear()
    current.append(key_reg_current)
    current.append(player_current)
    return current


def posev_test(posev, group, m):
    """возвращает словарь предыдущих посевов регион - группы, где они есть"""
    uniq_region = []  # уникальный список регионов которые уже посеяны
    tmp_posev = {}
    previous_region_group = {} 
    gr = [] 
    gr_tmp = []
    # список регионов данного посева
    for p in range(1, m):
        tmp_posev = posev[f"{p}_посев"]
        for a in range(1, group + 1):
            v = tmp_posev.setdefault(a)
            if v not in uniq_region:
                uniq_region.append(v)
    # уникальный список регионов
    for val in uniq_region:  # цикл получения словаря (номер региона - список групп где они уже есть)
        for d in range(1, m):
            for key, value in posev[f"{d}_посев"].items():
                if val == value:
                    gr_tmp.append(key)
        gr = gr_tmp.copy()
        previous_region_group[val] = gr
        gr_tmp.clear()
    return previous_region_group


def choice_setka(fin):
    """проба жеребьевки сетки на 16"""
    sys = System.select().where(System.title_id == title_id())  # находит system id последнего
    system = sys.select().where(System.stage == fin).get()

    flag = system.choice_flag
    if flag is True:  # перед повторной жеребьевкой
        del_choice = Game_list.select().where(Game_list.title_id == title_id()
                                              and Game_list.number_group == fin)
        for i in del_choice:
            i.delete_instance()  # удаляет строки финала (fin) из таблицы -Game_list
        del_result = Result.select().where(Result.number_group == fin)
        for i in del_result:
            i.delete_instance()  # удаляет строки финала (fin) из таблицы -Result-
        # ========= рано отмечает, что сделана жеребьевка
    player_in_setka(fin)
    load_tableWidget()


def choice_tbl_made():
    """создание таблицы жеребьевка, заполняет db списком участников для жеребьевки"""
    title = title_id()
    player = Player.select().order_by(Player.rank.desc()).where(Player.title_id == title)
    system = System.select().where(System.title_id == title)
    choice = Choice.select().where(Choice.title_id == title)
    for k in system:
        stage = k.stage
        if stage == "Одна таблица":
            sys = System(choice_flag=True).save()
    chc = len(choice)
    if chc == 0:
        for i in player:
            pl = Player.get(Player.id == i)
            cch = Coach.get(Coach.id == pl.coach_id)
            coach = cch.coach
            chc = Choice(player_choice=pl, family=pl.player, region=pl.region, coach=coach, rank=pl.rank,
                         title_id=title).save()


def choice_filter_group():
    """фильтрует таблицу жеребьевка по группам"""
    gamer = my_win.lineEdit_title_gamer.text()
    fg = my_win.comboBox_filter_choice.currentText()
    choice = Choice.select().where(Choice.title_id == title_id())
    if fg == "все группы":
        player_choice = Choice.select().where(Choice.title_id == title_id())
    elif my_win.radioButton_4.isChecked():
        player_choice = choice.select().where(Choice.group == fg)
        color_region_in_tableWidget(fg)
    else:
        p_choice = Choice.select().order_by(Choice.posev_group).where(Choice.group == fg)
        player_choice = p_choice.select().where(Choice.title_id == title_id())
    count = len(player_choice)
    choice_list = player_choice.dicts().execute()
    row_count = len(choice_list)  # кол-во строк в таблице
    column_count = 10  # кол-во столбцов в таблице
    # вставляет в таблицу необходимое кол-во строк
    my_win.tableWidget.setRowCount(row_count)
    if row_count != 0:
        for row in range(row_count):  # добавляет данные из базы в TableWidget
            for column in range(column_count):
                item = str(list(choice_list[row].values())[column])
                my_win.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))

        # ставит размер столбцов согласно записям
        my_win.tableWidget.resizeColumnsToContents()
        color_region_in_tableWidget(fg)
        for d in range(0, row_count):  # сортирует нумерация по порядку
            my_win.tableWidget.setItem(d, 0, QTableWidgetItem(str(d + 1)))


def color_region_in_tableWidget(fg):
    """смена цвета шрифта в QtableWidget -fg- номер группы"""
    reg = []
    rid = []

    if fg != "все группы" and fg != "":
        choice = Choice.select().where(Choice.title_id == title_id())
        line = choice.select().where(Choice.group == fg)
        for i in line:
            region = i.region
            region = str(region.rstrip())  # удаляет пробел в конце строки
            reg.append(region)
        if len(reg) != 0:
            for x in reg:
                count_region = reg.count(x)
                if count_region > 1:  # если повторяющихся регионов больше одного
                    p = 0
                    for m in range(len(reg)):
                        ind = reg.index(x, p)
                        p = ind + 1
                        rid.append(ind)                       
                        if m == count_region - 1:
                            break
            rid = list(set(rid))  # получает список индексов повторяющихся регионов
            rows = my_win.tableWidget.rowCount()  # кол-во строк в отсортированной таблице
            # for u in range(0, rows):
            #     my_win.tableWidget.item(u, 3).setForeground(QBrush(QColor(0, 0, 0)))  # окрашивает текст в черный цвет
            if rows != 0:
                for k in rid:
                    my_win.tableWidget.item(k, 3).setForeground(QBrush(QColor(255, 0, 0)))  # окрашивает текст в красный цвет


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
    sender = my_win.sender()
    if sender != my_win.comboBox_etap_1:
        if my_win.comboBox_etap_1.currentText() == "Одна таблица":
            one_table()
            player_in_table()
        if my_win.comboBox_etap_1.currentText() == "Предварительный" and my_win.comboBox_etap_2.isHidden():
            kol_player_in_group()
        elif my_win.comboBox_etap_2.currentText() == "Финальный" and my_win.comboBox_etap_3.isHidden():
            total_game_table(kpt=0, fin="", pv="", cur_index=0)
        elif my_win.comboBox_etap_3.currentText() == "Финальный" and my_win.comboBox_etap_4.isHidden():
            total_game_table(kpt=0, fin="", pv="", cur_index=0)
        elif my_win.comboBox_etap_4.currentText() == "Финальный" and my_win.comboBox_etap_5.isHidden():
            total_game_table(kpt=0, fin="", pv="", cur_index=0)


def total_game_table(kpt, fin, pv, cur_index):
    """количество участников и кол-во игр"""
    msgBox = QMessageBox
    gamer = my_win.lineEdit_title_gamer.text()
    system = System.select().order_by(System.id).where(System.title_id == title_id()).get()  # находит system id последнего
    total_player = system.total_athletes
    if kpt != 0:  # подсчет кол-во игр из выбора кол-ва игроков вышедших из группы и системы финала
        player_in_final = system.total_group * kpt
        if cur_index == 1:
            vt = "Сетка (-2) на"
            my_win.comboBox_page_vid.setCurrentText("книжная")
            type_table = "сетка"
        elif cur_index == 2:
            vt = "Сетка (с розыгрышем всех мест) на"
            my_win.comboBox_page_vid.setCurrentText("книжная")
            type_table = "сетка"
        elif cur_index == 3:
            vt = "Сетка (с играми за 1-3 места) на"
            my_win.comboBox_page_vid.setCurrentText("книжная")
            type_table = "сетка"
        elif cur_index == 4:
            vt = "Круговая таблица на"
            type_table = "круг"

        total_games = numbers_of_games(cur_index, player_in_final)  # подсчет кол-во игр

        pv = my_win.comboBox_page_vid.currentText()
        str_setka = f"{vt} {player_in_final} участников"
        s = System.select().order_by(System.id.desc()).get()
        total_athletes = s.total_athletes
        stage_exit = ""
        stroka_kol_game = f"{total_games} игр"

        if total_athletes == player_in_final:
            stage_exit = "Предварительный"
        final = fin

        system = System(title_id=title_id(), total_athletes=total_athletes, total_group=0, kol_game_string=stroka_kol_game,
                        max_player=player_in_final, stage=final, type_table=type_table, page_vid=pv, label_string=str_setka,
                        choice_flag=0, score_flag=5, visible_game=True, stage_exit=stage_exit).save()    
        
        return [str_setka, player_in_final, total_athletes, stroka_kol_game]
    else:  # нажата кнопка создания этапа, если еще не все игроки посеяны в финал, то продолжает этапы соревнования
        sys_last = System.select().where(System.title_id == title_id())
        sys_fin = sys_last.select().where(System.stage ** '%финал') # отбирает записи, где
        # титул id и стадия содержит слово финал (1 и 2 заменяет %)
        system = System.select().order_by(System.id).where(System.title_id == title_id())
        system_id = system.select().where(System.stage ** '%финал')
        tot_fin = len(system_id)
        sum_final = []
        for i in system_id:
            player_in_etap = i.max_player
            sum_final.append(player_in_etap)
        total_final = sum(sum_final)
        t = total_player - total_final
        txt = ""
        if total_final == total_player or t <= 3: # подсчитывает все ли игроки распределены по финалам
            if t == 1:     
                txt = "Остался 1 участник, не вошедший в финальную часть"
                msgBox.information(my_win, "Уведомление", txt)
            elif t == 2:
                txt = "Остались 2 игрока, они могут сыграть за место между собой"
                msgBox.information(my_win, "Уведомление", txt)   
            elif t == 3:  
                txt = "Остались 3 игрока, они могут сыграть за места по кругу" 
                msgBox.information(my_win, "Уведомление", txt)
            result = msgBox.question(my_win, "", "Система соревнований создана.\n"
                                                 "Теперь необходимо сделать жеребъевку\n"
                                                 "предварительного этапа.\n"
                                                 "Хотите ее сделать сейчас?",
                                     msgBox.Ok, msgBox.Cancel)
            if result == msgBox.Ok:
                choice_gr_automat()
                tab_enabled(gamer)
            else:
                return    
        elif t >= 4:
            my_win.comboBox_table.hide()
            if tot_fin == 1:
                my_win.comboBox_etap_3.show()
            elif tot_fin ==2:
                my_win.comboBox_etap_4.show()
            elif tot_fin == 3:
                my_win.comboBox_etap_5.show()

            my_win.Button_etap_made.setEnabled(True)
            my_win.comboBox_page_vid.setEnabled(True)
        

def numbers_of_games(cur_index, player_in_final):
    """подсчет количество игр в зависимости от системы (пока сетки на 16)"""
    if cur_index == 1:  # сетка - 2
        if player_in_final == 16:
            total_games = 38
        elif player_in_final == 32:
            total_games = 94
    elif cur_index == 2:  # прогрессивная сетка
        if player_in_final == 16:
            total_games = 32
        elif player_in_final == 32:
            total_games = 80
    elif cur_index == 3:  # сетка с розыгрышем призовых мест
        pass
    else:
        total_games = (player_in_final * (player_in_final - 1)) // 2
    return total_games


def clear_db_before_edit():
    """очищает таблицы при повторном создании системы"""
    t_id = title_id()
    system = System.select().where(System.title_id == title_id())
    for i in system:  # удаляет все записи
        i.delete_instance()
    sys = System(title_id=t_id, total_athletes=0, total_group=0, max_player=0, stage="", type_table="", page_vid="",
                 label_string="", kol_game_string="", choice_flag=False, score_flag=5, visible_game=True,
                 stage_exit="", mesta_exit="").save()

    gl = Game_list.select().where(Game_list.title_id == t_id)
    for i in gl:
        gl_d = Game_list.get(Game_list.id == i)
        gl_d.delete_instance()
    chc = Choice.select().where(Choice.title_id == t_id)
    for i in chc:
        ch_d = Choice.get(Choice.id == i)
        ch_d.delete_instance()
    rs = Result.select().where(Result.title_id == t_id)
    for i in rs:
        r_d = Result.get(Result.id == i)
        r_d.delete_instance()


def clear_db_before_choice():
    """очищает систему перед повторной жеребьевкой и изменяет кол-во участников если они изменились"""
    msgBox = QMessageBox
    sys = System.select().where(System.title_id == title_id())
    player = Player.select().where(Player.title_id == title_id())
    system = sys.select().where(System.stage == "Предварительный").get()
    sys_id = system.id
    tg = system.total_group
    total_player = system.total_athletes
    max_pl = system.max_player
    new_total_player = len(player)
    free_group = 0
    if total_player != new_total_player: #  если изменилось число участников
        result = msgBox.question(my_win, "Список участников", "Был изменено число участников.\n"
        "вы хотите изменить систему соревнований?",
                                    msgBox.Ok, msgBox.Cancel)
        if result == msgBox.Ok:
             # очищает таблицы перед новой системой соревнования (system, choice)
            clear_db_before_edit()
            choice_tbl_made()  # заполняет db жеребьевка
        else:
            e1 = new_total_player % tg  # остаток до полного посева групп, где спортсменов на одного больше
                # если количество участников равно делится на группы (кол-во групп)
            p_min = new_total_player // tg  # минимальное число спортсменов в группах
            g1 = int(tg) - e1  # кол-во групп, где наименьшее кол-во спортсменов
            p_max= p_min + 1  # кол-во человек в группе с наибольшим их количеством
            if e1 == 0:  # то в группах равное количество человек -e1-
                stroka_kol_group = f"{tg} группы по {str(p_min)} чел."
                skg = int((p_min * (p_min - 1) / 2) * int(tg))
                max_pl = p_min
            else:
                stroka_kol_group = f"{str(g1)} групп(а) по {str(p_min)} чел. и {str(e1)} групп(а) по {str(p_max)} чел."
                skg = int((((p_min * (p_min - 1)) / 2 * g1) + ((p_max * (p_max - 1)) / 2 * e1)))
                max_pl = p_max
            kgs = f"{skg} игр"
            sys_t = System.select().where(System.id == sys_id).get()
            sys_t.max_player = max_pl
            sys_t.label_string = stroka_kol_group
            sys_t.kol_game_string = kgs
            sys_t.save()

            for x in sys:
                x.total_athletes = new_total_player
                x.save()
    # else:  # если число спортсменов не изменилось (просто смена участников)
    gl = Game_list.select().where(Game_list.title_id == title_id())
    for i in gl:
        gl_d = Game_list.get(Game_list.id == i)
        gl_d.delete_instance()
    chc = Choice.select().where(Choice.title_id == title_id())
    for i in chc:
        ch_d = Choice.get(Choice.id == i)
        ch_d.delete_instance()
    rs = Result.select().where(Result.title_id == title_id())
    for i in rs:
        r_d = Result.get(Result.id == i)
        r_d.delete_instance()
    choice_tbl_made()
    choice_gr_automat()


def ready_system():
    """проверка на готовность системы"""
    sid_first = System.select().where(System.title_id == title_id())  # находит system id первого
    count = len(sid_first)
    if count == 1:
        system = System.get(System.id == sid_first)
        stage = system.stage
        if stage == "Одна таблица":
            my_win.statusbar.showMessage("Система соревнований создана", 5000)
            flag = True
        else:
            my_win.statusbar.showMessage("Необходимо создать систему соревнований", 500)
            flag = False
    elif count > 1:
        my_win.statusbar.showMessage("Система соревнований создана", 5000)
        flag = True
    else:
        my_win.statusbar.showMessage("Необходимо создать систему соревнований", 500)
        flag = False
    return flag


def ready_choice(stage):
    """проверка на готовность жеребьевки групп"""
    sys = System.select().where(System.title_id == title_id())
    greb_flag = False
    if stage != "":
        system = sys.select().where(System.stage == stage).get()
        greb_flag = system.choice_flag
    
    if greb_flag is True:
        my_win.statusbar.showMessage("Жеребьевка сделана", 5000)
        flag = True
    else:
        my_win.statusbar.showMessage("Жеребьевка групп еще не выполнена", 5000)
        flag = False
    return flag


def select_choice_final():
    """выбор жеребьевки финала"""
    system = System.select().where(System.title_id == title_id())  # находит system id последнего

    fin = []
    for sys in system:
        if sys.stage != "Предварительный" and sys.stage != "Полуфиналы":
            fin.append(sys.stage)
    fin, ok = QInputDialog.getItem(my_win, "Выбор финала", "Выберите финал для жеребъевки", fin, 0, False)
    if ok:
        return fin
    else:
        fin = None
        return fin


def check_choice(fin):
    """Проверяет перед жеребьевкой финалов, сыграны ли все партиии в группах"""
    msg = QMessageBox
    system = System.select().where(System.title_id == title_id())  # находит system id последнего
    final = system.select().where(System.stage == fin).get() # получаем запись конкретного финала
    exit = final.stage_exit  # запись откуда идет выход в финал
    res = Result.select().where(Result.title_id == title_id())  # отбираем записи с выходом в финал
    gr = res.select().where(Result.system_stage == exit)
    for i in gr:
        game = i.points_win       
        if game is None:
            result = msg.information(my_win, "Предварительный этап", "Еще не все встречи сыграны в предварительном этапе.",
                                    msg.Ok)
            check_flag = False
            break                        
        else:
            check_flag = True  
    return check_flag


def del_player_table():
    """таблица удаленных игроков на данных соревнованиях"""
    if my_win.checkBox_6.isChecked():
        my_win.Button_clear_del.setEnabled(True)
        my_win.tableWidget.hideColumn(8)
        player_list = Delete_player.select().where(Delete_player.title_id == title_id())
        count = len(player_list)
        if count == 0:
            my_win.statusbar.showMessage(
                "Удаленных участников соревнований нет", 10000)
            fill_table(player_list)
        else:
            load_tableWidget()
            fill_table(player_list)
            my_win.statusbar.showMessage(
                "Список удаленных участников соревнований", 10000)
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
        my_win.Button_clear_del.setEnabled(False)
        my_win.statusbar.showMessage("Список участников соревнований", 10000)


def clear_del_player():
    """Очистка базы данных удаленных игроков"""
    msgBox = QMessageBox
    del_player = Delete_player.select().where(Delete_player.title_id == title_id())
    result = msgBox.question(my_win, "Участники", "Вы действительно хотите очистить список\n"
                                "удаленных игроков?",
                                        msgBox.Ok, msgBox.Cancel)
    if result == msgBox.Ok:
        for i in del_player:
            i.delete_instance()
        my_win.Button_clear_del.setEnabled(False)  
        my_win.checkBox_6.setChecked(False)      
    else:
        return


def kol_player_in_final():
    """после выбора из комбобокс системы финала подсчитывает сколько игр в финале"""
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
            else:
                return
        elif sender == my_win.comboBox_table_2:
            cur_index = my_win.comboBox_table_2.currentIndex()
            ct = my_win.comboBox_etap_3.currentText()
            if ct == "Финальный":
                my_win.label_32.setText("Финальный этап")
                fin = "2-й финал"
            else:
                return
        elif sender == my_win.comboBox_table_3:
            cur_index = my_win.comboBox_table_3.currentIndex()
            ct = my_win.comboBox_etap_4.currentText()
            if ct == "Финальный":
                my_win.label_55.setText("Финальный этап")
                fin = "3-й финал"
            else:
                return
        elif sender == my_win.comboBox_table_4:
            cur_index = my_win.comboBox_table_4.currentIndex()
            ct = my_win.comboBox_etap_5.currentText()
            if ct == "Финальный":
                my_win.label_56.setText("Финальный этап")
                fin = "4-й финал"
            else:
                return
        kpt, ok = QInputDialog.getInt(my_win, "Число участников", "Введите число участников,\nвыходящих "
                                                                  f"из группы в {fin}", min=1)
                
        # возвращает из функции несколько значения в списке
        list = total_game_table(kpt, fin, pv, cur_index)
        if ok:
            if sender == my_win.comboBox_table:
                my_win.label_27.show()
                # пишет кол-во игр 2-ого этапа
                my_win.label_27.setText(list[3])
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
            elif sender == my_win.comboBox_table_3:
                my_win.label_53.setText(list[3])
                my_win.label_53.show()
                my_win.label_61.setText(list[0])
                my_win.label_61.show()
                if list[2] - list[1] == 0:  # подсчитывает все ли игроки распределены по финалам
                    my_win.statusbar("Система создана.", 10000)
                else:
                    my_win.comboBox_table_3.hide()
            elif sender == my_win.comboBox_table_4:
                my_win.label_58.setText(list[3])
                my_win.label_58.show()
                my_win.label_62.setText(list[0])
                my_win.label_62.show()
                if list[2] - list[1] == 0:  # подсчитывает все ли игроки распределены по финалам
                    my_win.statusbar("Система создана.", 10000)
                else:
                    my_win.comboBox_table_4.hide()
            my_win.Button_etap_made.setEnabled(True)
            my_win.comboBox_page_vid.setEnabled(True)


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
        # показывает статус бар на 5 секунд
        my_win.statusbar.showMessage(
            "Резервное копирование базы данных завершено успешно", 5000)
    except sqlite3.Error as error:
        # показывает статус бар на 5 секунд
        my_win.statusbar.showMessage(
            "Ошибка при копировании базы данных", 5000)
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
        title = t.select().where(Title.gamer == gamer).get()
        title_id = title.id  # получает его id
    else:
        # получение последней записи в таблице
        t_id = Title.select().order_by(Title.id.desc()).get()
        title_id = t_id.id
    return title_id


def func_zagolovok(canvas, doc):
    """создание заголовка страниц"""
    pagesizeW = doc.width
    pagesizeH = doc.height
 
    if pagesizeH > pagesizeW:
        pv = A4
    else:
        pv = landscape(A4)
    (width, height) = pv

    title = Title.get(Title.id == title_id())

    nz = title.name
    ms = title.mesto
    sr = f"среди {title.sredi} {title.vozrast}"
    data_comp = data_title_string()

    canvas.saveState()
    canvas.setFont("DejaVuSerif-Italic", 14)
    # центральный текст титула
    canvas.drawCentredString(width / 2.0, height - 1.1 * cm, nz)
    # canvas.drawCentredString(width / 2.0, height - 1.3 * cm, final)  # центральный текст номер финала
    canvas.setFont("DejaVuSerif-Italic", 11)
    # текста титула по основным
    canvas.drawCentredString(width / 2.0, height - 1.5 * cm, sr)
    canvas.drawRightString(width - 1 * cm, height - 1.6 * cm, f"г. {ms}")  # город
    canvas.drawString(0.8 * cm, height - 1.6 * cm, data_comp)  # дата начала

    canvas.setFont("DejaVuSerif-Italic", 11)
    canvas.setFillColor(blue)  # меняет цвет шрифта списка судейской коллеги
    if pv == landscape(A4):
        main_referee_collegia = f"Гл. судья: {title.referee} судья {title.kat_ref}______________  " \
                                f"Гл. секретарь: {title.secretary} судья {title.kat_sek} ______________"
        # текста титула по основным
        canvas.drawCentredString(
            width / 2.0, height - 20 * cm, main_referee_collegia)
    else:
        main_referee = f"Гл. судья: {title.referee} судья {title.kat_ref} ______________"
        main_secretary = f"Гл. секретарь: {title.secretary} судья {title.kat_sek} ______________"
        # подпись главного судьи
        canvas.drawString(2 * cm, 2 * cm, main_referee)
        # подпись главного секретаря
        canvas.drawString(2 * cm, 1 * cm, main_secretary)
    canvas.restoreState()
    return func_zagolovok


def tbl(stage, kg, ts, zagolovok, cW, rH):
    """данные таблицы и применение стиля и добавления заголовка столбцов
    tdt_new - [[[участник],[регион счет в партиях]]]"""
    from reportlab.platypus import Table
    dict_tbl = {}
    tdt_all = table_data(stage, kg)  # данные результатов в группах
    # данные результатов победителей в группах для окрашивания очков в красный цвет
    tdt_new = tdt_all[0]
    for i in range(0, kg):
        tdt_new[i].insert(0, zagolovok)       
        dict_tbl[i] = Table(tdt_new[i], colWidths=cW, rowHeights=rH)
        # ставит всю таблицу в синий цвет
        ts.add('TEXTCOLOR', (0, 0), (-1, -1), colors.darkblue)
        for k in tdt_all[1][i]:
            col = k[0]  # столбец очков победителя
            row = k[1]  # ряд очков победителя
            ts.add('TEXTCOLOR', (col, row + 1), (col, row + 1), colors.red)  # красный цвет очков победителя
        dict_tbl[i].setStyle(ts)  # применяет стиль к таблице данных
    return dict_tbl


def table_made(pv, stage):
    """создание таблиц kg - количество групп(таблиц), g2 - наибольшое кол-во участников в группе
     pv - ориентация страницы, е - если участников четно группам, т - их количество"""
    from reportlab.platypus import Table
    system = System.select().where(System.title_id == title_id())  # находит system id последнего
    for s_id in system:
        if s_id.stage == stage:
            ta = s_id.max_player
            type_tbl = s_id.type_table
            break
    if stage == "Одна таблица":
        kg = 1
        t = ta
    elif stage != "Одна таблица" and type_tbl == "круг":  # финальные игры по кругу
        kg = 1
        t = ta
    else:  # групповые игры
        kg = s_id.total_group  # кол-во групп
        if int(kg) % int(ta) == 0:
            t = ta
        else:
            t = ta + 1
    if pv == "альбомная":  # альбомная ориентация стр
        pv = landscape(A4)
        if kg == 1 or t in [10, 11, 12, 13, 14, 15, 16]:
            # ширина столбцов таблицы в зависимости от кол-во чел (1 таблица)
            wcells = 21.4 / t
        else:
            # ширина столбцов таблицы в зависимости от кол-во чел (2-ух в ряд)
            wcells = 7.4 / t
    else:  # книжная ориентация стр
        pv = A4
        wcells = 12.8 / t  # ширина столбцов таблицы в зависимости от кол-во чел
    col = ((wcells * cm,) * t)

    elements = []

    # кол-во столбцов в таблице и их ширина
    cW = ((0.4 * cm, 3.2 * cm) + col + (1 * cm, 1 * cm, 1 * cm))
    if kg == 1:
        rH = (0.45 * cm)  # высота строки
    else:
        rH = (0.34 * cm)  # высота строки
    # rH = None  # высота строки
    num_columns = []  # заголовки столбцов и их нумерация в зависимости от кол-во участников
    for i in range(0, t):
        i += 1
        i = str(i)
        num_columns.append(i)
    zagolovok = (['№', 'Участники/ Город'] + num_columns + ['Очки', 'Соот', 'Место'])

    tblstyle = []
    # =========  цикл создания стиля таблицы ================
    for q in range(1, t + 1):  # город участника делает курсивом
        # город участника делает курсивом
        fn = ('FONTNAME', (1, q * 2), (1, q * 2), "DejaVuSerif-Italic")
        tblstyle.append(fn)
        fn = ('FONTNAME', (1, q * 2 - 1), (1, q * 2 - 1),
              "DejaVuSerif-Bold")  # участника делает жирным шрифтом
        tblstyle.append(fn)
        # центрирование текста в ячейках)
        fn = ('ALIGN', (1, q * 2 - 1), (1, q * 2 - 1), 'LEFT')
        tblstyle.append(fn)
        # объединяет 1-2, 3-4, 5-6, 7-8 ячейки 1 столбца
        fn = ('SPAN', (0, q * 2 - 1), (0, q * 2))
        tblstyle.append(fn)
        # объединяет клетки очки
        fn = ('SPAN', (t + 2, q * 2 - 1), (t + 2, q * 2))
        tblstyle.append(fn)
        # объединяет клетки соот
        fn = ('SPAN', (t + 3, q * 2 - 1), (t + 3, q * 2))
        tblstyle.append(fn)
        # объединяет клетки  место
        fn = ('SPAN', (t + 4, q * 2 - 1), (t + 4, q * 2))
        tblstyle.append(fn)
        # объединяет диагональные клетки
        fn = ('SPAN', (q + 1, q * 2 - 1), (q + 1, q * 2))
        tblstyle.append(fn)
        fn = ('BACKGROUND', (q + 1, q * 2 - 1), (q + 1, q * 2),
              colors.lightgreen)  # заливает диагональные клетки
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
                     # цвет шрифта в ячейках
                     ('TEXTCOLOR', (0, 0), (-1, -1), colors.darkblue),
                     ('LINEABOVE', (0, 0), (-1, 1), 1,
                      colors.black),  # цвет линий нижней
                     # цвет и толщину внутренних линий
                     ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                     ('BOX', (0, 0), (-1, -1), 2, colors.black)])  # внешние границы таблицы

    #  ============ создание таблиц и вставка данных =================
    h1 = PS("normal", fontSize=10, fontName="DejaVuSerif-Italic",
            leftIndent=150)  # стиль параграфа (номера таблиц)
    h2 = PS("normal", fontSize=10, fontName="DejaVuSerif-Italic",
            leftIndent=50)  # стиль параграфа (номера таблиц)
    if kg == 1:  # одна таблицу
        dict_table = tbl(stage, kg, ts, zagolovok, cW, rH)
        data = [[dict_table[0]]]
        shell_table = Table(data, colWidths=["*"])
        elements.append(shell_table)
        # elements.append(stage)
    elif kg == 2:
        dict_table = tbl(stage, kg, ts, zagolovok, cW, rH)
        # страница альбомная, то таблицы размещаются обе в ряд
        if pv == landscape(A4) and t in [3, 4, 5, 6]:
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
        dict_table = tbl(stage, kg, ts, zagolovok, cW, rH)
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
        dict_table = tbl(stage, kg, ts, zagolovok, cW, rH)
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
        dict_table = tbl(stage, kg, ts, zagolovok, cW, rH)
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
        dict_table = tbl(stage, kg, ts, zagolovok, cW, rH)
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
        dict_table = tbl(stage, kg, ts, zagolovok, cW, rH)
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
        dict_table = tbl(stage, kg, ts, zagolovok, cW, rH)
        if pv == landscape(A4):  # страница альбомная, то таблицы размещаются обе в ряд
            data = [[dict_table[0], dict_table[1]]]
            data1 = [[dict_table[2], dict_table[3]]]
            data2 = [[dict_table[4], dict_table[5]]]
            data3 = [[dict_table[6], dict_table[7]]]
            shell_table = Table(data, colWidths=["*"])
            shell_table1 = Table(data1, colWidths=["*"])
            shell_table2 = Table(data2, colWidths=["*"])
            shell_table3 = Table(data3, colWidths=["*"])
            # заголовки групп (надо точно позиционировать)
            elements.append(Paragraph('группа 1 группа 2', h2))
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
    if pv == A4:
        pv = A4
    else:
        pv = landscape(A4)
    t_id = Title.get(Title.id == title_id())
    short_name = t_id.short_name_comp

    if stage == "Одна таблица":
        name_table = f"one_table_{short_name}.pdf"
    elif stage == "Предварительный":
        name_table = f"table_group_{short_name}.pdf"
    else:
        txt = stage.rfind("-")
        stage = stage[:txt + 1]
        name_table = f"{stage}финал_{short_name}.pdf"
    doc = SimpleDocTemplate(name_table, pagesize=pv)
    change_dir()
    doc.build(elements, onFirstPage=func_zagolovok, onLaterPages=func_zagolovok)
    change_dir()


def setka_16_full_made(fin):
    """сетка на 16 в pdf"""
    from reportlab.platypus import Table
    table = "setka_16_full"
    elements = []
    data = []
    style = []
    column = ['']
    column_count = column * 11
    # добавить в аргументы функции
    final = fin
    first_mesto = mesto_in_final(fin)
    # first_mesto = 1  # временный финал для чистой сетки
    for i in range(0, 69):
        # column_count[10] = i  # нумерация 10 столбца для удобного просмотра таблицы
        list_tmp = column_count.copy()
        data.append(list_tmp)
    # ========= места ==========
    y = 0
    for i in range(0, 32, 2):
        y += 1
        data[i][0] = str(y)  # рисует начальные номера таблицы 1-16
    # data[0][5] = final
    # ========= нумерация встреч сетки ==========
    draw_num(row_n=1, row_step=2, col_n=2, number_of_columns=4, number_of_game=1, player=16, data=data) # рисует номера встреч 1-32
    draw_num(row_n=32, row_step=2, col_n=6, number_of_columns=2, number_of_game=17, player=4, data=data) # рисует номера встреч 1-32
    draw_num(row_n=41, row_step=2, col_n=4, number_of_columns=3, number_of_game=21, player=8, data=data) # рисует номера встреч 1-32
    draw_num(row_n=58, row_step=2, col_n=6, number_of_columns=2, number_of_game=29, player=4, data=data) # рисует номера встреч 1-32
    draw_num_lost(row_n=29, row_step=2, col_n=6, number_of_game=13, player=2, data=data) # номера минус проигравшие встречи -1 -16
    draw_num_lost(row_n=32, row_step=2, col_n=4, number_of_game=9, player=4, data=data) # номера минус проигравшие встречи -1 -16
    draw_num_lost(row_n=39, row_step=2, col_n=6, number_of_game=17, player=2, data=data) # номера минус проигравшие встречи -1 -16
    draw_num_lost(row_n=41, row_step=2, col_n=2, number_of_game=1, player=8, data=data) # номера минус проигравшие встречи -1 -16
    draw_num_lost(row_n=58, row_step=2, col_n=4, number_of_game=21, player=4, data=data) # номера минус проигравшие встречи -1 -16
    draw_num_lost(row_n=55, row_step=2, col_n=6, number_of_game=25, player=2, data=data) # номера минус проигравшие встречи -1 -16
    draw_num_lost(row_n=65, row_step=2, col_n=6, number_of_game=29, player=2, data=data) # номера минус проигравшие встречи -1 -16
   
    data[8][8] = str(15)  # создание номеров встреч 15
    data[25][8] = str(-15)
    data[29][8] = str(16)  # создание номеров встреч 16
    data[31][8] = str(-16)
    data[37][8] = str(-19)
    data[39][8] = str(20)
    data[41][8] = str(-20)
    data[44][8] = str(27)  # создание номеров встреч 27
    data[52][8] = str(-27)
    data[55][8] = str(28)  # создание номеров встреч 28
    data[57][8] = str(-28)
    data[63][8] = str(-31)
    data[65][8] = str(32)  # создание номеров встреч 32
    data[67][8] = str(-32)

    # ============= данные игроков и встреч и размещение по сетке =============
    tds = write_in_setka(data, fin, first_mesto, table)
    #===============
    cw = ((0.3 * cm, 4.6 * cm, 0.4 * cm, 2.6 * cm, 0.4 * cm, 2.6 * cm, 0.4 * cm, 2.6 * cm,
           0.4 * cm, 4.4 * cm, 1.3 * cm))
    # основа сетки на чем чертить таблицу (ширина столбцов и рядов, их кол-во)
    color_mesta(data, first_mesto, table) # раскрашивает места участников красным цветом
    t = Table(data, cw, 69 * [0.35 * cm])
    # =========  цикл создания стиля таблицы ================
    # ==== рисует основной столбец сетки 
    style = draw_setka(1, 1, 16, style) # рисует кусок сетки(номер столбца, номер строки на 16 человека)
    style = draw_setka(7, 29, 2, style) # рисует кусок сетки(номер столбца, номер строки на 32 человека)
    style = draw_setka(5, 32, 4, style) # рисует кусок сетки(номер столбца, номер строки на 32 человека)
    style = draw_setka(7, 39, 2, style) # рисует кусок сетки(номер столбца, номер строки на 32 человека)
    style = draw_setka(3, 41, 8, style) # рисует кусок сетки(номер столбца, номер строки на 32 человека)
    style = draw_setka(7, 55, 2, style) # рисует кусок сетки(номер столбца, номер строки на 32 человека)
    style = draw_setka(5, 58, 4, style) # рисует кусок сетки(номер столбца, номер строки на 32 человека)
    style = draw_setka(7, 65, 2, style) # рисует кусок сетки(номер столбца, номер строки на 32 человека)
    # ======= встречи за места =====
    for q in range(0, 11, 10):
        fn = ('LINEABOVE', (9, q + 16), (10, q + 16),
              1, colors.darkblue)  # за 1-2 место
        style.append(fn)
    for q in range(0, 3, 2):
        fn = ('LINEABOVE', (9, q + 30), (10, q + 30),
              1, colors.darkblue)  # за 3-4 место
        style.append(fn)
        fn = ('LINEABOVE', (9, q + 40), (10, q + 40),
              1, colors.darkblue)  # за 7-8 место
        style.append(fn)
        fn = ('LINEABOVE', (9, q + 56), (10, q + 56),
              1, colors.darkblue)  # за 11-12 место
        style.append(fn)
        fn = ('LINEABOVE', (9, q + 66), (10, q + 66),
              1, colors.darkblue)  # за 15-16 место
        style.append(fn)
    for q in range(0, 4, 3):
        fn = ('LINEABOVE', (9, q + 35), (10, q + 35),
              1, colors.darkblue)  # за 5-6 место
        style.append(fn)
        fn = ('LINEABOVE', (9, q + 61), (10, q + 61),
              1, colors.darkblue)  # за 13-14 место
        style.append(fn)
    for q in range(0, 6, 5):
        fn = ('LINEABOVE', (9, q + 48), (10, q + 48),
              1, colors.darkblue)  # за 9-10 место
        style.append(fn)

    for i in range(1, 8, 2):
        fn = ('TEXTCOLOR', (i, 0), (i, 68), colors.black)  # цвет шрифта игроков
        style.append(fn)
        fn = ('TEXTCOLOR', (i + 1, 0), (i + 1, 68), colors.green)  # цвет шрифта номеров встреч
        style.append(fn)
        # выравнивание фамилий игроков по левому краю
        fn = ('ALIGN', (i, 0), (i, 68), 'LEFT') 
        style.append(fn)
        # центрирование номеров встреч
        fn = ('ALIGN', (i + 1, 0), (i + 1, 68), 'CENTER')
        style.append(fn)
    # fn = ('INNERGRID', (0, 0), (-1, -1), 0.01, colors.grey)  # временное отображение сетки
    # style.append(fn)

    ts = style   # стиль таблицы (список оформления строк и шрифта)
    t.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                           ('FONTNAME', (0, 0), (-1, -1), "DejaVuSerif"),
                           ('FONTSIZE', (0, 0), (-1, -1), 7),
                           ('FONTNAME', (1, 0), (1, 32), "DejaVuSerif-Bold"),
                           ('FONTSIZE', (1, 0), (1, 32), 7),
                           # 10 столбец с 0 по 68 ряд (цвет места)
                           ('TEXTCOLOR', (10, 0), (10, 68), colors.red),
                        #    ('ALIGN', (10, 0), (10, 68), 'RIGHT'),
                           ('ALIGN', (9, 0), (9, 68), 'LEFT'),
                           # цвет шрифта игроков 1 ого тура
                           ('TEXTCOLOR', (0, 0), (0, 68), colors.blue),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
                           ] + ts))

    elements.append(t)
    pv = A4
    znak = final.rfind("-")
    f = final[:znak]

    if pv == A4:
        pv = A4
    else:
        pv = landscape(A4)
    t_id = Title.get(Title.id == title_id())
    short_name = t_id.short_name_comp
    # short_name = "чист_16_сетка"  # имя для чистой сетки
    name_table_final = f"{f}-финал_{short_name}.pdf"
    doc = SimpleDocTemplate(name_table_final, pagesize=pv)
    change_dir()
    doc.build(elements, onFirstPage=func_zagolovok, onLaterPages=func_zagolovok)
    change_dir()
    return tds


def setka_32_made(fin):
    """сетка на 32 с розыгрышем 1-3 места"""
    from reportlab.platypus import Table
    table = "setka_32"
    elements = []
    style = []
    data = []
    column = ['']
    column_count = column * 13
    final = fin
    # first_mesto = mesto_in_final(fin)
    first_mesto = 1
    strok = 69
    for i in range(0, strok):
        # column_count[12] = i  # нумерация 10 столбца для удобного просмотра таблицы
        list_tmp = column_count.copy()
        data.append(list_tmp)
    # ========= нумерация встреч сетки ==========
    y = 0
    for i in range(1, 65, 2):
        y += 1
        data[i + 1][0] = str(y)  # рисует начальные номера таблицы 1-32
    number_of_game = draw_num(row_n=3, row_step=2, col_n=2, number_of_columns=5, number_of_game=1, player=32, data=data) # рисует номера встреч 1-32
    data[60][8] = str((number_of_game - 3) * -1)  # номера проигравших 29
    data[62][8] = str((number_of_game - 2) * -1)  # номера проигравших 30
    data[18][10] = str(number_of_game - 1)  # создание номеров встреч (31)
    data[55][10] = str((number_of_game - 1) * -1)  # номер проигравшего финал (-31)
    data[61][10] = str(number_of_game)  # создание номеров встреч 32
    data[66][10] = str((number_of_game) * -1)  # номер проигравшего финал (-32)

    # ============= данные игроков и встреч и размещение по сетке =============
    # ======= создать словарь  ключ - номер встречи, значение - номер ряда
    dict_num_game = {}
    for d in range(2, 11, 2):
        for r in range(0, 69):
            key = data[r][d]
            if key != "":
                dict_num_game[key] = r
    # ===== добавить данные игроков и счета в data ==================
    all_list = setka_data_clear(fin)
    tds = all_list[0]
    for i in range(0, 31, 2):  # цикл расстановки игроков по своим номерам в 1-ом посеве
        n = i - (i // 2)
        data[i][1] = tds[n]
    # ==============
    cw = ((0.2 * cm, 3.8 * cm, 0.35 * cm, 2.7 * cm, 0.35 * cm, 2.7 * cm, 0.35 * cm, 2.7 * cm, 0.35 * cm,
        2.5 * cm, 0.35 * cm, 3.0 * cm, 0.3 * cm))
    # основа сетки на чем чертить таблицу (ширина столбцов и рядов, их кол-во)
    style_color = color_mesta(data, first_mesto, table) # раскрашивает места участников красным цветом
    t = Table(data, cw, strok * [0.35 * cm])
    # =========  цикл создания стиля таблицы =======
    # ========= 1 страница =========
    style = draw_setka(1, 3, 32, style) # рисует кусок сетки(номер столбца, номер строки на 32 человека)
   
    for l in range(34, 57, 22):
        fn = ('LINEABOVE', (11, l), (13, l), 1, colors.darkblue)  # рисует линии встреч за 1-2 места
        style.append(fn)
    for l in range(62, 68, 5):
        fn = ('LINEABOVE', (11, l), (13, l), 1, colors.darkblue)  # рисует линии встреч за 3-4 места
        style.append(fn)
    for l in range(61, 64, 2):
        fn = ('LINEABOVE', (9, l), (10, l), 1, colors.darkblue)  # рисует линии встреч за -29 -30
        style.append(fn)
    fn = ('BOX', (10, 61), (10, 62), 1, colors.darkblue)
    style.append(fn) 
    fn = ('SPAN', (10, 61), (10, 62))  # встреча 32
    style.append(fn)       
    fn = ('BACKGROUND', (10, 61), (10, 62), colors.lightyellow)  # встречи 32 за 3-4 место
    style.append(fn)

    for i in range(0, 11, 2):
        fn = ('TEXTCOLOR', (i + 1, 0), (i + 1, strok), colors.black)  # цвет шрифта игроков
        style.append(fn)
        fn = ('TEXTCOLOR', (i, 0), (i, strok), colors.green)  # цвет шрифта номеров встреч
        style.append(fn)
        # выравнивание фамилий игроков по левому краю
        fn = ('ALIGN', (i + 1, 0), (i + 1, strok), 'LEFT')
        style.append(fn)
        # центрирование номеров встреч
        fn = ('ALIGN', (i, 0), (i, strok), 'CENTER')
        style.append(fn)
    # fn = ('INNERGRID', (0, 0), (-1, -1), 0.01, colors.grey)  # временное отображение сетки
    # style.append(fn)
    ts = style   # стиль таблицы (список оформления строк и шрифта)
    for b in style_color:
        ts.append(b)

    t.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                           ('FONTNAME', (0, 0), (-1, -1), "DejaVuSerif"),
                           ('FONTSIZE', (0, 0), (-1, -1), 7),
                           ('FONTNAME', (1, 0), (1, 32), "DejaVuSerif-Bold"),
                           ('FONTSIZE', (1, 0), (1, 32), 7)] + ts 
                           + [
                           # цвет шрифта игроков 1 ого тура
                           ('TEXTCOLOR', (0, 0), (0, 68), colors.blue),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
                           
    elements.append(t)
    pv = A4
    znak = final.rfind("-")
    f = final[:znak]

    if pv == A4:
        pv = A4
    else:
        pv = landscape(A4)
    t_id = Title.get(Title.id == title_id())
    # short_name = t_id.short_name_comp
    short_name = "чист_32_сетка"
    name_table_final = f"{f}-финал_{short_name}.pdf"
    doc = SimpleDocTemplate(name_table_final, pagesize=pv)
    change_dir()
    doc.build(elements, onFirstPage=func_zagolovok, onLaterPages=func_zagolovok)
    change_dir()
    return tds


def setka_32_full_made(fin):
    """сетка на 32 с розыгрышем всех мест"""
    from reportlab.platypus import Table
    table = "setka_32_full"
    elements = []
    style = []
    data = []
    column = ['']
    column_count = column * 13
    final = fin
    first_mesto = mesto_in_final(fin)
    # first_mesto = 1
    strok = 207
    for i in range(0, strok):
        # column_count[12] = i  # нумерация 10 столбца для удобного просмотра таблицы
        list_tmp = column_count.copy()
        data.append(list_tmp)
    # ========= нумерация встреч сетки ==========
    y = 0
    for i in range(1, 65, 2):
        y += 1
        data[i + 1][0] = str(y)  # рисует начальные номера таблицы 1-32
    number_of_game = draw_num(row_n=3, row_step=2, col_n=2, number_of_columns=5, number_of_game=1, player=32, data=data) # рисует номера встреч 1-32
    data[60][8] = str((number_of_game - 3) * -1)  # номера проигравших 29
    data[62][8] = str((number_of_game - 2) * -1)  # номера проигравших 30
    data[18][10] = str(number_of_game - 1)  # создание номеров встреч (31)
    data[55][10] = str((number_of_game - 1) * -1)  # номер проигравшего финал (-31)
    data[61][10] = str(number_of_game)  # создание номеров встреч 32
    data[66][10] = str((number_of_game) * -1)  # номер проигравшего финал (-32)
    #===== 2-я страница =========
    y = 0
    for i in range(78, 89, 10):
        y += 1
        data[i][8] = str((y + 34) * -1)  # номер проигравшего финал (-35, -36)
    y = 0
    for i in range(101, 112, 9):
        y += 1
        data[i][8] = str((y + 42) * -1)  # номер проигравшего финал (-43, -44)
    y = 0
    for i in range(120, 131, 10):
        y += 1
        data[i][8] = str((y + 46) * -1)  # номер проигравшего финал (-47, -48)
    y = 0
    for i in range(172, 187, 14):
        y += 4
        data[i][10] = str((y + 60) * -1)  # номер проигравшего финал (-64, -68)
    y = 0
    for i in range(198, 206, 7):
        y += 4
        data[i][10] = str((y + 72) * -1)  # номер проигравшего финал (-76, -80)
    data[178][8] = str(-67)  # номер проигравшего финал (-67)
    data[191][6] = str(-75)  # номер проигравшего финал (-75)
    data[164][8] = str(-63)  # номер проигравшего финал (-63)
    data[203][4] = str(-79)  # номер проигравшего финал (-79)

    number_of_game = draw_num(row_n=72, row_step=2, col_n=6, number_of_columns=2, number_of_game=33, player=4, data=data) # рисует номера встреч 1-32
    data[84][8] = str(number_of_game)  # создание номеров встреч 36
    number_of_game = draw_num(row_n=89, row_step=2, col_n=4, number_of_columns=3, number_of_game=37, player=8, data=data) # рисует номера встреч 1-32
    data[106][8] = str(number_of_game)
    number_of_game = draw_num(row_n=114, row_step=2, col_n=6, number_of_columns=2, number_of_game=45, player=4, data=data) # рисует номера встреч 1-32
    data[126][8] = str(number_of_game)  # создание номеров встреч 48
    draw_num_lost(row_n=72, row_step=2, col_n=4, number_of_game=25, player=4, data=data) # номера минус проигравшие встречи -1 -16
    draw_num_lost(row_n=84, row_step=2, col_n=6, number_of_game=33, player=2, data=data) # номера минус проигравшие встречи -1 -16
    draw_num_lost(row_n=89, row_step=2, col_n=2, number_of_game=17, player=8, data=data) # номера минус проигравшие встречи -1 -16
    draw_num_lost(row_n=106, row_step=2, col_n=6, number_of_game=41, player=2, data=data) # номера минус проигравшие встречи -1 -16
    draw_num_lost(row_n=114, row_step=2, col_n=4, number_of_game=37, player=4, data=data) # номера минус проигравшие встречи -1 -16
    draw_num_lost(row_n=126, row_step=2, col_n=6, number_of_game=45, player=2, data=data) # номера минус проигравшие встречи -1 -16
#========== 3-я страница ==============
    number_of_game = draw_num(row_n=140, row_step=2, col_n=2, number_of_columns=4, number_of_game=49, player=16, data=data) # рисует номера встреч 1-32
    data[168][10] = str(number_of_game)  # создание номеров встреч 64
    number_of_game = draw_num(row_n=172, row_step=2, col_n=6, number_of_columns=2, number_of_game=65, player=4, data=data) # рисует номера встреч 1-32
    data[182][10] = str(number_of_game)  # создание номеров встреч 68
    number_of_game = draw_num(row_n=179, row_step=2, col_n=2, number_of_columns=3, number_of_game=69, player=8, data=data) # рисует номера встреч 1-32
    data[194][10] = str(number_of_game)
    number_of_game = draw_num(row_n=197, row_step=2, col_n=2, number_of_columns=2, number_of_game=77, player=4, data=data) # рисует номера встреч 1-32
    data[201][10] = str(number_of_game)  # создание номеров встреч 68
    draw_num_lost(row_n=140, row_step=2, col_n=0, number_of_game=1, player=16, data=data) # номера минус проигравшие встречи -1 -16
    draw_num_lost(row_n=172, row_step=2, col_n=4, number_of_game=57, player=4, data=data) # номера минус проигравшие встречи -1 -16
    draw_num_lost(row_n=179, row_step=2, col_n=0, number_of_game=49, player=8, data=data) # номера минус проигравшие встречи -1 -16
    draw_num_lost(row_n=197, row_step=2, col_n=0, number_of_game=69, player=4, data=data) # номера минус проигравшие встречи -1 -16
    draw_num_lost(row_n=168, row_step=2, col_n=8, number_of_game=61, player=2, data=data) # номера минус проигравшие встречи -1 -16
    draw_num_lost(row_n=182, row_step=2, col_n=8, number_of_game=65, player=2, data=data) # номера минус проигравшие встречи -1 -16
    draw_num_lost(row_n=194, row_step=2, col_n=8, number_of_game=73, player=2, data=data) # номера минус проигравшие встречи -1 -16
    draw_num_lost(row_n=201, row_step=2, col_n=8, number_of_game=77, player=2, data=data) # номера минус проигравшие встречи -1 -16
    # ============= данные игроков и встреч и размещение по сетке =============
    tds = write_in_setka(data, fin, first_mesto, table)
    #===============
    cw = ((0.2 * cm, 3.8 * cm, 0.35 * cm, 2.7 * cm, 0.35 * cm, 2.7 * cm, 0.35 * cm, 2.7 * cm, 0.35 * cm,
        2.5 * cm, 0.35 * cm, 3.0 * cm, 0.3 * cm))
    # основа сетки на чем чертить таблицу (ширина столбцов и рядов, их кол-во)
    style_color = color_mesta(data, first_mesto, table) # раскрашивает места участников красным цветом
    t = Table(data, cw, strok * [0.35 * cm])
    # =========  цикл создания стиля таблицы =======
    # ========= 1 страница =========
    style = draw_setka(1, 3, 32, style) # рисует кусок сетки(номер столбца, номер строки на 32 человека)
   
    for l in range(34, 57, 22):
        fn = ('LINEABOVE', (11, l), (13, l), 1, colors.darkblue)  # рисует линии встреч за 1-2 места
        style.append(fn)
    for l in range(62, 68, 5):
        fn = ('LINEABOVE', (11, l), (13, l), 1, colors.darkblue)  # рисует линии встреч за 3-4 места
        style.append(fn)
    for l in range(61, 64, 2):
        fn = ('LINEABOVE', (9, l), (10, l), 1, colors.darkblue)  # рисует линии встреч за -29 -30
        style.append(fn)

    fn = ('BOX', (10, 61), (10, 62), 1, colors.darkblue)
    style.append(fn) 
    fn = ('SPAN', (10, 61), (10, 62))  # встреча 32
    style.append(fn)       
    fn = ('BACKGROUND', (10, 61), (10, 62), colors.lightyellow)  # встречи 32 за 3-4 место
    style.append(fn)
# =========== 2 страница ===================
    # ======= встречи (33-35) за 5-6 место =====
    style = draw_setka(5, 72, 4, style) # рисует кусок сетки(номер столбца, номер строки на 4 человека)
    style = draw_mesta(row=75, col=9, player=4, style=style) # рисует линии сетки за места(номер строки, участники)
    # ======= встречи (36) за 7-8 место =====
    style = draw_setka(7, 84, 2, style) # рисует кусок сетки(номер столбца, номер строки на 2 человека)
    style = draw_mesta(row=85, col=9, player=4, style=style) # рисует линии сетки за места(номер строки, участники)
    # ======= встречи (37-43) за 9-10 место =====
    style = draw_setka(3, 89, 8, style) # рисует кусок сетки(номер столбца, номер строки на 4 человека)
    style = draw_mesta(row=96, col=9, player=8, style=style) # рисует линии сетки за места(номер строки, участники)
    # ======= встречи (44) за 11-12 место =====
    style = draw_setka(7, 106, 2, style) # рисует кусок сетки(номер столбца, номер строки на 4 человека)
    style = draw_mesta(row=107, col=9, player=2, style=style) # рисует линии сетки за места(номер строки, участники)
    # ======= встречи (45-47) за 13-14 место =====
    style = draw_setka(5, 114, 4, style) # рисует кусок сетки(номер столбца, номер строки на 4 человека)
    style = draw_mesta(row=117, col=9, player=4, style=style) # рисует линии сетки за места(номер строки, участники)
    # ======= встречи (48) за 15-16 место =====
    style = draw_setka(7, 126, 2, style) # рисует кусок сетки(номер столбца, номер строки на 4 человека)
    style = draw_mesta(row=127, col=9, player=2, style=style) # рисует линии сетки за места(номер строки, участники)
# =========== 3 страница ==================
    # ======= встречи (49-56) за 17-18 место =====
    style = draw_setka(1, 140, 16, style) # рисует кусок сетки(номер столбца, номер строки на 16человека)
    style = draw_mesta(row=155, col=9, player=16, style=style) # рисует линии сетки за места(номер строки, участники)
    # ======= встречи (64) за 19-20 место =====
    style = draw_setka(9, 168, 2, style) # рисует кусок сетки(номер столбца, номер строки на 2 человека)
    style = draw_mesta(row=169, col=10, player=2, style=style) # рисует линии сетки за места(номер строки, участники)
    # ======= встречи (33-35) за 21-24 место =====
    style = draw_setka(5, 172, 4, style) # рисует кусок сетки(номер столбца, номер строки на 4 человека)
    style = draw_mesta(row=175, col=8, player=4, style=style) # рисует линии сетки за места(номер строки, участники)
    # ======= встречи (68) за 25-26 место =====
    style = draw_setka(9, 182, 2, style) # рисует кусок сетки(номер столбца, номер строки на 2 человека)
    style = draw_mesta(row=183, col=11, player=2, style=style) # рисует линии сетки за места(номер строки, участники)
    # ======= встречи (69 - 75) за 25-26 место =====
    style = draw_setka(1, 179, 8, style) # рисует кусок сетки(номер столбца, номер строки на 8 человека)
    style = draw_mesta(row=186, col=7, player=8, style=style) # рисует линии сетки за места(номер строки, участники)
    # ======= встречи (64) за 25-26 место =====
    style = draw_setka(9, 194, 2, style) # рисует кусок сетки(номер столбца, номер строки на 2 человека)
    style = draw_mesta(row=195, col=10, player=2, style=style) # рисует линии сетки за места(номер строки, участники)
     # ======= встречи (64) за 25-26 место =====
    style = draw_setka(1, 197, 4, style) # рисует кусок сетки(номер столбца, номер строки на 2 человека)
    style = draw_mesta(row=200, col=5, player=4, style=style) # рисует линии сетки за места(номер строки, участники)
     # ======= встречи (64) за 25-26 место =====
    style = draw_setka(9, 201, 2, style) # рисует кусок сетки(номер столбца, номер строки на 2 человека)
    style = draw_mesta(row=202, col=10, player=2, style=style) # рисует линии сетки за места(номер строки, участники)
    
# =========================================
    for i in range(0, 11, 2):
        fn = ('TEXTCOLOR', (i + 1, 0), (i + 1, 206), colors.black)  # цвет шрифта игроков
        style.append(fn)
        fn = ('TEXTCOLOR', (i, 0), (i, 206), colors.green)  # цвет шрифта номеров встреч
        style.append(fn)
        # выравнивание фамилий игроков по левому краю
        fn = ('ALIGN', (i + 1, 0), (i + 1, 206), 'LEFT')
        style.append(fn)
        # центрирование номеров встреч
        fn = ('ALIGN', (i, 0), (i, 206), 'CENTER')
        style.append(fn)
    # fn = ('INNERGRID', (0, 0), (-1, -1), 0.01, colors.grey)  # временное отображение сетки
    # style.append(fn)
    ts = style   # стиль таблицы (список оформления строк и шрифта)
    for b in style_color:
        ts.append(b)

    t.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                           ('FONTNAME', (0, 0), (-1, -1), "DejaVuSerif"),
                           ('FONTSIZE', (0, 0), (-1, -1), 7),
                           ('FONTNAME', (1, 0), (1, 64), "DejaVuSerif-Bold"),
                           ('FONTSIZE', (1, 0), (1, 64), 7)] + ts 
                           + [
                           # цвет шрифта игроков 1 ого тура
                           ('TEXTCOLOR', (0, 0), (0, 68), colors.blue),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
                           

    elements.append(t)
    pv = A4
    znak = final.rfind("-")
    f = final[:znak]

    if pv == A4:
        pv = A4
    else:
        pv = landscape(A4)
    t_id = Title.get(Title.id == title_id())
    short_name = t_id.short_name_comp
    # short_name = "чист_32_full_сетка"
    name_table_final = f"{f}-финал_{short_name}.pdf"
    doc = SimpleDocTemplate(name_table_final, pagesize=pv)
    change_dir()
    doc.build(elements, onFirstPage=func_zagolovok, onLaterPages=func_zagolovok)
    change_dir()
    return tds


def setka_32_2_made(fin):
    """сетка на 32 (-2) с розыгрышем всех мест"""
    from reportlab.platypus import Table
    table = "setka_32_2"
    elements = []
    style = []
    data = []
    column = ['']
    column_count = column * 15
    final = fin
    # first_mesto = mesto_in_final(fin)
    first_mesto = 1
    strok = 207
    for i in range(0, strok):
        # column_count[14] = i  # нумерация 10 столбца для удобного просмотра таблицы
        list_tmp = column_count.copy()
        data.append(list_tmp)
    # ========= нумерация встреч сетки ==========
    y = 0
    for i in range(1, 65, 2):
        y += 1
        data[i + 1][0] = str(y)  # рисует начальные номера таблицы 1-32
    number_of_game = draw_num(row_n=3, row_step=2, col_n=2, number_of_columns=5, number_of_game=1, player=32, data=data) # рисует номера встреч 1-32 
    data[18][10] = str(number_of_game - 1)  # создание номеров встреч (31)
    data[55][10] = str((number_of_game - 1) * -1)  # номер проигравшего финал (-31)
 # ======= 2-я страница ===========
    draw_num_lost(row_n=74, row_step=2, col_n=0, number_of_game=1, player=16, data=data) # номера минус проигравшие встречи -1 -16
    draw_num_lost(row_n=102, row_step=2, col_n=10, number_of_game=58, player=2, data=data) # номера минус проигравшие встречи -58-59
    draw_num_lost(row_n=110, row_step=2, col_n=10, number_of_game=56, player=2, data=data) # номера минус проигравшие встречи -56-57
    draw_num_lost(row_n=112, row_step=2, col_n=0, number_of_game=52, player=4, data=data) # номера минус проигравшие встречи -52-55
    draw_num_lost(row_n=124, row_step=2, col_n=0, number_of_game=51, player=4, data=data) # номера минус проигравшие встречи -48-51
    draw_num_lost(row_n=120, row_step=2, col_n=8, number_of_game=63, player=2, data=data) # номера минус проигравшие встречи -63-64
    draw_num_lost(row_n=128, row_step=2, col_n=8, number_of_game=67, player=2, data=data) # номера минус проигравшие встречи -67-68
    draw_num_lost_2(row_n=72, row_step=2, col_n=2, revers_number=1, number_of_game=17, player=8, data=data) # номера минус проигравшие встречи -17-24
    draw_num_lost_2(row_n=71, row_step=4, col_n=6, revers_number=1, number_of_game=25, player=2, data=data) # номера минус проигравшие встречи -25-26
    draw_num_lost_2(row_n=87, row_step=4, col_n=6, revers_number=1, number_of_game=27, player=2, data=data) # номера минус проигравшие встречи -27-28
    draw_num_lost_2(row_n=71, row_step=8, col_n=10, revers_number=1, number_of_game=29, player=2, data=data) # номера минус проигравшие встречи -29-30

    number_of_game = draw_num_2(row_n=74, row_step=2, col_n=2, number_of_columns=2, number_of_game=32, player=16, data=data) # рисует номера встреч 33-47 
    number_of_game = draw_num_2(row_n=74, row_step=4, col_n=6, number_of_columns=2, number_of_game=48, player=16, data=data) # рисует номера встреч 48-55
    number_of_game = draw_num_2(row_n=74, row_step=8, col_n=10, number_of_columns=1, number_of_game=56, player=16, data=data) # рисует номера встреч 56-57
    number_of_game = draw_num_2(row_n=72, row_step=8, col_n=12, number_of_columns=1, number_of_game=58, player=16, data=data) # рисует номера встреч 58-59
    number_of_game = draw_num(row_n=112, row_step=2, col_n=2, number_of_columns=2, number_of_game=63, player=4, data=data) # рисует номера встреч 63-65
    number_of_game = draw_num(row_n=124, row_step=2, col_n=2, number_of_columns=2, number_of_game=67, player=4, data=data) # рисует номера встреч 67-69

    data[75][14] = str(number_of_game - 10)  # создание номеров встреч (60)
    data[98][12] = str((number_of_game - 10) * -1)  # номер проигравшего финал (-60)
    data[102][12] = str(number_of_game - 9)  # создание номеров встреч (61)
    data[106][12] = str((number_of_game - 9) * -1)  # номер проигравшего финал (-61)
    data[110][12] = str(number_of_game - 8)  # создание номеров встреч (62)
    data[114][12] = str((number_of_game - 8) * -1)  # номер проигравшего финал (-62)
    data[120][10] = str(number_of_game - 4)  # создание номеров встреч (66)
    data[124][10] = str((number_of_game - 4) * -1)  # номер проигравшего финал (-66)
    data[128][10] = str(number_of_game)  # создание номеров встреч (70)
    data[132][10] = str((number_of_game) * -1)  # номер проигравшего финал (-70)
    data[118][4] = str((number_of_game - 5) * -1)  # номер проигравшего финал (-65)
    data[130][4] = str((number_of_game - 1) * -1)  # номер проигравшего финал (-69)
# ======= 3-я страница ===========
    draw_num_lost(row_n=141, row_step=2, col_n=0, number_of_game=40, player=8, data=data) # номера минус проигравшие встречи
    draw_num_lost(row_n=156, row_step=2, col_n=8, number_of_game=75, player=2, data=data) # номера минус проигравшие встречи
    draw_num_lost(row_n=171, row_step=2, col_n=8, number_of_game=79, player=2, data=data) # номера минус проигравшие встречи
    draw_num_lost(row_n=186, row_step=2, col_n=8, number_of_game=87, player=2, data=data) # номера минус проигравшие встречи
    draw_num_lost(row_n=201, row_step=2, col_n=8, number_of_game=91, player=2, data=data) # номера минус проигравшие встречи
    draw_num_lost(row_n=160, row_step=2, col_n=2, number_of_game=71, player=4, data=data) # номера минус проигравшие встречи
    draw_num_lost(row_n=171, row_step=2, col_n=0, number_of_game=32, player=8, data=data) # номера минус проигравшие встречи
    draw_num_lost(row_n=192, row_step=2, col_n=2, number_of_game=83, player=4, data=data) # номера минус проигравшие встречи

    number_of_game = draw_num(row_n=141, row_step=2, col_n=2, number_of_columns=3, number_of_game=71, player=8, data=data) # рисует номера встреч 49
    data[153][6] = str((number_of_game - 1) * -1)  # создание номеров встреч -77
    data[156][10] = str(number_of_game)  # создание номеров встреч 78
    data[160][10] = str(number_of_game * -1)  # создание номеров встреч -78
    number_of_game = draw_num(row_n=160, row_step=2, col_n=4, number_of_columns=2, number_of_game=79, player=4, data=data) # рисует номера встреч 49
    data[166][6] = str((number_of_game - 1) * -1)  # создание номеров встреч -77
    data[171][10] = str(number_of_game)  # создание номеров встреч 68
    data[175][10] = str(number_of_game * -1)  # создание номеров встреч 68
    number_of_game = draw_num(row_n=171, row_step=2, col_n=2, number_of_columns=3, number_of_game=83, player=8, data=data) # рисует номера встреч 49
    data[183][6] = str((number_of_game - 1) * -1)  # создание номеров встреч -77
    data[186][10] = str(number_of_game)  # создание номеров встреч 90
    data[190][10] = str(number_of_game * -1)  # создание номеров встреч -90
    number_of_game = draw_num(row_n=192, row_step=2, col_n=4, number_of_columns=2, number_of_game=91, player=4, data=data) # рисует номера встреч 49
    data[198][6] = str((number_of_game - 1) * -1)  # создание номеров встреч -77
    data[201][10] = str(number_of_game)  # создание номеров встреч 94
    data[205][10] = str(number_of_game * -1)  # создание номеров встреч -94

    data[205][10] = str(number_of_game * -1)  # создание номеров встреч -94
    data[205][10] = str(number_of_game * -1)  # создание номеров встреч -94
    data[205][10] = str(number_of_game * -1)  # создание номеров встреч -94
    data[205][10] = str(number_of_game * -1)  # создание номеров встреч -94

    # ============= данные игроков и встреч и размещение по сетке =============
    # ======= создать словарь  ключ - номер встречи, значение - номер ряда
    dict_num_game = {}
    for d in range(2, 11, 2):
        for r in range(0, 69):
            key = data[r][d]
            if key != "":
                dict_num_game[key] = r
    # ===== добавить данные игроков и счета в data ==================
    all_list = setka_data_clear(fin)
    tds = all_list[0]
    for i in range(0, 31, 2):  # цикл расстановки игроков по своим номерам в 1-ом посеве
        n = i - (i // 2)
        data[i][1] = tds[n]
    # ==============
    cw = ((0.2 * cm, 3.5 * cm, 0.35 * cm, 2.4 * cm, 0.35 * cm, 2.4 * cm, 0.35 * cm, 2.4 * cm, 0.35 * cm, 2.4 * cm, 0.35 * cm,
        2.4 * cm, 0.35 * cm, 2.6 * cm, 0.35 * cm))
    # основа сетки на чем чертить таблицу (ширина столбцов и рядов, их кол-во)
    style_color = color_mesta(data, first_mesto, table) # раскрашивает места участников красным цветом
    t = Table(data, cw, strok * [0.35 * cm])
    # =========  цикл создания стиля таблицы =======
    # ========= 1 страница =========
    style = draw_setka(1, 3, 32, style) # рисует кусок сетки(номер столбца, номер строки на 32 человека)
   
    for l in range(34, 57, 22):
        fn = ('LINEABOVE', (11, l), (13, l), 1, colors.darkblue)  # рисует линии встреч за 1-2 места
        style.append(fn)
# =========== 2 страница ===================
    # # ======= встречи (33-35) за 3-4 место =====
    style = draw_setka_2(1, 74, 16, style) # рисует кусок сетки(номер столбца, номер строки на 16 человека)
    for k in range(0, 7, 6):
        for l in range(72 + k, 89 + k, 16):
            fn = ('LINEABOVE', (11, l), (12, l), 1, colors.darkblue)  # рисует линии встреч за 1-2 места
            style.append(fn)   
    for k in range(0, 17, 16):
        fn = ('BOX', (12, 72 + k), (12, 77 + k), 1, colors.darkblue)
        style.append(fn) 
        fn = ('SPAN', (12, 72 + k), (12, 77 + k))  # встреча 32
        style.append(fn)       
        fn = ('BACKGROUND', (12, 72 + k), (12, 77 + k), colors.lightyellow)  # встречи 32 за 3-4 место
        style.append(fn) 
           
    for l in range(75, 101, 8):
        fn = ('LINEABOVE', (13, l), (13, l), 1, colors.darkblue)  # рисует линии встреч за 3-4 места
        style.append(fn)
    fn = ('BOX', (14, 75), (14, 90), 1, colors.darkblue)
    style.append(fn) 
    fn = ('SPAN', (14, 75), (14, 90))  # встреча 32
    style.append(fn)       
    fn = ('BACKGROUND', (14, 75), (14, 90), colors.lightyellow)  # встречи 32 за 3-4 место
    style.append(fn)  
    # # ======= встречи (61) за 5-6 место =====
    style = draw_setka(11, 102, 2, style) # рисует кусок сетки(номер столбца, номер строки на 2 человека)
    style = draw_mesta(row=103, col=13, player=2, style=style) # рисует линии сетки за места(номер строки, участники)
    # ======= встречи (36) за 7-8 место =====
    style = draw_setka(11, 110, 2, style) # рисует кусок сетки(номер столбца, номер строки на 2 человека)
    style = draw_mesta(row=111, col=13, player=2, style=style) # рисует линии сетки за места(номер строки, участники)
    # ======= встречи (37-43) за 9-10 место =====
    style = draw_setka(1, 112, 4, style) # рисует кусок сетки(номер столбца, номер строки на 4 человека)
    style = draw_mesta(row=115, col=5, player=2, style=style) # рисует линии сетки за места(номер строки, участники)
    # ======= встречи (44) за 11-12 место =====
    style = draw_setka(9, 120, 2, style) # рисует кусок сетки(номер столбца, номер строки на 4 человека)
    style = draw_mesta(row=121, col=11, player=2, style=style) # рисует линии сетки за места(номер строки, участники)
     # ======= встречи (37-43) за 13-14 место =====
    style = draw_setka(1, 124, 4, style) # рисует кусок сетки(номер столбца, номер строки на 4 человека)
    style = draw_mesta(row=127, col=5, player=4, style=style) # рисует линии сетки за места(номер строки, участники)
    # ======= встречи (44) за 15-16 место =====
    style = draw_setka(9, 128, 2, style) # рисует кусок сетки(номер столбца, номер строки на 4 человека)
    style = draw_mesta(row=129, col=11, player=2, style=style) # рисует линии сетки за места(номер строки, участники)
# =========== 3 страница ==================
    # ======= встречи (49-56) за 17-18 место =====
    style = draw_setka(1, 141, 8, style) # рисует кусок сетки(номер столбца, номер строки на 8 человека)
    style = draw_mesta(row=148, col=7, player=8, style=style) # рисует линии сетки за места(номер строки, участники)
   # ======= встречи (64) за 19-20 место =====
    style = draw_setka(9, 156, 2, style) # рисует кусок сетки(номер столбца, номер строки на 2 человека)
    style = draw_mesta(row=157, col=10, player=2, style=style) # рисует линии сетки за места(номер строки, участники)
    # ======= встречи (33-35) за 21-24 место =====
    style = draw_setka(3, 160, 4, style) # рисует кусок сетки(номер столбца, номер строки на 4 человека)
    style = draw_mesta(row=163, col=6, player=4, style=style) # рисует линии сетки за места(номер строки, участники)
    # ======= встречи (68) за 25-26 место =====
    style = draw_setka(9, 171, 2, style) # рисует кусок сетки(номер столбца, номер строки на 2 человека)
    style = draw_mesta(row=172, col=10, player=2, style=style) # рисует линии сетки за места(номер строки, участники)
    # ======= встречи (69 - 75) за 25-26 место =====
    style = draw_setka(1, 171, 8, style) # рисует кусок сетки(номер столбца, номер строки на 8 человека)
    style = draw_mesta(row=178, col=7, player=8, style=style) # рисует линии сетки за места(номер строки, участники)
    # ======= встречи (64) за 25-26 место =====
    style = draw_setka(9, 186, 2, style) # рисует кусок сетки(номер столбца, номер строки на 2 человека)
    style = draw_mesta(row=187, col=10, player=2, style=style) # рисует линии сетки за места(номер строки, участники)
     # ======= встречи (64) за 25-26 место =====
    style = draw_setka(3, 192, 4, style) # рисует кусок сетки(номер столбца, номер строки на 2 человека)
    style = draw_mesta(row=195, col=6, player=4, style=style) # рисует линии сетки за места(номер строки, участники)
     # ======= встречи (64) за 25-26 место =====
    style = draw_setka(9, 201, 2, style) # рисует кусок сетки(номер столбца, номер строки на 2 человека)
    style = draw_mesta(row=202, col=10, player=2, style=style) # рисует линии сетки за места(номер строки, участники)
   
# =========================================
    for i in range(0, 15, 2):
        fn = ('TEXTCOLOR', (i + 1, 0), (i + 1, 206), colors.black)  # цвет шрифта игроков
        style.append(fn)
        fn = ('TEXTCOLOR', (i, 0), (i, 206), colors.green)  # цвет шрифта номеров встреч
        style.append(fn)
        # выравнивание фамилий игроков по левому краю
        fn = ('ALIGN', (i + 1, 0), (i + 1, 206), 'LEFT')
        style.append(fn)
        # центрирование номеров встреч
        fn = ('ALIGN', (i, 0), (i, 206), 'CENTER')
        style.append(fn)
    # fn = ('INNERGRID', (0, 0), (-1, -1), 0.01, colors.grey)  # временное отображение сетки
    # style.append(fn)
    ts = style   # стиль таблицы (список оформления строк и шрифта)
    for b in style_color:
        ts.append(b)

    t.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                           ('FONTNAME', (0, 0), (-1, -1), "DejaVuSerif"),
                           ('FONTSIZE', (0, 0), (-1, -1), 7),
                           ('FONTNAME', (1, 0), (1, 32), "DejaVuSerif-Bold"),
                           ('FONTSIZE', (1, 0), (1, 32), 7)] + ts 
                           + [
                           # цвет шрифта игроков 1 ого тура
                           ('TEXTCOLOR', (0, 0), (0, 68), colors.blue),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
                           
    elements.append(t)
    pv = A4
    znak = final.rfind("-")
    f = final[:znak]

    if pv == A4:
        pv = A4
    else:
        pv = landscape(A4)
    t_id = Title.get(Title.id == title_id())
    # short_name = t_id.short_name_comp
    short_name = "чист_32_2_сетка"
    name_table_final = f"{f}-финал_{short_name}.pdf"
    doc = SimpleDocTemplate(name_table_final, pagesize=pv)
    change_dir()
    doc.build(elements, onFirstPage=func_zagolovok, onLaterPages=func_zagolovok)
    change_dir()
    return tds


def mesto_in_final(fin):
    """с какого номера расставляются места в финале, в зависимости от его номера и кол-во участников fin - финал"""
    final = []
    mesto = {}
    tmp = []

    system = System.select().where(System.title_id == title_id())  # находит system id последнего

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


def write_in_setka(data, fin, first_mesto, table):
    """функция заполнения сетки результатами встреч"""
    sender = my_win.sender()
    row_num_los = {}
    row_end = 0  # кол-во строк для начальной расстоновки игроков в зависимости от таблицы
    column = 3
    flag_clear = False
    # уточнить кол-во столбцов
    if table == "setka_16_full":
        row_last = 69
        column_last = 11
        row_end = 31
        row_num_win = {9: [1, 5], 10: [9, 13], 11: [17, 21], 12: [25, 29], 13: [3, 11], 14: [19, 27], 25: [41, 45], 26: [49, 53], 
                    15: [7, 23], 19: [32, 36], 27: [43, 51], 31: [58, 62]}
                 # ======= list mest
        mesta_dict = {15: 15, 16: 29, 19: 34, 20: 39, 27: 47, 28: 55, 31: 60, 32: 65}
    elif table == "setka_16_2":
        row_end = 31
    elif table == "setka_32":
        row_last = 69
        column_last = 11
        row_end = 65
        # column = [[49, 50, 51, 52, 53, 54, 55, 56, 69, 70, 71, 72, 77, 78], 
        # [17, 18, 19, 20, 21, 22, 23, 24, 37, 38, 39, 40, 57, 58, 59, 60, 73, 74], 
        # [25, 26, 27, 28, 33, 34, 41, 42, 45, 46, 61, 62, 65, 66],
        # [29, 30]]
                 # ======= list mest
        # mesta_list = [31, -31, 32, -32, 35, -35, 36, -36, 43, -43, 44, -44, 47, -47, 48, -48, 63, -63,
        #                 64, -64, 67, -67, 68, -68, 75, -75, 76, -76, 79, -79, 80, -80]
        row_num_win = {17: [3, 7], 18: [11, 15], 19: [19, 23], 20: [27, 31], 21: [35, 39], 22: [43, 47], 23: [51, 55],
        24: [59, 63], 25: [5, 13], 26: [21, 29], 27: [37, 45], 28: [53, 61], 29: [9, 25], 30:[41, 57], 31: [17, 49], 
        35: [72, 76], 41: [89, 93], 42: [97, 101], 43: [91, 99], 47: [114, 118],  57: [140, 144], 58: [148, 152], 
        59: [156, 160], 60: [164, 168], 61: [142, 150], 62: [158, 166], 63: [146, 162], 67: [172, 176], 73: [179, 183],
        74: [187, 191], 75: [181, 189], 79: [197, 201]}
        mesta_list = [31, -31, 32, -32, 35, -35, 36, -36, 43, -43, 44, -44, 47, -47, 48, -48, 63, -63,
                        64, -64, 67, -67, 68, -68, 75, -75, 76, -76, 79, -79, 80, -80]
    elif table == "setka_32_2":
        row_last = 207
        column_last = 15
        row_end = 65
    elif table == "setka_32_full":
        row_last = 207
        column_last = 11
        row_end = 65
        row_num_win = {17: [3, 7], 18: [11, 15], 19: [19, 23], 20: [27, 31], 21: [35, 39], 22: [43, 47], 23: [51, 55],
        24: [59, 63], 25: [5, 13], 26: [21, 29], 27: [37, 45], 28: [53, 61], 29: [9, 25], 30:[41, 57], 31: [17, 49], 
        35: [72, 76], 41: [89, 93], 42: [97, 101], 43: [91, 99], 47: [114, 118],  57: [140, 144], 58: [148, 152], 
        59: [156, 160], 60: [164, 168], 61: [142, 150], 62: [158, 166], 63: [146, 162], 67: [172, 176], 73: [179, 183],
        74: [187, 191], 75: [181, 189], 79: [197, 201]}
                 # ======= dict mest
        mesta_dict = {31: 33, 32: 61, 35: 74, 36: 84, 43: 95, 44: 106, 47: 116, 48: 126, 63: 154,
                        64: 168, 67: 174, 68: 182, 75: 185, 76: 194, 79: 199, 80: 201}
    

    if sender == my_win.clear_s32_Action or sender == my_win.clear_s32_full_Action or sender == my_win.clear_s32_2_Action:
        all_list = setka_data_clear(fin, table)  # печать чистой сетки
        col_first = 0
        row_first = 2
        flag_clear = True
    elif sender == my_win.clear_s16_Action:
        all_list = setka_data_clear(fin, table)  # печать чистой сетки
        col_first = 2
        row_first = 0
        flag_clear = True
    else:
        col_first = 0
        sys = System.select().where(System.title_id == title_id())
        system = sys.select().where(System.stage == fin).get()
        setka_string = system.label_string
        if setka_string == "Сетка (с розыгрышем всех мест) на 16 участников":
            all_list = setka_data_16(fin)
            col_first = 2
            row_first = 0
        elif setka_string == "Сетка (с розыгрышем всех мест) на 32 участников":
            col_first = 0
            row_first = 2
            all_list = setka_data_32(fin)
        id_name_city = all_list[1]
        id_sh_name = all_list[2]
    tds = all_list[0]  # список фамилия/ город 1-ого посева
  
    for d in range(col_first, column_last, 2):
        for r in range(row_first, row_last):
            key = data[r][d]
            if key != "":
                k = int(key)
            if key != "" and k < 0:
                row_num_los[key] = r # словарь номер игры, сноски - номер строки

    n = 0
    for t in range(row_first, row_end, 2):  # цикл расстановки игроков по своим номерам в 1-ом посеве
        data[t][1] = tds[n]
        n += 1
    # ==============
    if flag_clear is False:
        # функция расстановки счетов и сносок игроков
        dict_setka = score_in_setka(fin)
        key_list = []
        mesta_list = []
        for k in dict_setka.keys():
            key_list.append(k)
        for v in mesta_dict.keys():
            mesta_list.append(v)
        # ============
        for i in key_list: # спиисок встреч которые сыграны
            match = dict_setka[i]
            pl_win = match[1]
            pl_los = match[4]
            if pl_win != "bye":
                id_win = id_sh_name[f"{pl_win}"]
            if pl_los != "bye":
                id_los = id_sh_name[f"{pl_los}"]
            i = int(i)
            r = str(match[3])
            # ===== определение мест и запись в db
            if i in mesta_list:
                # index = mesta_list.index(row_rank)
                index = mesta_list.index(i)
                mesto = first_mesto + index
                pl1 = match[1]
                pl1_mesto = mesto - 1
                pl2 = match[4]
                pl2_mesto = mesto
                # записывает места в таблицу -Player-
                player = Player.get(Player.id == id_win)
                win = f"{player.player}/ {player.city}"
                player.mesto = pl1_mesto
                player.save()
                player = Player.get(Player.id == id_los)
                los = f"{player.player}/ {player.city}"
                player.mesto = pl2_mesto
                player.save()
            c = match[0]
            c_mesto = 1
            # ========== расстановка для сетки на 16
            if c != 0: # встречи в сетке не за места
                row_win_list = row_num_win[c]  # номера строк данной встречи в сетке
                if abs(match[3]) % 2 != 0: # выбирает из списка номер строки в зависимости от четности встречи(вверх или низ)
                    row_win = row_win_list[0]
                else:
                    row_win = row_win_list[1]

                c1 = []
                c = str(c)

                win = match[1]
                los = match[4]
            elif c == 0:  # встречи за места
                c_mesto = 0
                win_r = int(r) * -1 # номер встречи
                row_win = mesta_dict[win_r]
                c = str(win_r)
            c1.clear()
            # цикл создания списков номеров встреч по столбцам
            for rd in range(0, row_last):
                d1 = data[rd][2]
                d2 = data[rd][4]
                d3 = data[rd][6]
                d4 = data[rd][8]
                d5 = data[rd][10]

                if d1 != "":
                    if type(d1) == str:
                        c1.append(d1)
                        if c in c1:
                            col_win = 1
                            break
                if d2 != "":
                    if type(d2) == str:
                        c1.append(d2)
                        if c in c1:
                            col_win = 3
                            break
                if d3 != "":
                    if type(d3) == str:
                        c1.append(d3)
                        if c in c1:
                            col_win = 5
                            break
                if d4 != "":
                    if type(d4) == str:
                        c1.append(d4)
                        if c in c1:
                            col_win = 7
                            break
                if d5 != "":
                    if type(d5) == str:
                        c1.append(d5)
                        if c in c1:
                            col_win = 9
                            break

            if c_mesto == 0: # если игры за место номер столбца меняется на +2
                col_win += 2

            row_los = row_num_los[r]  # строка проигравшего
            score = match[2]  # счет во встречи
            row_list_los = data[row_los]  # получаем список строки, где ищет номер куда сносится проигравший
            col_los = row_list_los.index(r) # номер столбца проигравшего
            data[row_win][col_win] = win
            data[row_win + 1][col_win] = score
            data[row_los][col_los + 1] = los

        return tds


def setka_data_clear(fin, table):
    """заполняет сетку для просмотра пустыми фамилиями"""
    all_list = []
    tmp = [""]
    if table == "setka_16_full" or table == "setka_16_2":
        max_pl = 16
    elif table == "setka_32" or table == "setka_32_full" or table == "setka_32_2":
        max_pl = 32
    tds = tmp * max_pl
    all_list.append(tds)
    return all_list
    

def kol_player():
    """выводит максимальное количество человек в группе t если все группы равны, а g2 если разное количество"""
    system = System.get(System.title_id == title_id())
    all_players = system.total_athletes
    all_group = system.total_group
    flat = all_players % all_group  # если количество участников равно делится на группы
    # если количество участников не равно делится на группы, g2 наибольшое кол-во человек в группе
    player_flat = all_players // all_group
    if flat == 0:
        max_gamer = player_flat
    else:
        max_gamer = player_flat + 1
    return max_gamer


def table_data(stage, kg):
    """циклом создаем список участников каждой группы"""
    tdt_all = []  # список списков [tdt_new] и [tdt_color]
    tdt_color = []
    tdt_new = []
    ta = Result.select().where(Result.title_id == title_id())  # находит system id последнего
    # проверяет заполнена ли таблица (если строк 0, то еще нет записей)
    tr = len(ta)  # общее кол-во игр в группах
    if kg == 1:  # система одна таблица круг или финалу по кругу
        # список словарей участник и его регион
        posev_data = player_choice_one_table(stage)
        count_player_group = len(posev_data)
        num_gr = "1 группа"
        max_gamer = count_player_group
        num_gr = stage
        tdt_tmp = tdt_news(max_gamer, posev_data, count_player_group, tr, num_gr)
        tdt_new.append(tdt_tmp[0])
        tdt_color.append(tdt_tmp[1])
        tdt_all.append(tdt_new)
        tdt_all.append(tdt_color)
    else:
        max_gamer = kol_player()
        for p in range(0, kg):
            num_gr = f"{p + 1} группа"
            posev_data = player_choice_in_group(num_gr)
            count_player_group = len(posev_data)
            tdt_tmp = tdt_news(max_gamer, posev_data, count_player_group, tr, num_gr)
            tdt_new.append(tdt_tmp[0])
            tdt_color.append(tdt_tmp[1])
            tdt_all.append(tdt_new)
            tdt_all.append(tdt_color)
    return tdt_all


def tdt_news(max_gamer, posev_data, count_player_group, tr, num_gr):
    tdt_tmp = []
    tbl_tmp = []  # временный список группы tbl
    # цикл нумерации строк (по 2-е строки на каждого участника)
    for k in range(1, max_gamer * 2 + 1):
        st = ['']
        # получаем пустой список (номер, фамилия и регион, клетки (кол-во уч), оч, соот, место)
        s = (st * (max_gamer + 4))
        s.insert(0, str((k + 1) // 2))  # получаем нумерацию строк по порядку
        tbl_tmp.append(s)
    for i in range(1, count_player_group * 2 + 1, 2):
        posev = posev_data[((i + 1) // 2) - 1]
        tbl_tmp[i - 1][1] = posev["фамилия"]
        tbl_tmp[i][1] = posev["регион"]
    td = tbl_tmp.copy()  # cписок (номер, фамилия, город и пустые ячейки очков)
    td_color = []

    if tr != 0:  # если еще не была жеребьевка, то пропуск счета в группе
        # список очки победителя красные (ряд, столбец) без заголовка
        td_color = score_in_table(td, num_gr)

    tdt_new = td
    tdt_tmp.append(tdt_new)
    tdt_tmp.append(td_color)

    return tdt_tmp


def setka_data_16(fin):
    """данные сетки на 16"""
    id_ful_name = {}
    id_name = {}
    system = System.select().where(System.title_id == title_id())  # находит system id последнего
    for sys in system:  # проходит циклом по всем отобранным записям
        if sys.stage == fin:
            mp = sys.max_player
    tds = []
    all_list = []
    posev_data = player_choice_in_setka(fin)  # посев
    for i in range(1, mp * 2 + 1, 2):
        posev = posev_data[((i + 1) // 2) - 1]
        family = posev['фамилия']
        if family != "bye":
            id_f_name = full_player_id(family)
            id_f_n = id_f_name[0]
            id_s_n = id_f_name[1]
            # словарь ключ - полное имя/ город, значение - id
            id_ful_name[id_f_n["name"]] = id_f_n["id"]
            id_name[id_s_n["name"]] = id_s_n["id"]
            # =================
            # находит пробел отделяющий имя от фамилии
            space = family.find(" ")
            line = family.find("/")  # находит черту отделяющий имя от города
            city_slice = family[line:]  # получает отдельно город
            # получает отдельно фамилия и первую букву имени
            family_slice = family[:space + 2]
            family_city = f'{family_slice}.{city_slice}'   # все это соединяет
            tds.append(family_city)
        else:
            tds.append(family)
    all_list.append(tds)
    all_list.append(id_ful_name)
    all_list.append(id_name)
    return all_list


def setka_data_32(fin):
    """данные сетки на 32"""
    id_ful_name = {}
    id_name = {}
    system = System.select().where(System.title_id == title_id())  # находит system id последнего
    for sys in system:  # проходит циклом по всем отобранным записям
        if sys.stage == fin:
            mp = sys.max_player
    tds = []
    all_list = []
    posev_data = player_choice_in_setka(fin)  # посев

    for i in range(1, mp * 2 + 1, 2):
        posev = posev_data[((i + 1) // 2) - 1]
        family = posev['фамилия']
        if family != "bye":
            id_f_name = full_player_id(family)
            id_f_n = id_f_name[0]
            id_s_n = id_f_name[1]
            # словарь ключ - полное имя/ город, значение - id
            id_ful_name[id_f_n["name"]] = id_f_n["id"]
            id_name[id_s_n["name"]] = id_s_n["id"]
            # =================
            # находит пробел отделяющий имя от фамилии
            space = family.find(" ")
            line = family.find("/")  # находит черту отделяющий имя от города
            city_slice = family[line:]  # получает отдельно город
            # получает отдельно фамилия и первую букву имени
            family_slice = family[:space + 2]
            family_city = f'{family_slice}.{city_slice}'   # все это соединяет
            tds.append(family_city)
        else:
            tds.append(family)
    all_list.append(tds)
    all_list.append(id_ful_name)
    all_list.append(id_name)
    return all_list


def full_player_id(family):
    """получает словарь -фамилия игрока и его город и соответствующий ему id в таблице Players"""
    full_name = {}
    short_name = {}
    # получение id последнего соревнования
    t = Title.select().order_by(Title.id.desc()).get()
    plr = Player.get(Player.title_id == t and Player.full_name == family)
    id_player = plr.id
    city = plr.city
    name = plr.player
    space = name.find(" ")  # находит пробел отделяющий имя от фамилии
    # получает отдельно фамилия и первую букву имени
    family_slice = name[:space + 2]
    full_name["name"] = f"{family_slice}./ {city}"
    full_name["id"] = id_player
    short_name["name"] = f"{family_slice}."
    short_name["id"] = id_player
    name_list = []
    name_list.append(full_name)
    name_list.append(short_name)

    return name_list


def score_in_table(td, num_gr):
    """заносит счет и места в таблицу группы или таблицу по кругу pdf
    -td- список строки таблицы, куда пишут счет"""
    td_color = []
    total_score = {}  # словарь, где ключ - номер участника группы, а значение - очки
    tab = my_win.tabWidget.currentIndex()
    system = System.select().where(System.title_id == title_id())
    if tab == 3:
        ta = system.select().where(System.stage == "Предварительный").get()  # находит system id последнего
    elif tab == 4:
        pass
    else:
        ta = system.select().where(System.stage == num_gr).get()  # находит system id последнего
    mp = ta.max_player
    stage = ta.stage

    result = Result.select().where(Result.title_id == title_id())
    ch = Choice.select().where(Choice.title_id == title_id())
    if stage == "Предварительный":
        r = result.select().where(Result.number_group == num_gr)
        choice = ch.select().where(Choice.group == num_gr)  # фильтрует по группе
    elif stage == "Одна таблица":
        r = result.select().where(Result.number_group == "1 группа")
        choice = ch.select().where(Choice.basic == "Одна таблица")  # фильтрует по одной таблице
    else:
        r = result.select().where(Result.number_group == num_gr)
        choice = ch.select().where(Choice.final == num_gr)  # фильтрует финал по кругу

    count = len(r)  # сколько игр в группе
    count_player = len(choice)  # определяет сколько игроков в группе
    result_list = r.dicts().execute()
    for s in range(1, count_player + 1):
        total_score[s] = 0
    for i in range(0, count):
        sc_game = str(list(result_list[i].values())[9])  # счет в партиях
        if sc_game != "" or sc_game != "None":
            scg = 9
        else:  # номер столбца
            scg = 8
        tours = str(list(result_list[i].values())[3])  # номера игроков в туре
        znak = tours.find("-")
        p1 = int(tours[:znak])  # игрок под номером в группе
        p2 = int(tours[znak + 1:])  # игрок под номером в группе

        win = str(list(result_list[i].values())[6])
        player1 = str(list(result_list[i].values())[4])
        if win != "" and win != "None":  # если нет сыгранной встречи данного тура
            if win == player1:  # если победитель игрок под первым номером в туре
                # очки 1-ого игрока
                td[p1 * 2 - 2][p2 + 1] = str(list(result_list[i].values())[7])  # ячейка в таблице очки
                # счет 1-ого игрока
                td[p1 * 2 - 1][p2 + 1] = str(list(result_list[i].values())[scg])   # ячейка в таблице счет впартии
                # очки 2-ого игрока
                td[p2 * 2 - 2][p1 + 1] = str(list(result_list[i].values())[11])  # ячейка в таблице очки
                # счет 2-ого игрока
                td[p2 * 2 - 1][p1 + 1] = str(list(result_list[i].values())[12])  # ячейка в таблице счет впартии
                # очки 1-ого игрока
                tp1 = str(list(result_list[i].values())[7])
                # очки 2-ого игрока
                tp2 = str(list(result_list[i].values())[11])
                # считывает из словаря 1-ого игрока всего очков
                plr1 = total_score[p1]
                # считывает из словаря 2-ого игрока всего очков
                plr2 = total_score[p2]
                plr1 = plr1 + int(tp1)  # прибавляет очки 1-ого игрока
                plr2 = plr2 + int(tp2)  # прибавляет очки 2-ого игрока
                total_score[p1] = plr1  # записывает сумму очков 1-му игроку
                total_score[p2] = plr2  # записывает сумму очков 2-му игроку
                col = p1 * 2 - 2
                row = p2 + 1
            else:  # если победитель игрок под вторым номером в туре
                # очки 1-ого игрока
                td[p1 * 2 - 2][p2 + 1] = str(list(result_list[i].values())[11])
                # счет 1-ого игрока
                td[p1 * 2 - 1][p2 + 1] = str(list(result_list[i].values())[12])
                # очки 2-ого игрока
                td[p2 * 2 - 2][p1 + 1] = str(list(result_list[i].values())[7])
                # счет 2-ого игрока
                td[p2 * 2 - 1][p1 + 1] = str(list(result_list[i].values())[scg])
                # очки 1-ого игрока
                tp1 = str(list(result_list[i].values())[11])
                # очки 2-ого игрока
                tp2 = str(list(result_list[i].values())[7])
                # считывает из словаря 1-ого игрока очки
                plr1 = total_score[p1]
                # считывает из словаря 2-ого игрока очки
                plr2 = total_score[p2]
                plr1 = plr1 + int(tp1)  # прибавляет очки 1-ого игрока
                plr2 = plr2 + int(tp2)  # прибавляет очки 2-ого игрока
                total_score[p1] = plr1  # записывает сумму очков 1-му игроку
                total_score[p2] = plr2  # записывает сумму очков 2-му игроку
                col = p2 * 2 - 2
                row = p1 + 1
            # список ряд столбец, где очки надо красить в красный
            td_tmp = [row, col]
            td_color.append(td_tmp)
    for t in range(0, count_player):  # записывает очки в зависимости от кол-во игроков в группе
        # записывает каждому игроку сумму очков
        td[t * 2][mp + 2] = total_score[t + 1]
    # ===== если сыграны все игры группе то выставляет места =========
    count_game = (count_player * (count_player - 1)) // 2
    result_id = Result.select().where(Result.title_id == title_id())
    if num_gr == "Одна таблица":
        result = result_id.select().where(Result.system_stage == num_gr)
    else:
        result = result_id.select().where(Result.number_group == num_gr)
    a = 0
    for r in result:
        if r.points_win == 2:
            a += 1
    if a == count_game:
        rank_in_group(total_score, mp, td, num_gr)  # определяет места в группе

    return td_color


def numer_game(num_game, vid_setki):
    """определяет куда записывать победителя и проигравшего по сноске в сетке, номера встреч"""
    snoska = []
    num_game = int(num_game)
    if vid_setki == 'Сетка (с розыгрышем всех мест) на 16 участников':
        dict_winner = {1: 9, 2: 9, 3: 10, 4: 10, 5: 11, 6: 11, 7: 12, 8: 12, 9: 13, 10: 13, 11: 14, 12: 14, 13: 15, 14: 15,
                   17: 19, 18: 19, 21: 25, 22: 25, 23: 26, 24: 26, 25: 27, 26: 27, 29: 31, 30: 31}
        dict_loser = {1: 21, 2: 21, 3: 22, 4: 22, 5: 23, 6: 23, 7: 24, 8: 24, 9: 17, 10: 17, 11: 18, 12: 18, 13: 16, 14: 16,
                  17: 20, 18: 20, 21: 29, 22: 29, 23: 30, 24: 30, 25: 28, 26: 28, 29: 32, 30: 32}
        dict_loser_pdf = {1: -1, 2: -2, 3: -3, 4: -4, 5: -5, 6: -6, 7: -7, 8: -8, 9: -9, 10: -10, 11: -11, 12: -12, 13: -13,
                      14: -14, 17: -17, 18: -18, 21: -21, 22: -22, 23: -23, 24: -24, 25: -25, 26: -26, 29: -29, 30: -30}
        dict_mesta = [15, 16, 19, 20, 27, 28, 31, 32]
    elif vid_setki == 'Сетка (минус 2) на 16 участников':
        pass
    elif vid_setki == 'Сетка (с розыгрышем всех мест) на 32 участников':
        dict_winner = {1: 17, 2: 17, 3: 18, 4: 18, 5: 19, 6: 19, 7: 20, 8: 20, 9: 21, 10: 21, 11: 22, 12: 22, 13: 23, 14: 23,
                   15: 24, 16: 24, 17: 25, 18: 25, 19: 26, 20: 26, 21: 27, 22: 27, 23: 28, 24: 28, 25: 29, 26: 29, 27: 30, 28: 30, 
                   29: 31, 30: 31, 33: 35, 34: 35, 37: 41, 38: 41, 39: 42, 40: 42, 41: 43, 42: 43, 45: 47, 46: 47, 49: 57, 50: 57,
                   51: 58, 52: 58, 53: 59, 54: 59, 55: 60, 56: 60, 57: 61, 58: 61, 59: 62, 60: 62, 61: 63, 62: 63, 65: 67, 66: 67,
                   69: 73, 70: 73, 71: 74, 72: 74, 73: 75, 74: 75, 77: 79, 78: 79}
        dict_loser = {1: 49, 2: 49, 3: 50, 4: 50, 5: 51, 6: 51, 7: 52, 8: 52, 9: 53, 10: 53, 11: 54, 12: 54, 13: 55, 14: 55, 15: 56, 16: 56,
                  17: 37, 18: 37, 19: 38, 20: 38, 21: 39, 22: 39, 23: 40, 24: 40, 25: 33, 26: 33, 27: 34, 28: 34, 29: 32, 30: 32,
                  33: 36, 34: 36, 37: 45, 38: 45, 39: 46, 40: 46, 41: 44, 42: 44, 45: 48, 46: 48, 49: 69, 50: 69, 51: 70, 52: 70, 53: 71, 54: 71, 55: 72, 56: 72,
                  57: 65, 58: 65, 59: 66, 60: 66, 61: 64, 62: 64, 65: 68, 66: 68, 69: 77, 70: 77, 71: 78, 72: 78, 73: 76, 74: 76, 77: 80, 78: 80}
        dict_loser_pdf = {1: -1, 2: -2, 3: -3, 4: -4, 5: -5, 6: -6, 7: -7, 8: -8, 9: -9, 10: -10, 11: -11, 12: -12, 13: -13,
                    14: -14, 15: -15, 16: -16, 17: -17, 18: -18, 19: -19, 20: -20, 21: -21, 22: -22, 23: -23, 24: -24, 25: -25, 26: -26, 
                    27: -27, 28: -28, 29: -29, 30: -30, 33: -33, 34: -34, 37: -37, 38: -38, 39: -39, 40: -40, 41: -41, 42: -42, 45: -45, 46: -46,
                    49: -49, 50: -50, 51: -51, 52: -52, 53: -53, 54: -54, 55: -55, 56: -56, 57: -57, 58: -58, 59: -59, 60: -60, 61: -61, 62: -62, 65: -65, 66: -66,
                    69: -69, 70: -70, 71: -71, 72: -72, 73: -73, 74: -74, 75: -75, 77: -77, 78: -78, 79: -79}
        dict_mesta = [31, 32, 35, 36, 43, 44, 47, 48, 63, 64, 67, 68, 75, 76, 79, 80]
    elif vid_setki == 'Сетка (минус 2) на 32 участников':
        pass
    elif vid_setki == 'Сетка (1-3 место) на 32 участников':
        pass

    if num_game in dict_mesta:
        index = dict_mesta.index(num_game)
        snoska = [0, 0]
        # для отображения в pdf (встречи с минусом)
        game_loser = dict_mesta[index] * -1
        snoska.append(game_loser)
    else:
        game_winner = dict_winner[num_game]  # номер игры победителя
        snoska.append(game_winner)
        game_loser = dict_loser[num_game]  # номер игры проигравшего
        snoska.append(game_loser)
        # для отображения в pdf (встречи с минусом)
        game_loser = dict_loser_pdf[num_game]
        snoska.append(game_loser) # список: номер встречи победителя, номер - проигравшего и куда снести проигравшего
    return snoska


def score_in_setka(fin):
    """ выставляет счет победителя и сносит на свои места в сетке"""
    dict_setka = {}
    match = []
    tmp_match = []
    sys = System.select().where(System.title_id == title_id())
    system = sys.select().where(System.stage == fin).get()
    vid_setki = system.label_string
    # получение id последнего соревнования
    res_t = Result.select().where(Result.title_id == title_id())
    result = res_t.select().where(Result.number_group == fin)  # находит system id последнего
    x = len(result)
    for res in result:
        num_game = int(res.tours)
        family_win = res.winner
        if res.winner is not None and res.winner != "":
            snoska = numer_game(num_game, vid_setki)
            tmp_match.append(snoska[0])
            tmp_match.append(res.winner)
            tmp_match.append(f'{res.score_in_game} {res.score_win}')
            tmp_match.append(snoska[2])
            tmp_match.append(res.loser)
            match = tmp_match.copy()
            tmp_match.clear()
            dict_setka[num_game] = match
    return dict_setka


def result_rank_group(num_gr, player_rank_group):
    """записывает места из группы в таблицу -Choice-, а если одна таблица в финале по кругу то в список
    player_rank_group список списков 1-е число номер игрок в группе, 2-е его место"""
    tab = my_win.tabWidget.currentIndex()
    chc = Choice.select().where(Choice.title_id == title_id())
    if len(player_rank_group) > 0:
        if tab == 3:
            choice = chc.select().where(Choice.group == num_gr)
        elif tab == 4:
            pass
        else:
            if num_gr == "Одна таблица":
                choice = chc.select().where(Choice.basic == "Одна таблица")
            else:
                choice = chc.select().where(Choice.final == num_gr)
        count = len(choice)
        n = 0
        for ch in choice:
            if tab == 3:
                for i in range(0, count):  # цикл по номерам посева в группе
                    # если есть совпадение, то место в списке
                    if ch.posev_group == player_rank_group[i][0]:
                        with db:
                            # записывает в таблицу -Choice- места в группе
                            ch.mesto_group = player_rank_group[i][1]
                            ch.save()
            elif tab == 4:
                pass
            else:
                player_rank_group.sort()
                ch.mesto_final = player_rank_group[n][1]
                player_id = ch.player_choice_id
                ch.save()
                player = Player.get(Player.id == player_id)
                player.mesto = player_rank_group[n][1]
                player.save()
                n += 1


def rank_in_group(total_score, max_person, td, num_gr):
    """выставляет места в группах соответственно очкам -men_of_circle - кол-во человек в крутиловке
    player_rank_group - список списков номер игрока - место -num_player -player_rank - список списков участник - место
    player_group - кол-во участников в группе"""
    tr_all = []
    ps = []
    pps = []
    rev_dict = {}  # словарь, где в качестве ключа очки, а значения - номера групп
    pp = {}  # ключ - игрок, значение его очки
    pg_win = {}
    pg_los = {}
    key_tmp = []
    tr = []
    player_rank_tmp = []
    player_rank = []
    # pl_group = Choice.select().where(Choice.group == num_gr)
    rev_dict = {}  # словарь, где в качестве ключа очки, а значения - номера групп
    player_rank_group = []
    result = Result.select().where(Result.title_id == title_id())
    if num_gr == "Одна таблица":
        game_max = result.select().where(Result.system_stage == num_gr)  # сколько всего игр в группе
    else:
        game_max = result.select().where(Result.number_group == num_gr)  # сколько всего игр в группе
    # 1-й запрос на выборку с группой
    game_played = game_max.select().where(Result.winner is None or Result.winner != "")  # 2-й запрос на выборку
    # с победителями из 1-ого запроса
    kol_tours_played = len(game_played)  # сколько игр сыгранных
    kol_tours_in_group = len(game_max)  # кол-во всего игр в группе

    for key, value in total_score.items():
        rev_dict.setdefault(value, set()).add(key)
    # result = [key for key, values in rev_dict.items() if len(values) > 1]
    res = [key for key, values in rev_dict.items() if len(values) > 1]

    # отдельно составляет список ключей (группы)
    key_list = list(total_score.keys())
    # отдельно составляет список значений (очки)
    val_list = list(total_score.values())
    # ======== новый вариант =========
    # получает словарь(ключ - номер участника, значение - очки)
    ds = {index: value for index, value in enumerate(val_list)}  
    # сортирует словарь по убыванию соот
    sorted_tuple = {k: ds[k] for k in sorted(ds, key=ds.get, reverse=True)}
    # mesto_points = {}  # словарь (ключ-очки, а значения места без учета соотношений)
    valuesList = list(sorted_tuple.values())  # список очков по убыванию
    unique_numbers = list(set(valuesList))  # множество уникальных очков
    unique_numbers.sort(reverse=True)  # список уникальных очков по убыванию
    mesto = 1

    for f in unique_numbers:  # проходим циклом по уник. значениям
        num_player = rev_dict.get(f)
        for x in num_player:
            tr.append(str(x))  # создает список (встречи игроков)
        m_new = valuesList.count(f)  # подсчитываем сколько раз оно встречается

        for k in range(0, max_person):
            if val_list[k] == f:
                key_tmp.append(key_list[k])

        if m_new == 1:  # если кол-во очков у одного спортсмена
            p1 = x
            # записывает место победителю
            td[p1 * 2 - 2][max_person + 4] = mesto
            player_rank_tmp.append([p1, mesto])
        # если кол-во очков у двух спортсмена (определение мест по игре между собой)
        elif m_new == 2:
            player_rank_tmp = circle_2_player(
                tr, td, max_person, mesto, num_gr)
        elif m_new == 3:
            men_of_circle = m_new
            # получает список 1-й уникальные
            u = summa_points_person(men_of_circle, tr, tr_all, pp, pg_win, pg_los, num_gr)
            # значения очков и список значения очков и у скольких спортсменов они есть
            z = u[1]  # список списков кол-во очков и у сколько игроков они есть
            points_person = z[0]
            player_rank_tmp = circle_3_player(points_person, tr, td, max_person, mesto, player_rank_tmp, num_gr, ps,
                                              tr_all, men_of_circle, pg_win, pg_los, pp, pps)
        # если кол-во очков у более трех спортсменов (крутиловка)
        elif m_new > 3:
            m_circle = m_new
            men_of_circle = m_new
            player_rank_tmp = circle(
                men_of_circle, tr, num_gr, td, max_person, mesto, m_circle)
        tr.clear()

        for i in player_rank_tmp:
            player_rank.append(i)
            # список участников в группе и его место
            player_rank_group.append(i)

        mesto = mesto + m_new
        player_rank_tmp.clear()
    if kol_tours_played == kol_tours_in_group:  # когда все встречи сыграны
        # функция простановки мест из группы в -Choice-
        result_rank_group(num_gr, player_rank_group)


def get_unique_numbers(pp_all):
    """получение списка уникальных значений"""
    unique = []
    for number in pp_all:
        if number not in unique:
            unique.append(number)
    return unique


def circle(men_of_circle, tr, num_gr, td, max_person, mesto, m_circle):
    """выставляет места в крутиловке -tour- встречи игроков, p1, p2 фамилии, num_gr номер группы
    -tr- список всех туров (номеров) участников в крутиловке men_of_circle кол-во игроков с одинаковым кол-вом очков,
    max_person общее кол-во игроков в группе player_rank - список (номер игроков и их места)"""
    pl_rank_tmp = []  # список списков (игрок и его место)
    player_rank_tmp = []
    tr_all = []
    ps = []
    pps = []
    rev_dict = {}  # словарь, где в качестве ключа очки, а значения - номера групп
    pp = {}  # ключ - игрок, значение его очки
    pg_win = {}
    pg_los = {}

    # получает список 1-й уникальные
    u = summa_points_person(men_of_circle, tr, tr_all,
                            pp, pg_win, pg_los, num_gr)
    # значения очков и список значения очков и у скольких спортсменов они есть
    unique_numbers = u[0]
    tr.clear()
    sort_tuple = {k: pp[k] for k in sorted(pp, key=pp.get, reverse=True)}
    for key, value in sort_tuple.items():
        rev_dict.setdefault(value, set()).add(key)

    # отдельно составляет список ключей (группы)
    key_list = list(sort_tuple.keys())

    for f in unique_numbers:  # проходим циклом по уник. значениям, очки в крутиловке
        m_new = 0
        num_player = rev_dict.get(f)
        count_point = len(num_player)

        if count_point == 1:
            for x in num_player:
                p1 = x
            # записывает место победителю
            td[p1 * 2 - 2][max_person + 4] = mesto
            td[p1 * 2 - 2][max_person + 3] = f  # записывает место победителю
            player_rank_tmp.append([p1, mesto])
            m_new += 1
        elif count_point == 2:
            for x in num_player:
                tr.append(str(x))  # создает список (встречи игроков)
                m_new += 1
            player_rank_tmp = circle_2_player(
                tr, td, max_person, mesto, num_gr)
        else:
            point = 0
            for x in num_player:
                tr.append(str(x))  # создает список (встречи игроков)
                m_new += 1
            player_rank_tmp = circle_in_circle(m_new, td, max_person, mesto, tr, num_gr, point,
                                               player_rank_tmp, tr_all, pp, pg_win, pg_los, x, pps, ps)
        mesto = mesto + m_new
        tr.clear()

        # заменяет список (места еще не проставлены) на новый с правильными местами
        for i in player_rank_tmp:
            pl_rank_tmp.append(i)
        player_rank_tmp.clear()
    player_rank_tmp = pl_rank_tmp
    return player_rank_tmp


def circle_in_circle(m_new, td, max_person, mesto, tr, num_gr, point, player_rank_tmp,
                     tr_all, pp, pg_win, pg_los, x, pps, ps):
    """крутиловка в крутиловке"""
    if m_new == 1:
        p1 = x
        td[p1 * 2 - 2][max_person + 4] = mesto  # записывает место победителю
        td[p1 * 2 - 2][max_person + 3] = point  # очки во встрече победителя
        player_rank_tmp.append([p1, mesto])
    elif m_new == 2:
        player_rank_tmp = circle_2_player(tr, td, max_person, mesto, num_gr)
    elif m_new == 3:
        men_of_circle = m_new
        # получает список 1-й уникальные
        u = summa_points_person(men_of_circle, tr, tr_all,
                                pp, pg_win, pg_los, num_gr)
        # значения очков и список значения очков и у скольких спортсменов они есть
        z = u[1]
        points_person = z[0]
        player_rank_tmp = circle_3_player(points_person, tr, td, max_person, mesto, player_rank_tmp, num_gr, ps,
                                          tr_all, men_of_circle, pg_win, pg_los, pp, pps)
    tr_all.clear()
    tr.clear()
    return player_rank_tmp


def tour_circle(pp, per_circ, circ):
    tr_new = []
    k_list = list(pp.keys())  # отдельно составляет список ключей (группы)
    v_list = list(pp.values())  # отдельно составляет список значений (очки)
    y = 0
    for s in range(0, circ):
        index = v_list.index(per_circ, y)
        per = str(k_list[index])
        y = index + 1
        tr_new.append(per)
    return tr_new


def summa_points_person(men_of_circle, tr, tr_all, pp, pg_win, pg_los, num_gr):
    """подсчитывает сумму очков у спортсменов в крутиловке"""
    pp_all = []
    u = []
    tr_all.clear()
    pg_win.clear()
    pg_los.clear()
    pp.clear()
    for r in tr:
        r = int(r)
        pp[r] = []  # словарь (игрок - сумма очков)
        pg_win[r] = []
        pg_los[r] = []

    for i in combinations(tr, 2):  # получает список с парами игроков в крутиловке
        i = list(i)
        tr_all.append(i)
    count_game_circle = len(tr_all)

    for n in range(0, count_game_circle):
        tour = "-".join(tr_all[n])  # получает строку встреча в туре
        ki1 = int(tr_all[n][0])  # 1-й игрок в туре
        ki2 = int(tr_all[n][1])  # 2-й игрок в туре

        sum_points_circle(num_gr, tour, ki1, ki2, pg_win, pg_los, pp)  # сумма очков игрока

    for i in tr:  # суммирует очки каждого игрока
        i = int(i)
        s = sum(pp[i])
        pp[i] = s  # словарь (участник - его очки)
        pp_all.append(s)

    list_uniq = []  # список списков сумма очков и кол-во игроков их имеющих
    list_tmp = []
    points_person = get_unique_numbers(pp_all)
    points_person.sort(reverse=True)

    for p in points_person:
        a = pp_all.count(p)
        list_tmp.append(p)
        list_tmp.append(a)
        # список (очки и скольких игроков они встречаются)
        list_uniq.append(list_tmp.copy())
        list_tmp.clear()
    u.append(points_person)
    u.append(list_uniq)
    return u


def circle_2_player(tr, td, max_person, mesto, num_gr):
    """крутиловка из 2-ух человек"""
    player_rank_tmp = []
    tour = "-".join(tr)  # делает строку встреча в туре
    # =====приводит туры к читаемому виду (1-й игрок меньше 2-ого)
    znak = tour.find("-")
    p1 = int(tour[:znak])  # игрок под номером в группе
    p2 = int(tour[znak + 1:])  # игрок под номером в группе
    if p1 > p2:  # меняет последовательность игроков в туре на обратную, чтоб у 1-ого игрока был номер меньше
        p_tmp = p1
        p1 = p2
        p2 = p_tmp
        tour = f"{p1}-{p2}"
    if num_gr != "Одна таблица":
        c = Result.select().where((Result.number_group == num_gr) &
                                  (Result.tours == tour)).get()  # ищет в базе
    # строчку номер группы и тур по двум столбцам
    else:
        c = Result.select().where((Result.system_stage == num_gr) &
                                  (Result.tours == tour)).get()  # ищет в базе
        # строчку номер группы и тур по двум столбцам
    if c.winner == c.player1:
        points_p1 = c.points_win  # очки во встрече победителя
        points_p2 = c.points_loser  # очки во встрече проигравшего
        td[p1 * 2 - 2][max_person + 4] = mesto  # записывает место победителю
        td[p2 * 2 - 2][max_person + 4] = mesto + \
            1  # записывает место проигравшему
        player_rank_tmp.append([p1, mesto])
        player_rank_tmp.append([p2, mesto + 1])
    else:
        points_p1 = c.points_loser
        points_p2 = c.points_win
        td[p1 * 2 - 2][max_person + 4] = mesto + \
            1  # записывает место победителю
        td[p2 * 2 - 2][max_person + 4] = mesto  # записывает место проигравшему
        player_rank_tmp.append([p1, mesto + 1])
        player_rank_tmp.append([p2, mesto])
    td[p1 * 2 - 2][max_person + 3] = points_p1  # очки во встрече победителя
    td[p2 * 2 - 2][max_person + 3] = points_p2  # очки во встрече проигравшего

    return player_rank_tmp


def circle_3_player(points_person, tr, td, max_person, mesto, player_rank_tmp, num_gr, ps, tr_all, men_of_circle,
                    pg_win, pg_los, pp, pps):
    """в крутиловке 3-и спортсмена"""
    if points_person[0] == points_person[1]:  # у всех трех участников равное кол-во очков
        for k in tr:  # суммирует выигранные и проигранные партии каждого игрока
            k = int(k)
            pg_win[k] = sum(pg_win[k])  # сумма выигранных партий
            pg_los[k] = sum(pg_los[k])  # сумма проигранных партий
            x = pg_win[k] / pg_los[k]
            x = float('{:.3f}'.format(x))
            ps.append(x)
            pps.append(pp[k])
        # получает словарь(ключ, номер участника)
        d = {index: value for index, value in enumerate(tr)}
        # получает словарь(ключ, соотношение)
        ds = {index: value for index, value in enumerate(ps)}
        # сортирует словарь по убываню соот
        sorted_tuple = {k: ds[k] for k in sorted(ds, key=ds.get, reverse=True)}
        key_l = list(sorted_tuple.keys())
        val_l = list(sorted_tuple.values())
        vls = set(val_l)  # группирует разные значения
        vl = len(vls)  # подсчитывает их количество
        m = 0
        if vl == 1:  # подсчитывает соотношения выигранных и проигранных мячей в партиях
            plr_ratio = score_in_circle(tr_all, men_of_circle, num_gr, tr)
            sorted_ratio = {k: plr_ratio[k] for k in
                            sorted(plr_ratio, key=plr_ratio.get, reverse=True)}  # сортирует словарь по убыванию соот
            # получает список ключей отсортированного словаря
            key_ratio = list(sorted_ratio.keys())
            r = 0
            for i in key_ratio:
                ratio = sorted_ratio[i]  # соотношение в крутиловке
                person = int(d[i])  # номер игрока
                # записывает соотношение
                td[person * 2 - 2][max_person + 3] = str(ratio)
                td[person * 2 - 2][max_person + 4] = str(mesto + r)  # записывает место
                # добавляет в список группа, место, чтоб занести в таблицу Choice
                player_rank_tmp.append([person, mesto + r])
                r += 1
        else:
            for i in val_l:
                # получает ключ, по которому в списке ищет игрока
                w = key_l[val_l.index(i)]
                # получает номер участника, соответствующий
                wq = int(d.setdefault(w))
                # записывает соотношения игроку
                td[wq * 2 - 2][max_person + 3] = str(i)
                # записывает место
                td[wq * 2 - 2][max_person + 4] = str(m + mesto)
                # добавляет в список группа, место, чтоб занести в таблицу Choice
                player_rank_tmp.append([wq, m + mesto])
                m += 1
    else:   # у трех участников разное кол-во очков
        # получает словарь(ключ, номер участника)
        d = {index: value for index, value in enumerate(tr)}
        # сортирует словарь по убыванию соот
        sorted_tuple = {k: pp[k] for k in sorted(pp, key=pp.get, reverse=True)}
        key_l = list(sorted_tuple.keys())
        val_l = list(sorted_tuple.values())
        m = 0
        for i in val_l:
            q = val_l.index(i)
            wq = int(d.setdefault(q))  # получает номер группы, соответствующий
            # записывает соотношения игроку
            td[wq * 2 - 2][max_person + 3] = str(i)
            td[wq * 2 - 2][max_person + 4] = str(m + mesto)  # записывает место
            # добавляет в список группа, место, чтоб занести в таблицу Choice
            player_rank_tmp.append([wq, m + mesto])
            m += 1
    return player_rank_tmp


def sum_points_circle(num_gr, tour, ki1, ki2, pg_win, pg_los, pp):
    """сумма очков каждого игрока в крутиловке"""
    # # =====приводит туры к читаемому виду (1-й игрок меньше 2-ого)
    znak = tour.find("-")
    p1 = int(tour[:znak])  # игрок под номером в группе
    p2 = int(tour[znak + 1:])  # игрок под номером в группе
    if p1 > p2:  # меняет последовательность игроков в туре на обратную, чтоб у 1-ого игрока был номер меньше
        # уточнить смену тура при p1>p2
        tour = f"{p2}-{p1}"
        ki1 = p2
        ki2 = p1
    result = Result.select().where(Result.title_id == title_id())
    if num_gr == "Одна таблица":
        res = result.select().where(Result.system_stage == num_gr)
    else:
        res = result.select().where(Result.number_group == num_gr)
    c = res.select().where(Result.tours == tour).get()  # ищет в базе  данную встречу
    if c.winner == c.player1:  # победил 1-й игрок
        points_p1 = c.points_win  # очки победителя
        points_p2 = c.points_loser  # очки проигравшего
        # счет во встречи (выигранные и проигранные партии) победителя
        game_p1 = c.score_in_game
        # счет во встречи (выигранные и проигранные партии) проигравшего
        game_p2 = c.score_loser
        if game_p1 != "W : L" or game_p1 != "l : W":
            p1_game_win = int(game_p1[0])
            p1_game_los = int(game_p1[4])
            p2_game_win = int(game_p2[0])
            p2_game_los = int(game_p2[4])
        else:
            p1_game_win = game_p1[0]
            p1_game_los = game_p1[4]
            # p2_game_win = game_p2[0]
            # p2_game_los = game_p2[4]
    else:
        points_p1 = c.points_loser
        points_p2 = c.points_win
        game_p1 = c.score_loser
        game_p2 = c.score_in_game
        # ======= если победа по неявке исправить
        txt = game_p1
        if game_p1 != "W : L" or game_p1 != "l : W":
            p1_game_win = int(game_p1[0])
            p1_game_los = int(game_p1[4])
            p2_game_win = int(game_p2[0])
            p2_game_los = int(game_p2[4])
        else:
            p1_game_win = game_p1[0]
            p1_game_los = game_p1[4]
            # p2_game_win = game_p2[0]
            # p2_game_los = game_p2[4]
    pp[ki1].append(points_p1)  # добавляет очки 1-ому игроку встречи
    pp[ki2].append(points_p2)  # добавляет очки 2-ому игроку встречи
    # записывает в словарь счет во встречи 1-ого игрока
    pg_win[ki1].append(p1_game_win)
    # записывает в словарь счет во встречи 1-ого игрока
    pg_los[ki1].append(p1_game_los)
    # записывает в словарь счет во встречи 2-ого игрока
    pg_win[ki2].append(p2_game_win)
    # записывает в словарь счет во встречи 2-ого игрока
    pg_los[ki2].append(p2_game_los)


def score_in_circle(tr_all, men_of_circle, num_gr, tr):
    """подсчитывает счет по партиям в крутиловке"""
    plr_win = {0: [], 1: [], 2: []}
    plr_los = {0: [], 1: [], 2: []}
    plr_ratio = {0: [], 1: [], 2: []}
    for n in range(0, men_of_circle):
        tour = "-".join(tr_all[n])  # получает строку встреча в туре
        znak = tour.find("-")
        p1 = int(tour[:znak])  # игрок под номером в группе
        p2 = int(tour[znak + 1:])  # игрок под номером в группе
        if p1 > p2:  # меняет последовательность игроков в туре на обратную, чтоб у 1-ого игрока был номер меньше
            tour = f"{p2}-{p1}"
        c = Result.select().where((Result.number_group == num_gr) &
                                  (Result.tours == tour)).get()  # ищет в базе
        k1 = tr_all[n][0]  # 1-й игрок в туре
        k2 = tr_all[n][1]  # 2-й игрок в туре
        ki1 = tr.index(k1)  # получение индекса 1-й игрока
        ki2 = tr.index(k2)
        g = c.score_win
        g_len = len(g)
        g = g[1:g_len - 1]
        sc_game = g.split(",")

        if c.winner == c.player1:  # победил 1-й игрок
            for i in sc_game:
                i = int(i)
                if i < 0:
                    plr_win[ki1].append(abs(i))
                    plr_los[ki2].append(abs(i))
                    if abs(i) < 10:
                        plr_los[ki1].append(11)
                        plr_win[ki2].append(11)
                    else:
                        plr_los[ki1].append(abs(i) + 2)
                        plr_win[ki2].append(abs(i) + 2)
                elif 0 <= i < 10:
                    plr_win[ki1].append(11)
                    plr_los[ki1].append(i)
                    plr_win[ki2].append(i)
                    plr_los[ki2].append(11)
                elif i >= 10:
                    plr_win[ki1].append(i + 2)
                    plr_los[ki1].append(i)
                    plr_win[ki2].append(i)
                    plr_los[ki2].append(i + 2)
        else:  # если победил 2-й игрок
            for i in sc_game:
                i = int(i)
                if i < 0:  # партию проиграл
                    plr_win[ki2].append(abs(i))
                    plr_los[ki1].append(abs(i))
                    if abs(i) < 10:
                        plr_los[ki2].append(11)
                        plr_win[ki1].append(11)
                    else:
                        plr_los[ki2].append(abs(i) + 2)
                        plr_win[ki1].append(abs(i) + 2)
                elif 0 <= i < 10:  # выиграл партию
                    plr_win[ki2].append(11)
                    plr_los[ki2].append(i)
                    plr_win[ki1].append(i)
                    plr_los[ki1].append(11)
                elif i >= 10:  # выиграл партию на больше меньше
                    plr_win[ki2].append(i + 2)
                    plr_los[ki2].append(i)
                    plr_win[ki1].append(i)
                    plr_los[ki1].append(i + 2)
    for n in range(0, men_of_circle):
        plr_win[n] = sum(plr_win[n])
        plr_los[n] = sum(plr_los[n])
        x = plr_win[n] / plr_los[n]
        x = float('{:.3f}'.format(x))
        plr_ratio[n] = x
    return plr_ratio


def player_choice_in_group(num_gr):
    """распределяет спортсменов по группам согласно жеребьевке"""
    posev_data = []
    t_id = title_id()
    choice = Choice.select().where(Choice.title_id == t_id)
    choice_group = choice.select().where(Choice.group == num_gr)
    for posev in choice_group:
        posev_data.append({
            'фамилия': posev.family,
            'регион': posev.region,
        })
    return posev_data


def player_choice_one_table(stage):
    """список спортсменов одной таблицы"""
    posev_data = []
    t_id = title_id()
    if stage == "Одна таблица":
        choice = Choice.select().order_by(Choice.rank.desc()).where(Choice.title_id == t_id and
                                                                    Choice.basic == "Одна таблица")
    else:
        choice = Choice.select().order_by(Choice.posev_final).where(
            Choice.title_id == t_id and Choice.final == stage)
    for posev in choice:
        posev_data.append({
            'фамилия': posev.family,
            'регион': posev.region,
        })
    return posev_data


def player_choice_in_setka(fin):
    """распределяет спортсменов в сетке согласно жеребьевке"""
    p_stage = []

    system = System.select().where(System.title_id == title_id())
    choice = Choice.select().where(Choice.title_id == title_id())  # отбирает все записи жеребьевки данныж соревнований
    # =================
    stage = fin
    flag = ready_choice(stage)
    if flag is False:
        for t in system:
            if t.stage == "Предварительный":
                p_stage.append(t.stage)
            elif t.stage == "Полуфиналы":
                p_stage.append(t.stage)
        count = len(p_stage)
        if count == 2:  # играются еще и полуфиналы
            pre_stage, ok = QInputDialog.getItem(my_win, "Число участников", "Выберите предварительный этап,\n откуда "
                                                 "спортсмены выходят" f"{p_stage} в {fin}")
            if ok:
                pass
        else:  # выходят в финал только из  группового этапа
            kpt, ok = QInputDialog.getInt(my_win, "Места в группе", "Введите место, которoе выходит\n"
                                          f"из группы в {fin}", value=1)
            if ok:
                syst = system.select().where(System.stage == fin).get()
                sys = syst.select().where(System.stage == "Предварительный").get()
                count_exit = system.max_player // sys.total_group
                if count_exit == 1:  # если выходит один человек
                    reply = QMessageBox.information(my_win, 'Уведомление',
                                                    "Из группы выходят спортсмены,\n"
                                                    "занявшие " f"{kpt} место, все верно?",
                                                    QMessageBox.Yes,
                                                    QMessageBox.Cancel)
                elif count_exit == 2: # если выходит два человека
                    reply = QMessageBox.information(my_win, 'Уведомление',
                                                    "Из группы выходят спортсмены,\n"
                                                    "занявшие " f"{kpt} и {kpt + 1} места, все верно?",
                                                    QMessageBox.Yes,
                                                    QMessageBox.Cancel)
                elif count_exit == 3:  # если выходит 4 человека
                    reply = QMessageBox.information(my_win, 'Уведомление',
                                                    "Из группы выходят спортсмены,\n"
                                                    "занявшие " f"{kpt}, {kpt + 1} и {kpt + 2} места, все верно?",
                                                    QMessageBox.Yes,
                                                    QMessageBox.Cancel)
                elif count_exit == 4:  # если выходит 4 человека
                    reply = QMessageBox.information(my_win, 'Уведомление',
                                                    "Из группы выходят спортсмены,\n"
                                                    "занявшие " f"{kpt}, {kpt + 1}, {kpt + 2} и {kpt + 3} места, все верно?",
                                                    QMessageBox.Yes,
                                                    QMessageBox.Cancel)   

                if reply == QMessageBox.Yes:
                    with db:
                        system.stage_exit = "Предварительный"
                        system.mesta_exit = kpt
                        system.save()
                else:
                    return

        mesto_first_poseva = kpt
        mesto_second_poseva = kpt + 1
        mesto_third_poseva = kpt + 2
        mesto_fourth_poseva = kpt + 3

    else:  # если была произведена жеребьевка
        sys = system.select().where(System.stage == fin).get()
        syst = sys.select().where(System.stage == sys.stage_exit).get()

        count_exit = sys.max_player // syst.total_group

        mesto_first_poseva = sys.mesta_exit
        mesto_second_poseva = mesto_first_poseva + 1
        mesto_third_poseva = mesto_first_poseva + 2
        mesto_fourth_poseva = mesto_first_poseva + 3

    # posev_data = choice_setka_automat(count_exit)    

    if count_exit == 1:
        mesto_first_poseva
        choice_first = choice.select().order_by(Choice.group).where(Choice.mesto_group == mesto_first_poseva)  # меств в группе для посева
    elif count_exit == 2:
        choice_first = choice.select().order_by(Choice.group).where(Choice.mesto_group == mesto_first_poseva)  # меств в группе для посева
        choice_second = choice.select().order_by(Choice.group).where(Choice.mesto_group == mesto_second_poseva)
        # first_number = [1, 16, 8, 9, 4, 5, 12, 13]
        # second_number = [10, 3, 11, 7, 14, 15, 2, 6]
        # count_sec_num = len(second_number)
    elif count_exit == 3:
        choice_first = choice.select().order_by(Choice.group).where(Choice.mesto_group == mesto_first_poseva)  # меств в группе для посева
        choice_second = choice.select().order_by(Choice.group).where(Choice.mesto_group == mesto_second_poseva)
        choice_third = choice.select().order_by(Choice.group).where(Choice.mesto_group == mesto_third_poseva)  # меств в группе для посева
    elif count_exit == 4:
        choice_first = choice.select().order_by(Choice.group).where(Choice.mesto_group == mesto_first_poseva)  # меств в группе для посева
        choice_second = choice.select().order_by(Choice.group).where(Choice.mesto_group == mesto_second_poseva)
        choice_third = choice.select().order_by(Choice.group).where(Choice.mesto_group == mesto_third_poseva)  # меств в группе для посева
        choice_fourth = choice.select().order_by(Choice.group).where(Choice.mesto_group == mesto_fourth_poseva)

        posev_data = choice_setka_automat(fin, count_exit, choice_first, choice_second, choice_third, choice_fourth)

    #     first_number = [1, 32, 16, 17, 8, 9, 24, 25]
    #     second_number = [4, 29, 12, 20, 5, 28, 13, 21]
    #     third_number = [3, 30, 11, 19, 6, 27, 14, 22]
    #     fourth_number = [2, 31, 15, 18, 7, 10, 23, 26]

    #     count_sec_num = len(second_number)
    #     count_third_num = len(third_number)
    #     count_fourth_num = len(fourth_number)
    # i = 0
    # for posev in choice_first:
    #     player = Player.get(Player.player == posev.family)
    #     city = player.city
    #     first_posev.append({'посев': first_number[i], 'фамилия': f'{posev.family}/ {city}'})
    #     i += 1
    # if count_exit == 2:
    #     i = 0
    #     for posev in choice_second:
    #         player = Player.get(Player.player == posev.family)
    #         city = player.city
    #         second_posev.append({'посев': second_number[i], 'фамилия': f'{posev.family}/ {city}'})
    #         i += 1
    #     if i != count_sec_num:
    #         no_gamer = second_number[i:]
    #         for m in no_gamer:
    #             second_posev.append({'посев': m, 'фамилия': 'bye'})
    #     posev_data = first_posev + second_posev
    # elif count_exit == 3:
    #     i = 0
    #     for posev in choice_second:
    #         player = Player.get(Player.player == posev.family)
    #         city = player.city
    #         second_posev.append({'посев': second_number[i], 'фамилия': f'{posev.family}/ {city}'})
    #         i += 1
    #     i = 0    
    #     for posev in choice_third:
    #         player = Player.get(Player.player == posev.family)
    #         city = player.city
    #         third_posev.append({'посев': third_number[i], 'фамилия': f'{posev.family}/ {city}'})
    #         i += 1
    #     if i != count_third_num:
    #         no_gamer = third_number[i:]
    #         for m in no_gamer:
    #             third_posev.append({'посев': m, 'фамилия': 'bye'})
    #     posev_data = first_posev + second_posev + third_posev
    # elif count_exit == 4:
    #     i = 0
    #     for posev in choice_second:
    #         player = Player.get(Player.player == posev.family)
    #         city = player.city
    #         second_posev.append({'посев': second_number[i], 'фамилия': f'{posev.family}/ {city}'})
    #         i += 1
    #     i = 0
    #     for posev in choice_third:
    #         player = Player.get(Player.player == posev.family)
    #         city = player.city
    #         third_posev.append({'посев': third_number[i], 'фамилия': f'{posev.family}/ {city}'})
    #         i += 1
    #     i = 0
    #     for posev in choice_fourth:
    #         player = Player.get(Player.player == posev.family)
    #         city = player.city
    #         fourth_posev.append({'посев': fourth_number[i], 'фамилия': f'{posev.family}/ {city}'})
    #         i += 1
    #     if i != count_fourth_num:
    #         no_gamer = fourth_number[i:]
    #         for m in no_gamer:
    #             fourth_posev.append({'посев': m, 'фамилия': 'bye'})
    #     posev_data = first_posev + second_posev + third_posev + fourth_posev

    # сортировка (списка словарей) по ключу словаря -посев-
    posev_data = sorted(posev_data, key=lambda i: i['посев'])
    with db:  # записывает в db, что жеребьевка произведена
        sys.choice_flag = True
        sys.save()
    return posev_data


def change_choice_group():
    """Смена жеребьевки групп если в группе 2 и более одинаковых регион чтоб развести тренеров"""
    msg = QMessageBox
    sender = my_win.sender()
    if my_win.radioButton_4.isChecked():
        reg = []
        reg_d = []
        gr_key = []
        reg_tmp = []
        double_reg = {}
        fg = my_win.comboBox_filter_choice.currentText()
        choice = Choice.select().where(Choice.title_id == title_id())
        system = System.select().where(System.title_id == title_id())
        sys = system.select().where(System.stage == "Предварительный").get()
        total_gr = sys.total_group
        for i in range(1, total_gr + 1):
            m = 0
            group = choice.select().where(Choice.group == f"{i} группа")
            for k in group:
                m += 1
                reg_n = k.region
                if reg_n not in reg:
                    reg.append(reg_n)
                else:
                    reg_tmp.append(reg_n)
            reg_d = reg_tmp.copy()
            count =len(reg_d)
            if count > 0:
                double_reg[f"{i} группа"] = reg_d
            reg_tmp.clear()
            reg.clear()
        dr_count = len(double_reg)
        if dr_count != 0:
            for key in double_reg.keys():
                gr_key.append(key)     
            my_win.comboBox_filter_choice.clear()
            my_win.comboBox_filter_choice.addItems(gr_key)
        else:
            msg.information(my_win, "Уведомление", "Нет групп с повторяющимися регионами.")
    else:
        return


def change_page_vid():
    """Смена вида страницы с таблицами""" 
    msgBox = QMessageBox
    sys = []
    sys.append("")
    system = System.select().where(System.title_id == title_id()) 
    for i in system:
        stage = i.stage
        sys.append(stage)
    stage, ok = QInputDialog.getItem(my_win, "Таблицы", "Выберите таблицы из списка для\n"
                                        "смены ориентации страницы", sys)
    if ok:                                   
        sys = system.select().where(System.stage == stage).get()
        vid = sys.page_vid
        vid_ed = "альбомная"
        if vid == "альбомная":
            vid_ed = "книжная"
        else:
            vid_ed = "альбомная"
        ok = msgBox.question(my_win, "Таблицы", "Текущая ориентация страницы\n"
                                            f"-{stage}-: {vid},\n"
                                            "Хотите ее изменить на:" f"{vid_ed}?", msgBox.Ok, msgBox.Cancel)
        if ok:
            sys.page_vid = vid_ed
            sys.save()
        else:
            return
    else:
        return


def change_dir():
    """смена директории, чтоб все pdf фалы сохранялися в папке table_pdf"""
    dir_path = pathlib.Path.cwd()
    p = str(dir_path)
    f = p.rfind("table_pdf")
    if f == -1:
        os.chdir("table_pdf")
    else:
        os.chdir(dir_path.parent)
  

def draw_setka(col, row, num, style):
    """рисование сетки встреч игроков
    col - начальный столбец, row - начальный ряд, num - кол-во игроков"""
    style_set = [] 
    # style = []   
    s = 1
    cf = 0  # кол-во туров
    if num == 2:  # кол-во игроков
        cf = 1
    elif num == 4:
        cf = 2
    elif num == 8:
        cf = 3
    elif num == 16:
        cf = 4
    elif num == 32:
        cf = 5
    row_b = row
    col_fin = col + cf * 2 # последний столбец
    row_fin = row + num * 2 - 1 # последняя строка 
    for i in range (col, col_fin, 2): # номер столбца 
        s *= 2
        for k in range(row, row_fin, s): # номер строки
            fn = ('LINEABOVE', (i, k), (i + 1, k), 1, colors.darkblue)  # рисует линии встреч
            style_set.append(fn)  
        row = row + s // 2
    s = 1
    for m in range(col + 1, col_fin + 1, 2):
        s *= 2
        for q in range(row_b, row_fin, s * 2):  # встречи 33-34
            fn = ('SPAN', (m, q), (m, q + s - 1 ))             
            style_set.append(fn)
            fn = ('BACKGROUND', (m, q), (m, q + s - 1 ), colors.lightyellow)  
            style_set.append(fn) 
            fn = ('BOX', (m, q), (m, q + s - 1), 1, colors.darkblue)
            style_set.append(fn)
        row_b = row_b + s // 2   
    for fn in style_set:
        style.append(fn)
    return style


def draw_setka_2(col, row, num, style):
    """рисование сетки встреч игроков
    col - начальный столбец, row - начальный ряд, num - кол-во игроков"""
    style_set = []  
    s = 1
    cf = 0  # кол-во туров
    if num == 2:  # кол-во игроков
        cf = 1
    elif num == 4:
        cf = 2
    elif num == 8:
        cf = 3
    elif num == 16:
        cf = 5
    
    row_b = row
    col_fin = col + cf * 2 # последний столбец
    row_fin = row + num * 2 - 1 # последняя строка 
    for i in range (col, col_fin, 2): # номер столбца 
        s *= 2
        for k in range(row, row_fin, s): # номер строки
            fn = ('LINEABOVE', (i, k), (i + 1, k), 1, colors.darkblue)  # рисует линии встреч
            style_set.append(fn)  
        if i == 1:
            row -= 1
            s = 1
        elif i == 3:
            row += 1
            s = 2
        elif i == 5:
            row -= 2
            row_fin -= 1
            s = 2
        elif i == 7:
            row += 2
            s = 4
 
    s = 1
    row_fin = row_b + num * 2 - 2 # последняя строка 
    for m in range(col + 1, col_fin + 1, 2):
        s *= 2
        for q in range(row_b, row_fin, s * 2):  # встречи 33-34
            fn = ('SPAN', (m, q), (m, q + s - 1 ))             
            style_set.append(fn)
            fn = ('BACKGROUND', (m, q), (m, q + s - 1 ), colors.lightyellow)  
            style_set.append(fn) 
            fn = ('BOX', (m, q), (m, q + s - 1), 1, colors.darkblue)
            style_set.append(fn)
        if m == 2:
            row_b -= 1
            s = 1
        elif m == 4:
            row_b += 1
            s = 2
        elif m == 6:
            row_b -= 2
            s = 2
        elif m == 8:
            row_b += 2
            s = 4

    for fn in style_set:
        style.append(fn)
    return style


def draw_mesta(row, col, player, style):
    """рисует линии встреч за место"""
    p = 0
    if player == 2:
        p = 4
    elif player == 4:
        p = 4
    elif player == 8:
        p = 6
    elif player == 16:
        p = 10

    col_f = 11

    if col == 9:
        col_f = col + 2
    else:
        col_f = col + 1

    for l in range(row, row + p + 1, p):
        fn = ('LINEABOVE', (col, l), (col_f, l), 1, colors.darkblue)  # рисует линии мест 5-6 места (4 чел)
        style.append(fn)
    return style


def draw_num(row_n, row_step, col_n, number_of_columns, number_of_game, player, data):
    """рисует номера встреч, row_n - начальный ряд, col_n - начальный столбец, 
    number_of_game - начальный номер встречи, player - кол-во участников, number_of_columns - кол-во столбцов """
    s = 1
    col_f = col_n + number_of_columns * 2 - 1
    row_f = row_n + (player * 2 - 1)
    for k in range(col_n, col_f, 2):
        step = row_step * 2
        for i in range (row_n, row_f, step):
            data[i][k] = str(number_of_game)
            number_of_game += 1
        row_step *= 2
        s *= 2
        row_n = row_n + s // 2
    return number_of_game


def draw_num_2(row_n, row_step, col_n, number_of_columns, number_of_game, data, player):
    """рисует номера встреч, row_n - начальный ряд, col_n - начальный столбец, 
    number_of_game - начальный номер встречи, player - кол-во участников, 
    number_of_columns - число столбцов"""
  
    col_f = col_n + number_of_columns * 2 - 1
    row_f = row_n + (player * 2 - 1)
    for k in range(col_n, col_f, 2): 
        for i in range (row_n, row_f, row_step * 2):
            data[i][k] = str(number_of_game)
            number_of_game += 1
        
        row_n -= int(row_step / 2)
        row_f -= int(row_step / 2)

    return number_of_game


def draw_num_lost(row_n, row_step, col_n, number_of_game, player, data):
    """нумерация встреч проигранных"""
    row_f = row_n + (player - 1) * 2 + 1
    for d in range(row_n, row_f, row_step):
            data[d - 1][col_n] = str(number_of_game * -1)
            number_of_game += 1


def draw_num_lost_2(row_n, row_step, col_n, revers_number, number_of_game, player, data):
    """нумерация встреч проигранных"""
    if revers_number == 0:
        row_n = row_n
        row_f = row_n + (player - 1) * row_step * 2 + 1
        step = row_step * 2
    else:
        row_n = row_n + (player - 1) * row_step * 2
        row_f = row_n - (player - 1) * row_step * 2 - 1
        step = row_step * 2 * -1

    for d in range(row_n, row_f, step):
            data[d][col_n] = str(number_of_game * -1)
            number_of_game += 1


def color_mesta(data, first_mesto, table):
    """окрашивает места в красный цвет"""
    b = 0
    style_color = []
    ml = []
    f = 0
    if table == "setka_32":
        f = 2
    elif table == "setka_32_full":
        f = 13
    elif table == "setka_32_2":
        f = 16
    elif table == "setka_16_full":
        f = 8

    for c in range(0, f):
        if c == 0: # 1-2 место
            if table == "setka_32_2":
                ml = [13, 31, 54, 22] 
            elif table == "setka_16_full":
                ml = [10, 15, 26, 10] 
            else:
                ml = [11, 31, 54, 22] 
        elif c == 1: # 3-4 место
            if table == "setka_32_2":
                ml = [13, 80, 97, 16]  
            elif table == "setka_16_full":
                ml = [10, 29, 32, 2] 
            else:                
                ml = [11, 59, 65, 5] 
        elif c == 2: # 5-6 место
            if table == "setka_32_2":
                ml = [13, 101, 106, 4]  
            elif table == "setka_16_full":
                ml = [10, 34, 38, 3] 
            else:
                ml = [11, 72, 92, 5]
        elif c == 3: # 7-8 место
            if table == "setka_32_2":
                ml = [13, 109, 114, 4]  
            elif table == "setka_16_full":
                ml = [10, 39, 42, 2] 
            else:
                ml = [11, 94, 95, 1]
        elif c == 4: # 9-10 место
            if table == "setka_32_2":
                ml = [5, 113, 118, 4]  
            elif table == "setka_16_full":
                ml = [10, 47, 53, 5] 
            else:
                ml = [11, 99, 133, 5]
        elif c == 5: # 11-12 место
            if table == "setka_32_2":
                ml = [11, 119, 124, 4]  
            elif table == "setka_16_full":
                ml = [10, 55, 58, 2] 
            else:
                ml = [11, 152, 163, 10]
        elif c == 6: # 13-14 место
            if table == "setka_32_2":
                ml = [5, 125, 130, 4]  
            elif table == "setka_16_full":
                ml = [10, 60, 64, 3] 
            else:
                ml = [11, 167, 172, 4]
        elif c == 7: # 15-16 место
            if table == "setka_32_2":
                ml = [11, 127, 132, 4] 
            elif table == "setka_16_full":
                ml = [10, 65, 68, 2] 
            else:
                ml = [9, 173, 178, 4]
        elif c == 8: # 17-18 место
            if table == "setka_32_2":
                ml = [7, 145, 153, 7]  
            else:
                ml = [11, 180, 186, 5]
        elif c == 9: # 19-20 место
            if table == "setka_32_2":
                ml = [11, 154, 160, 5]  
            else:
                ml = [7, 184, 191, 6]
        elif c == 10: # 21-22 место
            if table == "setka_32_2":
                ml = [7, 161, 166, 4]  
            else:
                ml = [11, 192, 198, 5]
        elif c == 11: # 23-24 место
            if table == "setka_32_2":
                ml = [11, 169, 175, 5]  
            else:
                ml = [5, 198, 203, 4]
        elif c == 12: # 25-26 место
            if table == "setka_32_2":
                ml = [7, 175, 183, 7] 
            else:
                ml = [11, 200, 205, 4]
        elif c == 13: # 27-28 место
            ml = [11, 184, 190, 5]  
        elif c == 14: # 29-30 место 
            ml = [7, 193, 198, 4] 
        elif c == 15: # 31-32 место
            ml = [11, 199, 205, 5]
            
        for i in range(ml[1], ml[2], ml[3]):

            data[i][ml[0]] = str(first_mesto + b) + " Место"
            fn = (('TEXTCOLOR', (ml[0], i), (ml[0], i), colors.red))
            style_color.append(fn)
            fn =  ('ALIGN', (ml[0], i), (ml[0], i), 'CENTER')
            style_color.append(fn)
            b += 1    
    return style_color   


def last_competition():
    """заполняе меню -последние- прошедшими соревнованиями 5 штук"""
    title = Title.select().order_by(Title.data_start.desc())
    i = 0
    for t in title:
        full_name = t.full_name_comp
        if i > 5:
            break
        if i == 0: 
            if full_name != "":
                my_win.first_comp_Action.setText(full_name)
            else:
                my_win.first_comp_Action.setText("Пусто")
        elif i == 1: 
            if full_name != "":
                my_win.second_comp_Action.setText(full_name)
            else:
                my_win.second_comp_Action.setText("Пусто")
        elif i == 2: 
            if full_name != "":
                my_win.third_comp_Action.setText(full_name)
            else:
                my_win.third_comp_Action.setText("Пусто")
        elif i == 3: 
            if full_name != "":
                my_win.fourth_comp_Action.setText(full_name)
            else:
                my_win.fourth_comp_Action.setText("Пусто")
        elif i == 4: 
            if full_name != "":
                my_win.fifth_comp_Action.setText(full_name)
            else:
                my_win.fifth_comp_Action.setText("Пусто")
        i += 1
    # go_to()


def tours_list(cp):
    """туры таблиц по кругу в зависимости от кол-во участников (-cp- + 3) кол-во участников"""
    tour_list = []
    tr = [[['1-3'], ['1-2'], ['2-3']],
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
          [['1-11', '2-10', '3-9', '4-8', '5-7'], ['6-11', '1-10', '2-9', '3-8', '4-7'], ['5-11', '6-10', '1-9', '2-8', '3-7'],
            ['4-11', '5-10', '6-9', '1-8', '2-7'], ['3-11', '4-10', '5-9', '6-8', '1-7'], ['2-11', '3-10', '4-9', '5-8', '6-7'],
            ['2-4', '1-5', '3-6', '7-10', '9-11'], ['1-4', '2-6', '3-5', '8-10', '7-11'], ['1-3', '2-5', '4-6', '7-9', '8-11'],
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
          ['6-13', '7-12', '1-11', '2-10', '3-9', '4-8', '5-14'], ['5-13',
                                                                   '6-12', '7-11', '1-10', '2-9', '3-8', '4-14'],
          ['4-13', '5-12', '6-11', '7-10', '1-9', '2-8', '3-14'], ['3-13',
                                                                   '4-12', '5-11', '6-10', '7-9', '1-8', '2-14'],
          ['1-7', '2-6', '3-5', '4-11', '9-13', '10-12', '8-14'], ['1-6',
                                                                   '2-5', '4-7', '3-12', '8-11', '10-13', '9-14'],
          ['1-4', '2-7', '3-6', '5-10', '8-13', '9-12', '11-14'], ['1-5',
                                                                   '3-7', '4-6', '2-13', '8-12', '9-11', '10-14'],
          ['1-3', '2-4', '5-7', '6-9', '8-10', '11-13', '12-14'], ['2-3',
                                                                   '4-5', '6-7', '8-9', '10-11', '12-13', '1-14'],
          ['1-2', '3-4', '5-6', '7-8', '9-10', '11-12', '13-14']],
          [['1-15', '2-14', '3-13', '4-12', '5-11', '6-10', '7-9'], ['8-15', '1-14', '2-13', '3-12', '4-11', '5-10', '6-9'],
          ['8-15', '1-14', '2-13', '3-12', '4-11', '5-10', '6-9'], ['7-15',
                                                                    '8-14', '1-13', '2-12', '3-11', '4-10', '5-9'],
          ['6-15', '7-14', '8-13', '1-12', '2-11', '3-10', '4-9'], ['5-15',
                                                                    '6-14', '7-13', '8-12', '1-11', '2-10', '3-9'],
          ['4-15', '5-14', '6-13', '7-12', '8-11', '1-10', '2-9'], ['3-15',
                                                                    '4-14', '5-13', '6-12', '7-11', '8-10', '1-9'],
          ['2-15', '3-14', '4-13', '5-12', '6-11', '7-10', '8-9'], ['1-7',
                                                                    '2-6', '3-5', '4-8', '9-13', '12-14', '11-15'],
          ['1-6', '2-5', '3-8', '4-7', '9-14', '10-13', '12-15'], ['1-5',
                                                                   '2-8', '3-7', '4-6', '9-15', '10-14', '11-13'],
          ['1-4', '2-7', '3-6', '5-8', '9-12', '10-15', '11-14'], ['1-3',
                                                                   '2-4', '5-7', '6-8', '9-11', '10-12', '13-15'],
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


# def open_close_fail(view_file):
# # Введите имя файла для проверки
#     # filename = input("Введите любое существующее имя файла:\n")
# # Откройте файл в первый раз с помощью функции open()
#     # fileHandler = open(view_file, "r")
#     view(view_file)
# # Попробуйте открыть файл с таким же именем снова
#     try:
#         with open("view_file") as file:

#             print("Файл открыт для чтения.")
# # Вызовите ошибку, если файл был открыт раньше
#     except IOError:
#         print("Файл уже открыт")


# def proba():
#     """добавление столбца в существующую таблицу"""
#
#     my_db = SqliteDatabase('comp_db.db')
#     migrator = SqliteMigrator(my_db)
#     short_name_comp = CharField(default='')
#     # mesta_exit = IntegerField(null=True)  # новый столбец, его поле и значение по умолчанию
# #
#     with db:
#         # migrate(migrator.drop_not_null('system', 'mesta_exit'))
#         # migrate(migrator.alter_column_type('system', 'mesta_exit', IntegerField()))
#         # migrate(migrator.rename_column('system', 'stage_final', 'stage_exit'))
#         migrate(migrator.add_column('titles', 'short_name_comp', short_name_comp))

    # ========================= создание таблицы
    # with db:
    #     Game_list.create_table()
    # ========================
    # System.create_table()
    # sys = System(title_id=t, total_athletes=0, total_group=0, max_player=0, stage="", page_vid="", label_string="",
    #              kol_game_string="", choice_flag=False, score_flag=5, visible_game=False).save()

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
# двойной клик по listWidget (рейтинг, тренеры)
my_win.listWidget.itemDoubleClicked.connect(dclick_in_listwidget)
# двойной клик по строке игроков в таблице -результаты-
my_win.tableWidget.doubleClicked.connect(select_player_in_game)

my_win.tabWidget.currentChanged.connect(tab)
my_win.toolBox.currentChanged.connect(page)
# ==================================
my_win.spinBox_kol_group.textChanged.connect(kol_player_in_group)
# ======== изменение индекса комбобоксов ===========

fir_window.comboBox.currentTextChanged.connect(change_sroki)
my_win.comboBox_one_table.currentTextChanged.connect(kol_player_in_final)
my_win.comboBox_table.currentTextChanged.connect(kol_player_in_final)
my_win.comboBox_table_2.currentTextChanged.connect(kol_player_in_final)
my_win.comboBox_table_3.currentTextChanged.connect(kol_player_in_final)
my_win.comboBox_table_4.currentTextChanged.connect(kol_player_in_final)
my_win.comboBox_etap_1.currentTextChanged.connect(system_competition)
my_win.comboBox_etap_2.currentTextChanged.connect(system_competition)
my_win.comboBox_etap_3.currentTextChanged.connect(system_competition)
my_win.comboBox_etap_4.currentTextChanged.connect(system_competition)
my_win.comboBox_etap_5.currentTextChanged.connect(system_competition)
my_win.comboBox_page_vid.currentTextChanged.connect(page_vid)
my_win.comboBox_filter_final.currentTextChanged.connect(game_in_visible)
my_win.comboBox_filter_choice.currentTextChanged.connect(choice_filter_group)


# =======  отслеживание переключение чекбоксов =========
my_win.radioButton_3.toggled.connect(load_combobox_filter_group)

my_win.radioButton_match_3.toggled.connect(match_score_db)
my_win.radioButton_match_5.toggled.connect(match_score_db)
my_win.radioButton_match_7.toggled.connect(match_score_db)
my_win.radioButton_4.toggled.connect(change_choice_group)


# при изменении чекбокса активирует кнопку создать
my_win.checkBox.stateChanged.connect(button_title_made_enable)
# my_win.checkBox_2.stateChanged.connect(button_etap_made_enabled)  # при изменении чекбокса активирует кнопку создать
# при изменении чекбокса активирует кнопку создать
my_win.checkBox_3.stateChanged.connect(button_system_made_enable)
# при изменении чекбокса показывает поля для ввода счета
my_win.checkBox_4.stateChanged.connect(game_in_visible)
# при изменении чекбокса показывает поля для ввода счета финала
my_win.checkBox_5.stateChanged.connect(game_in_visible)
# при изменении чекбокса показывает список удаленных игроков
my_win.checkBox_6.stateChanged.connect(del_player_table)
my_win.checkBox_7.stateChanged.connect(no_play)  # поражение по неявке
my_win.checkBox_8.stateChanged.connect(no_play)  # поражение по неявке
my_win.checkBox_9.stateChanged.connect(no_play)  # поражение по неявке
my_win.checkBox_10.stateChanged.connect(no_play)  # поражение по неявке
# =======  нажатие кнопок =========


my_win.Button_Ok.setAutoDefault(True)  # click on <Enter>
my_win.Button_Ok_fin.setAutoDefault(True)  # click on <Enter>
my_win.Button_clear_del.clicked.connect(clear_del_player)
my_win.Button_reset_filter.clicked.connect(reset_filter)
my_win.Button_reset_filter_fin.clicked.connect(reset_filter)
my_win.Button_filter_fin.clicked.connect(filter_fin)
my_win.Button_filter.clicked.connect(filter_gr)
# рисует таблицы группового этапа и заполняет game_list
my_win.Button_etap_made.clicked.connect(etap_made)
# my_win.Button_system_made.clicked.connect(player_in_table)  # заполнение таблицы Game_list
my_win.Button_add_edit_player.clicked.connect(add_player)  # добавляет игроков в список и базу
my_win.Button_group.clicked.connect(player_in_table)  # вносит спортсменов в группы
# записывает в базу или редактирует титул
my_win.Button_title_made.clicked.connect(title_made)
# записывает в базу счет в партии встречи
my_win.Button_Ok.clicked.connect(enter_score)
# записывает в базу счет в партии встречи
my_win.Button_Ok_fin.clicked.connect(enter_score)
my_win.Button_del_player.clicked.connect(delete_player)

# my_win.Button_proba.clicked.connect(test_choice_group)

my_win.Button_sort_mesto.clicked.connect(sort)
my_win.Button_sort_R.clicked.connect(sort)
my_win.Button_sort_Name.clicked.connect(sort)


sys.exit(app.exec())
