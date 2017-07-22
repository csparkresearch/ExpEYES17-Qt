# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
from ..Qt import QtGui, QtCore
from ..templates import ui_plotTemplate as plotTemplate
from ..utilities.expeyesWidgetsNew import expeyesWidgets


import sys,time,functools,os

class AppWindow(QtGui.QWidget, plotTemplate.Ui_Form,expeyesWidgets):
	subsection = 'apps'
	helpfile = 'halfwave.html'
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.p = kwargs.get('handler',None)
		self.widgetLayout.setAlignment(QtCore.Qt.AlignTop)

		
		# ADD AN OSCILLOSCOPE PLOT TO THE plotLayout
		# This assumes self.plotLayout, and makes a dictionary self.curves with keys 'A1','A2','A3','MIC'
		#You should be able to access after executing this function. self.myCurves is a dictionary of curves with 4 Elements
		self.SCOPEPLOT(['A1','A2'],rangeA1='4V',rangeA2='4V') #You can also make up your own curve names. WORK IN PROGRESS [ e.g. A1+A2  should make a channel that automatically shows the sum]

		#Add a vertical spacer in the widgetLayout . about 0.5cm
		self.SPACER(20)

		# ADD A SINE WIDGET SLIDER WITH NUMBERIC INPUT to the widgetLayout
		self.TIMEBASE()
		self.TRIGGER()
		self.TITLE('Controls')
		self.SINE()
		self.IMAGE(os.path.join('pics','halfwave.png'))
		
		self.timer = self.newTimer()
		self.setInterval(self.timer,200,self.update)
		#self.setTimeout(1000,functools.partial(self.capture,'A1',200,3),self.update)

	def update(self):
		self.CAPTURE()  #This assumes self.TRIGGER , self.SCOPEPLOT etc were used to initialize. Uses default values wherever possible
	
