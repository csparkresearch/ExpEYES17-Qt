# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plot2Template.ui'
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
        self.widgetsParent = QtGui.QFrame(self.splitter)
        self.widgetsParent.setMaximumSize(QtCore.QSize(300, 16777215))
        self.widgetsParent.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.widgetsParent.setFrameShape(QtGui.QFrame.StyledPanel)
        self.widgetsParent.setFrameShadow(QtGui.QFrame.Raised)
        self.widgetsParent.setObjectName(_fromUtf8("widgetsParent"))
        self.widgetLayoutParent = QtGui.QVBoxLayout(self.widgetsParent)
        self.widgetLayoutParent.setSpacing(2)
        self.widgetLayoutParent.setMargin(2)
        self.widgetLayoutParent.setObjectName(_fromUtf8("widgetLayoutParent"))
        self.frame = QtGui.QFrame(self.widgetsParent)
        self.frame.setMaximumSize(QtCore.QSize(16777215, 230))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.plot2Layout = QtGui.QVBoxLayout(self.frame)
        self.plot2Layout.setSpacing(0)
        self.plot2Layout.setMargin(0)
        self.plot2Layout.setObjectName(_fromUtf8("plot2Layout"))
        self.widgetLayoutParent.addWidget(self.frame)
        self.widgets = QtGui.QFrame(self.widgetsParent)
        self.widgets.setFrameShape(QtGui.QFrame.StyledPanel)
        self.widgets.setFrameShadow(QtGui.QFrame.Raised)
        self.widgets.setObjectName(_fromUtf8("widgets"))
        self.widgetLayout = QtGui.QVBoxLayout(self.widgets)
        self.widgetLayout.setSpacing(2)
        self.widgetLayout.setMargin(2)
        self.widgetLayout.setObjectName(_fromUtf8("widgetLayout"))
        self.widgetLayoutParent.addWidget(self.widgets)
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

