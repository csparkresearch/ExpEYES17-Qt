# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'allTracesDetailed.ui'
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
        Form.resize(204, 168)
        Form.setMaximumSize(QtCore.QSize(16777215, 250))
        Form.setStyleSheet(_fromUtf8(""))
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.scrollArea = QtGui.QScrollArea(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 202, 137))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.traceLayout = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.traceLayout.setSpacing(0)
        self.traceLayout.setMargin(0)
        self.traceLayout.setObjectName(_fromUtf8("traceLayout"))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.saveButton = QtGui.QPushButton(Form)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.verticalLayout.addWidget(self.saveButton)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.saveButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.saveData)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.saveButton.setText(_translate("Form", "SAVE DATA", None))

