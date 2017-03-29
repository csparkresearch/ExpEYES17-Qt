# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fileBrowser.ui'
#
# Created: Wed Mar 29 21:28:04 2017
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
        Form.resize(704, 512)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame = QtGui.QFrame(Form)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout_10 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setMargin(0)
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.pathLabel = QtGui.QLabel(self.frame)
        self.pathLabel.setObjectName(_fromUtf8("pathLabel"))
        self.horizontalLayout_10.addWidget(self.pathLabel)
        self.dirChange = QtGui.QPushButton(self.frame)
        self.dirChange.setMinimumSize(QtCore.QSize(0, 0))
        self.dirChange.setMaximumSize(QtCore.QSize(150, 30))
        self.dirChange.setObjectName(_fromUtf8("dirChange"))
        self.horizontalLayout_10.addWidget(self.dirChange)
        self.verticalLayout.addWidget(self.frame)
        self.listWidget = QtGui.QListWidget(Form)
        self.listWidget.setFrameShape(QtGui.QFrame.NoFrame)
        self.listWidget.setDragEnabled(True)
        self.listWidget.setIconSize(QtCore.QSize(200, 180))
        self.listWidget.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.listWidget.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.listWidget.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.listWidget.setMovement(QtGui.QListView.Free)
        self.listWidget.setResizeMode(QtGui.QListView.Adjust)
        self.listWidget.setLayoutMode(QtGui.QListView.Batched)
        self.listWidget.setGridSize(QtCore.QSize(220, 190))
        self.listWidget.setViewMode(QtGui.QListView.IconMode)
        self.listWidget.setUniformItemSizes(True)
        self.listWidget.setSelectionRectVisible(False)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.verticalLayout.addWidget(self.listWidget)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.dirChange, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.changeDirectory)
        QtCore.QObject.connect(self.listWidget, QtCore.SIGNAL(_fromUtf8("itemClicked(QListWidgetItem*)")), Form.itemClicked)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.frame.setProperty("class", _translate("Form", "deep", None))
        self.pathLabel.setText(_translate("Form", "Directory:", None))
        self.dirChange.setText(_translate("Form", "Change Directory", None))

