# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'allTraces.ui'
#
# Created: Mon Jul 17 12:53:05 2017
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(227, 29)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widgetLayout = QtGui.QHBoxLayout()
        self.widgetLayout.setSpacing(8)
        self.widgetLayout.setContentsMargins(-1, 0, -1, -1)
        self.widgetLayout.setObjectName(_fromUtf8("widgetLayout"))
        self.enableButton = QtGui.QCheckBox(Form)
        self.enableButton.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.enableButton.setFont(font)
        self.enableButton.setObjectName(_fromUtf8("enableButton"))
        self.widgetLayout.addWidget(self.enableButton)
        self.traceList = QtGui.QComboBox(Form)
        self.traceList.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.traceList.setFont(font)
        self.traceList.setObjectName(_fromUtf8("traceList"))
        self.widgetLayout.addWidget(self.traceList)
        self.menuButton = QtGui.QPushButton(Form)
        self.menuButton.setMaximumSize(QtCore.QSize(20, 16777215))
        self.menuButton.setText(_fromUtf8(""))
        self.menuButton.setObjectName(_fromUtf8("menuButton"))
        self.widgetLayout.addWidget(self.menuButton)
        self.verticalLayout.addLayout(self.widgetLayout)

        self.retranslateUi(Form)
        self.traceList.setCurrentIndex(-1)
        QtCore.QObject.connect(self.traceList, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), Form.traceChanged)
        QtCore.QObject.connect(self.enableButton, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), Form.traceToggled)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.enableButton.setText(_translate("Form", "Visible", None))

