# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'douts.ui'
#
# Created: Mon Jul 17 12:53:06 2017
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
        Form.resize(239, 25)
        Form.setStyleSheet(_fromUtf8(""))
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widgetLayout = QtGui.QHBoxLayout()
        self.widgetLayout.setSpacing(2)
        self.widgetLayout.setContentsMargins(-1, 0, -1, -1)
        self.widgetLayout.setObjectName(_fromUtf8("widgetLayout"))
        self.OD1 = QtGui.QCheckBox(Form)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.OD1.setFont(font)
        self.OD1.setObjectName(_fromUtf8("OD1"))
        self.widgetLayout.addWidget(self.OD1)
        self.SQR1 = QtGui.QCheckBox(Form)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.SQR1.setFont(font)
        self.SQR1.setObjectName(_fromUtf8("SQR1"))
        self.widgetLayout.addWidget(self.SQR1)
        self.SQR2 = QtGui.QCheckBox(Form)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.SQR2.setFont(font)
        self.SQR2.setObjectName(_fromUtf8("SQR2"))
        self.widgetLayout.addWidget(self.SQR2)
        self.CCS = QtGui.QCheckBox(Form)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.CCS.setFont(font)
        self.CCS.setObjectName(_fromUtf8("CCS"))
        self.widgetLayout.addWidget(self.CCS)
        self.verticalLayout.addLayout(self.widgetLayout)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.OD1, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), Form.setOD1)
        QtCore.QObject.connect(self.SQR1, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), Form.setSQR1)
        QtCore.QObject.connect(self.SQR2, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), Form.setSQR2)
        QtCore.QObject.connect(self.CCS, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), Form.setCCS)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.OD1.setText(_translate("Form", "OD1", None))
        self.SQR1.setText(_translate("Form", "SQR1", None))
        self.SQR2.setText(_translate("Form", "SQR2", None))
        self.CCS.setText(_translate("Form", "CCS", None))

