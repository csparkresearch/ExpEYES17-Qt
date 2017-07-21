# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ResCapFreq.ui'
#
# Created: Sat Jul 22 01:49:02 2017
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
        Form.resize(269, 52)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout.addWidget(self.pushButton_2, 0, 1, 1, 1)
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
        self.pushButton_3 = QtGui.QPushButton(Form)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.gridLayout.addWidget(self.pushButton_3, 0, 2, 1, 1)
        self.resLabel = QtGui.QLabel(Form)
        self.resLabel.setObjectName(_fromUtf8("resLabel"))
        self.gridLayout.addWidget(self.resLabel, 1, 0, 1, 1)
        self.capLabel = QtGui.QLabel(Form)
        self.capLabel.setObjectName(_fromUtf8("capLabel"))
        self.gridLayout.addWidget(self.capLabel, 1, 1, 1, 1)
        self.freqLabel = QtGui.QLabel(Form)
        self.freqLabel.setObjectName(_fromUtf8("freqLabel"))
        self.gridLayout.addWidget(self.freqLabel, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.getResistance)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.getCapacitance)
        QtCore.QObject.connect(self.pushButton_3, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.getFrequency)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.pushButton_2.setToolTip(_translate("Form", "Measure Capacitance on IN1", None))
        self.pushButton_2.setText(_translate("Form", "CAP", None))
        self.pushButton.setToolTip(_translate("Form", "Measure Resistance on SEN", None))
        self.pushButton.setText(_translate("Form", "RES", None))
        self.pushButton_3.setToolTip(_translate("Form", "Measure Frequency on IN2", None))
        self.pushButton_3.setText(_translate("Form", "FREQ", None))
        self.resLabel.setToolTip(_translate("Form", "Result of Resistance measured on SEN", None))
        self.resLabel.setText(_translate("Form", "Res : SEN", None))
        self.capLabel.setToolTip(_translate("Form", "Result of Capacitance measured on IN1", None))
        self.capLabel.setText(_translate("Form", "Cap: IN1", None))
        self.freqLabel.setToolTip(_translate("Form", "Result of measured Frequency on IN2", None))
        self.freqLabel.setText(_translate("Form", "Freq: IN2", None))

