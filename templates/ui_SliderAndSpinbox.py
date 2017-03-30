# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SliderAndSpinbox.ui'
#
# Created: Thu Mar 30 18:57:02 2017
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
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(8)
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_5.addWidget(self.label)
        self.slider = QtGui.QSlider(Form)
        self.slider.setMaximumSize(QtCore.QSize(16777215, 15))
        self.slider.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))
        self.slider.setMinimum(-3300)
        self.slider.setMaximum(3300)
        self.slider.setSingleStep(10)
        self.slider.setPageStep(100)
        self.slider.setProperty("value", 0)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setTickPosition(QtGui.QSlider.NoTicks)
        self.slider.setTickInterval(0)
        self.slider.setObjectName(_fromUtf8("slider"))
        self.horizontalLayout_5.addWidget(self.slider)
        self.spinbox = QtGui.QDoubleSpinBox(Form)
        self.spinbox.setMinimumSize(QtCore.QSize(75, 0))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.spinbox.setFont(font)
        self.spinbox.setFrame(True)
        self.spinbox.setAlignment(QtCore.Qt.AlignCenter)
        self.spinbox.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.spinbox.setDecimals(1)
        self.spinbox.setMinimum(-3300.0)
        self.spinbox.setMaximum(3300.0)
        self.spinbox.setProperty("value", 0.0)
        self.spinbox.setObjectName(_fromUtf8("spinbox"))
        self.horizontalLayout_5.addWidget(self.spinbox)
        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label.setText(_translate("Form", "___", None))
        self.spinbox.setSuffix(_translate("Form", "mV", None))

