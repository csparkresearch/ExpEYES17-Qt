# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
try:
	from PyQt5 import QtGui,QtCore
except:
	from PyQt4 import QtGui,QtCore

from templates import ui_plotTemplate as plotTemplate
from utilities.expeyesWidgetsNew import expeyesWidgets

import pyqtgraph as pg
import sys,time,functools

class AppWindow(QtGui.QWidget, plotTemplate.Ui_Form,expeyesWidgets):
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.p = kwargs.get('handler',None)
		self.widgetLayout.setAlignment(QtCore.Qt.AlignTop)

		# ADD AN OSCILLOSCOPE PLOT TO THE plotLayout
		# This assumes self.plotLayout, and makes a dictionary self.curves with keys 'A1','A2','A3','MIC'
		#You should be able to access after executing this function. self.myCurves is a dictionary of curves with 4 Elements
		
		self.TITLE('4-Channel Oscilloscope')
		self.SCOPEPLOT(['A1','A2','A3','MIC'],rangeA1='4V',rangeA2='4V')   #You can also make up your own curve names. WORK IN PROGRESS [ e.g. A1+A2  should make a channel that automatically shows the sum]
		self.xaxis = self.plot.getAxis('bottom')

		self.TIMEBASE()
		self.TRIGGER()

		#Add a spacer
		self.SPACER(20)

		# ADD A SINE WIDGET SLIDER WITH NUMBERIC INPUT to the widgetLayout
		self.TITLE('Output Controls')
		self.SINE(value=2000)
		self.SQR1()
		self.PV1()
		self.PV2()
		self.DOUTS()

		self.paused = self.CHECKBOX('Pause')
		self.timer = self.newTimer()
		self.setInterval(self.timer,300,self.autoCapture)
		


	def autoCapture(self):
		if self.p.busy or self.paused.isChecked():return
		self.CAPTURE()
		self.showStatus('capturing at :%s'%time.ctime())
	
