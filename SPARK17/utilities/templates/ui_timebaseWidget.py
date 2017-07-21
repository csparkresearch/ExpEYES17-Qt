# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'timebaseWidget.ui'
#
# Created: Sat Jul 22 01:49:03 2017
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
        Form.resize(248, 27)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widgetLayout = QtGui.QHBoxLayout()
        self.widgetLayout.setSpacing(8)
        self.widgetLayout.setContentsMargins(-1, 0, -1, 5)
        self.widgetLayout.setObjectName(_fromUtf8("widgetLayout"))
        self.label = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.widgetLayout.addWidget(self.label)
        self.slider = QtGui.QSlider(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.slider.sizePolicy().hasHeightForWidth())
        self.slider.setSizePolicy(sizePolicy)
        self.slider.setMaximumSize(QtCore.QSize(16777215, 15))
        self.slider.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.slider.setMinimum(0)
        self.slider.setMaximum(9)
        self.slider.setSingleStep(1)
        self.slider.setPageStep(1)
        self.slider.setProperty("value", 0)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setTickPosition(QtGui.QSlider.NoTicks)
        self.slider.setTickInterval(0)
        self.slider.setObjectName(_fromUtf8("slider"))
        self.widgetLayout.addWidget(self.slider)
        self.value = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.value.sizePolicy().hasHeightForWidth())
        self.value.setSizePolicy(sizePolicy)
        self.value.setMinimumSize(QtCore.QSize(60, 0))
        self.value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.value.setObjectName(_fromUtf8("value"))
        self.widgetLayout.addWidget(self.value)
        self.verticalLayout.addLayout(self.widgetLayout)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.slider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), Form.valueChanged)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label.setText(_translate("Form", "Time", None))
        self.value.setText(_translate("Form", "mS", None))

