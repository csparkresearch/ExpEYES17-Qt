# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'triggerWidget.ui'
#
# Created: Fri Jul 21 19:50:00 2017
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
        Form.resize(276, 33)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widgetLayout = QtGui.QHBoxLayout()
        self.widgetLayout.setSpacing(2)
        self.widgetLayout.setContentsMargins(-1, 0, -1, 5)
        self.widgetLayout.setObjectName(_fromUtf8("widgetLayout"))
        self.enable = QtGui.QCheckBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.enable.sizePolicy().hasHeightForWidth())
        self.enable.setSizePolicy(sizePolicy)
        self.enable.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.enable.setFont(font)
        self.enable.setChecked(True)
        self.enable.setObjectName(_fromUtf8("enable"))
        self.widgetLayout.addWidget(self.enable)
        self.chanBox = QtGui.QComboBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chanBox.sizePolicy().hasHeightForWidth())
        self.chanBox.setSizePolicy(sizePolicy)
        self.chanBox.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.chanBox.setFont(font)
        self.chanBox.setObjectName(_fromUtf8("chanBox"))
        self.widgetLayout.addWidget(self.chanBox)
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setMaximumSize(QtCore.QSize(20, 16777215))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.widgetLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.widgetLayout)

        self.retranslateUi(Form)
        self.chanBox.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.enable.setText(_translate("Form", "Trigger: 0V (Drag trigger line)", None))
        self.pushButton.setText(_translate("Form", "?", None))

