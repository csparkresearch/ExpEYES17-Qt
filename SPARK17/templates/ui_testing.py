# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testing.ui'
#
# Created: Sat Jul 22 01:49:01 2017
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
        MainWindow.resize(934, 510)
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
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.tabs = QtGui.QTabWidget(self.centralwidget)
        self.tabs.setObjectName(_fromUtf8("tabs"))
        self.tab1 = QtGui.QWidget()
        self.tab1.setObjectName(_fromUtf8("tab1"))
        self.gridLayout = QtGui.QGridLayout(self.tab1)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.frame_2 = QtGui.QFrame(self.tab1)
        self.frame_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.evalLayout = QtGui.QHBoxLayout(self.frame_2)
        self.evalLayout.setMargin(3)
        self.evalLayout.setObjectName(_fromUtf8("evalLayout"))
        self.pushButton = QtGui.QPushButton(self.frame_2)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.evalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtGui.QPushButton(self.frame_2)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.evalLayout.addWidget(self.pushButton_2)
        self.gridLayout.addWidget(self.frame_2, 0, 0, 1, 1)
        self.tbl = QtGui.QTableWidget(self.tab1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tbl.sizePolicy().hasHeightForWidth())
        self.tbl.setSizePolicy(sizePolicy)
        self.tbl.setMinimumSize(QtCore.QSize(400, 0))
        self.tbl.setFrameShape(QtGui.QFrame.NoFrame)
        self.tbl.setRowCount(15)
        self.tbl.setColumnCount(4)
        self.tbl.setObjectName(_fromUtf8("tbl"))
        self.tbl.horizontalHeader().setDefaultSectionSize(120)
        self.tbl.horizontalHeader().setStretchLastSection(True)
        self.tbl.verticalHeader().setDefaultSectionSize(25)
        self.tbl.verticalHeader().setStretchLastSection(False)
        self.gridLayout.addWidget(self.tbl, 1, 0, 1, 1)
        self.frame_3 = QtGui.QFrame(self.tab1)
        self.frame_3.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.pushButton_4 = QtGui.QPushButton(self.frame_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.horizontalLayout_3.addWidget(self.pushButton_4)
        self.gridLayout.addWidget(self.frame_3, 3, 0, 1, 1)
        self.frame = QtGui.QFrame(self.tab1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.plot_area = QtGui.QGridLayout(self.frame)
        self.plot_area.setMargin(1)
        self.plot_area.setSpacing(2)
        self.plot_area.setObjectName(_fromUtf8("plot_area"))
        self.gridLayout.addWidget(self.frame, 0, 1, 4, 1)
        self.tabs.addTab(self.tab1, _fromUtf8(""))
        self.tab2 = QtGui.QWidget()
        self.tab2.setObjectName(_fromUtf8("tab2"))
        self.tabs.addTab(self.tab2, _fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.tabs)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabs.setCurrentIndex(0)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.eval1)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.eval2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Edit Calibration", None))
        self.frame_2.setProperty("class", _translate("MainWindow", "deep", None))
        self.pushButton.setText(_translate("MainWindow", "Evaluate Group 1", None))
        self.pushButton.setShortcut(_translate("MainWindow", "1", None))
        self.pushButton_2.setText(_translate("MainWindow", "Evaluate Group 2", None))
        self.pushButton_2.setShortcut(_translate("MainWindow", "2", None))
        self.frame_3.setProperty("class", _translate("MainWindow", "deep", None))
        self.pushButton_4.setText(_translate("MainWindow", "Save Values and Screenshot", None))
        self.pushButton_4.setShortcut(_translate("MainWindow", "Ctrl+S", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab1), _translate("MainWindow", "Automated", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab2), _translate("MainWindow", "Advanced tests", None))

