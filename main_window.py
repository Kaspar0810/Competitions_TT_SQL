# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt6 UI code generator 6.0.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1347, 754)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame_main = QtWidgets.QFrame(self.centralwidget)
        self.frame_main.setGeometry(QtCore.QRect(10, 570, 171, 131))
        self.frame_main.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_main.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_main.setObjectName("frame_main")
        self.pushButton_view = QtWidgets.QPushButton(self.frame_main)
        self.pushButton_view.setGeometry(QtCore.QRect(10, 70, 150, 30))
        self.pushButton_view.setObjectName("pushButton_view")
        self.pushButton_db = QtWidgets.QPushButton(self.frame_main)
        self.pushButton_db.setGeometry(QtCore.QRect(10, 40, 150, 30))
        self.pushButton_db.setObjectName("pushButton_db")
        self.pushButton_export = QtWidgets.QPushButton(self.frame_main)
        self.pushButton_export.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.pushButton_export.setObjectName("pushButton_export")
        self.pushButton_Rlist = QtWidgets.QPushButton(self.frame_main)
        self.pushButton_Rlist.setGeometry(QtCore.QRect(10, 100, 150, 30))
        self.pushButton_Rlist.setObjectName("pushButton_Rlist")
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setGeometry(QtCore.QRect(190, 250, 821, 451))
        self.frame_3.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")
        self.toolBox = QtWidgets.QToolBox(self.centralwidget)
        self.toolBox.setGeometry(QtCore.QRect(10, 0, 171, 421))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setItalic(True)
        self.toolBox.setFont(font)
        self.toolBox.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.toolBox.setObjectName("toolBox")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 169, 215))
        self.page.setObjectName("page")
        self.pushButton_titul_made = QtWidgets.QPushButton(self.page)
        self.pushButton_titul_made.setGeometry(QtCore.QRect(10, 0, 150, 30))
        self.pushButton_titul_made.setAutoDefault(False)
        self.pushButton_titul_made.setDefault(True)
        self.pushButton_titul_made.setFlat(False)
        self.pushButton_titul_made.setObjectName("pushButton_titul_made")
        self.pushButton_titul_edit = QtWidgets.QPushButton(self.page)
        self.pushButton_titul_edit.setGeometry(QtCore.QRect(10, 30, 150, 30))
        self.pushButton_titul_edit.setObjectName("pushButton_titul_edit")
        self.toolBox.addItem(self.page, "")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 169, 215))
        self.page_2.setObjectName("page_2")
        self.pushButton_add_player = QtWidgets.QPushButton(self.page_2)
        self.pushButton_add_player.setGeometry(QtCore.QRect(10, 0, 151, 32))
        self.pushButton_add_player.setObjectName("pushButton_add_player")
        self.groupBox = QtWidgets.QGroupBox(self.page_2)
        self.groupBox.setGeometry(QtCore.QRect(10, 130, 151, 91))
        self.groupBox.setObjectName("groupBox")
        self.pushButton_sort_R = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_sort_R.setGeometry(QtCore.QRect(0, 60, 151, 32))
        self.pushButton_sort_R.setObjectName("pushButton_sort_R")
        self.pushButton_sort_Name = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_sort_Name.setGeometry(QtCore.QRect(0, 30, 151, 32))
        self.pushButton_sort_Name.setObjectName("pushButton_sort_Name")
        self.toolBox.addItem(self.page_2, "")
        self.page_6 = QtWidgets.QWidget()
        self.page_6.setGeometry(QtCore.QRect(0, 0, 169, 215))
        self.page_6.setObjectName("page_6")
        self.toolBox.addItem(self.page_6, "")
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setGeometry(QtCore.QRect(0, 0, 169, 215))
        self.page_3.setObjectName("page_3")
        self.toolBox.addItem(self.page_3, "")
        self.page_5 = QtWidgets.QWidget()
        self.page_5.setGeometry(QtCore.QRect(0, 0, 169, 215))
        self.page_5.setObjectName("page_5")
        self.toolBox.addItem(self.page_5, "")
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setGeometry(QtCore.QRect(0, 0, 169, 215))
        self.page_4.setObjectName("page_4")
        self.toolBox.addItem(self.page_4, "")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(190, 0, 821, 241))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setItalic(True)
        self.tabWidget.setFont(font)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.TabPosition.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.tabWidget.setElideMode(QtCore.Qt.TextElideMode.ElideLeft)
        self.tabWidget.setMovable(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label_nazvanie = QtWidgets.QLabel(self.tab)
        self.label_nazvanie.setGeometry(QtCore.QRect(180, 10, 211, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setItalic(True)
        self.label_nazvanie.setFont(font)
        self.label_nazvanie.setObjectName("label_nazvanie")
        self.lineEdit_titul_nazvanie = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_titul_nazvanie.setGeometry(QtCore.QRect(20, 30, 621, 21))
        self.lineEdit_titul_nazvanie.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.lineEdit_titul_nazvanie.setObjectName("lineEdit_titul_nazvanie")
        self.comboBox_sredi = QtWidgets.QComboBox(self.tab)
        self.comboBox_sredi.setGeometry(QtCore.QRect(120, 70, 201, 26))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setItalic(True)
        self.comboBox_sredi.setFont(font)
        self.comboBox_sredi.setObjectName("comboBox_sredi")
        self.lineEdit_titul_vozrast = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_titul_vozrast.setGeometry(QtCore.QRect(330, 70, 311, 21))
        self.lineEdit_titul_vozrast.setObjectName("lineEdit_titul_vozrast")
        self.label_sredi = QtWidgets.QLabel(self.tab)
        self.label_sredi.setGeometry(QtCore.QRect(50, 70, 60, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setItalic(True)
        self.label_sredi.setFont(font)
        self.label_sredi.setAlignment(QtCore.Qt.Alignment.AlignRight|QtCore.Qt.Alignment.AlignTop|QtCore.Qt.Alignment.AlignTrailing)
        self.label_sredi.setObjectName("label_sredi")
        self.label_data_provedenia = QtWidgets.QLabel(self.tab)
        self.label_data_provedenia.setGeometry(QtCore.QRect(140, 100, 161, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setItalic(True)
        self.label_data_provedenia.setFont(font)
        self.label_data_provedenia.setAlignment(QtCore.Qt.Alignment.AlignCenter)
        self.label_data_provedenia.setObjectName("label_data_provedenia")
        self.label_2str_4 = QtWidgets.QLabel(self.tab)
        self.label_2str_4.setGeometry(QtCore.QRect(470, 100, 161, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setItalic(True)
        self.label_2str_4.setFont(font)
        self.label_2str_4.setAlignment(QtCore.Qt.Alignment.AlignCenter)
        self.label_2str_4.setObjectName("label_2str_4")
        self.lineEdit_city_titul = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_city_titul.setGeometry(QtCore.QRect(470, 120, 171, 21))
        self.lineEdit_city_titul.setObjectName("lineEdit_city_titul")
        self.label_city = QtWidgets.QLabel(self.tab)
        self.label_city.setGeometry(QtCore.QRect(390, 120, 60, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setItalic(True)
        self.label_city.setFont(font)
        self.label_city.setAlignment(QtCore.Qt.Alignment.AlignRight|QtCore.Qt.Alignment.AlignTop|QtCore.Qt.Alignment.AlignTrailing)
        self.label_city.setObjectName("label_city")
        self.label_kat_sek = QtWidgets.QLabel(self.tab)
        self.label_kat_sek.setGeometry(QtCore.QRect(510, 150, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setItalic(True)
        self.label_kat_sek.setFont(font)
        self.label_kat_sek.setAlignment(QtCore.Qt.Alignment.AlignCenter)
        self.label_kat_sek.setObjectName("label_kat_sek")
        self.comboBox_kategor_sek = QtWidgets.QComboBox(self.tab)
        self.comboBox_kategor_sek.setGeometry(QtCore.QRect(550, 170, 91, 26))
        self.comboBox_kategor_sek.setObjectName("comboBox_kategor_sek")
        self.label_main_sekretar = QtWidgets.QLabel(self.tab)
        self.label_main_sekretar.setGeometry(QtCore.QRect(310, 150, 191, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setItalic(True)
        self.label_main_sekretar.setFont(font)
        self.label_main_sekretar.setAlignment(QtCore.Qt.Alignment.AlignCenter)
        self.label_main_sekretar.setObjectName("label_main_sekretar")
        self.lineEdit_sekretar = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_sekretar.setGeometry(QtCore.QRect(330, 170, 211, 21))
        self.lineEdit_sekretar.setObjectName("lineEdit_sekretar")
        self.dateEdit_end = QtWidgets.QDateEdit(self.tab)
        self.dateEdit_end.setGeometry(QtCore.QRect(220, 120, 121, 24))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.dateEdit_end.setFont(font)
        self.dateEdit_end.setDateTime(QtCore.QDateTime(QtCore.QDate(2021, 1, 1), QtCore.QTime(0, 0, 0)))
        self.dateEdit_end.setCurrentSection(QtWidgets.QDateTimeEdit.Sections.YearSection)
        self.dateEdit_end.setCalendarPopup(True)
        self.dateEdit_end.setCurrentSectionIndex(0)
        self.dateEdit_end.setDate(QtCore.QDate(2021, 1, 1))
        self.dateEdit_end.setObjectName("dateEdit_end")
        self.label_po = QtWidgets.QLabel(self.tab)
        self.label_po.setGeometry(QtCore.QRect(180, 120, 31, 20))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setItalic(True)
        self.label_po.setFont(font)
        self.label_po.setAlignment(QtCore.Qt.Alignment.AlignRight|QtCore.Qt.Alignment.AlignTop|QtCore.Qt.Alignment.AlignTrailing)
        self.label_po.setObjectName("label_po")
        self.dateEdit_start = QtWidgets.QDateEdit(self.tab)
        self.dateEdit_start.setGeometry(QtCore.QRect(50, 120, 121, 24))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.dateEdit_start.setFont(font)
        self.dateEdit_start.setDateTime(QtCore.QDateTime(QtCore.QDate(2021, 1, 2), QtCore.QTime(0, 0, 0)))
        self.dateEdit_start.setCalendarPopup(True)
        self.dateEdit_start.setDate(QtCore.QDate(2021, 1, 2))
        self.dateEdit_start.setObjectName("dateEdit_start")
        self.label_s = QtWidgets.QLabel(self.tab)
        self.label_s.setGeometry(QtCore.QRect(0, 120, 31, 20))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setItalic(True)
        self.label_s.setFont(font)
        self.label_s.setAlignment(QtCore.Qt.Alignment.AlignRight|QtCore.Qt.Alignment.AlignTop|QtCore.Qt.Alignment.AlignTrailing)
        self.label_s.setObjectName("label_s")
        self.label_main_refery = QtWidgets.QLabel(self.tab)
        self.label_main_refery.setGeometry(QtCore.QRect(20, 150, 161, 20))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setItalic(True)
        self.label_main_refery.setFont(font)
        self.label_main_refery.setAlignment(QtCore.Qt.Alignment.AlignCenter)
        self.label_main_refery.setObjectName("label_main_refery")
        self.lineEdit_refery = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_refery.setGeometry(QtCore.QRect(20, 170, 201, 21))
        self.lineEdit_refery.setObjectName("lineEdit_refery")
        self.label_kat_ref = QtWidgets.QLabel(self.tab)
        self.label_kat_ref.setGeometry(QtCore.QRect(230, 150, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setItalic(True)
        self.label_kat_ref.setFont(font)
        self.label_kat_ref.setAlignment(QtCore.Qt.Alignment.AlignCenter)
        self.label_kat_ref.setObjectName("label_kat_ref")
        self.comboBox_kategor_ref = QtWidgets.QComboBox(self.tab)
        self.comboBox_kategor_ref.setGeometry(QtCore.QRect(230, 170, 91, 26))
        self.comboBox_kategor_ref.setObjectName("comboBox_kategor_ref")
        self.tabWidget.addTab(self.tab, "")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.lineEdit_Family_name = QtWidgets.QLineEdit(self.tab_1)
        self.lineEdit_Family_name.setGeometry(QtCore.QRect(10, 30, 271, 21))
        self.lineEdit_Family_name.setObjectName("lineEdit_Family_name")
        self.lineEdit_bday = QtWidgets.QLineEdit(self.tab_1)
        self.lineEdit_bday.setGeometry(QtCore.QRect(290, 30, 113, 21))
        self.lineEdit_bday.setObjectName("lineEdit_bday")
        self.lineEdit_R = QtWidgets.QLineEdit(self.tab_1)
        self.lineEdit_R.setGeometry(QtCore.QRect(420, 30, 61, 21))
        self.lineEdit_R.setObjectName("lineEdit_R")
        self.lineEdit_city_list = QtWidgets.QLineEdit(self.tab_1)
        self.lineEdit_city_list.setGeometry(QtCore.QRect(10, 80, 161, 21))
        self.lineEdit_city_list.setObjectName("lineEdit_city_list")
        self.lineEdit_coach = QtWidgets.QLineEdit(self.tab_1)
        self.lineEdit_coach.setGeometry(QtCore.QRect(10, 130, 471, 21))
        self.lineEdit_coach.setObjectName("lineEdit_coach")
        self.label = QtWidgets.QLabel(self.tab_1)
        self.label.setGeometry(QtCore.QRect(100, 10, 91, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.tab_1)
        self.label_2.setGeometry(QtCore.QRect(290, 10, 111, 20))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setItalic(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.tab_1)
        self.label_3.setGeometry(QtCore.QRect(420, 10, 61, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setItalic(True)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.tab_1)
        self.label_4.setGeometry(QtCore.QRect(50, 60, 51, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setItalic(True)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.tab_1)
        self.label_5.setGeometry(QtCore.QRect(230, 60, 91, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setItalic(True)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.tab_1)
        self.label_6.setGeometry(QtCore.QRect(410, 60, 51, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setItalic(True)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.tab_1)
        self.label_7.setGeometry(QtCore.QRect(180, 110, 91, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setItalic(True)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.comboBox_razryad = QtWidgets.QComboBox(self.tab_1)
        self.comboBox_razryad.setGeometry(QtCore.QRect(413, 80, 71, 26))
        self.comboBox_razryad.setObjectName("comboBox_razryad")
        self.comboBox_region = QtWidgets.QComboBox(self.tab_1)
        self.comboBox_region.setGeometry(QtCore.QRect(180, 80, 231, 26))
        self.comboBox_region.setSizeAdjustPolicy(QtWidgets.QComboBox.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self.comboBox_region.setObjectName("comboBox_region")
        self.listWidget = QtWidgets.QListWidget(self.tab_1)
        self.listWidget.setGeometry(QtCore.QRect(490, 20, 321, 181))
        font = QtGui.QFont()
        font.setFamily("Times")
        font.setItalic(True)
        self.listWidget.setFont(font)
        self.listWidget.setTabletTracking(False)
        self.listWidget.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.listWidget.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.listWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.listWidget.setResizeMode(QtWidgets.QListView.ResizeMode.Adjust)
        self.listWidget.setObjectName("listWidget")
        self.textEdit = QtWidgets.QTextEdit(self.tab_1)
        self.textEdit.setGeometry(QtCore.QRect(10, 160, 471, 41))
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(14)
        font.setItalic(True)
        self.textEdit.setFont(font)
        self.textEdit.setInputMethodHints(QtCore.Qt.InputMethodHints.ImhDigitsOnly|QtCore.Qt.InputMethodHints.ImhMultiLine)
        self.textEdit.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.textEdit.setObjectName("textEdit")
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tabWidget.addTab(self.tab_4, "")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(200, 261, 801, 431))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setItalic(True)
        self.tableWidget.setFont(font)
        self.tableWidget.setLineWidth(2)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.tableWidget.setGridStyle(QtCore.Qt.PenStyle.SolidLine)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(1020, 0, 321, 701))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.tableWidget_R_list = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_R_list.setGeometry(QtCore.QRect(200, 260, 801, 431))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setItalic(True)
        self.tableWidget_R_list.setFont(font)
        self.tableWidget_R_list.setObjectName("tableWidget_R_list")
        self.tableWidget_R_list.setColumnCount(0)
        self.tableWidget_R_list.setRowCount(0)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1347, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(2)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_view.setText(_translate("MainWindow", "Просмотр"))
        self.pushButton_db.setText(_translate("MainWindow", "Создание DB"))
        self.pushButton_export.setText(_translate("MainWindow", "экспорт таблицы"))
        self.pushButton_Rlist.setText(_translate("MainWindow", "R-лист"))
        self.pushButton_titul_made.setText(_translate("MainWindow", "Создать"))
        self.pushButton_titul_edit.setText(_translate("MainWindow", "Редактировать"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), _translate("MainWindow", "Титульный лист"))
        self.pushButton_add_player.setText(_translate("MainWindow", "Добавить"))
        self.groupBox.setTitle(_translate("MainWindow", "Сортировка"))
        self.pushButton_sort_R.setText(_translate("MainWindow", "По рейтингу"))
        self.pushButton_sort_Name.setText(_translate("MainWindow", "По алфавиту"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), _translate("MainWindow", "Список участников"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_6), _translate("MainWindow", "Система"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_3), _translate("MainWindow", "Предварительный этап"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_5), _translate("MainWindow", "Полуфиналы"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_4), _translate("MainWindow", "Финальный этап"))
        self.label_nazvanie.setText(_translate("MainWindow", "<html><head/><body><p>Название соревнования</p></body></html>"))
        self.label_sredi.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-style:italic;\">среди</span></p></body></html>"))
        self.label_data_provedenia.setText(_translate("MainWindow", "<html><head/><body><p>Сроки проведения</p></body></html>"))
        self.label_2str_4.setText(_translate("MainWindow", "<html><head/><body><p>Место проведения</p></body></html>"))
        self.label_city.setText(_translate("MainWindow", "<html><head/><body><p>город</p></body></html>"))
        self.label_kat_sek.setText(_translate("MainWindow", "<html><head/><body><p>Категория</p></body></html>"))
        self.label_main_sekretar.setText(_translate("MainWindow", "<html><head/><body><p>Гл. секретарь / Город</p></body></html>"))
        self.dateEdit_end.setDisplayFormat(_translate("MainWindow", "yyyy-MM-dd"))
        self.label_po.setText(_translate("MainWindow", "<html><head/><body><p>по</p></body></html>"))
        self.dateEdit_start.setDisplayFormat(_translate("MainWindow", "yyyy-MM-dd"))
        self.label_s.setText(_translate("MainWindow", "<html><head/><body><p>с</p></body></html>"))
        self.label_main_refery.setText(_translate("MainWindow", "<html><head/><body><p>Гл. судья / Город</p></body></html>"))
        self.label_kat_ref.setText(_translate("MainWindow", "<html><head/><body><p>Категория</p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Титул"))
        self.label.setText(_translate("MainWindow", "Фамилия, Имя"))
        self.label_2.setText(_translate("MainWindow", "Дата рождения"))
        self.label_3.setText(_translate("MainWindow", "Рейтинг"))
        self.label_4.setText(_translate("MainWindow", "Город"))
        self.label_5.setText(_translate("MainWindow", "Регион"))
        self.label_6.setText(_translate("MainWindow", "Разряд"))
        self.label_7.setText(_translate("MainWindow", "Тренер(ы)"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("MainWindow", "Участники"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Группы"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Полуфиналы"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Финалы"))
