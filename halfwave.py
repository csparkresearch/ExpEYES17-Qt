from PyQt4 import QtGui,QtCore

from templates import ui_plotTemplate as plotTemplate
from utilities.expeyesWidgets import expeyesWidgets


import sys,time

class AppWindow(QtGui.QWidget, plotTemplate.Ui_Form,expeyesWidgets):
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.p = kwargs.get('handler',None)
		print(self.p)
		self.widgetLayout.addWidget(self.addSine(self.p))
		self.widgetLayout.addWidget(self.addSQR1(self.p))
		self.widgetLayout.addWidget(self.addPV1(self.p) )
		self.widgetLayout.addWidget(self.addPV2(self.p))
