# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tracesRow.ui'
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
        Form.resize(263, 28)
        Form.setStyleSheet(_fromUtf8("QPushButton{\n"
"padding:1px;\n"
"border : 1px solid gray;\n"
"}\n"
"QSpinBox{\n"
"padding:0px;\n"
"}\n"
"QCheckBox{\n"
"padding:1px;\n"
"}\n"
"QLabel{\n"
"color:#000;\n"
"}"))
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widgetLayout = QtGui.QHBoxLayout()
        self.widgetLayout.setSpacing(3)
        self.widgetLayout.setContentsMargins(-1, 0, -1, -1)
        self.widgetLayout.setObjectName(_fromUtf8("widgetLayout"))
        self.enable = QtGui.QCheckBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.enable.sizePolicy().hasHeightForWidth())
        self.enable.setSizePolicy(sizePolicy)
        self.enable.setMaximumSize(QtCore.QSize(20, 16777215))
        self.enable.setText(_fromUtf8(""))
        self.enable.setChecked(True)
        self.enable.setObjectName(_fromUtf8("enable"))
        self.widgetLayout.addWidget(self.enable)
        self.name = QtGui.QLabel(Form)
        self.name.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.name.setObjectName(_fromUtf8("name"))
        self.widgetLayout.addWidget(self.name)
        self.widthBox = QtGui.QSpinBox(Form)
        self.widthBox.setMinimumSize(QtCore.QSize(60, 0))
        self.widthBox.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setKerning(True)
        self.widthBox.setFont(font)
        self.widthBox.setWrapping(False)
        self.widthBox.setFrame(True)
        self.widthBox.setAlignment(QtCore.Qt.AlignCenter)
        self.widthBox.setPrefix(_fromUtf8(""))
        self.widthBox.setMinimum(1)
        self.widthBox.setMaximum(7)
        self.widthBox.setObjectName(_fromUtf8("widthBox"))
        self.widgetLayout.addWidget(self.widthBox)
        self.colorButton = QtGui.QPushButton(Form)
        self.colorButton.setMinimumSize(QtCore.QSize(50, 0))
        self.colorButton.setMaximumSize(QtCore.QSize(35, 16777215))
        self.colorButton.setObjectName(_fromUtf8("colorButton"))
        self.widgetLayout.addWidget(self.colorButton)
        self.closeButton = QtGui.QPushButton(Form)
        self.closeButton.setMaximumSize(QtCore.QSize(15, 16777215))
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.widgetLayout.addWidget(self.closeButton)
        self.verticalLayout.addLayout(self.widgetLayout)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.enable, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), Form.traceToggled)
        QtCore.QObject.connect(self.widthBox, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), Form.changeWidth)
        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.removeTrace)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.enable.setToolTip(_translate("Form", "Show/Hide this trace", None))
        self.name.setText(_translate("Form", "TextLabel", None))
        self.widthBox.setToolTip(_translate("Form", "Set the width of the trace", None))
        self.widthBox.setSuffix(_translate("Form", " px", None))
        self.colorButton.setToolTip(_translate("Form", "Change the color of the trace", None))
        self.colorButton.setText(_translate("Form", "Color", None))
        self.closeButton.setToolTip(_translate("Form", "Delete this trace", None))
        self.closeButton.setText(_translate("Form", "X", None))

