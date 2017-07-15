# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
try:
	from PyQt5 import QtGui,QtCore
except:
	from PyQt4 import QtGui,QtCore

from templates import ui_plotTemplate as plotTemplate
from utilities.expeyesWidgetsNew import expeyesWidgets


import sys,time,functools,os

class AppWindow(QtGui.QWidget, plotTemplate.Ui_Form,expeyesWidgets):
	subsection = 'apps'
	helpfile = 'opamp-circuits.html'
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.p = kwargs.get('handler',None)
		self.widgetLayout.setAlignment(QtCore.Qt.AlignTop)
		self.SCOPEPLOT(['A1','A2'],rangeA1='4V',rangeA2='4V')
		self.timebase = 4

		#Add a vertical spacer in the widgetLayout . about 0.5cm
		self.SPACER(20)

		self.TIMEBASE()
		self.TRIGGER()
		self.TITLE('Controls')
		self.sineW = self.SINE()
		self.sineW.setValue(1500)
		self.pv1W = self.PV1()
		self.pv1W.setValue(0)
		
		self.timer = self.newTimer()
		self.setInterval(self.timer,200,self.update)
		#self.setTimeout(1000,functools.partial(self.capture,'A1',200,3),self.update)

	def update(self):
		self.CAPTURE()  #This assumes self.TRIGGER , self.SCOPEPLOT etc were used to initialize. Uses default values wherever possible
	
