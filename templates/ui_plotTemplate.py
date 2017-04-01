# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plotTemplate.ui'
#
# Created: Sat Apr  1 22:49:57 2017
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
        Form.resize(624, 524)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.splitter = QtGui.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.widgets = QtGui.QFrame(self.splitter)
        self.widgets.setMaximumSize(QtCore.QSize(250, 16777215))
        self.widgets.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.widgets.setFrameShape(QtGui.QFrame.StyledPanel)
        self.widgets.setFrameShadow(QtGui.QFrame.Raised)
        self.widgets.setObjectName(_fromUtf8("widgets"))
        self.widgetLayout = QtGui.QVBoxLayout(self.widgets)
        self.widgetLayout.setSpacing(0)
        self.widgetLayout.setMargin(0)
        self.widgetLayout.setObjectName(_fromUtf8("widgetLayout"))
        self.plotFrame = QtGui.QFrame(self.splitter)
        self.plotFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.plotFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.plotFrame.setObjectName(_fromUtf8("plotFrame"))
        self.plotLayout = QtGui.QVBoxLayout(self.plotFrame)
        self.plotLayout.setSpacing(0)
        self.plotLayout.setMargin(0)
        self.plotLayout.setObjectName(_fromUtf8("plotLayout"))
        self.verticalLayout.addWidget(self.splitter)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))

