# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'layoutNew.ui'
#
# Created: Mon Jul 17 12:53:04 2017
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(936, 637)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/control/eyes17-logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(_fromUtf8("*{outline:none;}\n"
"\n"
"QMainWindow{background: rgb(56, 102, 115);} \n"
"QMessageBox {background: #444544;} \n"
"\n"
"QTabBar{font:16px;} \n"
"QTabBar::tab{ padding:10px 50px; color:#CCCCCC;background: rgb(56, 102, 115);}\n"
"QTabBar::tab:selected{color:white; background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:.7 rgb(126, 197, 220) , stop:1 rgba(0,0,0,100) );} \n"
"QTabBar::tab:hover{color:white; background:qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(26, 177, 191,255), stop:1 rgba(100, 100, 200,255) );} \n"
"\n"
".deep,#widgets{ background: rgb(57, 79, 99); }\n"
"\n"
"QListWidget{background: rgb(26, 32, 35);color:#FFFFFF;} \n"
"QListWidget::item:hover{background: #223344;color:#FFFFFF;} \n"
"\n"
"QLabel,QRadioButton{color:#FFFFFF; margin:1px 2px;}\n"
"QCheckBox{color:#FFFFEE; margin:3px 0px;}\n"
"\n"
"QSlider::groove:horizontal {margin:0px; padding:0px; border:none; background:#DDFDFE; color:#BB7777; height: 4px;}\n"
"QSlider::handle:horizontal {background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #eee, stop:1 #ccc);border: 2px solid #777;width: 13px;margin-top: -3px;margin-bottom: -3px;border-radius: 3px;}\n"
"\n"
"QPushButton{border:1px solid #424242; padding:6px;color:#000000;background:#AAAAAA;}\n"
"QPushButton:hover{background:rgb(26, 177, 191) ; color:white; border-color:#FFFFFF;}\n"
"QPushButton::disabled{background:#333333 ; color:black;}\n"
"QComboBox QAbstractItemView::item {\n"
"    border-bottom: 5px solid white; margin:3px;\n"
"}\n"
"QComboBox QAbstractItemView::item:selected {\n"
"    border-bottom: 5px solid black; margin:3px;\n"
"}\n"
"\n"
"QToolTip{background:#FBE9E7;color:#757575; padding:4px; border:0px; margin:0px;} QPushButton{min-height24px; min-width:30px;}  "))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.North)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setIconSize(QtCore.QSize(25, 25))
        self.tabWidget.setUsesScrollButtons(False)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.helpTab = QtGui.QWidget()
        self.helpTab.setObjectName(_fromUtf8("helpTab"))
        self.helpLayout = QtGui.QVBoxLayout(self.helpTab)
        self.helpLayout.setSpacing(0)
        self.helpLayout.setMargin(0)
        self.helpLayout.setObjectName(_fromUtf8("helpLayout"))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/control/file.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.helpTab, icon1, _fromUtf8(""))
        self.experimentTab = QtGui.QWidget()
        self.experimentTab.setObjectName(_fromUtf8("experimentTab"))
        self.experimentLayout = QtGui.QVBoxLayout(self.experimentTab)
        self.experimentLayout.setMargin(0)
        self.experimentLayout.setObjectName(_fromUtf8("experimentLayout"))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/control/plots.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.experimentTab, icon2, _fromUtf8(""))
        self.controlTab = QtGui.QWidget()
        self.controlTab.setObjectName(_fromUtf8("controlTab"))
        self.groupBox = QtGui.QGroupBox(self.controlTab)
        self.groupBox.setGeometry(QtCore.QRect(5, 5, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout_11 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_11.setSpacing(1)
        self.horizontalLayout_11.setMargin(0)
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.DIN_IN2 = QtGui.QLabel(self.groupBox)
        self.DIN_IN2.setStyleSheet(_fromUtf8(""))
        self.DIN_IN2.setObjectName(_fromUtf8("DIN_IN2"))
        self.horizontalLayout_11.addWidget(self.DIN_IN2)
        self.DIN_SQR1 = QtGui.QLabel(self.groupBox)
        self.DIN_SQR1.setObjectName(_fromUtf8("DIN_SQR1"))
        self.horizontalLayout_11.addWidget(self.DIN_SQR1)
        self.DIN_OD1 = QtGui.QLabel(self.groupBox)
        self.DIN_OD1.setObjectName(_fromUtf8("DIN_OD1"))
        self.horizontalLayout_11.addWidget(self.DIN_OD1)
        self.DIN_SEN = QtGui.QLabel(self.groupBox)
        self.DIN_SEN.setObjectName(_fromUtf8("DIN_SEN"))
        self.horizontalLayout_11.addWidget(self.DIN_SEN)
        self.DIN_CCS = QtGui.QLabel(self.groupBox)
        self.DIN_CCS.setObjectName(_fromUtf8("DIN_CCS"))
        self.horizontalLayout_11.addWidget(self.DIN_CCS)
        self.tabWidget.addTab(self.controlTab, _fromUtf8(""))
        self.saveTab = QtGui.QWidget()
        self.saveTab.setObjectName(_fromUtf8("saveTab"))
        self.saveLayout = QtGui.QVBoxLayout(self.saveTab)
        self.saveLayout.setSpacing(0)
        self.saveLayout.setMargin(0)
        self.saveLayout.setObjectName(_fromUtf8("saveLayout"))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/control/saved.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.saveTab, icon3, _fromUtf8(""))
        self.verticalLayout_2.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 936, 25))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuOptions = QtGui.QMenu(self.menuBar)
        self.menuOptions.setObjectName(_fromUtf8("menuOptions"))
        MainWindow.setMenuBar(self.menuBar)
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setIcon(icon3)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.menuOptions.addAction(self.actionSave)
        self.menuBar.addAction(self.menuOptions.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QObject.connect(self.tabWidget, QtCore.SIGNAL(_fromUtf8("currentChanged(int)")), MainWindow.tabChanged)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "ExpEYES - 17", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.helpTab), _translate("MainWindow", "Help", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.experimentTab), _translate("MainWindow", "Experiments", None))
        self.groupBox.setTitle(_translate("MainWindow", "Digital Inputs", None))
        self.DIN_IN2.setText(_translate("MainWindow", "IN2", None))
        self.DIN_SQR1.setText(_translate("MainWindow", "SQR1", None))
        self.DIN_OD1.setText(_translate("MainWindow", "OD1", None))
        self.DIN_SEN.setText(_translate("MainWindow", "SEN", None))
        self.DIN_CCS.setText(_translate("MainWindow", "CCS", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.controlTab), _translate("MainWindow", "Controls/Readback", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.saveTab), _translate("MainWindow", "Saved plots", None))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.saveTab), _translate("MainWindow", "View saved plots. Click on them to load them to the plot window for analysis", None))
        self.menuOptions.setTitle(_translate("MainWindow", "File", None))
        self.actionSave.setText(_translate("MainWindow", "save", None))
        self.actionSave.setToolTip(_translate("MainWindow", "save plot data", None))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S", None))

import res_rc
