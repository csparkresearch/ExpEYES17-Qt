# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'channelSelector.ui'
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
        Form.resize(227, 28)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widgetLayout = QtGui.QHBoxLayout()
        self.widgetLayout.setSpacing(8)
        self.widgetLayout.setContentsMargins(-1, 0, -1, -1)
        self.widgetLayout.setObjectName(_fromUtf8("widgetLayout"))
        self.enable = QtGui.QCheckBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.enable.sizePolicy().hasHeightForWidth())
        self.enable.setSizePolicy(sizePolicy)
        self.enable.setMaximumSize(QtCore.QSize(70, 16777215))
        self.enable.setChecked(True)
        self.enable.setObjectName(_fromUtf8("enable"))
        self.widgetLayout.addWidget(self.enable)
        self.gain = QtGui.QComboBox(Form)
        self.gain.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.gain.setFont(font)
        self.gain.setObjectName(_fromUtf8("gain"))
        self.gain.addItem(_fromUtf8(""))
        self.gain.addItem(_fromUtf8(""))
        self.gain.addItem(_fromUtf8(""))
        self.gain.addItem(_fromUtf8(""))
        self.gain.addItem(_fromUtf8(""))
        self.gain.addItem(_fromUtf8(""))
        self.gain.addItem(_fromUtf8(""))
        self.gain.addItem(_fromUtf8(""))
        self.widgetLayout.addWidget(self.gain)
        self.fit = QtGui.QCheckBox(Form)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.fit.setFont(font)
        self.fit.setObjectName(_fromUtf8("fit"))
        self.widgetLayout.addWidget(self.fit)
        self.verticalLayout.addLayout(self.widgetLayout)

        self.retranslateUi(Form)
        self.gain.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.enable.setText(_translate("Form", "_", None))
        self.gain.setItemText(0, _translate("Form", "16V", None))
        self.gain.setItemText(1, _translate("Form", "8V", None))
        self.gain.setItemText(2, _translate("Form", "4V", None))
        self.gain.setItemText(3, _translate("Form", "2.5V", None))
        self.gain.setItemText(4, _translate("Form", "1.5V", None))
        self.gain.setItemText(5, _translate("Form", "1V", None))
        self.gain.setItemText(6, _translate("Form", ".5V", None))
        self.gain.setItemText(7, _translate("Form", ".25V", None))
        self.fit.setText(_translate("Form", "FIT", None))

