# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plotTemplate.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(624, 524)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.widgets = QtWidgets.QFrame(self.splitter)
        self.widgets.setMaximumSize(QtCore.QSize(300, 16777215))
        self.widgets.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.widgets.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.widgets.setFrameShadow(QtWidgets.QFrame.Raised)
        self.widgets.setObjectName("widgets")
        self.widgetLayout = QtWidgets.QVBoxLayout(self.widgets)
        self.widgetLayout.setSpacing(2)
        self.widgetLayout.setContentsMargins(2, 2, 2, 2)
        self.widgetLayout.setObjectName("widgetLayout")
        self.plotFrame = QtWidgets.QFrame(self.splitter)
        self.plotFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.plotFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.plotFrame.setObjectName("plotFrame")
        self.plotLayout = QtWidgets.QVBoxLayout(self.plotFrame)
        self.plotLayout.setSpacing(0)
        self.plotLayout.setContentsMargins(0, 0, 0, 0)
        self.plotLayout.setObjectName("plotLayout")
        self.verticalLayout.addWidget(self.splitter)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

