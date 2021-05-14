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
        MainWindow.resize(1448, 686)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame_main = QtWidgets.QFrame(self.centralwidget)
        self.frame_main.setGeometry(QtCore.QRect(10, 505, 201, 114))
        self.frame_main.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_main.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_main.setObjectName("frame_main")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_main)
        self.gridLayout.setObjectName("gridLayout")
        self.Button_export = QtWidgets.QPushButton(self.frame_main)
        self.Button_export.setObjectName("Button_export")
        self.gridLayout.addWidget(self.Button_export, 0, 0, 1, 1)
        self.Button_db = QtWidgets.QPushButton(self.frame_main)
        self.Button_db.setObjectName("Button_db")
        self.gridLayout.addWidget(self.Button_db, 1, 0, 1, 1)
        self.Button_view = QtWidgets.QPushButton(self.frame_main)
        self.Button_view.setObjectName("Button_view")
        self.gridLayout.addWidget(self.Button_view, 2, 0, 1, 1)
        self.frame_table = QtWidgets.QFrame(self.centralwidget)
        self.frame_table.setGeometry(QtCore.QRect(220, 250, 801, 371))
        self.frame_table.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.frame_table.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.frame_table.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_table.setObjectName("frame_table")
        self.toolBox = QtWidgets.QToolBox(self.centralwidget)
        self.toolBox.setGeometry(QtCore.QRect(10, 10, 201, 441))
        self.toolBox.setMinimumSize(QtCore.QSize(180, 430))
        self.toolBox.setMaximumSize(QtCore.QSize(1200, 1200))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setItalic(True)
        self.toolBox.setFont(font)
        self.toolBox.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.toolBox.setObjectName("toolBox")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 199, 235))
        self.page.setObjectName("page")
        self.Button_title_made = QtWidgets.QPushButton(self.page)
        self.Button_title_made.setGeometry(QtCore.QRect(19, 0, 141, 40))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setBold(True)
        font.setWeight(75)
        self.Button_title_made.setFont(font)
        self.Button_title_made.setAutoDefault(False)
        self.Button_title_made.setDefault(False)
        self.Button_title_made.setFlat(False)
        self.Button_title_made.setObjectName("Button_title_made")
        self.checkBox = QtWidgets.QCheckBox(self.page)
        self.checkBox.setGeometry(QtCore.QRect(170, 10, 21, 20))
        self.checkBox.setText("")
        self.checkBox.setObjectName("checkBox")
        self.toolBox.addItem(self.page, "")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 199, 235))
        self.page_2.setObjectName("page_2")
        self.Button_add_player = QtWidgets.QPushButton(self.page_2)
        self.Button_add_player.setGeometry(QtCore.QRect(10, 0, 151, 32))
        self.Button_add_player.setObjectName("Button_add_player")
        self.groupBox = QtWidgets.QGroupBox(self.page_2)
        self.groupBox.setGeometry(QtCore.QRect(10, 110, 151, 121))
        self.groupBox.setObjectName("groupBox")
        self.Button_sort_R = QtWidgets.QPushButton(self.groupBox)
        self.Button_sort_R.setGeometry(QtCore.QRect(0, 60, 151, 32))
        self.Button_sort_R.setObjectName("Button_sort_R")
        self.Button_sort_Name = QtWidgets.QPushButton(self.groupBox)
        self.Button_sort_Name.setGeometry(QtCore.QRect(0, 30, 151, 32))
        self.Button_sort_Name.setObjectName("Button_sort_Name")
        self.Button_sort_mesto = QtWidgets.QPushButton(self.groupBox)
        self.Button_sort_mesto.setGeometry(QtCore.QRect(0, 90, 151, 32))
        self.Button_sort_mesto.setObjectName("Button_sort_mesto")
        self.toolBox.addItem(self.page_2, "")
        self.page_6 = QtWidgets.QWidget()
        self.page_6.setGeometry(QtCore.QRect(0, 0, 199, 235))
        self.page_6.setObjectName("page_6")
        self.toolBox.addItem(self.page_6, "")
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setGeometry(QtCore.QRect(0, 0, 199, 235))
        self.page_3.setObjectName("page_3")
        self.toolBox.addItem(self.page_3, "")
        self.page_5 = QtWidgets.QWidget()
        self.page_5.setGeometry(QtCore.QRect(0, 0, 199, 235))
        self.page_5.setObjectName("page_5")
        self.toolBox.addItem(self.page_5, "")
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setGeometry(QtCore.QRect(0, 0, 199, 235))
        self.page_4.setObjectName("page_4")
        self.toolBox.addItem(self.page_4, "")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(220, 0, 801, 241))
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
        self.lineEdit_title_nazvanie = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_title_nazvanie.setGeometry(QtCore.QRect(20, 30, 621, 21))
        self.lineEdit_title_nazvanie.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.lineEdit_title_nazvanie.setObjectName("lineEdit_title_nazvanie")
        self.comboBox_sredi = QtWidgets.QComboBox(self.tab)
        self.comboBox_sredi.setGeometry(QtCore.QRect(120, 70, 201, 26))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setItalic(True)
        self.comboBox_sredi.setFont(font)
        self.comboBox_sredi.setObjectName("comboBox_sredi")
        self.lineEdit_title_vozrast = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_title_vozrast.setGeometry(QtCore.QRect(330, 70, 311, 21))
        self.lineEdit_title_vozrast.setObjectName("lineEdit_title_vozrast")
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
        self.lineEdit_city_title = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_city_title.setGeometry(QtCore.QRect(470, 120, 171, 21))
        self.lineEdit_city_title.setObjectName("lineEdit_city_title")
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
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.tabWidget.addTab(self.tab_5, "")
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
        self.tableWidget.setGeometry(QtCore.QRect(230, 261, 781, 351))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Ignored)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("DejaVu Serif")
        font.setPointSize(11)
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
        self.frame_score = QtWidgets.QFrame(self.centralwidget)
        self.frame_score.setGeometry(QtCore.QRect(1030, 10, 400, 611))
        self.frame_score.setMinimumSize(QtCore.QSize(400, 600))
        self.frame_score.setMaximumSize(QtCore.QSize(16000, 16777215))
        self.frame_score.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_score.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_score.setObjectName("frame_score")
        self.lineEdit = QtWidgets.QLineEdit(self.frame_score)
        self.lineEdit.setGeometry(QtCore.QRect(30, 20, 113, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame_score)
        self.lineEdit_2.setGeometry(QtCore.QRect(160, 20, 113, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.tableWidget_R_list = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_R_list.setGeometry(QtCore.QRect(230, 260, 781, 351))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setItalic(True)
        self.tableWidget_R_list.setFont(font)
        self.tableWidget_R_list.setObjectName("tableWidget_R_list")
        self.tableWidget_R_list.setColumnCount(0)
        self.tableWidget_R_list.setRowCount(0)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1448, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setItalic(True)
        self.menubar.setFont(font)
        self.menubar.setNativeMenuBar(True)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Button_export.setText(_translate("MainWindow", "экспорт таблицы"))
        self.Button_db.setText(_translate("MainWindow", "Создание DB"))
        self.Button_view.setText(_translate("MainWindow", "Просмотр"))
        self.Button_title_made.setText(_translate("MainWindow", "Создать"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), _translate("MainWindow", "Титульный лист"))
        self.Button_add_player.setText(_translate("MainWindow", "Добавить"))
        self.groupBox.setTitle(_translate("MainWindow", "Сортировка"))
        self.Button_sort_R.setText(_translate("MainWindow", "По рейтингу"))
        self.Button_sort_Name.setText(_translate("MainWindow", "По алфавиту"))
        self.Button_sort_mesto.setText(_translate("MainWindow", "По месту"))
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
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "Система"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Группы"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Полуфиналы"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Финалы"))
